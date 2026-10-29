"""
Graph Model Builder for PROLOG-PARSE Studio.
Computes layout coordinates, hierarchical levels, and dependency metadata for:
1. Predicate Dependency Graph (PDG) with layered topological layout
2. Collapsible Abstract Syntax Tree (AST) Hierarchy
3. SLD Resolution Proof Tree with branch lineage
4. Schema Evolution State Transitions
"""

from typing import Dict, List, Any, Optional, Set
from ast_nodes import Program, Fact, Rule, Query, Term, CompoundTerm, Variable, Atom, Number, ListTerm

class GraphBuilder:

    @staticmethod
    def build_pdg_graph(ast: Program, width: int = 1100, height: int = 700) -> Dict[str, Any]:
        """
        Constructs a balanced, layered Predicate Dependency Graph (PDG).
        Computes levels (Facts, Intermediate Rules, Recursive Rules) and spread coordinates.
        """
        nodes_dict: Dict[str, Dict[str, Any]] = {}
        edges: List[Dict[str, Any]] = []
        edge_set: Set[tuple] = set()

        # Step 1: Register all predicates
        for idx, clause in enumerate(ast.clauses):
            if isinstance(clause, (Fact, Rule)):
                head = clause.head
                sig = f"{head.functor}/{head.arity}"
                if sig not in nodes_dict:
                    nodes_dict[sig] = {
                        "id": sig,
                        "label": sig,
                        "type": "PREDICATE_NODE",
                        "functor": head.functor,
                        "arity": head.arity,
                        "facts": 0,
                        "rules": 0,
                        "lines": [],
                        "is_recursive": False,
                        "upstream": [],
                        "downstream": []
                    }
                nodes_dict[sig]["lines"].append(clause.line)
                if isinstance(clause, Fact):
                    nodes_dict[sig]["facts"] += 1
                else:
                    nodes_dict[sig]["rules"] += 1

        # Step 2: Extract call dependencies
        for clause in ast.clauses:
            if isinstance(clause, Rule):
                caller_sig = f"{clause.head.functor}/{clause.head.arity}"
                for goal in clause.body:
                    if isinstance(goal, CompoundTerm):
                        callee_sig = f"{goal.functor}/{goal.arity}"
                        if callee_sig not in nodes_dict:
                            nodes_dict[callee_sig] = {
                                "id": callee_sig,
                                "label": callee_sig,
                                "type": "BUILTIN_OR_EXTERN",
                                "functor": goal.functor,
                                "arity": goal.arity,
                                "facts": 0,
                                "rules": 0,
                                "lines": [goal.line],
                                "is_recursive": False,
                                "upstream": [],
                                "downstream": []
                            }

                        edge_key = (caller_sig, callee_sig)
                        if edge_key not in edge_set:
                            edge_set.add(edge_key)
                            is_rec = (caller_sig == callee_sig)
                            if is_rec:
                                nodes_dict[caller_sig]["is_recursive"] = True

                            edges.append({
                                "id": f"pdg_{caller_sig}_to_{callee_sig}",
                                "source": caller_sig,
                                "target": callee_sig,
                                "kind": "RECURSIVE_CALL" if is_rec else "SUBGOAL_CALL",
                                "line": goal.line
                            })

                            nodes_dict[caller_sig]["downstream"].append(callee_sig)
                            nodes_dict[callee_sig]["upstream"].append(caller_sig)

        # Step 3: Layer Assignment (Topological Rank)
        # Layer 0: Pure facts (no outgoing calls)
        # Layer 1: Rules calling only facts
        # Layer 2: Higher-order or recursive rules
        # Layer 3: Operators / Builtins
        layer_0 = [] # facts
        layer_1 = [] # intermediate rules
        layer_2 = [] # recursive rules
        layer_3 = [] # builtins / terminal utilities

        for sig, node in nodes_dict.items():
            if node["type"] == "BUILTIN_OR_EXTERN":
                layer_3.append(node)
            elif node["is_recursive"]:
                layer_2.append(node)
            elif node["facts"] > 0 and node["rules"] == 0:
                layer_0.append(node)
            else:
                layer_1.append(node)

        # Compute balanced (x, y) coordinates
        layers = [layer_0, layer_1, layer_2, layer_3]
        active_layers = [l for l in layers if l]
        total_layers = len(active_layers)
        y_step = height / (total_layers + 1)

        for l_idx, layer in enumerate(active_layers):
            y_pos = (l_idx + 1) * y_step
            count = len(layer)
            x_step = width / (count + 1)
            for n_idx, node in enumerate(layer):
                node["x"] = int((n_idx + 1) * x_step - 80)
                node["y"] = int(y_pos - 25)

        return {
            "nodes": list(nodes_dict.values()),
            "edges": edges,
            "total_predicates": len(nodes_dict),
            "total_dependencies": len(edges)
        }

    @staticmethod
    def build_ast_graph(ast: Program) -> Dict[str, Any]:
        """Constructs an expandable AST hierarchy with pre-grouped clause packages."""
        clauses_data = []

        for idx, clause in enumerate(ast.clauses):
            c_type = "Fact" if isinstance(clause, Fact) else ("Rule" if isinstance(clause, Rule) else "Query")
            head_str = f"{clause.head.functor}/{clause.head.arity}" if hasattr(clause, 'head') else "Query"

            clause_entry = {
                "id": f"clause_{idx+1}",
                "index": idx + 1,
                "type": c_type,
                "head": head_str,
                "line": clause.line,
                "col": clause.col,
                "code": repr(clause),
                "nodes": []
            }

            # Collect terms inside this clause
            def collect_terms(t: Term, parent_label: str):
                if isinstance(t, CompoundTerm):
                    clause_entry["nodes"].append({
                        "label": f"{t.functor}/{t.arity}",
                        "kind": "Compound",
                        "line": t.line,
                        "parent": parent_label
                    })
                    for a in t.args:
                        collect_terms(a, f"{t.functor}/{t.arity}")
                elif isinstance(t, Atom):
                    clause_entry["nodes"].append({
                        "label": f"'{t.name}'",
                        "kind": "Atom",
                        "line": t.line,
                        "parent": parent_label
                    })
                elif isinstance(t, Variable):
                    clause_entry["nodes"].append({
                        "label": t.name,
                        "kind": "Variable",
                        "line": t.line,
                        "parent": parent_label
                    })
                elif isinstance(t, Number):
                    clause_entry["nodes"].append({
                        "label": str(t.value),
                        "kind": "Number",
                        "line": t.line,
                        "parent": parent_label
                    })
                elif isinstance(t, ListTerm):
                    clause_entry["nodes"].append({
                        "label": f"[{len(t.elements)} items]",
                        "kind": "List",
                        "line": t.line,
                        "parent": parent_label
                    })

            if hasattr(clause, 'head'):
                collect_terms(clause.head, "Head")
            if hasattr(clause, 'body'):
                for b in clause.body:
                    collect_terms(b, "Body")

            clauses_data.append(clause_entry)

        return {
            "total_clauses": len(clauses_data),
            "clauses": clauses_data,
            "count": sum(len(c["nodes"]) for c in clauses_data) + len(clauses_data)
        }

    @staticmethod
    def build_schema_evolution(ast: Program) -> List[Dict[str, Any]]:
        """Constructs state transitions with clause diffs."""
        states = []
        registered_symbols = set()
        facts_cnt = 0
        rules_cnt = 0

        for idx, clause in enumerate(ast.clauses):
            if isinstance(clause, Fact):
                facts_cnt += 1
                sig = f"{clause.head.functor}/{clause.head.arity}"
                registered_symbols.add(sig)
                states.append({
                    "step": idx + 1,
                    "id": f"state_{idx+1}",
                    "title": f"{sig} [Fact #{facts_cnt}]",
                    "type": "FACT_REGISTRATION",
                    "line": clause.line,
                    "symbol_name": clause.head.functor,
                    "arity": clause.head.arity,
                    "code_snippet": repr(clause),
                    "active_predicates_count": len(registered_symbols),
                    "facts_count": facts_cnt,
                    "rules_count": rules_cnt,
                    "added_symbols": [sig]
                })
            elif isinstance(clause, Rule):
                rules_cnt += 1
                sig = f"{clause.head.functor}/{clause.head.arity}"
                registered_symbols.add(sig)
                states.append({
                    "step": idx + 1,
                    "id": f"state_{idx+1}",
                    "title": f"{sig} [Rule #{rules_cnt}]",
                    "type": "RULE_REGISTRATION",
                    "line": clause.line,
                    "symbol_name": clause.head.functor,
                    "arity": clause.head.arity,
                    "code_snippet": repr(clause),
                    "subgoals": [repr(g) for g in clause.body],
                    "active_predicates_count": len(registered_symbols),
                    "facts_count": facts_cnt,
                    "rules_count": rules_cnt,
                    "added_symbols": [sig]
                })

        return states
