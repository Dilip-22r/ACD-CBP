"""
Phase 2: Syntax Analyzer (Parser) for ISO Prolog.
Constructs Concrete Syntax Tree (CST) and Abstract Syntax Tree (AST).
Provides Derivation Trace, FIRST & FOLLOW Sets, and Detailed Syntax Error Reporting.
"""

from typing import List, Optional, Tuple, Dict, Any
from lexer import Token, TokenType, PrologLexer
from ast_nodes import (
    ASTNode, Program, Clause, Fact, Rule, Query,
    Term, CompoundTerm, Atom, Variable, Number, ListTerm
)

class SyntaxError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        if token:
            loc = f"Line {token.line}, Col {token.col} (near '{token.raw_text}')"
        else:
            loc = "End of File"
        super().__init__(f"Syntax Error at {loc}: {message}")
        self.message = message
        self.token = token

class PrologParser:
    """
    Predictive Recursive Descent Parser for ISO Prolog.
    
    Complete Formal Context-Free Grammar (CFG) Productions:
    -------------------------------------------------------
    1.  Program          ::= ClauseList EOF
    2.  ClauseList       ::= Clause ClauseList | ε
    3.  Clause           ::= Fact | Rule | Query
    4.  Fact             ::= Head '.'
    5.  Rule             ::= Head ':-' GoalList '.'
    6.  Query            ::= '?-' GoalList '.'
    7.  Head             ::= CompoundTerm | ATOM
    8.  GoalList         ::= Goal ConjGoalList
    9.  ConjGoalList     ::= ',' Goal ConjGoalList | ';' Goal ConjGoalList | ε
    10. Goal             ::= RelExpr | CutGoal
    11. CutGoal          ::= '!'
    12. RelExpr          ::= AddExpr ( RelOp AddExpr )*
    13. RelOp            ::= 'is' | '=' | '\\=' | '==' | '\\==' | '<' | '>' | '=<' | '>='
    14. AddExpr          ::= MulExpr ( AddOp MulExpr )*
    15. AddOp            ::= '+' | '-'
    16. MulExpr          ::= Term ( MulOp Term )*
    17. MulOp            ::= '*' | '/' | 'mod'
    18. Term             ::= CompoundTerm | AtomicTerm | VariableTerm | ListTerm | GroupExpr
    19. GroupExpr        ::= '(' RelExpr ')'
    20. AtomicTerm       ::= ATOM | NUMBER | STRING
    21. VariableTerm     ::= VARIABLE | ANON_VAR
    22. CompoundTerm     ::= ATOM '(' ArgList ')'
    23. ArgList          ::= RelExpr ( ',' RelExpr )*
    24. ListTerm         ::= EmptyList | BracketList
    25. EmptyList        ::= '[' ']'
    26. BracketList      ::= '[' ListElements ']'
    27. ListElements     ::= RelExpr ( ',' RelExpr )* ( '|' TailTerm )?
    28. TailTerm         ::= Term
    """
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token: Token = tokens[0] if tokens else Token(TokenType.EOF, "<EOF>", 1, 1)
        self.derivation_trace: List[Dict[str, Any]] = []
        self.errors: List[str] = []

    def record_derivation(self, non_terminal: str, production: str):
        self.derivation_trace.append({
            "step": len(self.derivation_trace) + 1,
            "non_terminal": non_terminal,
            "production": production,
            "current_token": self.current_token.to_dict()
        })

    def peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def advance(self) -> Token:
        consumed = self.current_token
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return consumed

    def expect(self, token_type: str, custom_error: str = "") -> Token:
        if self.current_token.type == token_type:
            return self.advance()
        msg = custom_error or f"Expected token {token_type}, but found {self.current_token.type} ('{self.current_token.raw_text}')"
        raise SyntaxError(msg, self.current_token)

    def match(self, *token_types: str) -> bool:
        return self.current_token.type in token_types

    # =========================================================================
    # GRAMMAR PRODUCTIONS (Recursive Descent)
    # =========================================================================

    def parse_program(self) -> Program:
        """Program -> Clause* EOF"""
        self.record_derivation("Program", "Clause* EOF")
        clauses = []
        while not self.match(TokenType.EOF):
            try:
                clause = self.parse_clause()
                if clause:
                    clauses.append(clause)
            except SyntaxError as e:
                self.errors.append(str(e))
                # Panic-mode error recovery: Synchronize to next DOT or EOF
                self.synchronize()

        return Program(clauses=clauses, line=1, col=1)

    def synchronize(self):
        """Panic-mode recovery: skip tokens until after a DOT '.' delimiter or fresh clause start."""
        if self.current_token.type in (TokenType.ATOM, TokenType.OP_QUERY):
            next_tok = self.peek(1)
            if next_tok.type in (TokenType.LPAREN, TokenType.DOT, TokenType.OP_RULE):
                return

        while not self.match(TokenType.EOF):
            tok = self.advance()
            if tok.type == TokenType.DOT:
                break
            if self.current_token.type in (TokenType.ATOM, TokenType.OP_QUERY):
                next_tok = self.peek(1)
                if next_tok.type in (TokenType.LPAREN, TokenType.DOT, TokenType.OP_RULE):
                    break

    def parse_clause(self) -> Optional[Clause]:
        """Clause -> Query | Rule | Fact"""
        self.record_derivation("Clause", "Query | Rule | Fact")

        # 1. Query: ?- GoalList .
        if self.match(TokenType.OP_QUERY):
            self.advance() # consume ?-
            body = self.parse_goal_list()
            self.expect(TokenType.DOT, "Missing '.' terminator at the end of query")
            return Query(goals=body, line=self.current_token.line, col=self.current_token.col)

        # 2. Rule or Fact: Head (':-' Body)? '.'
        start_tok = self.current_token
        head_term = self.parse_term()

        if not isinstance(head_term, (CompoundTerm, Atom)):
            raise SyntaxError(f"Clause head must be an Atom or Compound Term (predicate), got {head_term.__class__.__name__}", start_tok)

        # Head can be converted to CompoundTerm if it's an Atom with 0 args
        if isinstance(head_term, Atom):
            head_term = CompoundTerm(functor=head_term.name, args=[], line=head_term.line, col=head_term.col)

        # Check if it has a neck ':-'
        if self.match(TokenType.OP_RULE):
            self.record_derivation("Rule", "Head ':-' GoalList '.'")
            self.advance() # consume ':-'
            body = self.parse_goal_list()
            self.expect(TokenType.DOT, "Missing '.' at the end of rule clause")
            return Rule(head=head_term, body=body, line=start_tok.line, col=start_tok.col)
        else:
            self.record_derivation("Fact", "Head '.'")
            self.expect(TokenType.DOT, "Missing '.' at the end of fact clause")
            return Fact(head=head_term, line=start_tok.line, col=start_tok.col)

    def parse_goal_list(self) -> List[Term]:
        """GoalList -> Goal ( (',' | ';') Goal )*"""
        self.record_derivation("GoalList", "Goal ((',' | ';') Goal)*")
        goals = [self.parse_goal()]
        while self.match(TokenType.COMMA, TokenType.SEMICOLON):
            conj_op = self.advance() # , or ;
            next_goal = self.parse_goal()
            if conj_op.type == TokenType.SEMICOLON:
                # Disjunction representation: ;(GoalA, GoalB)
                goals[-1] = CompoundTerm(functor=";", args=[goals[-1], next_goal], line=conj_op.line, col=conj_op.col)
            else:
                goals.append(next_goal)
        return goals

    def parse_goal(self) -> Term:
        """Goal -> Term (Op Term)* | Cut ('!')"""
        self.record_derivation("Goal", "Term (Op Term)* | '!'")
        if self.match(TokenType.CUT):
            cut_tok = self.advance()
            return Atom(name="!", line=cut_tok.line, col=cut_tok.col)
        return self.parse_expression()

    # Infix operator precedence (higher binds tighter)
    PRECEDENCE = {
        "is": 10, "=": 10, "\\=": 10, "==": 10, "\\==": 10,
        ">": 20, "<": 20, ">=": 20, "=<": 20, "->": 20,
        "+": 30, "-": 30,
        "*": 40, "/": 40,
    }

    def parse_expression(self, min_prec: int = 0) -> Term:
        """Expression -> Term (Operator Expression)? via precedence climbing."""
        left = self.parse_term()

        while self.match(TokenType.OPERATOR):
            op_tok = self.current_token
            op = op_tok.raw_text
            prec = self.PRECEDENCE.get(op)
            if prec is None or prec < min_prec:
                break
            self.advance()
            right = self.parse_expression(prec + 1)
            left = CompoundTerm(functor=op, args=[left, right], line=op_tok.line, col=op_tok.col)

        return left

    def parse_term(self) -> Term:
        """
        Term -> CompoundTerm | Atom | Variable | Number | ListTerm | '(' Term ')'
        """
        tok = self.current_token

        # 1. Parenthesized Expression: ( Term )
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Missing closing ')'")
            return expr

        # 2. Number literal
        if self.match(TokenType.NUMBER):
            self.advance()
            return Number(value=tok.value, line=tok.line, col=tok.col)

        # 3. Variable or Anonymous Variable
        if self.match(TokenType.VARIABLE, TokenType.ANON_VAR):
            self.advance()
            return Variable(name=tok.raw_text, line=tok.line, col=tok.col)

        # 4. List: [ Elements (| Tail)? ]
        if self.match(TokenType.LBRACKET):
            return self.parse_list()

        # 5. Atom or Compound Term: functor(arg1, arg2, ...)
        if self.match(TokenType.ATOM):
            atom_name = self.advance().value
            # Check if immediately followed by '(' without whitespace
            if self.match(TokenType.LPAREN):
                self.advance() # consume '('
                args = self.parse_argument_list()
                self.expect(TokenType.RPAREN, f"Missing ')' for compound term {atom_name}(...)")
                return CompoundTerm(functor=atom_name, args=args, line=tok.line, col=tok.col)
            return Atom(name=atom_name, line=tok.line, col=tok.col)

        # 6. String literal
        if self.match(TokenType.STRING):
            self.advance()
            return Atom(name=tok.value, line=tok.line, col=tok.col)

        raise SyntaxError(f"Unexpected token {tok.type} ('{tok.raw_text}') while parsing term", tok)

    def parse_argument_list(self) -> List[Term]:
        """ArgumentList -> Expression (',' Expression)*"""
        args = []
        if not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance() # consume ','
                args.append(self.parse_expression())
        return args

    def parse_list(self) -> ListTerm:
        """ListTerm -> '[' [ Term (',' Term)* ('|' Term)? ] ']'"""
        start_tok = self.expect(TokenType.LBRACKET)
        elements = []
        tail = None

        if not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance() # consume ','
                elements.append(self.parse_expression())

            if self.match(TokenType.PIPE):
                self.advance() # consume '|'
                tail = self.parse_term()

        self.expect(TokenType.RBRACKET, "Missing closing ']' for list literal")
        return ListTerm(elements=elements, tail=tail, line=start_tok.line, col=start_tok.col)

    # =========================================================================
    # FIRST & FOLLOW SETS (Essential for Compiler Design Viva Defense)
    # =========================================================================

    @staticmethod
    def get_first_and_follow_sets() -> Dict[str, Dict[str, List[str]]]:
        """
        Returns complete FIRST and FOLLOW sets for all non-terminals in the ISO Prolog CFG.
        Essential for LL(1) parsing validation and compiler lab viva defense.
        """
        return {
            "Program": {
                "FIRST": ["ATOM", "VARIABLE", "?-", "ε"],
                "FOLLOW": ["$"]
            },
            "Clause": {
                "FIRST": ["ATOM", "VARIABLE", "?-"],
                "FOLLOW": ["ATOM", "VARIABLE", "?-", "$"]
            },
            "Fact": {
                "FIRST": ["ATOM"],
                "FOLLOW": ["ATOM", "VARIABLE", "?-", "$"]
            },
            "Rule": {
                "FIRST": ["ATOM"],
                "FOLLOW": ["ATOM", "VARIABLE", "?-", "$"]
            },
            "Query": {
                "FIRST": ["?-"],
                "FOLLOW": ["ATOM", "VARIABLE", "?-", "$"]
            },
            "Head": {
                "FIRST": ["ATOM"],
                "FOLLOW": [".", ":-"]
            },
            "GoalList": {
                "FIRST": ["ATOM", "VARIABLE", "NUMBER", "STRING", "[", "(", "!"],
                "FOLLOW": ["."]
            },
            "Goal": {
                "FIRST": ["ATOM", "VARIABLE", "NUMBER", "STRING", "[", "(", "!"],
                "FOLLOW": [",", ";", "."]
            },
            "Expr": {
                "FIRST": ["ATOM", "VARIABLE", "NUMBER", "STRING", "[", "("],
                "FOLLOW": [",", ";", ".", ")", "]"]
            },
            "Term": {
                "FIRST": ["ATOM", "VARIABLE", "NUMBER", "STRING", "[", "("],
                "FOLLOW": [",", ")", "]", "|", ".", ":-", ";", "OPERATOR", "$"]
            },
            "CompoundTerm": {
                "FIRST": ["ATOM"],
                "FOLLOW": [".", ":-", ",", ";", ")", "]", "|", "OPERATOR", "$"]
            },
            "ArgList": {
                "FIRST": ["ATOM", "VARIABLE", "NUMBER", "STRING", "[", "("],
                "FOLLOW": [")"]
            },
            "ListTerm": {
                "FIRST": ["["],
                "FOLLOW": [",", ")", "]", "|", ".", ":-", ";", "OPERATOR", "$"]
            },
            "List": {
                "FIRST": ["["],
                "FOLLOW": [",", ")", "]", "|", ".", ":-", ";", "$"]
            }
        }
