"""
Phase 1: Lexical Analyzer (Tokenizer) for ISO Prolog.
Recognizes Atoms, Variables, Numbers, Strings, Functors, Operators, Comments, and Punctuation.
Provides line/column position tracking and detailed DFA-style token classification.
"""

import re
from typing import List, Optional, Dict, Any

class TokenType:
    ATOM = "ATOM"              # e.g., parent, cse, 'john doe'
    VARIABLE = "VARIABLE"      # e.g., X, Student, _Result
    ANON_VAR = "ANON_VAR"      # _
    NUMBER = "NUMBER"          # 42, 3.14
    STRING = "STRING"          # "hello"
    OP_RULE = "OP_RULE"        # :-
    OP_QUERY = "OP_QUERY"      # ?-
    DOT = "DOT"                # .
    COMMA = "COMMA"            # ,
    SEMICOLON = "SEMICOLON"    # ;
    LPAREN = "LPAREN"          # (
    RPAREN = "RPAREN"          # )
    LBRACKET = "LBRACKET"      # [
    RBRACKET = "RBRACKET"      # ]
    PIPE = "PIPE"              # |
    CUT = "CUT"                # !
    OPERATOR = "OPERATOR"      # =, \=, is, +, -, *, /, <, >, =<, >=, ==, \==
    COMMENT = "COMMENT"        # % ... or /* ... */
    EOF = "EOF"
    ERROR = "ERROR"

class Token:
    def __init__(self, type_: str, value: Any, line: int, col: int, raw_text: str = ""):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
        self.raw_text = raw_text or str(value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "value": str(self.value),
            "line": self.line,
            "col": self.col,
            "raw": self.raw_text
        }

    def __repr__(self) -> str:
        return f"Token({self.type}, {repr(self.value)}, L{self.line}:C{self.col})"

class LexicalError(Exception):
    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"Lexical Error at Line {line}, Col {col}: {message}")
        self.message = message
        self.line = line
        self.col = col

class PrologLexer:
    """
    Finite State Lexical Analyzer for Prolog Source Code.
    """
    OPERATORS_MULTI = [":-", "?-", "\\=", "==", "\\==", "=<", ">=", "->"]
    OPERATORS_SINGLE = ["=", "+", "-", "*", "/", "<", ">"]

    def __init__(self, source_code: str):
        self.source = source_code
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
        self.errors: List[str] = []

    def peek(self, offset: int = 0) -> Optional[str]:
        idx = self.pos + offset
        if idx < self.length:
            return self.source[idx]
        return None

    def advance(self) -> Optional[str]:
        if self.pos < self.length:
            ch = self.source[self.pos]
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            return ch
        return None

    def match(self, expected: str) -> bool:
        if self.source.startswith(expected, self.pos):
            for _ in expected:
                self.advance()
            return True
        return False

    def skip_whitespace_and_comments(self):
        while self.pos < self.length:
            ch = self.peek()
            # Whitespace
            if ch.isspace() or ch == '\xa0':
                self.advance()
            # Single-line comment: % ...
            elif ch == '%':
                while self.pos < self.length and self.peek() != '\n':
                    self.advance()
            # Multi-line comment: /* ... */
            elif ch == '/' and self.peek(1) == '*':
                start_l, start_c = self.line, self.col
                self.advance() # /
                self.advance() # *
                closed = False
                while self.pos < self.length:
                    if self.peek() == '*' and self.peek(1) == '/':
                        self.advance()
                        self.advance()
                        closed = True
                        break
                    self.advance()
                if not closed:
                    self.errors.append(f"Unclosed block comment starting at Line {start_l}, Col {start_c}")
            else:
                break

    def tokenize(self) -> List[Token]:
        self.tokens = []
        self.errors = []
        self.pos = 0
        self.line = 1
        self.col = 1

        while self.pos < self.length:
            self.skip_whitespace_and_comments()
            if self.pos >= self.length:
                break

            start_line = self.line
            start_col = self.col
            ch = self.peek()

            # 1. Multi-character Neck and Query operators
            if self.match(":-"):
                self.tokens.append(Token(TokenType.OP_RULE, ":-", start_line, start_col))
                continue
            if self.match("?-"):
                self.tokens.append(Token(TokenType.OP_QUERY, "?-", start_line, start_col))
                continue
            if self.match("\\="):
                self.tokens.append(Token(TokenType.OPERATOR, "\\=", start_line, start_col))
                continue
            if self.match("=="):
                self.tokens.append(Token(TokenType.OPERATOR, "==", start_line, start_col))
                continue
            if self.match("\\=="):
                self.tokens.append(Token(TokenType.OPERATOR, "\\==", start_line, start_col))
                continue
            if self.match("=<"):
                self.tokens.append(Token(TokenType.OPERATOR, "=<", start_line, start_col))
                continue
            if self.match(">="):
                self.tokens.append(Token(TokenType.OPERATOR, ">=", start_line, start_col))
                continue

            # 2. Single-character Punctuation
            if ch == '.':
                # Check if it's a clause terminator or floating point
                # In Prolog, a dot is a terminator only when followed by whitespace, comment, or EOF
                next_ch = self.peek(1)
                if next_ch is None or next_ch in (' ', '\t', '\r', '\n', '%'):
                    self.advance()
                    self.tokens.append(Token(TokenType.DOT, ".", start_line, start_col))
                    continue
                else:
                    # Could be symbol or error
                    self.advance()
                    self.tokens.append(Token(TokenType.DOT, ".", start_line, start_col))
                    continue
            if ch == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ",", start_line, start_col))
                continue
            if ch == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ";", start_line, start_col))
                continue
            if ch == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col))
                continue
            if ch == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col))
                continue
            if ch == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, "[", start_line, start_col))
                continue
            if ch == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, "]", start_line, start_col))
                continue
            if ch == '|':
                self.advance()
                self.tokens.append(Token(TokenType.PIPE, "|", start_line, start_col))
                continue
            if ch == '!':
                self.advance()
                self.tokens.append(Token(TokenType.CUT, "!", start_line, start_col))
                continue

            # 3. Arithmetic / Comparison operators
            if ch in self.OPERATORS_SINGLE:
                self.advance()
                self.tokens.append(Token(TokenType.OPERATOR, ch, start_line, start_col))
                continue

            # 4. Numeric Constants (Integers and Floats)
            if ch.isdigit():
                num_str = ""
                while self.pos < self.length and self.peek().isdigit():
                    num_str += self.advance()
                # Check for floating point
                if self.peek() == '.' and self.peek(1) and self.peek(1).isdigit():
                    num_str += self.advance() # .
                    while self.pos < self.length and self.peek().isdigit():
                        num_str += self.advance()
                    val = float(num_str)
                else:
                    val = int(num_str)
                self.tokens.append(Token(TokenType.NUMBER, val, start_line, start_col, num_str))
                continue

            # 5. Anonymous Variable '_'
            if ch == '_':
                var_str = self.advance()
                # If followed by alphanumeric/underscore, it's a named anonymous/throwaway variable like _Rest
                while self.pos < self.length and (self.peek().isalnum() or self.peek() == '_'):
                    var_str += self.advance()
                if var_str == "_":
                    self.tokens.append(Token(TokenType.ANON_VAR, "_", start_line, start_col, "_"))
                else:
                    self.tokens.append(Token(TokenType.VARIABLE, var_str, start_line, start_col, var_str))
                continue

            # 6. Variables (Start with uppercase letter)
            if ch.isupper():
                var_str = ""
                while self.pos < self.length and (self.peek().isalnum() or self.peek() == '_'):
                    var_str += self.advance()
                self.tokens.append(Token(TokenType.VARIABLE, var_str, start_line, start_col, var_str))
                continue

            # 7. Atoms (Start with lowercase letter)
            if ch.islower():
                atom_str = ""
                while self.pos < self.length and (self.peek().isalnum() or self.peek() == '_'):
                    atom_str += self.advance()
                # Special keyword operators like 'is'
                if atom_str == "is":
                    self.tokens.append(Token(TokenType.OPERATOR, "is", start_line, start_col, "is"))
                else:
                    self.tokens.append(Token(TokenType.ATOM, atom_str, start_line, start_col, atom_str))
                continue

            # 8. Quoted Atoms ('john doe')
            if ch == "'":
                self.advance() # skip opening quote
                quoted_str = ""
                closed = False
                while self.pos < self.length:
                    curr = self.advance()
                    if curr == "'":
                        closed = True
                        break
                    quoted_str += curr
                if not closed:
                    self.errors.append(f"Unterminated single-quoted atom starting at Line {start_line}, Col {start_col}")
                self.tokens.append(Token(TokenType.ATOM, quoted_str, start_line, start_col, f"'{quoted_str}'"))
                continue

            # 9. String Literals ("string")
            if ch == '"':
                self.advance() # skip opening quote
                s_val = ""
                closed = False
                while self.pos < self.length:
                    curr = self.advance()
                    if curr == '"':
                        closed = True
                        break
                    s_val += curr
                if not closed:
                    self.errors.append(f"Unterminated string literal starting at Line {start_line}, Col {start_col}")
                self.tokens.append(Token(TokenType.STRING, s_val, start_line, start_col, f'"{s_val}"'))
                continue

            # Unrecognized character
            bad_ch = self.advance()
            err_msg = f"Unexpected character '{bad_ch}' at Line {start_line}, Col {start_col}"
            self.errors.append(err_msg)
            self.tokens.append(Token(TokenType.ERROR, bad_ch, start_line, start_col, bad_ch))

        self.tokens.append(Token(TokenType.EOF, "<EOF>", self.line, self.col))
        return self.tokens

    def get_token_summary(self) -> Dict[str, Any]:
        """Provides frequency breakdown and metrics for the compiler visualizer."""
        counts = {}
        for tok in self.tokens:
            counts[tok.type] = counts.get(tok.type, 0) + 1
        return {
            "total_tokens": len(self.tokens),
            "line_count": self.line,
            "distribution": counts,
            "errors": self.errors
        }
