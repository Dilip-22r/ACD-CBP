# 🚀 PROLOG-PARSE / PROLOG-C: Formal Visual Compiler & Logic Inference Studio

[![Compiler Design Lab](https://img.shields.io/badge/Course-22PC2CS301-blue.svg)](https://vnrvjiet.ac.in)
[![Institution](https://img.shields.io/badge/Institution-VNRVJIET%20CSE-green.svg)](https://vnrvjiet.ac.in)
[![Grammar Rules](https://img.shields.io/badge/Grammar%20Rules-1%2C000%2B-purple.svg)](./GRAMMAR_SPEC_1000.md)
[![Unit Tests](https://img.shields.io/badge/Unit%20Tests-36%2F36%20Passing-brightgreen.svg)](./tests_edge_cases.py)
[![License](https://img.shields.io/badge/License-Academic%20Lab-orange.svg)](./REPORT.md)

> **Course:** Compiler Design and Computer Networks Laboratory (22PC2CS301)  
> **Department:** Department of Computer Science & Engineering, VNR Vignana Jyothi Institute of Engineering and Technology (VNRVJIET)  
> **Student Author:** Dilip-22r  

---

## 🧭 Project Overview

**PROLOG-PARSE** is an end-to-end, industrial-strength visual compiler and deductive inference engine for the **ISO/IEC 13211-1 Prolog** language.

Unlike simple toy parsers or black-box wrappers, this system implements the complete classical 5-phase compiler pipeline from scratch, backed by both a **formal native C/Yacc LALR(1) engine** and an **interactive visual Python studio**.

```
                           PROLOG COMPILER PIPELINE
                           
       +-------------------------------------------------------------+
       |               Prolog Source Program (.pl)                   |
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       | Phase 1: Lexical Analyzer (DFA Scanner - prolog.l / lexer.py)|
       +-------------------------------------------------------------+
                                      |  Tokens: ATOM, VAR, NUMBER, OP
                                      v
       +-------------------------------------------------------------+
       | Phase 2: Syntax Analyzer (CFG Parser - prolog.y / parser.py)|
       +-------------------------------------------------------------+
                                      |  Concrete / Abstract Syntax Tree
                                      v
       +-------------------------------------------------------------+
       | Phase 3: Semantic Analyzer & Symbol Table (semantic.py)     |
       +-------------------------------------------------------------+
                                      |  Functor/Arity Index & Scope Checks
                                      v
       +-------------------------------------------------------------+
       | Phase 4: Intermediate Code Generation (wam_compiler.py)     |
       +-------------------------------------------------------------+
                                      |  Warren Abstract Machine (WAM) Bytecode
                                      v
       +-------------------------------------------------------------+
       | Phase 5: Logic Resolution Engine (engine.py)                |
       +-------------------------------------------------------------+
                                      |  Robinson Unification + SLD Search
                                      v
       +-------------------------------------------------------------+
       | Visual Studio UI (app.py) & Native Binary (prolog_yacc.exe) |
       +-------------------------------------------------------------+
```

---

## ✨ Key Architectural Features

1. **Dual-Engine Architecture:**
   * **Formal YACC/Bison LALR(1) Engine (`prolog.y` + `prolog.l`):** 1,000+ lines of formal BNF productions, operator precedence declarations (`%left`, `%right`), and C Abstract Syntax Tree node constructors.
   * **Python Recursive Descent Engine (`parser.py` + `lexer.py`):** Pure Python LL(1) with operator precedence climbing and panic-mode error recovery.
2. **Exhaustive 1,000-Rule Grammar Specification ([`GRAMMAR_SPEC_1000.md`](./GRAMMAR_SPEC_1000.md)):**
   * Detailed formal rules spanning Lexical DFA ($L_1-L_{100}$), Syntax CFG ($P_1-P_{250}$), Semantics ($S_1-S_{150}$), Error Recovery ($R_1-R_{100}$), WAM Bytecode ($W_1-W_{100}$), Engine ($E_1-E_{100}$), Graph Topology ($G_1-G_{100}$), and ISO Built-ins ($B_1-B_{100}$).
3. **Panic-Mode Error Recovery:**
   * Both parsers catch syntax violations, resynchronize on the clause boundary `.` token, and continue compiling subsequent valid clauses. Tested on [`examples/bad_syntax_suite.pl`](./examples/bad_syntax_suite.pl).
4. **Intermediate Code Generation (WAM Bytecode):**
   * Lowers Prolog logic clauses to Warren Abstract Machine instructions (`put_variable`, `get_structure`, `call`, `proceed`) and Three-Address Code (TAC) quadruples.
5. **Robinson's First-Order Unification Engine:**
   * Full sound unification with **Occurs-Check** to prevent circular variable loops, combined with depth-first SLD resolution and chronological backtracking.
6. **AI-Native OLED Dark Mode Studio:**
   * Interactive web dashboard with real-time token inspector, AST tree visualizer, SVG Predicate Dependency Graph, WAM bytecode diff viewer, and live query console.

---

## 📁 Repository File Map

| File Name | Description | Lines |
| :--- | :--- | :---: |
| [`prolog.y`](./prolog.y) | **Formal YACC/Bison Grammar:** Full ISO Prolog CFG rules & C AST builders | ~1,000 |
| [`prolog.l`](./prolog.l) | **Formal Lex/Flex Scanner:** DFA regular expressions for tokens | ~220 |
| [`build_yacc.bat`](./build_yacc.bat) | 1-Click batch script compiling `prolog.y` and `prolog.l` into `prolog_yacc.exe` | ~30 |
| [`prolog_yacc.exe`](./prolog_yacc.exe) | Compiled native Windows LALR(1) parser binary | Binary |
| [`app.py`](./app.py) | Flask Visual Compiler Studio Web Server (port 5050) | ~4,700 |
| [`parser.py`](./parser.py) | Python Predictive Recursive Descent Parser with panic-mode `synchronize()` | ~400 |
| [`lexer.py`](./lexer.py) | Python Lexical Scanner tracking line/col tokens | ~320 |
| [`ast_nodes.py`](./ast_nodes.py) | AST Node definitions: Fact, Rule, Query, CompoundTerm, ListTerm | ~250 |
| [`semantic.py`](./semantic.py) | Symbol table indexing (`functor/arity`) and singleton variable linter | ~240 |
| [`wam_compiler.py`](./wam_compiler.py) | Warren Abstract Machine bytecode & TAC quadruple code generator | ~300 |
| [`engine.py`](./engine.py) | Robinson's Unification Algorithm & SLD Resolution Engine | ~360 |
| [`graph_builder.py`](./graph_builder.py) | Predicate Dependency Graph (PDG) and AST tree coordinate layout engine | ~260 |
| [`sample_programs.py`](./sample_programs.py) | Built-in presets: Family Tree, Graph Paths, Lists, NLP/Expert System | ~150 |
| [`tests_edge_cases.py`](./tests_edge_cases.py) | 36 unit tests validating all compiler phases (100% passing) | ~530 |
| [`SMALL.md`](./SMALL.md) | **Quick 1-Page Viva Cheat Sheet:** Where and how grammar is implemented | ~120 |
| [`GRAMMAR_SPEC_1000.md`](./GRAMMAR_SPEC_1000.md) | **Massive 1,000-Rule Specification Catalog** across all 8 compiler phases | ~500 |
| [`YACC_GRAMMAR_GUIDE.md`](./YACC_GRAMMAR_GUIDE.md) | In-depth guide to the Lex/Yacc architecture and C AST generation | ~290 |
| [`REPORT.md`](./REPORT.md) | Academic Laboratory Report conforming to Course 22PC2CS301 | ~1,200 |

---

## ⚡ Quick Start & Commands

### 1. Compile & Run the Native YACC Parser:
```bash
# Build the native parser from prolog.y and prolog.l:
build_yacc.bat

# Run the parser on a sample Prolog file:
prolog_yacc.exe examples\ancestor.pl

# Test panic-mode error recovery on deliberately malformed code:
prolog_yacc.exe examples\bad_syntax_suite.pl
```

### 2. Launch the Visual Compiler Studio:
```bash
# Start Flask Server:
python app.py

# Open in your browser:
http://127.0.0.1:5050
```

### 3. Run Automated Compiler Test Suite:
```bash
python tests_edge_cases.py
# (36/36 tests pass in ~1.2s)
```

---

## 🎓 Academic Viva Defense Guide

* **"Where are your grammar rules?"**  
  *In [`prolog.y`](./prolog.y) (Yacc BNF specification) and [`parser.py`](./parser.py) (Python Recursive Descent parser).*
* **"How do you handle syntax errors?"**  
  *Via Panic-Mode error recovery: the parser logs the diagnostic, discards bad tokens up to the clause terminator `.`, resynchronizes, and continues parsing the remaining clauses cleanly.*
* **"What is the intermediate representation?"**  
  *Warren Abstract Machine (WAM) bytecode instructions (`put_*`, `get_*`, `unify_*`, `call`, `proceed`) and Three-Address Code (TAC) quadruples.*

---

© 2026 Dept. of Computer Science & Engineering, VNRVJIET. Course 22PC2CS301.
