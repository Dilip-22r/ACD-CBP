# 🛠️ PROLOG-C / PROLOG-PARSE: Technology Stack & Architectural Specification

**Course:** Compiler Design and Computer Networks Laboratory (22PC2CS301)  
**Institution:** Department of Computer Science and Engineering, VNR Vignana Jyothi Institute of Engineering & Technology (VNRVJIET)  
**Project:** PROLOG-PARSE / PROLOG-C — AI-Native Visual Compiler & Logic Inference Studio  
**Artifact:** Complete Technology Stack, Tools, Libraries & Architectural Matrix  

---

## 📌 Executive Summary

**PROLOG-C** (branded as **PROLOG-PARSE**) is an end-to-end, multi-phase compiler, static semantic analyzer, intermediate code generator, and logic execution engine built specifically for **ISO Prolog (First-Order Logic Horn Clauses)**. 

The system combines a **zero-dependency, purely implemented classical compiler core** in Python with an **AI-Native, Dark OLED visual studio workbench** running on a lightweight Flask backend with Vanilla Web Technologies (HTML5, modern CSS custom properties, and ES6+ JavaScript).

```
+─────────────────────────────────────────────────────────────────────────────+
|                               PROLOG-PARSE STACK                            |
+─────────────────────────────────────────────────────────────────────────────+
|  PRESENTATION LAYER      HTML5 · Vanilla CSS3 (Custom Tokens) · ES6+ JS     |
|                          SVG Graph Engine · Dark/Light Modes · Bento Grid   |
+─────────────────────────────────────────────────────────────────────────────+
|  HTTP / WSGI LAYER       Python 3.11+ · Flask 3.1 (REST API Endpoints)      |
+─────────────────────────────────────────────────────────────────────────────+
|  COMPILER PIPELINE       Lexer (DFA) ──► Recursive Descent Parser (LL(1))   |
|                          Semantic Analyzer ──► Symbol Table (functor/arity) |
|                          WAM Code Generator ──► TAC Quadruple Generator     |
|                          Peephole Optimizer Pass                            |
+─────────────────────────────────────────────────────────────────────────────+
|  LOGIC EXECUTION ENGINE  Robinson's Unification (Occurs-Check)              |
|                          SLD Resolution · Chronological Backtracking · Cut  |
+─────────────────────────────────────────────────────────────────────────────+
|  TOOLING & QA            Python unittest (36+ Edge Tests) · CLI Workbench   |
|                          Chrome DevTools Protocol (CDP) Screenshot Engine   |
+─────────────────────────────────────────────────────────────────────────────+
```

---

## 1. 🐍 Core Language & Runtime Environment

| Component | Specification | Technical Rationale & Role |
| :--- | :--- | :--- |
| **Primary Language** | **Python 3.11+** (compatible with 3.10+) | Provides clean pattern matching, expressive object-oriented abstractions, structured typing, and rapid tree manipulation capabilities without memory overhead. |
| **Type System** | `typing` & `dataclasses` | Strongly typed Abstract Syntax Tree (AST) nodes, token models, and semantic symbols utilizing Python's static type annotations for robust data integrity. |
| **Design Philosophy** | **Zero External Dependencies Core** | The entire compiler (Phases 1–7), the unification engine, and the SVG generator rely exclusively on the **Python Standard Library** (`re`, `enum`, `dataclasses`, `abc`, `copy`, `math`, `json`, `argparse`, `sys`). |

---

## 2. ⚙️ Compiler Phases & Implementation Architecture

The core compiler implements the canonical classical compiler design phases tailored to declarative logic programming:

```
[Source Code .pl]
       │
       ▼
 [Phase 1: Lexical Analysis] (lexer.py)
       │ Linear Token Stream (TokenType, Lexeme, Line, Col)
       ▼
 [Phase 2: Syntax Analysis] (parser.py)
       │ Concrete Derivation & Typed AST Tree
       ▼
 [Phase 3: Semantic Analysis] (semantic.py)
       │ Symbol Table, functor/arity, Scope, Singleton Detection
       ▼
 [Phase 4: Intermediate Code Generation] (wam_compiler.py)
       │ Warren Abstract Machine (WAM) Bytecode & TAC Quadruples
       ▼
 [Phase 5: Code Optimization] (wam_compiler.py)
       │ Register Allocation Peephole Optimizer
       ▼
 [Phase 6: Execution & Inference Engine] (engine.py)
       │ Robinson Unification & SLD Resolution with Backtracking
       ▼
 [Output / Solutions / Proof Trees]
```

### Phase-by-Phase Technical Details:

1. **Phase 1: Lexical Analysis (`lexer.py`)**
   - **Mechanism:** Custom Deterministic Finite Automaton (DFA) scanner with 1-character lookahead.
   - **Supported Tokens:** Atoms, Logic Variables (uppercase / `_`), Numbers (integer & float), Strings, Neck operator `:-`, Query directive `?-`, List constructors `[` `]` `|`, Cut operator `!`, and End-of-clause period `.`.
   - **Lookahead Resolution:** Distinguishes floating-point numbers (`3.14`) from the clause terminator period (`.`) by examining following whitespace, newline, or EOF.
   - **Comments:** Supports single-line comments (`% ...`) and C-style block comments (`/* ... */`).

2. **Phase 2: Syntax Analysis (`parser.py`)**
   - **Grammar Class:** Context-Free Grammar (CFG) for ISO Prolog Horn Clauses.
   - **Parsing Strategy:** Predictive Recursive Descent parser with LL(1) prediction sets and operator precedence climbing.
   - **Error Handling:** **Panic-Mode Error Recovery** with synchronization tokens (`.` and clause boundary operators), allowing the parser to report line-accurate syntax diagnostics and continue parsing subsequent clauses.
   - **FIRST & FOLLOW Sets:** Explicitly computed and programmatically exposed for LL(1) validation.

3. **Phase 3: Abstract Syntax Tree (`ast_nodes.py`)**
   - **Hierarchy:** Object-Oriented typed AST using `@dataclass`.
   - **Node Types:** `Program`, `Clause`, `Fact`, `Rule`, `Query`, `CompoundTerm`, `Atom`, `Variable`, `Number`, `ListTerm`.
   - **Metadata:** Every AST node preserves source coordinates (`line`, `col`) for high-precision diagnostic mapping.

4. **Phase 4: Semantic Analysis & Symbol Table (`semantic.py`)**
   - **Signature Indexing:** Predicates indexed strictly by `functor/arity` (e.g., `parent/2` vs. `parent/3`).
   - **Scope Discipline:** Implements clause-local variable scope resolution.
   - **Linter & Diagnostics:** Industrial-grade **Singleton Variable Detection** flags variables that occur only once in a rule or fact (a classic logic programming bug).

5. **Phase 5 & 6: Intermediate Code Generation & Optimization (`wam_compiler.py`)**
   - **Target Virtual Architecture:** **Warren Abstract Machine (WAM)** virtual assembly:
     - Argument allocation instructions: `put_variable`, `put_value`, `put_constant`, `put_structure`.
     - Head matching instructions: `get_variable`, `get_value`, `get_constant`, `get_structure`.
     - Control flow instructions: `call`, `proceed`, `allocate`, `deallocate`.
   - **Three-Address Code (TAC):** Quadruple format `(OP, ARG1, ARG2, RESULT)` for intermediate low-level evaluation.
   - **Optimization Pass:** Peephole optimization eliminates redundant register moves, dead argument allocations, and compresses consecutive unified loads.

6. **Phase 7: Execution & Logic Inference Engine (`engine.py`)**
   - **Unification:** **Robinson's First-Order Unification Algorithm** with occurs-check protection to avoid cyclic infinite structures.
   - **Proof Strategy:** Selective Linear Definite (SLD) resolution with chronological depth-first backtracking.
   - **Variable Renaming:** Implements *standardizing apart* (generating fresh variable instances per recursive invocation to avoid variable capture).
   - **Pruning:** Native support for the Cut operator (`!`) to prune alternative search choice points.

---

## 3. 🌐 Web Studio & Visualization Frontend

The visual frontend is an AI-Native, Dark OLED visual studio embedded directly in `app.py`:

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Backend Web Server** | **Flask 3.1.x** (Python WSGI) | Lightweight microframework serving JSON REST API endpoints (`/api/compile`, `/api/query`, `/api/grammar`) and rendering the single-page application. |
| **Markup** | **Semantic HTML5** | Accessible layout featuring responsive container regions, header controls, a code editor pane, and a bento-grid multi-tab visualizer. |
| **Styling & Theme** | **Vanilla CSS3 (Design Tokens)** | Comprehensive CSS Custom Property design system featuring Dark OLED midnight palette (`--bg-abyss: #060a14`, `--bg-surface: #0e1626`), high-contrast light mode, smooth transitions, glassmorphism, and responsive CSS grid/flexbox. |
| **Typography** | **Google Fonts** | • `JetBrains Mono`: Monospaced font for code editor, token tables, and WAM assembly.<br>• `IBM Plex Sans`: High-legibility sans-serif for UI labels, badges, and metrics. |
| **Client-Side Logic** | **Vanilla JavaScript (ES6+)** | Zero third-party framework overhead (no React, Angular, or Vue). Uses native Fetch API, dynamic DOM manipulation, interactive tab management, and keyboard shortcuts (`Ctrl + Enter` to compile). |
| **Interactive UX** | **Custom Physics Cursor** | Interactive dual-layer cursor with smooth center dot and trailing ring (`#cursorDot`, `#cursorRing`). |
| **Graph Visualizer** | **Custom Mathematical SVG Engine** (`graph_builder.py`) | Generates pure inline vector SVG diagrams for Predicate Dependency Graphs (PDG) and Call Graphs with dynamic node layouts, connection splines, recursive self-loop arcs, and status badges. |

---

## 4. 💻 Command Line Interface & Tooling

In addition to the Web Studio, the compiler provides terminal utilities:

| Tool | File | Features |
| :--- | :--- | :--- |
| **CLI Workbench** | [cli.py](file:///d:/CBPS/Prolog_Compiler_CD/cli.py) | Comprehensive developer tool with subcommands:<br>• `lex`: Token dump with line/col positions<br>• `parse`: Indented AST hierarchy tree<br>• `pdg`: ASCII / text dependency graph<br>• `check`: Semantic linter and singleton detector<br>• `wam`: WAM bytecode and TAC quadruples<br>• `query`: Direct goal solving in terminal<br>• `debug`: Interactive step-by-step backtracking trace |
| **Batch Launcher** | [RUN_PROJECT.bat](file:///d:/CBPS/Prolog_Compiler_CD/RUN_PROJECT.bat) | Windows 1-click execution script that boots `python app.py` on port 5050. |

---

## 5. 🧪 Testing & Automated Verification

| Component | Framework / Tool | Coverage & Details |
| :--- | :--- | :--- |
| **Unit Test Suite** | Python standard `unittest` ([tests_edge_cases.py](file:///d:/CBPS/Prolog_Compiler_CD/tests_edge_cases.py)) | 36+ unit tests covering edge cases across all compiler phases: empty inputs, multi-line comment boundary conditions, malformed terms, circular unification, infinite recursion protection, and list concatenation. |
| **Screenshot Engine** | **Chrome DevTools Protocol (CDP)** ([capture_screenshots.py](file:///d:/CBPS/Prolog_Compiler_CD/capture_screenshots.py)) | Automated headless Chromium capture script using `asyncio` and `websockets` to snapshot visual tabs, theme modes, and proof trees. |

---

## 6. 📜 Formal Standards & Language Specifications

- **ISO/IEC 13211-1 (1995):** Information Technology — Programming Languages — Prolog (Part 1: General Core).
- **First-Order Horn Clause Logic:** Definite clauses $\forall (A \lor \neg B_1 \lor \dots \lor \neg B_n)$.
- **SLD Resolution:** Selected Linear Definite clause resolution.
- **Warren Abstract Machine (WAM):** David H. D. Warren's 1983 execution model for Prolog.

---

## 7. 📊 Technology Stack Summary Table

| Category | Technology / Library | Purpose | Dependency Type |
| :--- | :--- | :--- | :--- |
| **Core Language** | Python 3.11.x | Primary compiler language | Runtime Environment |
| **Web Framework** | Flask 3.1.3 | Local WSGI web server & API | Python Library (`pip install flask`) |
| **Frontend UI** | HTML5 / CSS3 / ES6+ JS | Studio user interface | Native Web Standards (Zero bundle) |
| **Typography** | Google Fonts (`JetBrains Mono`, `IBM Plex Sans`) | Monospaced code and UI font | External CDN Asset |
| **Graphing** | Custom Pure SVG Generator | Call graphs & PDG rendering | Built-in Python Math & Strings |
| **Type Checking** | Python `typing` & `dataclasses` | Compiler data structures | Python Standard Library |
| **Lexer/Parser** | Custom DFA & Recursive Descent | Phase 1 & 2 Compiler | Python Standard Library |
| **Logic Engine** | Robinson's Unification Algorithm | Logic reasoning & proof search | Python Standard Library |
| **IR / Bytecode** | WAM Bytecode & TAC Quadruples | Intermediate Representation | Python Standard Library |
| **CLI Framework** | `argparse` & `sys` | Terminal developer workbench | Python Standard Library |
| **Testing** | `unittest` | Regression & edge-case suite | Python Standard Library |
| **Capture & CDP** | `websockets` & Headless Chrome | Automated documentation photos | Optional Development Utility |
| **Operating System**| Windows / Linux / macOS | Host operating systems | Platform-Agnostic |
