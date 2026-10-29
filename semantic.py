"""
Phase 3: Semantic Analyzer & Symbol Table Manager for ISO Prolog.
Performs:
1. Predicate Indexing & Signature Tracking (functor/arity)
2. Clause-Level Variable Scope Resolution
3. Singleton Variable Warnings (Key Prolog Compiler Diagnostic)
4. Undefined Predicate Reference Detection & Arity Mismatches
"""

from typing import List, Dict, Set, Any, Tuple
from ast_nodes import Program, Clause, Fact, Rule, Query, Term, CompoundTerm, Variable, Atom, ListTerm, Number

class PredicateSymbol:
    """Represents a defined predicate signature: functor/arity."""
    def __init__(self, functor: str, arity: int):
        self.functor = functor
        self.arity = arity
        self.signature = f"{functor}/{arity}"
        self.fact_count = 0
        self.rule_count = 0
        self.definition_lines: List[int] = []
        self.called_by: Set[str] = set()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "functor": self.functor,
            "arity": self.arity,
            "signature": self.signature,
            "facts": self.fact_count,
            "rules": self.rule_count,
            "total_clauses": self.fact_count + self.rule_count,
            "defined_at_lines": self.definition_lines,
            "callers": list(self.called_by)
        }

class SemanticDiagnostic:
    """Represents an error, warning, or informational message."""
    def __init__(self, level: str, message: str, line: int = 1, col: int = 1, code: str = ""):
        self.level = level  # 'ERROR', 'WARNING', 'INFO'
        self.message = message
        self.line = line
        self.col = col
        self.code = code

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "message": self.message,
            "line": self.line,
            "col": self.col,
            "code": self.code
        }

class SemanticAnalyzer:
    """
    Semantic analysis pipeline verifying Prolog rules, scopes, and symbol tables.
    """
    BUILTIN_PREDICATES = {
        "=/2", "\\=/2", "==/2", "\\==/2", "is/2",
        "</2", ">/2", "=<//2", ">=/2", "+/2", "-/2",
        "write/1", "writeln/1", "nl/0", "fail/0", "true/0",
        "!/0", "append/3", "member/2", "length/2", "reverse/2"
    }

    def __init__(self, ast: Program):
        self.ast = ast
        self.symbol_table: Dict[str, PredicateSymbol] = {}
        self.clause_variable_scopes: List[Dict[str, Any]] = []
        self.diagnostics: List[SemanticDiagnostic] = []
        self.references: Set[Tuple[str, int, int]] = set() # (functor, arity, line)

    def analyze(self) -> Dict[str, Any]:
        self.symbol_table.clear()
        self.clause_variable_scopes.clear()
        self.diagnostics.clear()
        self.references.clear()

        # Pass 1: Predicate Registration & Clause Header Symbol Table population
        for clause_idx, clause in enumerate(self.ast.clauses):
            if isinstance(clause, (Fact, Rule)):
                head = clause.head
                sig = f"{head.functor}/{head.arity}"
                if sig not in self.symbol_table:
                    self.symbol_table[sig] = PredicateSymbol(head.functor, head.arity)

                sym = self.symbol_table[sig]
                sym.definition_lines.append(clause.line)
                if isinstance(clause, Fact):
                    sym.fact_count += 1
                else:
                    sym.rule_count += 1

        # Pass 2: Variable Scope & Singleton Analysis per Clause
        for clause_idx, clause in enumerate(self.ast.clauses):
            scope_info = self.analyze_clause_variables(clause_idx, clause)
            self.clause_variable_scopes.append(scope_info)

        # Pass 3: Cross-Reference & Undefined Predicate Verification
        self.check_references()

        return {
            "symbol_table": {k: v.to_dict() for k, v in self.symbol_table.items()},
            "clause_scopes": self.clause_variable_scopes,
            "diagnostics": [d.to_dict() for d in self.diagnostics],
            "total_predicates": len(self.symbol_table),
            "warnings_count": sum(1 for d in self.diagnostics if d.level == "WARNING"),
            "errors_count": sum(1 for d in self.diagnostics if d.level == "ERROR")
        }

    def analyze_clause_variables(self, clause_idx: int, clause: Clause) -> Dict[str, Any]:
        var_occurrences: Dict[str, List[Variable]] = {}

        def collect_vars(term: Term):
            if isinstance(term, Variable):
                var_occurrences.setdefault(term.name, []).append(term)
            elif isinstance(term, CompoundTerm):
                # Also track references to predicates in the rule body
                for arg in term.args:
                    collect_vars(arg)
            elif isinstance(term, ListTerm):
                for elem in term.elements:
                    collect_vars(elem)
                if term.tail:
                    collect_vars(term.tail)

        # Traverse Head
        if isinstance(clause, (Fact, Rule)):
            collect_vars(clause.head)
            clause_name = f"{clause.head.functor}/{clause.head.arity}"
        elif isinstance(clause, Query):
            clause_name = "Query (? -)"

        # Traverse Body
        if isinstance(clause, Rule):
            for goal in clause.body:
                collect_vars(goal)
                if isinstance(goal, CompoundTerm):
                    self.references.add((goal.functor, goal.arity, goal.line))
        elif isinstance(clause, Query):
            for goal in clause.goals:
                collect_vars(goal)
                if isinstance(goal, CompoundTerm):
                    self.references.add((goal.functor, goal.arity, goal.line))

        # Check for Singleton Variables (Variables appearing only once in the clause)
        singletons = []
        for var_name, occurrences in var_occurrences.items():
            if len(occurrences) == 1 and not var_name.startswith("_"):
                singletons.append(var_name)
                tok_var = occurrences[0]
                self.diagnostics.append(SemanticDiagnostic(
                    level="WARNING",
                    message=f"Singleton variable '{var_name}' in clause '{clause_name}'. Prefix with '_' if intentionally unused.",
                    line=tok_var.line,
                    col=tok_var.col,
                    code="W_SINGLETON_VAR"
                ))

        return {
            "clause_index": clause_idx + 1,
            "clause": clause_name,
            "line": clause.line,
            "variable_count": len(var_occurrences),
            "variables": {k: len(v) for k, v in var_occurrences.items()},
            "singletons": singletons
        }

    def check_references(self):
        """Identifies calls to undefined predicates."""
        for functor, arity, line in self.references:
            sig = f"{functor}/{arity}"
            if sig not in self.symbol_table and sig not in self.BUILTIN_PREDICATES:
                # Check if same functor exists with different arity
                alt_arities = [sym.arity for sym in self.symbol_table.values() if sym.functor == functor]
                if alt_arities:
                    self.diagnostics.append(SemanticDiagnostic(
                        level="WARNING",
                        message=f"Predicate '{functor}/{arity}' called at line {line}, but defined with arity {alt_arities}.",
                        line=line,
                        code="W_ARITY_MISMATCH"
                    ))
                else:
                    self.diagnostics.append(SemanticDiagnostic(
                        level="INFO",
                        message=f"Referenced predicate '{sig}' at line {line} has no local clauses defined (may be external or dynamic).",
                        line=line,
                        code="I_UNDEFINED_PRED"
                    ))
