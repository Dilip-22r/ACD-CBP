"""
AST (Abstract Syntax Tree) Node Definitions for Prolog Compiler.
Covers Clauses (Facts, Rules), Queries, Terms (Atoms, Variables, Numbers, Compounds, Lists).
"""

from typing import List, Optional, Any, Dict

class ASTNode:
    """Base class for all Abstract Syntax Tree nodes."""
    def __init__(self, line: int = 1, col: int = 1):
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    def pretty_print(self, indent: int = 0) -> str:
        return "  " * indent + self.__repr__()

class Term(ASTNode):
    """Base class for all Prolog Terms (arguments in predicates/goals)."""
    pass

class Atom(Term):
    """An atom identifier (e.g. john, cse, likes, 'quoted string')."""
    def __init__(self, name: str, line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Atom",
            "name": self.name,
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        return f"Atom({self.name})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Atom) and self.name == other.name

    def __hash__(self) -> int:
        return hash(("Atom", self.name))

class Variable(Term):
    """A logic variable (starts with Uppercase or underscore, e.g. X, Student, _Rest)."""
    def __init__(self, name: str, line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.name = name
        self.is_anonymous = name == "_" or name.startswith("_")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Variable",
            "name": self.name,
            "is_anonymous": self.is_anonymous,
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        return f"Var({self.name})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self) -> int:
        return hash(("Variable", self.name))

class Number(Term):
    """A numeric literal (integer or floating point)."""
    def __init__(self, value: float, line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Number",
            "value": self.value,
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        return f"Num({self.value})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Number) and self.value == other.value

    def __hash__(self) -> int:
        return hash(("Number", self.value))

class CompoundTerm(Term):
    """A compound term or predicate: functor(arg1, arg2, ..., argN)."""
    def __init__(self, functor: str, args: List[Term], line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.functor = functor
        self.args = args
        self.arity = len(args)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "CompoundTerm",
            "functor": self.functor,
            "arity": self.arity,
            "args": [arg.to_dict() for arg in self.args],
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        args_str = ", ".join(repr(a) for a in self.args)
        return f"{self.functor}({args_str})"

    def __eq__(self, other) -> bool:
        return (isinstance(other, CompoundTerm) and 
                self.functor == other.functor and 
                self.arity == other.arity and 
                self.args == other.args)

    def __hash__(self) -> int:
        return hash(("CompoundTerm", self.functor, self.arity, tuple(self.args)))

class ListTerm(Term):
    """A Prolog list: [head_elements | tail_term] or [] empty list."""
    def __init__(self, elements: List[Term], tail: Optional[Term] = None, line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.elements = elements
        self.tail = tail

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "ListTerm",
            "elements": [e.to_dict() for e in self.elements],
            "tail": self.tail.to_dict() if self.tail else None,
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        elem_str = ", ".join(repr(e) for e in self.elements)
        if self.tail:
            return f"[{elem_str} | {repr(self.tail)}]"
        return f"[{elem_str}]"

class Clause(ASTNode):
    """Base class for program clauses (Facts, Rules, Directives)."""
    pass

class Fact(Clause):
    """A Prolog Fact: head."""
    def __init__(self, head: CompoundTerm, line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.head = head

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Fact",
            "head": self.head.to_dict(),
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        return f"Fact({repr(self.head)})."

class Rule(Clause):
    """A Prolog Rule: head :- goal1, goal2, ..."""
    def __init__(self, head: CompoundTerm, body: List[Term], line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.head = head
        self.body = body

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Rule",
            "head": self.head.to_dict(),
            "body": [b.to_dict() for b in self.body],
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        body_str = ", ".join(repr(b) for b in self.body)
        return f"Rule({repr(self.head)} :- {body_str})."

class Query(ASTNode):
    """A top-level interactive query: ?- goal1, goal2, ..."""
    def __init__(self, goals: List[Term], line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.goals = goals

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Query",
            "goals": [g.to_dict() for g in self.goals],
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        goals_str = ", ".join(repr(g) for g in self.goals)
        return f"?- {goals_str}."

class Program(ASTNode):
    """Root node representing the entire Prolog knowledge base."""
    def __init__(self, clauses: List[Clause], line: int = 1, col: int = 1):
        super().__init__(line, col)
        self.clauses = clauses

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": "Program",
            "clause_count": len(self.clauses),
            "clauses": [c.to_dict() for c in self.clauses],
            "line": self.line,
            "col": self.col
        }

    def __repr__(self) -> str:
        return f"Program({len(self.clauses)} clauses)"
