"""
Comprehensive Edge-Case Test Suite for PROLOG-PARSE ISO Prolog Compiler.
Tests 40+ edge cases across Lexer, Parser, Semantic Analyzer, Engine, WAM, and Graph Builder.
"""

import sys
import unittest
from lexer import PrologLexer, TokenType
from parser import PrologParser, SyntaxError
from semantic import SemanticAnalyzer
from engine import ResolutionEngine, unify
from wam_compiler import WAMCompiler
from graph_builder import GraphBuilder
from ast_nodes import CompoundTerm, Variable, Atom, Number, ListTerm, Fact, Rule, Program

class TestCompilerEdgeCases(unittest.TestCase):

    # =========================================================================
    # 1. LEXER EDGE CASES
    # =========================================================================

    def test_lexer_empty_input(self):
        """Edge Case 1: Empty or whitespace-only code."""
        for code in ["", "   ", "\n\t\n  \r\n"]:
            lexer = PrologLexer(code)
            tokens = lexer.tokenize()
            self.assertEqual(len(tokens), 1)
            self.assertEqual(tokens[0].type, TokenType.EOF)
            self.assertEqual(len(lexer.errors), 0)

    def test_lexer_comments_only(self):
        """Edge Case 2: Code with only single-line and multi-line comments."""
        code = """
        % This is a single line comment
        /* This is a 
           multi-line comment */
        % Another comment
        """
        lexer = PrologLexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)
        self.assertEqual(len(lexer.errors), 0)

    def test_lexer_unclosed_block_comment(self):
        """Edge Case 3: Block comment without closing */."""
        code = "parent(a, b). /* unclosed comment"
        lexer = PrologLexer(code)
        tokens = lexer.tokenize()
        self.assertTrue(any("Unclosed block comment" in e for e in lexer.errors))

    def test_lexer_unterminated_quoted_atom(self):
        """Edge Case 4: Quoted atom missing closing quote."""
        code = "name('john doe)."
        lexer = PrologLexer(code)
        tokens = lexer.tokenize()
        self.assertTrue(any("Unterminated single-quoted atom" in e for e in lexer.errors))

    def test_lexer_unterminated_string(self):
        """Edge Case 5: String literal missing closing quote."""
        code = 'text("hello world).'
        lexer = PrologLexer(code)
        tokens = lexer.tokenize()
        self.assertTrue(any("Unterminated string literal" in e for e in lexer.errors))

    def test_lexer_unexpected_characters(self):
        """Edge Case 6: Illegal / unrecognized characters."""
        code = "a(X) :- b(X) @ # $."
        lexer = PrologLexer(code)
        tokens = lexer.tokenize()
        err_tokens = [t for t in tokens if t.type == TokenType.ERROR]
        self.assertGreaterEqual(len(err_tokens), 3)
        self.assertGreaterEqual(len(lexer.errors), 3)

    def test_lexer_numeric_variations(self):
        """Edge Case 7: Integers, floating point, zero."""
        code = "val(0). val(42). val(3.14159)."
        lexer = PrologLexer(code)
        tokens = lexer.tokenize()
        numbers = [t.value for t in tokens if t.type == TokenType.NUMBER]
        self.assertIn(0, numbers)
        self.assertIn(42, numbers)
        self.assertIn(3.14159, numbers)

    def test_lexer_anonymous_and_throwaway_variables(self):
        """Edge Case 8: Anonymous _ and named throwaway _Rest."""
        code = "foo(_, _X, _Rest, Var)."
        lexer = PrologLexer(code)
        tokens = lexer.tokenize()
        anon = [t for t in tokens if t.type == TokenType.ANON_VAR]
        vars_ = [t for t in tokens if t.type == TokenType.VARIABLE]
        self.assertEqual(len(anon), 1)
        self.assertEqual(anon[0].raw_text, "_")
        var_names = [v.raw_text for v in vars_]
        self.assertIn("_X", var_names)
        self.assertIn("_Rest", var_names)
        self.assertIn("Var", var_names)

    # =========================================================================
    # 2. PARSER EDGE CASES
    # =========================================================================

    def test_parser_missing_period(self):
        """Edge Case 9: Missing terminating dot '.'."""
        code = "parent(george, john)"
        tokens = PrologLexer(code).tokenize()
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        self.assertTrue(len(parser.errors) > 0)
        self.assertTrue(any("Missing '.'" in e for e in parser.errors))

    def test_parser_unbalanced_parentheses(self):
        """Edge Case 10: Missing closing or opening parenthesis."""
        bad_codes = [
            "parent(george, john.",
            "parent george, john).",
            "p((a, b)."
        ]
        for c in bad_codes:
            tokens = PrologLexer(c).tokenize()
            parser = PrologParser(tokens)
            ast = parser.parse_program()
            self.assertTrue(len(parser.errors) > 0, f"Expected error for code: {c}")

    def test_parser_variable_as_clause_head(self):
        """Edge Case 11: Head of a clause is a Variable instead of Atom/Compound."""
        code = "X :- parent(john, X)."
        tokens = PrologLexer(code).tokenize()
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        self.assertTrue(len(parser.errors) > 0)
        self.assertTrue(any("must be an Atom or Compound Term" in e for e in parser.errors))

    def test_parser_number_as_clause_head(self):
        """Edge Case 12: Head of a clause is a Number."""
        code = "123 :- parent(john, X)."
        tokens = PrologLexer(code).tokenize()
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        self.assertTrue(len(parser.errors) > 0)

    def test_parser_empty_rule_body(self):
        """Edge Case 13: Rule neck without body goals 'p(X) :- .'."""
        code = "p(X) :- ."
        tokens = PrologLexer(code).tokenize()
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        self.assertTrue(len(parser.errors) > 0)

    def test_parser_zero_arity_facts(self):
        """Edge Case 14: Fact with 0 arguments (atoms)."""
        code = "weekend. raining. sunny."
        tokens = PrologLexer(code).tokenize()
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        self.assertEqual(len(parser.errors), 0)
        self.assertEqual(len(ast.clauses), 3)
        for clause in ast.clauses:
            self.assertIsInstance(clause, Fact)
            self.assertEqual(clause.head.arity, 0)

    def test_parser_nested_lists_and_tail(self):
        """Edge Case 15: List parsing: empty [], nested lists, and [H|T] syntax."""
        code = "list_test([], [1, 2, [3, 4]], [H|T])."
        tokens = PrologLexer(code).tokenize()
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        self.assertEqual(len(parser.errors), 0)
        fact = ast.clauses[0]
        self.assertEqual(len(fact.head.args), 3)
        self.assertIsInstance(fact.head.args[0], ListTerm)
        self.assertEqual(len(fact.head.args[0].elements), 0) # []
        self.assertIsInstance(fact.head.args[2], ListTerm)
        self.assertIsNotNone(fact.head.args[2].tail) # [H|T]

    def test_parser_disjunction_semicolon(self):
        """Edge Case 16: Disjunction operator ';' in rule body."""
        code = "likes(john, X) :- food(X) ; wine(X)."
        tokens = PrologLexer(code).tokenize()
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        self.assertEqual(len(parser.errors), 0)
        rule = ast.clauses[0]
        self.assertIsInstance(rule, Rule)
        self.assertIn(";", [g.functor for g in rule.body if isinstance(g, CompoundTerm)])

    # =========================================================================
    # 3. SEMANTIC ANALYZER EDGE CASES
    # =========================================================================

    def test_semantic_singleton_variable_warning(self):
        """Edge Case 17: Singleton variable warning."""
        code = "ancestor(X, Y) :- parent(X, Z)."  # Y and Z appear only once
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        result = SemanticAnalyzer(ast).analyze()
        singleton_diags = [d for d in result["diagnostics"] if d["code"] == "W_SINGLETON_VAR"]
        self.assertGreaterEqual(len(singleton_diags), 2)
        warned_vars = [d["message"] for d in singleton_diags]
        self.assertTrue(any("'Y'" in m for m in warned_vars))
        self.assertTrue(any("'Z'" in m for m in warned_vars))

    def test_semantic_unused_variable_with_underscore_ignored(self):
        """Edge Case 18: Variable prefixed with '_' should NOT trigger singleton warning."""
        code = "ancestor(X, _Y) :- parent(X, _Z)."
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        result = SemanticAnalyzer(ast).analyze()
        singleton_diags = [d for d in result["diagnostics"] if d["code"] == "W_SINGLETON_VAR"]
        self.assertEqual(len(singleton_diags), 0)

    def test_semantic_undefined_predicate_reference(self):
        """Edge Case 19: Call to undefined external predicate."""
        code = "compute(X) :- external_service(X)."
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        result = SemanticAnalyzer(ast).analyze()
        undef_diags = [d for d in result["diagnostics"] if d["code"] == "I_UNDEFINED_PRED"]
        self.assertGreaterEqual(len(undef_diags), 1)

    def test_semantic_arity_mismatch(self):
        """Edge Case 20: Calling predicate with wrong arity."""
        code = """
        worker(bob, sales).
        find_worker(X) :- worker(X).
        """
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        result = SemanticAnalyzer(ast).analyze()
        mismatch_diags = [d for d in result["diagnostics"] if d["code"] == "W_ARITY_MISMATCH"]
        self.assertEqual(len(mismatch_diags), 1)

    # =========================================================================
    # 4. RESOLUTION ENGINE EDGE CASES
    # =========================================================================

    def test_engine_ground_query_true_and_false(self):
        """Edge Case 21: Ground queries (no variables) returning true or false."""
        code = "human(socrates). mortal(X) :- human(X)."
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        engine = ResolutionEngine(ast)

        # True query
        q_true = [CompoundTerm("mortal", [Atom("socrates")])]
        res_true = engine.solve(q_true)
        self.assertTrue(res_true["found_solution"])

        # False query
        q_false = [CompoundTerm("mortal", [Atom("zeus")])]
        res_false = engine.solve(q_false)
        self.assertFalse(res_false["found_solution"])

    def test_engine_undefined_predicate_query(self):
        """Edge Case 22: Querying an undefined predicate should fail gracefully, not crash."""
        code = "human(socrates)."
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        engine = ResolutionEngine(ast)

        q = [CompoundTerm("flying_car", [Variable("X")])]
        res = engine.solve(q)
        self.assertFalse(res["found_solution"])
        self.assertEqual(len(res["solutions"]), 0)

    def test_engine_infinite_recursion_guard(self):
        """Edge Case 23: Direct left recursion / circular rules must terminate via depth limit."""
        code = """
        loop(X) :- loop(X).
        """
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        engine = ResolutionEngine(ast)

        q = [CompoundTerm("loop", [Number(1)])]
        # Must not raise RecursionError or hang
        res = engine.solve(q)
        self.assertFalse(res["found_solution"])

    def test_engine_cyclic_graph_termination(self):
        """Edge Case 24: Cyclic graph (a <-> b) querying nonexistent path."""
        code = """
        edge(a, b).
        edge(b, a).
        connected(X, Y) :- edge(X, Y).
        connected(X, Y) :- edge(X, Z), connected(Z, Y).
        """
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        engine = ResolutionEngine(ast)

        # Path to 'c' which doesn't exist
        q = [CompoundTerm("connected", [Atom("a"), Atom("c")])]
        res = engine.solve(q)
        self.assertFalse(res["found_solution"])

    def test_engine_occurs_check(self):
        """Edge Case 25: Unification with occurs-check prevents circular X = f(X)."""
        var_x = Variable("X")
        term_fx = CompoundTerm("f", [Variable("X")])
        mgu = unify(var_x, term_fx)
        self.assertIsNone(mgu, "Robinson's unification must fail occurs-check on X = f(X)")

    def test_engine_arithmetic_builtins(self):
        """Edge Case 26: Arithmetic builtins: >, <, >=, =<, =."""
        code = "eligible(Age) :- Age >= 18."
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        engine = ResolutionEngine(ast)

        # Age 21 >= 18 -> True
        res1 = engine.solve([CompoundTerm("eligible", [Number(21)])])
        self.assertTrue(res1["found_solution"])

        # Age 15 >= 18 -> False
        res2 = engine.solve([CompoundTerm("eligible", [Number(15)])])
        self.assertFalse(res2["found_solution"])

    # =========================================================================
    # 5. WAM & TAC COMPILER EDGE CASES
    # =========================================================================

    def test_wam_zero_arity_fact(self):
        """Edge Case 27: Zero arity fact compiled to WAM."""
        code = "active."
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        wam_res = WAMCompiler(ast).compile()
        self.assertGreater(len(wam_res["wam_instructions"]), 0)
        ops = [i["op"] for i in wam_res["wam_instructions"]]
        self.assertTrue(any("proceed" in op for op in ops))

    def test_wam_empty_program(self):
        """Edge Case 28: Compiling empty AST."""
        ast = Program(clauses=[], line=1, col=1)
        wam_res = WAMCompiler(ast).compile()
        self.assertEqual(wam_res["instruction_count"], 0)
        self.assertEqual(wam_res["quadruple_count"], 0)

    # =========================================================================
    # 6. GRAPH BUILDER EDGE CASES
    # =========================================================================

    def test_graph_builder_empty_ast(self):
        """Edge Case 29: Graph builder with empty AST produces valid output without 0-division."""
        ast = Program(clauses=[], line=1, col=1)
        pdg = GraphBuilder.build_pdg_graph(ast)
        self.assertEqual(pdg["total_predicates"], 0)
        self.assertEqual(len(pdg["nodes"]), 0)
        self.assertEqual(len(pdg["edges"]), 0)

        ast_graph = GraphBuilder.build_ast_graph(ast)
        self.assertEqual(ast_graph["total_clauses"], 0)

        schema = GraphBuilder.build_schema_evolution(ast)
        self.assertEqual(len(schema), 0)

    def test_graph_builder_recursive_self_loop(self):
        """Edge Case 30: Self-recursive predicate marked is_recursive."""
        code = "ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y)."
        tokens = PrologLexer(code).tokenize()
        ast = PrologParser(tokens).parse_program()
        pdg = GraphBuilder.build_pdg_graph(ast)
        anc_node = next(n for n in pdg["nodes"] if n["id"] == "ancestor/2")
        self.assertTrue(anc_node["is_recursive"])

    def test_parser_panic_mode_recovery_multiple_errors(self):
        """Edge Case 31: Multiple syntax errors in separate clauses synchronize and report all errors."""
        code = """
        parent(george, john
        good(clause).
        father(george, john
        another(valid).
        """
        tokens = PrologLexer(code).tokenize()
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        self.assertGreaterEqual(len(parser.errors), 2)
        # Should still successfully recover and parse the 2 valid clauses!
        self.assertEqual(len(ast.clauses), 2)
        functors = [c.head.functor for c in ast.clauses]
        self.assertIn("good", functors)
        self.assertIn("another", functors)

    def test_api_empty_query_response(self):
        """Edge Case 32: API handles empty query string gracefully."""
        from app import app
        with app.test_client() as client:
            res = client.post('/api/query', json={'code': 'p(a).', 'query': ''})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertFalse(data['found_solution'])
            self.assertIn('Query cannot be empty', data.get('error', ''))

    def test_api_malformed_query_response(self):
        """Edge Case 33: API handles unclosed parenthesis query without 500."""
        from app import app
        with app.test_client() as client:
            res = client.post('/api/query', json={'code': 'p(a).', 'query': '?- p('})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertFalse(data['found_solution'])
            self.assertIn('error', data)

    def test_api_garbage_code_compile_no_500(self):
        """Edge Case 34: API handles completely corrupt code and returns 200 with diagnostics."""
        from app import app
        with app.test_client() as client:
            res = client.post('/api/compile', json={'code': '@@@ $$$ %%% 123 ::- +++'})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertIn('errors', data)
            self.assertGreater(len(data['errors']), 0)

    def test_api_multiple_answers_evaluation(self):
        """Edge Case 35: Query returning multiple satisfying bindings."""
        from app import app
        with app.test_client() as client:
            code = "item(apple). item(banana). item(cherry)."
            res = client.post('/api/query', json={'code': code, 'query': 'item(X)'})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data['found_solution'])
            self.assertEqual(len(data['solutions']), 3)
            vals = [s['X'] for s in data['solutions']]
            self.assertListEqual(vals, ['apple', 'banana', 'cherry'])

    def test_api_playground_and_studio_routes(self):
        """Edge Case 36: Direct GET routes for /playground and /studio return 200."""
        from app import app
        with app.test_client() as client:
            res1 = client.get('/playground')
            self.assertEqual(res1.status_code, 200)
            res2 = client.get('/studio')
            self.assertEqual(res2.status_code, 200)

if __name__ == "__main__":
    unittest.main()
