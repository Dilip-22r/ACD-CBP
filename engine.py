"""
Phase 5: First-Order Unification Algorithm & SLD Resolution Engine for Prolog.
Implements:
1. Robinson's Unification Algorithm with Occurs-Check
2. SLD-Resolution with Chronological Backtracking
3. Step-by-Step Execution Trace Visualizer
"""

import copy
from typing import Dict, List, Optional, Any, Tuple
from ast_nodes import Program, Fact, Rule, Query, Term, CompoundTerm, Variable, Atom, Number, ListTerm

Substitution = Dict[str, Term]

def apply_subst(term: Term, theta: Substitution) -> Term:
    """Recursively replaces variables in term using substitution map theta."""
    if isinstance(term, Variable):
        if term.name in theta:
            return apply_subst(theta[term.name], theta)
        return term
    elif isinstance(term, CompoundTerm):
        new_args = [apply_subst(arg, theta) for arg in term.args]
        return CompoundTerm(term.functor, new_args, term.line, term.col)
    elif isinstance(term, ListTerm):
        new_elements = [apply_subst(elem, theta) for elem in term.elements]
        new_tail = apply_subst(term.tail, theta) if term.tail else None
        return ListTerm(new_elements, new_tail, term.line, term.col)
    return term

def occurs_check(var_name: str, term: Term, theta: Substitution) -> bool:
    """Occurs-check: returns True if variable var_name occurs inside term."""
    term = apply_subst(term, theta)
    if isinstance(term, Variable):
        return term.name == var_name
    elif isinstance(term, CompoundTerm):
        return any(occurs_check(var_name, arg, theta) for arg in term.args)
    elif isinstance(term, ListTerm):
        in_elems = any(occurs_check(var_name, elem, theta) for elem in term.elements)
        in_tail = occurs_check(var_name, term.tail, theta) if term.tail else False
        return in_elems or in_tail
    return False

def eval_arithmetic(term: Term, theta: Substitution) -> Optional[float]:
    """Evaluate an arithmetic expression (numbers, + - * / // mod). Returns None on failure."""
    term = apply_subst(term, theta)
    if isinstance(term, Number):
        return term.value
    if isinstance(term, CompoundTerm) and len(term.args) == 2:
        op = term.functor
        if op in ("+", "-", "*", "/", "//", "mod"):
            left = eval_arithmetic(term.args[0], theta)
            right = eval_arithmetic(term.args[1], theta)
            if left is None or right is None:
                return None
            try:
                if op == "+": return left + right
                if op == "-": return left - right
                if op == "*": return left * right
                if op == "/": return left / right
                if op == "//": return left // right
                if op == "mod": return left % right
            except ZeroDivisionError:
                return None
    return None

def unify(term1: Term, term2: Term, theta: Optional[Substitution] = None) -> Optional[Substitution]:
    """
    Robinson's First-Order Unification Algorithm.
    Returns the Most General Unifier (MGU) substitution theta, or None if terms cannot unify.
    """
    if theta is None:
        theta = {}

    term1 = apply_subst(term1, theta)
    term2 = apply_subst(term2, theta)

    # 1. Identical terms
    if term1 == term2:
        return theta

    # 2. Variable unification
    if isinstance(term1, Variable):
        if occurs_check(term1.name, term2, theta):
            return None # Circular reference fails occurs-check
        new_theta = dict(theta)
        new_theta[term1.name] = term2
        return new_theta

    if isinstance(term2, Variable):
        if occurs_check(term2.name, term1, theta):
            return None
        new_theta = dict(theta)
        new_theta[term2.name] = term1
        return new_theta

    # 3. Numbers & Atoms
    if isinstance(term1, Number) and isinstance(term2, Number):
        return theta if term1.value == term2.value else None

    if isinstance(term1, Atom) and isinstance(term2, Atom):
        return theta if term1.name == term2.name else None

    # 4. Compound terms: functor and arity must match
    if isinstance(term1, CompoundTerm) and isinstance(term2, CompoundTerm):
        if term1.functor != term2.functor or term1.arity != term2.arity:
            return None
        curr_theta = theta
        for a1, a2 in zip(term1.args, term2.args):
            curr_theta = unify(a1, a2, curr_theta)
            if curr_theta is None:
                return None
        return curr_theta

    # 5. List terms: cons-cell unification of [H|T] against proper or partial lists
    if isinstance(term1, ListTerm) and isinstance(term2, ListTerm):
        a_elems, a_tail = term1.elements, term1.tail
        b_elems, b_tail = term2.elements, term2.tail
        curr_theta = theta
        common = min(len(a_elems), len(b_elems))
        for i in range(common):
            curr_theta = unify(a_elems[i], b_elems[i], curr_theta)
            if curr_theta is None:
                return None

        if len(a_elems) > len(b_elems):
            remainder = ListTerm(a_elems[common:], a_tail, term1.line, term1.col)
            if b_tail is None:
                return curr_theta if (not remainder.elements and remainder.tail is None) else None
            return unify(b_tail, remainder, curr_theta)

        if len(b_elems) > len(a_elems):
            remainder = ListTerm(b_elems[common:], b_tail, term2.line, term2.col)
            if a_tail is None:
                return curr_theta if (not remainder.elements and remainder.tail is None) else None
            return unify(a_tail, remainder, curr_theta)

        # Same visible length: the tails must agree
        if a_tail is None and b_tail is None:
            return curr_theta
        if a_tail is None:
            return unify(ListTerm([], None, term1.line, term1.col), b_tail, curr_theta)
        if b_tail is None:
            return unify(a_tail, ListTerm([], None, term2.line, term2.col), curr_theta)
        return unify(a_tail, b_tail, curr_theta)

    return None

class ResolutionEngine:
    """
    SLD Resolution with Chronological Backtracking.
    Evaluates queries against knowledge base clauses parsed from the AST.
    """
    def __init__(self, ast: Program):
        self.ast = ast
        self.clauses = ast.clauses
        self.var_counter = 0

    def rename_variables(self, clause: Any, level: int) -> Any:
        """Standardizes variables apart to avoid name collisions across recursive calls."""
        c = copy.deepcopy(clause)
        rename_map: Dict[str, str] = {}

        def walk(t: Term) -> Term:
            if isinstance(t, Variable):
                if t.name not in rename_map:
                    self.var_counter += 1
                    rename_map[t.name] = f"{t.name}_{level}_{self.var_counter}"
                return Variable(rename_map[t.name], t.line, t.col)
            elif isinstance(t, CompoundTerm):
                return CompoundTerm(t.functor, [walk(a) for a in t.args], t.line, t.col)
            elif isinstance(t, ListTerm):
                return ListTerm([walk(e) for e in t.elements], walk(t.tail) if t.tail else None, t.line, t.col)
            return t

        if isinstance(c, Fact):
            c.head = walk(c.head)
        elif isinstance(c, Rule):
            c.head = walk(c.head)
            c.body = [walk(b) for b in c.body]
        return c

    def solve(self, query_goals: List[Term], max_solutions: int = 10) -> Dict[str, Any]:
        """Solves query_goals and returns all satisfying variable bindings and step trace."""
        solutions = []
        trace = []
        self.var_counter = 0

        # Collect user-requested query variables
        query_vars = set()
        def collect_qvars(t: Term):
            if isinstance(t, Variable):
                query_vars.add(t.name)
            elif isinstance(t, CompoundTerm):
                for a in t.args:
                    collect_qvars(a)
        for g in query_goals:
            collect_qvars(g)

        MAX_DEPTH = 35
        MAX_STEPS = 1000

        def evaluate_goals(goals: List[Term], theta: Substitution, depth: int):
            if len(solutions) >= max_solutions:
                return

            if depth > MAX_DEPTH or len(trace) >= MAX_STEPS:
                trace.append({
                    "step": len(trace) + 1,
                    "depth": depth,
                    "event": "DEPTH_LIMIT_EXCEEDED",
                    "description": f"Maximum resolution depth ({MAX_DEPTH}) reached; pruning branch."
                })
                return

            if not goals:
                # All subgoals satisfied! Extract answer substitution
                ans = {}
                for v in sorted(query_vars):
                    resolved = apply_subst(Variable(v), theta)
                    ans[v] = self.format_term(resolved)

                trace.append({
                    "step": len(trace) + 1,
                    "depth": depth,
                    "event": "SUCCESS",
                    "bindings": dict(ans),
                    "description": f"Goal proved with bindings: {ans if ans else 'true.'}"
                })
                solutions.append(ans)
                return

            current_goal = goals[0]
            rest_goals = goals[1:]

            # Built-in arithmetic evaluation: X is Expr, X > Y, X < Y, X >= Y, X =< Y, X = Y, X \= Y
            if isinstance(current_goal, CompoundTerm):
                f = current_goal.functor
                if f in (">", "<", ">=", "=<", "==", "\\==") and len(current_goal.args) == 2:
                    left = apply_subst(current_goal.args[0], theta)
                    right = apply_subst(current_goal.args[1], theta)
                    if isinstance(left, Number) and isinstance(right, Number):
                        lv, rv = left.value, right.value
                        sat = False
                        if f == ">": sat = lv > rv
                        elif f == "<": sat = lv < rv
                        elif f == ">=": sat = lv >= rv
                        elif f == "=<": sat = lv <= rv
                        elif f == "==": sat = lv == rv
                        elif f == "\\==": sat = lv != rv
                        if sat:
                            trace.append({
                                "step": len(trace) + 1,
                                "depth": depth,
                                "event": "BUILTIN_TRUE",
                                "description": f"Arithmetic condition {lv} {f} {rv} passed"
                            })
                            evaluate_goals(rest_goals, theta, depth + 1)
                        else:
                            trace.append({
                                "step": len(trace) + 1,
                                "depth": depth,
                                "event": "BUILTIN_FAIL",
                                "description": f"Arithmetic condition {lv} {f} {rv} failed; backtracking"
                            })
                        return

                if f == "is" and len(current_goal.args) == 2:
                    value = eval_arithmetic(current_goal.args[1], theta)
                    if value is not None:
                        mgu = unify(current_goal.args[0], Number(value), theta)
                        if mgu is not None:
                            shown = str(int(value)) if float(value).is_integer() else str(value)
                            trace.append({
                                "step": len(trace) + 1,
                                "depth": depth,
                                "event": "BUILTIN_ARITH",
                                "description": f"Arithmetic evaluation: result is {shown}"
                            })
                            evaluate_goals(rest_goals, mgu, depth + 1)
                            return
                    trace.append({
                        "step": len(trace) + 1,
                        "depth": depth,
                        "event": "BUILTIN_FAIL",
                        "description": "Arithmetic evaluation failed for 'is' expression; backtracking"
                    })
                    return

                if f == "=" and len(current_goal.args) == 2:
                    mgu = unify(current_goal.args[0], current_goal.args[1], theta)
                    if mgu is not None:
                        evaluate_goals(rest_goals, mgu, depth + 1)
                    return

            # Search Knowledge Base clauses
            for clause in self.clauses:
                renamed_clause = self.rename_variables(clause, depth)

                if isinstance(renamed_clause, Fact):
                    mgu = unify(current_goal, renamed_clause.head, theta)
                    if mgu is not None:
                        trace.append({
                            "step": len(trace) + 1,
                            "depth": depth,
                            "event": "UNIFY_FACT",
                            "goal": self.format_term(current_goal),
                            "clause": self.format_term(renamed_clause.head),
                            "description": f"Unification SUCCESS: goal '{self.format_term(current_goal)}' matched fact '{renamed_clause.head.functor}'"
                        })
                        evaluate_goals(rest_goals, mgu, depth + 1)

                elif isinstance(renamed_clause, Rule):
                    mgu = unify(current_goal, renamed_clause.head, theta)
                    if mgu is not None:
                        trace.append({
                            "step": len(trace) + 1,
                            "depth": depth,
                            "event": "UNIFY_RULE",
                            "goal": self.format_term(current_goal),
                            "rule_head": self.format_term(renamed_clause.head),
                            "subgoals": [self.format_term(b) for b in renamed_clause.body],
                            "description": f"Goal '{self.format_term(current_goal)}' matches rule head; expanding {len(renamed_clause.body)} subgoals"
                        })
                        # Replace current_goal with rule body
                        new_goals = renamed_clause.body + rest_goals
                        evaluate_goals(new_goals, mgu, depth + 1)

        evaluate_goals(query_goals, {}, 1)

        return {
            "query": " ?- " + ", ".join(self.format_term(g) for g in query_goals) + ".",
            "found_solution": len(solutions) > 0,
            "solution_count": len(solutions),
            "solutions": solutions,
            "trace": trace
        }

    def format_term(self, t: Term) -> str:
        if isinstance(t, Atom):
            return t.name
        elif isinstance(t, Variable):
            return t.name
        elif isinstance(t, Number):
            return str(int(t.value)) if t.value == int(t.value) else str(t.value)
        elif isinstance(t, CompoundTerm):
            args_str = ", ".join(self.format_term(a) for a in t.args)
            return f"{t.functor}({args_str})"
        elif isinstance(t, ListTerm):
            elems = [self.format_term(e) for e in t.elements]
            tail = t.tail
            while isinstance(tail, ListTerm):
                elems.extend(self.format_term(e) for e in tail.elements)
                tail = tail.tail
            suffix = f" | {self.format_term(tail)}" if tail is not None else ""
            return f"[{', '.join(elems)}{suffix}]"
        return str(t)
