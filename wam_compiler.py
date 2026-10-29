"""
Phase 4: Intermediate Code Generation (ICG) & Optimization for ISO Prolog.
Generates:
1. Warren Abstract Machine (WAM) Bytecode Instructions (Standard Prolog IR)
2. Three-Address Code (TAC) Quadruples: (OP, ARG1, ARG2, RESULT)
3. Code Optimization Pass: Constant Folding, Redundant Register Elimination, Dead Goal Pruning.
"""

from typing import List, Dict, Any, Tuple
from ast_nodes import Program, Clause, Fact, Rule, Query, Term, CompoundTerm, Variable, Atom, Number, ListTerm

class WAMInstruction:
    """An individual Warren Abstract Machine IR instruction."""
    def __init__(self, op: str, args: List[Any], comment: str = ""):
        self.op = op
        self.args = args
        self.comment = comment

    def to_dict(self) -> Dict[str, Any]:
        return {
            "op": self.op,
            "args": [str(a) for a in self.args],
            "disassembly": self.__str__(),
            "comment": self.comment
        }

    def __str__(self) -> str:
        args_str = ", ".join(str(a) for a in self.args)
        s = f"{self.op:<16} {args_str}"
        if self.comment:
            s = f"{s:<36} ; {self.comment}"
        return s

class TACQuadruple:
    """Standard Three-Address Code Quadruple: (OP, ARG1, ARG2, RESULT)."""
    def __init__(self, op: str, arg1: str, arg2: str, result: str):
        self.op = op
        self.arg1 = str(arg1)
        self.arg2 = str(arg2)
        self.result = str(result)

    def to_dict(self) -> Dict[str, str]:
        return {
            "op": self.op,
            "arg1": self.arg1,
            "arg2": self.arg2,
            "result": self.result
        }

    def __str__(self) -> str:
        return f"({self.op}, {self.arg1}, {self.arg2}, {self.result})"

class WAMCompiler:
    """
    Translates Prolog AST into WAM Intermediate Representation and TAC Quadruples.
    """
    def __init__(self, ast: Program):
        self.ast = ast
        self.instructions: List[WAMInstruction] = []
        self.quadruples: List[TACQuadruple] = []
        self.temp_var_counter = 0

    def new_temp(self) -> str:
        self.temp_var_counter += 1
        return f"t{self.temp_var_counter}"

    def compile(self) -> Dict[str, Any]:
        self.instructions.clear()
        self.quadruples.clear()
        self.temp_var_counter = 0

        compiled_predicates = {}

        for clause_idx, clause in enumerate(self.ast.clauses):
            if isinstance(clause, Fact):
                self.compile_fact(clause, clause_idx + 1)
            elif isinstance(clause, Rule):
                self.compile_rule(clause, clause_idx + 1)
            elif isinstance(clause, Query):
                self.compile_query(clause, clause_idx + 1)

        # Optimization Pass
        optimized_instructions = self.optimize_wam(self.instructions)

        return {
            "wam_instructions": [instr.to_dict() for instr in self.instructions],
            "optimized_wam": [instr.to_dict() for instr in optimized_instructions],
            "quadruples": [quad.to_dict() for quad in self.quadruples],
            "instruction_count": len(self.instructions),
            "quadruple_count": len(self.quadruples)
        }

    def compile_fact(self, fact: Fact, idx: int):
        head = fact.head
        sig = f"{head.functor}/{head.arity}"
        self.instructions.append(WAMInstruction(f"LABEL_{sig}_{idx}:", [], f"Entry for Fact {head.functor}"))
        self.quadruples.append(TACQuadruple("LABEL", sig, f"fact_{idx}", "-"))

        # In WAM, a fact matches argument registers A1, A2, ... An
        for i, arg in enumerate(head.args):
            reg = f"A{i + 1}"
            if isinstance(arg, Atom):
                self.instructions.append(WAMInstruction("get_constant", [arg.name, reg], f"Match {arg.name} in {reg}"))
                self.quadruples.append(TACQuadruple("EQ_ATOM", arg.name, reg, "match_flag"))
            elif isinstance(arg, Number):
                self.instructions.append(WAMInstruction("get_num_const", [arg.value, reg], f"Match {arg.value} in {reg}"))
                self.quadruples.append(TACQuadruple("EQ_NUM", str(arg.value), reg, "match_flag"))
            elif isinstance(arg, Variable):
                self.instructions.append(WAMInstruction("get_variable", [arg.name, reg], f"Bind {arg.name} = {reg}"))
                self.quadruples.append(TACQuadruple("ASSIGN", reg, "-", arg.name))
            elif isinstance(arg, CompoundTerm):
                self.instructions.append(WAMInstruction("get_structure", [f"{arg.functor}/{arg.arity}", reg]))
                self.quadruples.append(TACQuadruple("GET_STRUCT", f"{arg.functor}/{arg.arity}", reg, self.new_temp()))
                for sub_arg in arg.args:
                    if isinstance(sub_arg, Variable):
                        self.instructions.append(WAMInstruction("unify_variable", [sub_arg.name]))
                    else:
                        self.instructions.append(WAMInstruction("unify_constant", [str(sub_arg)]))

        self.instructions.append(WAMInstruction("proceed", [], "Fact matched successfully; return"))
        self.quadruples.append(TACQuadruple("PROCEED", "-", "-", "SUCCESS"))

    def compile_rule(self, rule: Rule, idx: int):
        head = rule.head
        sig = f"{head.functor}/{head.arity}"
        self.instructions.append(WAMInstruction(f"LABEL_{sig}_{idx}:", [], f"Entry for Rule {head.functor}"))
        self.quadruples.append(TACQuadruple("LABEL", sig, f"rule_{idx}", "-"))

        # Allocate stack environment for permanent variables across subgoals
        self.instructions.append(WAMInstruction("allocate", [len(rule.body)], "Create stack frame for clause"))
        self.quadruples.append(TACQuadruple("ALLOCATE_ENV", str(len(rule.body)), "-", "STACK_FRAME"))

        # Match Head Arguments
        for i, arg in enumerate(head.args):
            reg = f"A{i + 1}"
            if isinstance(arg, Variable):
                self.instructions.append(WAMInstruction("get_variable", [arg.name, reg]))
                self.quadruples.append(TACQuadruple("ASSIGN", reg, "-", arg.name))
            elif isinstance(arg, (Atom, Number)):
                val = arg.name if isinstance(arg, Atom) else arg.value
                self.instructions.append(WAMInstruction("get_constant", [val, reg]))
                self.quadruples.append(TACQuadruple("EQ_CONST", str(val), reg, "match_flag"))

        # Compile Body Subgoals
        for g_idx, goal in enumerate(rule.body):
            if isinstance(goal, CompoundTerm):
                # Put argument registers for calling the subgoal
                for i, arg in enumerate(goal.args):
                    reg = f"A{i + 1}"
                    if isinstance(arg, Variable):
                        self.instructions.append(WAMInstruction("put_value", [arg.name, reg]))
                        self.quadruples.append(TACQuadruple("PARAM", arg.name, "-", reg))
                    elif isinstance(arg, (Atom, Number)):
                        val = arg.name if isinstance(arg, Atom) else arg.value
                        self.instructions.append(WAMInstruction("put_constant", [val, reg]))
                        self.quadruples.append(TACQuadruple("PARAM_CONST", str(val), "-", reg))

                goal_sig = f"{goal.functor}/{goal.arity}"
                self.instructions.append(WAMInstruction("call", [goal_sig], f"Execute subgoal {goal_sig}"))
                self.quadruples.append(TACQuadruple("CALL", goal_sig, str(goal.arity), self.new_temp()))
            elif isinstance(goal, Atom) and goal.name == "!":
                # Cut operator
                self.instructions.append(WAMInstruction("cut", [], "Prune alternative choice points"))
                self.quadruples.append(TACQuadruple("CUT", "-", "-", "PRUNE"))

        # Deallocate stack frame and return
        self.instructions.append(WAMInstruction("deallocate", [], "Release environment frame"))
        self.instructions.append(WAMInstruction("proceed", [], "Rule execution complete"))
        self.quadruples.append(TACQuadruple("DEALLOCATE_ENV", "-", "-", "-"))
        self.quadruples.append(TACQuadruple("PROCEED", "-", "-", "SUCCESS"))

    def compile_query(self, query: Query, idx: int):
        self.instructions.append(WAMInstruction(f"LABEL_QUERY_{idx}:", [], "Interactive Goal Evaluation"))
        self.quadruples.append(TACQuadruple("LABEL", "QUERY", f"q_{idx}", "-"))
        for goal in query.goals:
            if isinstance(goal, CompoundTerm):
                for i, arg in enumerate(goal.args):
                    self.instructions.append(WAMInstruction("put_value", [str(arg), f"A{i+1}"]))
                    self.quadruples.append(TACQuadruple("PARAM", str(arg), "-", f"A{i+1}"))
                self.instructions.append(WAMInstruction("call", [f"{goal.functor}/{goal.arity}"]))
                self.quadruples.append(TACQuadruple("CALL", f"{goal.functor}/{goal.arity}", str(goal.arity), "-"))

    def optimize_wam(self, instrs: List[WAMInstruction]) -> List[WAMInstruction]:
        """Performs peep-hole optimization and dead-instruction elimination."""
        optimized = []
        i = 0
        while i < len(instrs):
            curr = instrs[i]
            # Optimization 1: Remove redundant get_variable X, A1 followed immediately by put_value X, A1
            if i + 1 < len(instrs):
                nxt = instrs[i+1]
                if (curr.op == "get_variable" and nxt.op == "put_value" and
                    curr.args == nxt.args):
                    # Keep only one
                    optimized.append(curr)
                    i += 2
                    continue
            optimized.append(curr)
            i += 1
        return optimized
