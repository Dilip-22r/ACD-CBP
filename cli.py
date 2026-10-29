#!/usr/bin/env python3
"""
PROLOG-C CLI Debugging & Analysis Tool
Course: Compiler Design Laboratory (22PC2CS301)
Department of Computer Science & Engineering, VNRVJIET

Commands:
  python cli.py lex <file.pl>          # Tokenizer & Lexical Analysis Dump
  python cli.py parse <file.pl>        # AST Tree Hierarchy Explorer
  python cli.py pdg <file.pl>          # Predicate Dependency Graph (PDG)
  python cli.py check <file.pl>        # Static Semantic Linting & Singleton Detection
  python cli.py wam <file.pl>          # Warren Abstract Machine (WAM) Bytecode & TAC
  python cli.py query <file.pl> <goal> # Execute query and print answers
  python cli.py debug <file.pl> <goal> # Interactive Step-by-Step Backtracking Debugger
"""

import sys
import os
import argparse

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from lexer import PrologLexer, TokenType
from parser import PrologParser, SyntaxError
from semantic import SemanticAnalyzer
from wam_compiler import WAMCompiler
from engine import ResolutionEngine
from graph_builder import GraphBuilder

def print_banner():
    print("=" * 68)
    print(" [PROLOG-C] CLI COMPILER & LOGIC DEBUGGING WORKBENCH")
    print("  Course: 22PC2CS301 (Compiler Design Lab)")
    print("=" * 68)

def cmd_lex(args):
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    lexer = PrologLexer(code)
    tokens = lexer.tokenize()

    print(f"\n--- [Phase 1: Lexical Analysis] ---")
    print(f"File: {args.file} | Total Tokens: {len(tokens)}\n")
    print(f"{'#':<4} {'Type':<16} {'Line:Col':<10} {'Lexeme Value'}")
    print("-" * 60)
    for idx, t in enumerate(tokens):
        if t.type == TokenType.EOF:
            continue
        print(f"{idx+1:<4} {t.type:<16} {f'{t.line}:{t.col}':<10} {repr(t.raw_text)}")

    summary = lexer.get_token_summary()
    print("\nToken Category Distribution:")
    for cat, cnt in sorted(summary['distribution'].items()):
        print(f"  • {cat:<16}: {cnt}")

    if lexer.errors:
        print("\n[!] Lexical Errors:")
        for err in lexer.errors:
            print(f"  ❌ {err}")

def cmd_parse(args):
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    tokens = PrologLexer(code).tokenize()
    parser = PrologParser(tokens)
    ast = parser.parse_program()

    print(f"\n--- [Phase 2: Abstract Syntax Tree (AST)] ---")
    print(f"File: {args.file} | Total Clauses: {len(ast.clauses)}\n")

    def print_ast_tree(node, prefix="", is_tail=True):
        connector = "└── " if is_tail else "├── "
        node_name = node.__class__.__name__

        if hasattr(node, "functor"):
            val_str = f" : {node.functor}/{node.arity}"
        elif hasattr(node, "name"):
            val_str = f" : '{node.name}'"
        elif hasattr(node, "value"):
            val_str = f" : {node.value}"
        else:
            val_str = ""

        print(prefix + connector + f"\033[36m[{node_name}]\033[0m" + val_str)
        new_prefix = prefix + ("    " if is_tail else "│   ")

        children = []
        if hasattr(node, "clauses"):
            children = node.clauses
        elif hasattr(node, "head") and hasattr(node, "body"):
            children = [node.head] + node.body
        elif hasattr(node, "head"):
            children = [node.head]
        elif hasattr(node, "args"):
            children = node.args
        elif hasattr(node, "elements"):
            children = node.elements + ([node.tail] if node.tail else [])
        elif hasattr(node, "goals"):
            children = node.goals

        for i, child in enumerate(children):
            print_ast_tree(child, new_prefix, i == len(children) - 1)

    print_ast_tree(ast)

    if parser.errors:
        print("\n[!] Syntax Errors Encountered:")
        for err in parser.errors:
            print(f"  ❌ {err}")

def cmd_pdg(args):
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    tokens = PrologLexer(code).tokenize()
    ast = PrologParser(tokens).parse_program()
    pdg = GraphBuilder.build_pdg_graph(ast)

    print(f"\n--- [Predicate Dependency Graph (PDG)] ---")
    print(f"File: {args.file} | Predicates: {pdg['total_predicates']} | Edges: {pdg['total_dependencies']}\n")

    for node in pdg['nodes']:
        rec_flag = " [RECURSIVE ↺]" if node['is_recursive'] else ""
        print(f"📌 \033[33m{node['label']}\033[0m (Facts: {node['facts']}, Rules: {node['rules']}){rec_flag}")
        if node['downstream']:
            print(f"   └── Calls Subgoals: {', '.join(node['downstream'])}")
        if node['upstream']:
            print(f"   └── Called By:      {', '.join(node['upstream'])}")
        print()

def cmd_check(args):
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    tokens = PrologLexer(code).tokenize()
    ast = PrologParser(tokens).parse_program()
    analyzer = SemanticAnalyzer(ast)
    results = analyzer.analyze()

    print(f"\n--- [Phase 3: Semantic Analysis & Symbol Table] ---")
    print(f"File: {args.file}\n")
    print(f"{'Signature':<18} {'Arity':<8} {'Facts':<8} {'Rules':<8} {'Defined at Lines'}")
    print("-" * 65)
    for sig, sym in sorted(results['symbol_table'].items()):
        print(f"{sig:<18} {sym['arity']:<8} {sym['facts']:<8} {sym['rules']:<8} {sym['defined_at_lines']}")

    print(f"\nDiagnostics ({len(results['diagnostics'])} total):")
    if not results['diagnostics']:
        print("  ✓ Zero semantic errors or singleton variables. Knowledge base is strictly verified!")
    else:
        for diag in results['diagnostics']:
            symbol = "⚠️ " if diag['level'] == "WARNING" else "❌"
            print(f"  {symbol} [{diag['level']}] Line {diag['line']}: {diag['message']}")

def cmd_wam(args):
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    tokens = PrologLexer(code).tokenize()
    ast = PrologParser(tokens).parse_program()
    wam = WAMCompiler(ast).compile()

    print(f"\n--- [Phase 4: Warren Abstract Machine (WAM) Bytecode] ---")
    for instr in wam['wam_instructions']:
        if instr['op'].startswith('LABEL'):
            print(f"\n\033[33m{instr['op']}\033[0m")
        else:
            comment = f" ; {instr['comment']}" if instr['comment'] else ""
            print(f"  \033[35m{instr['op']:<18}\033[0m {', '.join(instr['args'])}{comment}")

    print(f"\n--- [Three-Address Code (TAC) Quadruples] ---")
    print(f"{'#':<4} {'OP':<16} {'ARG1':<16} {'ARG2':<16} {'RESULT'}")
    print("-" * 65)
    for idx, q in enumerate(wam['quadruples']):
        print(f"{idx+1:<4} {q['op']:<16} {q['arg1']:<16} {q['arg2']:<16} {q['result']}")

def cmd_query(args):
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    ast = PrologParser(PrologLexer(code).tokenize()).parse_program()
    
    q_str = args.query.strip()
    if q_str.startswith('?-'):
        q_str = q_str[2:].strip()
    if q_str.endswith('.'):
        q_str = q_str[:-1].strip()

    q_goals = PrologParser(PrologLexer(q_str).tokenize()).parse_goal_list()
    engine = ResolutionEngine(ast)
    res = engine.solve(q_goals)

    print(f"\nQuery: ?- {q_str}.")
    if res['found_solution']:
        print(f"Status: \033[32mSUCCESS\033[0m ({res['solution_count']} answers found)\n")
        for i, sol in enumerate(res['solutions']):
            bindings = ", ".join(f"{k} = {v}" for k, v in sol.items()) if sol else "true."
            print(f"[{i+1}] {bindings}")
    else:
        print(f"Status: \033[31mFAIL (false.)\033[0m")

def cmd_debug(args):
    """Interactive Step-by-Step Resolution Debugger."""
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    ast = PrologParser(PrologLexer(code).tokenize()).parse_program()
    q_str = args.query.strip()
    if q_str.startswith('?-'):
        q_str = q_str[2:].strip()
    if q_str.endswith('.'):
        q_str = q_str[:-1].strip()

    q_goals = PrologParser(PrologLexer(q_str).tokenize()).parse_goal_list()
    engine = ResolutionEngine(ast)
    res = engine.solve(q_goals)

    print("\n" + "=" * 68)
    print(f" 🐞 INTERACTIVE SLD RESOLUTION DEBUGGER")
    print(f" Goal: ?- {q_str}.")
    print(" Press [Enter] to step through each inference step...")
    print("=" * 68 + "\n")

    for step in res['trace']:
        depth_indent = "  " * (step['depth'] - 1)
        event_color = {
            "UNIFY_FACT": "\033[32m[UNIFY_FACT]\033[0m",
            "UNIFY_RULE": "\033[34m[UNIFY_RULE]\033[0m",
            "SUCCESS": "\033[32m[SUCCESS ★]\033[0m",
            "BUILTIN_TRUE": "\033[36m[BUILTIN]\033[0m",
            "BUILTIN_FAIL": "\033[31m[BACKTRACK]\033[0m"
        }.get(step['event'], f"[{step['event']}]")

        print(f"{depth_indent}Step #{step['step']} {event_color} {step['description']}")
        if 'bindings' in step and step['bindings']:
            print(f"{depth_indent}  ↳ Bindings: {step['bindings']}")
        try:
            input(f"{depth_indent}  [Press Enter to continue | Ctrl+C to quit]")
        except (KeyboardInterrupt, EOFError):
            print("\nDebugger interrupted by user.")
            break

    print("\nResolution proof trace complete.")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="PROLOG-C: Full-Phase Compiler & Logic Debugging Tool")
    subparsers = parser.add_subparsers(dest="command", help="Compiler operations")

    # lex
    p_lex = subparsers.add_parser("lex", help="Tokenize source file")
    p_lex.add_argument("file", help="Path to .pl source file")

    # parse
    p_parse = subparsers.add_parser("parse", help="Parse and display AST tree")
    p_parse.add_argument("file", help="Path to .pl source file")

    # pdg
    p_pdg = subparsers.add_parser("pdg", help="Display Predicate Dependency Graph")
    p_pdg.add_argument("file", help="Path to .pl source file")

    # check
    p_check = subparsers.add_parser("check", help="Semantic check and singleton variable linting")
    p_check.add_argument("file", help="Path to .pl source file")

    # wam
    p_wam = subparsers.add_parser("wam", help="Generate WAM Bytecode and TAC Quadruples")
    p_wam.add_argument("file", help="Path to .pl source file")

    # query
    p_query = subparsers.add_parser("query", help="Run a query against knowledge base")
    p_query.add_argument("file", help="Path to .pl source file")
    p_query.add_argument("query", help="Prolog query string, e.g. 'ancestor(george, X).'")

    # debug
    p_debug = subparsers.add_parser("debug", help="Step-by-step interactive resolution debugger")
    p_debug.add_argument("file", help="Path to .pl source file")
    p_debug.add_argument("query", help="Prolog query string")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    handlers = {
        "lex": cmd_lex,
        "parse": cmd_parse,
        "pdg": cmd_pdg,
        "check": cmd_check,
        "wam": cmd_wam,
        "query": cmd_query,
        "debug": cmd_debug
    }

    if args.command in handlers:
        handlers[args.command](args)

if __name__ == "__main__":
    main()
