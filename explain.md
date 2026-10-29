# 📘 PROLOG-PARSE: Studio Prototype & Interactive Buttons Guide

**Course:** Compiler Design & Computer Networks Laboratory (22PC2CS301)  
**Institution:** VNR Vignana Jyothi Institute of Engineering & Technology (VNRVJIET)  
**Project:** PROLOG-PARSE / PROLOG-C — AI-Native Visual Compiler & Logic Inference Studio  
**Artifact:** User Interface Prototype & Complete Button Interaction Reference  

---

## 🧭 1. Prototype Overview

The **PROLOG-PARSE** prototype is an interactive visual workbench designed to demonstrate every phase of classical compiler engineering applied to declarative logic programming (**ISO Prolog Horn Clauses**). 

Instead of treating the compiler as an opaque black box, the studio decomposes execution into transparent, visual representations:
- **Left Workspace**: Source code editor with live syntax highlighting and an interactive logic query console.
- **Right Workspace**: Multi-tab visualizer displaying token streams, Abstract Syntax Trees (AST), Symbol Tables, Predicate Dependency Graphs (PDG), Warren Abstract Machine (WAM) bytecode, Three-Address Code (TAC) quadruples, and a guided 6-step live demo tour.

Below is an exhaustive breakdown of **all buttons and interactive controls** present across the prototype interface, categorized by UI region.

---

## 🗂️ 2. Top Navigation Bar (Header)

The persistent top navigation bar provides global controls, preset program selections, and the primary compiler trigger.

```
+───────────────────────────────────────────────────────────────────────────────────────────────────────────+
| [🏠] [PROLOG-PARSE]  |  [Family Tree] [Network Paths] [List Ops] [Evaluator]  |  [⤹] [🌙] [📖 Grammar] [▶ Demo] [⚡ Analyze & Compile] [↺ Reset] |
+───────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 2.1 Brand & Navigation
| Button / Element | Selector / Handler | Purpose & Technical Behavior |
| :--- | :--- | :--- |
| **`[🏠]` Home / Exit Button** | `<button class="icon-btn" onclick="exitStudioToLanding()">` | Exits the compiler studio workspace and transitions the view back to the full marketing and academic syllabus landing page (`#landingView`). |
| **`PROLOG-PARSE` Brand Badge** | `<span class="brand-badge">` | Displays the system identity. Visual indicator styled with deep indigo background and glow effect. |

---

### 2.2 Preset Program Toolbar (`.preset-bar`)
These buttons instantly populate the editor with pre-verified ISO Prolog benchmark programs to showcase different compiler characteristics and recursive structures.

| Button | Handler / Key | Loaded Benchmark & Compiler Characteristics |
| :--- | :--- | :--- |
| **`Family Tree`** *(Active in screenshot)* | `selectPreset('ancestor_tree', this)` | **Classical Kinship & Transitive Recursion:**<br>• Contains 54 lines, 20 Horn clauses (`parent`, `male`, `female`, `father`, `mother`, `ancestor`).<br>• Demonstrates linear recursive rules: `ancestor(X, Y) :- parent(X, Y).` and `ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).`<br>• Triggers singleton variable validation and self-loop detection in call graphs. |
| **`Network Paths`** | `selectPreset('graph_network', this)` | **Directed Graph Traversal & Reachability:**<br>• Defines network vertices and directed edges `edge(NodeA, NodeB)`.<br>• Implements path traversal `path(X, Y)` to test cycle prevention and backtracking during SLD resolution. |
| **`List Ops`** | `selectPreset('list_algorithms', this)` | **Recursive List Processing & Pattern Matching:**<br>• Implements `member/2`, `concat/3` (append), and `reverse_list/2`.<br>• Stresses the parser with Prolog bracket syntax `[Head|Tail]` and nested list constructor functors `./2`. |
| **`Evaluator`** | `selectPreset('expr_evaluator', this)` | **Symbolic Expression Evaluation & Arithmetic:**<br>• Defines an algebraic arithmetic interpreter `eval(Expr, Val)`.<br>• Compiles complex nested functor terms (e.g. `plus(N, M)`, `mult(A, B)`) into WAM register-allocation instructions. |

---

### 2.3 Global Header Action Controls (`.header-actions`)
| Button | Selector / Handler | Purpose & Technical Behavior |
| :--- | :--- | :--- |
| **`[⤹]` Custom Cursor Toggle** | `#cursorToggleStudio`<br>`onclick="toggleCursor()"` | Toggles the custom physics-based glowing pointer (a center dot `#cursorDot` and smooth trailing ring `#cursorRing`). Stored in session preferences. |
| **`[🌙 / ☀️]` Theme Toggle** | `onclick="toggleTheme()"` | Toggles between **OLED Dark Mode** (`data-theme="dark"`) and **Clean Light Mode** (`data-theme="light"`). Dynamically swaps the Moon/Sun SVG icon and adjusts CSS custom property tokens. |
| **`📖 Grammar` Spec Button** | `#btnGrammarDocsStudio`<br>`onclick="openGrammarModal()"` | Opens the **Formal Language Specification & Grammar Reference Modal**, providing official ISO references, an operator precedence & associativity table, the complete GNU Bison LALR(1) grammar, deliberate simplifications, and FIRST/FOLLOW sets. |
| **`▶ Demo` Header Button** | `<button class="btn btn-demo" onclick="startLiveDemo()">` | Shortcut button that immediately activates the **Live Demo** tab (`tab-demo`) in the right panel and scrolls it into view for presentations. |
| **`⚡ Analyze & Compile`** *(Primary Action)* | `#btnCompileCode`<br>`onclick="compileCode()"`<br>*(Keyboard: `Ctrl + Enter`)* | **Master Pipeline Trigger:**<br>1. Posts source code payload to `/api/compile`.<br>2. Executes **Lexer DFA** to tokenize code.<br>3. Executes **Predictive Parser** to build AST with panic-mode error recovery.<br>4. Executes **Semantic Analysis** for symbol table construction and singleton warnings.<br>5. Generates **WAM Bytecode** and **TAC Quadruples**.<br>6. Constructs **Predicate Dependency Graph**.<br>7. Updates line/clause metrics, badges, and all visualizer tabs. |
| **`↺ Reset`** | `#btnResetStudio`<br>`onclick="resetStudio()"` | Reverts the source editor and query input back to their default sample state, clearing any transient errors or compilation caches. |

---

## 📝 3. Left Panel: Source Code & Interactive Logic Query

The left panel is split into two interactive cards: source code editing on top and logic query evaluation at the bottom.

```
+───────────────────────────────────────────────+
| Source Code (ISO Prolog)  [Syntax Valid] [54L] |
| 1 | % Classical Recursive Logic...            |
| 2 | parent(george, john).                     |
| ...                                           |
+───────────────────────────────────────────────+
| Interactive Logic Query        [5 solutions]  |
| [ ?- ancestor(george, X).           ] [Solve] |
| 1. X = john                                   |
| 2. X = mary ...                               |
| [▶ SLD proof trace — 27 resolution steps]     |
+───────────────────────────────────────────────+
```

### 3.1 Source Code Card
- **Status Badges**:
  - `#compilerStatusBadge`: Displays `Ready`, `Compiling...`, `Syntax Valid` (green), or `Syntax Error` (red).
  - `#codeMetrics`: Displays dynamic line count and total clause count (e.g. `54 lines • 20 clauses`).
- **Code Editor Area**:
  - `#sourceEditor`: Multi-line textarea capturing ISO Prolog syntax.
  - `#lineNumbers`: Synchronized gutter rendering 1-indexed line numbers.
  - `#codeHighlight`: Syntax-highlighting backdrop reflecting real-time token colors.

### 3.2 Interactive Logic Query Card
| Control / Button | Selector / Handler | Purpose & Technical Behavior |
| :--- | :--- | :--- |
| **Query Input Field** | `#queryGoalInput`<br>*(Pressing `Enter` triggers `solveQuery()`)* | Single-line text input for user goals (e.g., `?- ancestor(george, X).`). Accepts queries with or without the `?-` prefix and auto-appends terminating period if omitted. |
| **`Solve` Button** | `#btnSolveQuery`<br>`onclick="solveQuery()"` | **Logic Inference Trigger:**<br>1. Posts the goal and current source to `/api/query`.<br>2. Tokenizes and parses the goal into an AST `Query` node.<br>3. Runs **Robinson's First-Order Unification Algorithm** (with occurs-check).<br>4. Performs **SLD Resolution with Chronological Backtracking** against the knowledge base.<br>5. Renders satisfying variable bindings (e.g. `X = john`, `X = mary`). |
| **`▶ SLD proof trace — N resolution steps`** *(Disclosure Button)* | `<details class="trace-details"><summary>` | **Collapsible Proof Tree Expander:**<br>Expands the step-by-step resolution trace table showing the exact derivation chain:<br>• **Step Number**: Chronological sequence index.<br>• **Current Goal**: Subgoal selected for resolution.<br>• **Clause Unified**: Head matched with variable substitution.<br>• **Remaining Subgoals**: Updated goal stack.<br>• **Backtracking Points**: Choice points pushed/popped on the execution stack. |

---

## 📊 4. Right Panel: Visualizer Tabs & Controls

The right panel features a 5-tab visualizer bar that reveals the internal representations created during compilation.

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
| [⚡ Lexer Tokens]  [🌿 AST & Symbols]  [🔀 Call Graph]  [💾 WAM & TAC]  [▶ Live Demo (Active)]    |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 4.1 Tab Switcher Buttons (`.visualizer-tabs-bar`)
| Tab Button | Selector / Target Tab | Visualized Compiler Phase |
| :--- | :--- | :--- |
| **`⚡ Lexer Tokens`** | `#btnTabLexer`<br>`onclick="switchTab('tab-lexer')"` | **Phase 1 (Lexical Analysis):**<br>Interactive token stream, token category breakdown, and LL(1) FIRST/FOLLOW prediction tables. |
| **`🌿 AST & Symbols`** | `#btnTabAst`<br>`onclick="switchTab('tab-ast')"` | **Phase 2 & 3 (Syntax & Semantics):**<br>Hierarchical Abstract Syntax Tree explorer alongside the Predicate Signature Symbol Table (`functor/arity`). |
| **`🔀 Call Graph`** | `#btnTabPdg`<br>`onclick="switchTab('tab-pdg')"` | **Static Analysis (Call Graph / PDG):**<br>Interactive SVG directed graph displaying predicate inter-dependencies and recursion cycles. |
| **`💾 WAM & TAC`** | `#btnTabWam`<br>`onclick="switchTab('tab-wam')"` | **Phase 4 & 5 (Intermediate Code Generation & Optimization):**<br>Warren Abstract Machine instructions and Three-Address Code quadruples. |
| **`▶ Live Demo`** *(Active in screenshot)* | `#btnTabDemo`<br>`onclick="switchTab('tab-demo')"` | **Live End-to-End Showcase:**<br>Guided 6-phase walkthrough stepping through ingestion, lexing, parsing, symbol indexing, graph generation, and logic proof. |

---

### 4.2 Sub-Buttons within Individual Tabs

#### A. Inside `Lexer Tokens` Tab (`tab-lexer`):
- **Filter Chip Buttons (`.filter-chip`)**:
  - `All tokens` (`filterTokens('all', this)`): Shows all lexical tokens.
  - `Atoms` (`filterTokens('atom', this)`): Filters to lowercase identifiers/constants (`george`, `john`, `parent`).
  - `Variables` (`filterTokens('variable', this)`): Filters to uppercase variables (`X`, `Y`, `Parent`).
  - `Operators` (`filterTokens('operator', this)`): Filters to rule/query operators (`:-`, `?-`).
  - `Punct` (`filterTokens('punct', this)`): Filters to delimiters (`(`, `)`, `,`, `.`, `[`).
  - `Numbers` (`filterTokens('number', this)`): Filters to numeric literals (`0-9`).

#### B. Inside `Call Graph` Tab (`tab-pdg`):
- **`Fit view` Button (`.graph-tool-btn`)**:
  - `onclick="renderPDGGraph()"`: Re-calculates node positions using circular auto-layout and centers the SVG viewport.

#### C. Inside `WAM & TAC` Tab (`tab-wam`):
- **`Original` Segment Button (`#segOrig`)**:
  - `onclick="selectWamView('orig', this)"`: Displays unoptimized Warren Abstract Machine bytecode.
- **`Optimized` Segment Button (`#segOpt`)**:
  - `onclick="selectWamView('opt', this)"`: Displays optimized WAM bytecode after peep-hole register rewriting and redundant instruction elimination.
- **`Copy WAM` Icon Button**:
  - `onclick="copyWam()"`: Copies compiled WAM assembly to clipboard.
- **`Copy TAC` Icon Button**:
  - `onclick="copyTac()"`: Copies Three-Address Code quadruples `(OP, ARG1, ARG2, RES)` to clipboard.

---

## 🎬 5. Live Demo Showcase (Current Active Tab)

The screenshot shows the **Live Demo** tab (`tab-demo`) actively open. This tab provides a structured, step-by-step presentation of the entire compilation pipeline using the current source code.

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
| Live end-to-end compiler showcase                                          [< Prev] [Play] [Next >]|
| Ingestion, tokenization, parsing, symbols, graph construction...                                   |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
| [1. Ingestion]  [2. Lexer DFA]  [3. AST Parser]  [4. Symbol Table]  [5. Live Call Graph]  [6. Logic Proof] |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
| Step 1: Reading Prolog Horn Clauses                                                               |
| Ready when you are — press Play or Next.                                                          |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 5.1 Playback Transport Controls (`.demo-controls`)
| Button | Selector / Handler | Purpose & Technical Behavior |
| :--- | :--- | :--- |
| **`< Prev`** | `<button class="btn btn-secondary" onclick="demoPrevStep()">` | Steps backward to the previous compiler phase (e.g. from *AST Parser* back to *Lexer DFA*). Updates the stage title, progress bar, and visual output canvas. |
| **`Play` / `Pause`** | `#btnAutoPlay`<br>`onclick="toggleAutoPlay()"` | **Automated Walkthrough Player:**<br>• Toggles automated playback across all 6 phases.<br>• Advances steps every 2.4 seconds with smooth animated progress bar filling.<br>• Label switches between `Play` and `Pause` dynamically. |
| **`Next >`** | `<button class="btn btn-primary" onclick="demoNextStep()">` | Steps forward to the next compiler phase. Automatically compiles the code if not already compiled. |

---

### 5.2 Step Indicator Track Buttons (`.demo-step-track`)
The 6 pill buttons allow jumping directly to any phase of the compiler presentation:

| Step Button | Handler | Phase Demonstrated & Visual Stage Output |
| :---: | :--- | :--- |
| **`1. Ingestion`** *(Active)* | `#dStep1`<br>`jumpToDemoStep(1)` | **Raw Source Code Ingestion:**<br>Displays raw input buffer statistics, byte counts, clause counts, and prepares the compiler pipeline. |
| **`2. Lexer DFA`** | `#dStep2`<br>`jumpToDemoStep(2)` | **Deterministic Finite Automaton Tokenization:**<br>Animates the character-by-character scanner emitting typed token pills with line and column coordinates. |
| **`3. AST Parser`** | `#dStep3`<br>`jumpToDemoStep(3)` | **Context-Free Grammar & Tree Construction:**<br>Visualizes the Recursive Descent parsing of Horn clauses into an indented Abstract Syntax Tree (`Fact`, `Rule`, `AtomTerm`, `VariableTerm`). |
| **`4. Symbol Table`** | `#dStep4`<br>`jumpToDemoStep(4)` | **Static Semantics & Scope Resolution:**<br>Inspects the predicate registry (`functor/arity`), identifies clauses per predicate, and validates singleton variables to catch syntax bugs. |
| **`5. Live Call Graph`** | `#dStep5`<br>`jumpToDemoStep(5)` | **Predicate Dependency Graph & Cycle Detection:**<br>Renders live SVG nodes and directed call edges on `#demoLiveGraphCanvas`, highlighting self-recursive loops (e.g. `ancestor/2`) in crimson red. |
| **`6. Logic Proof`** | `#dStep6`<br>`jumpToDemoStep(6)` | **SLD Resolution & Robinson's Unification:**<br>Runs a real live query against the compiled AST and prints the resulting variable bindings and goal substitutions. |

---

## 📖 6. Grammar & Language Specification Reference Modal

Triggered by the **`📖 Grammar`** button (`#btnGrammarDocsStudio` or `#btnGrammarDocsLanding`), this full-fidelity dialog presents the formal theoretical foundations of the compiler across 5 structured tabs:

### 6.1 Official Language Specification References
- **ISO/IEC 13211-1:1995 (Official ISO Prolog Standard):** Core international standard for Prolog syntax, term algebra, unification algorithms, and built-in operator classifications.
- **SWI-Prolog Syntax & Operator Reference:** Production reference for Edinburgh/ISO operator tables (1200 down to 1), lexical conventions, and escape sequences.
- **Edinburgh Prolog Standard Syntax (Warren, Pereira, Byrd):** Foundational syntax specification establishing classical Horn clause rules (`Head :- Body.`), atom/variable distinction, and bracketed list constructors (`[H|T]`).
- **Warren's Abstract Machine (WAM) Specification (Aït-Kaci):** Definitive tutorial reconstruction modeling registers, heap/choice-point stacks, and intermediate logic instructions.

### 6.2 Operator Precedence & Associativity Table
| Precedence Level | Operators | Associativity | ISO Specifier | Description |
| :--- | :--- | :--- | :--- | :--- |
| **1 (Lowest) / 1200** | `:-`, `?-` | Right / Prefix | `xfx, fx` | Clause Neck (Rule definition) & Query Directive |
| **2 / 1100** | `;` | Right | `xfy` | Logical Disjunction (OR) |
| **3 / 1050** | `->` | Right | `xfy` | If-Then Implication / Local conditional branch |
| **4 / 1000** | `,` | Right | `xfy` | Logical Conjunction (AND - sequential goal evaluation) |
| **5 / 900** | `\+` | Right | `fy` | Negation-as-Failure (Logical NOT / unprovability) |
| **6 / 700** | `=`, `\=` | None | `xfx` | Syntactic Unification & Syntactic Non-Unification |
| **7 / 700** | `==`, `\==` | None | `xfx` | Strict Structural Term Identity & Non-Identity |
| **8 / 700** | `<`, `>`, `=<`, `>=` | None | `xfx` | Relational Arithmetic Comparison |
| **9 / 700** | `is` | None | `xfx` | Arithmetic Evaluation & Variable Binding |
| **10 / 500** | `+`, `-` | Left | `yfx, fx` | Binary Addition, Subtraction & Unary Plus/Minus |
| **11 / 400** | `*`, `/`, `mod` | Left | `yfx` | Multiplication, Float Division, Integer Modulo |
| **12 (Highest)** | `!`, `[H\|T]`, `f(...)`, `(expr)` | Left / Enclosing | `Primary` | Cut barrier, List constructor, Functor call, Grouping |

### 6.3 Supported Grammar Subset (GNU Bison LALR(1) / CFG Syntax)
Provides the formal grammar subset implemented in `parser.py` with an interactive **Copy Grammar** button:
```bison
program     : clause_list EOF ;
clause_list : clause_list clause | /* empty */ ;
clause      : fact | rule | query ;
fact        : head '.' ;
rule        : head OP_RULE goal_list '.' ;
query       : OP_QUERY goal_list '.' ;
head        : compound_term | ATOM ;
goal_list   : goal_list ',' goal | goal_list ';' goal | goal ;
goal        : expr | '!' ;
expr        : expr '=' expr | expr OPERATOR expr | expr IS expr | expr '+' expr | expr '-' expr | expr '*' expr | expr '/' expr | primary_term ;
primary_term: compound_term | ATOM | VARIABLE | ANON_VAR | NUMBER | STRING | list_term | '(' expr ')' ;
compound_term : ATOM '(' arg_list ')' ;
arg_list    : arg_list ',' expr | expr ;
list_term   : '[' ']' | '[' list_elements ']' ;
list_elements : expr_list '|' primary_term | expr_list ;
expr_list   : expr_list ',' expr | expr ;
```

### 6.4 Deliberate Simplifications & Unsupported Constructs
- **Definite Clause Grammars (DCG):** Native syntactic sugar (`-->`) omitted; programs use explicit difference lists `(S0, S)`.
- **Dynamic Database Mutation:** `asserta/1`, `assertz/1`, and `retract/1` omitted to enforce purely declarative compile-time static analysis and static call graphs.
- **Higher-Order Meta-Predicates:** Built-in collection predicates (`findall/3`, `bagof/3`, `setof/3`) scoped out to focus on first-order Robinson unification and WAM instruction lowering.
- **Dynamic Operator Redefinition:** Runtime `:- op/3` dynamic declarations excluded; compiler uses the complete static ISO precedence climbing table.
- **Coroutining & Delayed Constraints:** `freeze/2`, `when/2`, and `dif/2` excluded from WAM stack activation records.
- **Module Namespaces & Exceptions:** Multi-file module prefixing (`module:pred/N`) and `catch/3` / `throw/1` blocks omitted; panic-mode recovery synchronizes on clause terminators (`.`).

### 6.5 FIRST & FOLLOW Sets Table
Defines the terminal sets for LL(1) predictive parsing validation:
- **Program:** FIRST = `{ ATOM, VARIABLE, '? -', ε }`, FOLLOW = `{ $ }`
- **Clause:** FIRST = `{ ATOM, VARIABLE, '? -' }`, FOLLOW = `{ ATOM, VARIABLE, '? -', $ }`
- **Fact / Rule:** FIRST = `{ ATOM }`, FOLLOW = `{ ATOM, VARIABLE, '? -', $ }`
- **Query:** FIRST = `{ '? -' }`, FOLLOW = `{ ATOM, VARIABLE, '? -', $ }`
- **GoalList:** FIRST = `{ ATOM, VARIABLE, NUMBER, '[', '(', '!' }`, FOLLOW = `{ '.' }`
- **Term:** FIRST = `{ ATOM, VARIABLE, NUMBER, STRING, '[', '(' }`, FOLLOW = `{ ',', ')', ']', '|', '.', ':-', ';', OPERATOR, $ }`
- **ListTerm:** FIRST = `{ '[' }`, FOLLOW = `{ ',', ')', ']', '|', '.', ':-', ';', $ }`

---

## 📋 7. Master Summary Table of All Prototype Buttons

| # | Button Label / Icon | CSS / HTML Identity | Primary JS Function | Role in Compiler Studio |
| :-: | :--- | :--- | :--- | :--- |
| 1 | `[🏠]` Home | `.site-header .icon-btn` | `exitStudioToLanding()` | Switch to landing page overview |
| 2 | `Family Tree` | `.preset-btn[data-key="ancestor_tree"]` | `selectPreset('ancestor_tree', this)` | Load recursive kinship program |
| 3 | `Network Paths` | `.preset-btn[data-key="graph_network"]` | `selectPreset('graph_network', this)` | Load directed network reachability program |
| 4 | `List Ops` | `.preset-btn[data-key="list_algorithms"]` | `selectPreset('list_algorithms', this)` | Load recursive list operations program |
| 5 | `Evaluator` | `.preset-btn[data-key="expr_evaluator"]` | `selectPreset('expr_evaluator', this)` | Load algebraic expression evaluator |
| 6 | `[⤹]` Cursor Toggle | `#cursorToggleStudio` | `toggleCursor()` | Enable/disable custom cursor follower |
| 7 | `[🌙/☀️]` Theme | `.site-header .icon-btn` | `toggleTheme()` | Toggle OLED Dark / Clean Light theme |
| 8 | `📖 Grammar` | `#btnGrammarDocsStudio` | `openGrammarModal()` | Open formal Prolog grammar & specification modal |
| 9 | `▶ Demo` (Header) | `.btn.btn-demo` | `startLiveDemo()` | Quick launch to Live Demo visualizer tab |
| 10 | `⚡ Analyze & Compile` | `#btnCompileCode` | `compileCode()` | Trigger full 6-phase compilation pipeline |
| 11 | `↺ Reset` | `#btnResetStudio` | `resetStudio()` | Restore default source and query |
| 12 | `Solve` | `#btnSolveQuery` | `solveQuery()` | Execute unification and SLD resolution query |
| 13 | `▶ SLD proof trace` | `<details> <summary>` | Built-in HTML `<details>` toggle | Expand/collapse step-by-step resolution steps |
| 14 | `⚡ Lexer Tokens` | `#btnTabLexer` | `switchTab('tab-lexer')` | Switch to lexical token stream view |
| 15 | `🌿 AST & Symbols` | `#btnTabAst` | `switchTab('tab-ast')` | Switch to AST tree and symbol table view |
| 16 | `🔀 Call Graph` | `#btnTabPdg` | `switchTab('tab-pdg')` | Switch to Predicate Dependency Graph view |
| 17 | `💾 WAM & TAC` | `#btnTabWam` | `switchTab('tab-wam')` | Switch to WAM bytecode & TAC view |
| 18 | `▶ Live Demo` (Tab) | `#btnTabDemo` | `switchTab('tab-demo')` | Switch to 6-step guided walkthrough tab |
| 19 | `All tokens` | `.filter-chip[data-ft="all"]` | `filterTokens('all', this)` | Show all lexical tokens |
| 20 | `Atoms` | `.filter-chip[data-ft="atom"]` | `filterTokens('atom', this)` | Filter token list to atoms |
| 21 | `Variables` | `.filter-chip[data-ft="variable"]` | `filterTokens('variable', this)` | Filter token list to variables |
| 22 | `Operators` | `.filter-chip[data-ft="operator"]` | `filterTokens('operator', this)` | Filter token list to operators (`:-`, `?-`) |
| 23 | `Punct` | `.filter-chip[data-ft="punct"]` | `filterTokens('punct', this)` | Filter token list to punctuation |
| 24 | `Numbers` | `.filter-chip[data-ft="number"]` | `filterTokens('number', this)` | Filter token list to numeric literals |
| 25 | `Fit view` | `.graph-tool-btn` | `renderPDGGraph()` | Recenter and fit Call Graph SVG |
| 26 | `Original` WAM | `#segOrig` | `selectWamView('orig', this)` | View unoptimized WAM bytecode |
| 27 | `Optimized` WAM | `#segOpt` | `selectWamView('opt', this)` | View optimized WAM bytecode |
| 28 | `Copy WAM` | `.wam-view .icon-btn` | `copyWam()` | Copy WAM instructions to clipboard |
| 29 | `Copy TAC` | `.wam-view .icon-btn` | `copyTac()` | Copy Three-Address Code to clipboard |
| 30 | `< Prev` (Demo) | `.demo-controls .btn-secondary` | `demoPrevStep()` | Step back to previous compiler phase |
| 31 | `Play / Pause` | `#btnAutoPlay` | `toggleAutoPlay()` | Start/pause auto-advancing demo tour |
| 32 | `Next >` (Demo) | `.demo-controls .btn-primary` | `demoNextStep()` | Step forward to next compiler phase |
| 33 | `1. Ingestion` | `#dStep1` | `jumpToDemoStep(1)` | Jump to Step 1: Input buffer ingestion |
| 34 | `2. Lexer DFA` | `#dStep2` | `jumpToDemoStep(2)` | Jump to Step 2: Lexer tokenizer output |
| 35 | `3. AST Parser` | `#dStep3` | `jumpToDemoStep(3)` | Jump to Step 3: Abstract Syntax Tree |
| 36 | `4. Symbol Table` | `#dStep4` | `jumpToDemoStep(4)` | Jump to Step 4: Semantic symbol analysis |
| 37 | `5. Live Call Graph` | `#dStep5` | `jumpToDemoStep(5)` | Jump to Step 5: SVG dependency call graph |
| 38 | `6. Logic Proof` | `#dStep6` | `jumpToDemoStep(6)` | Jump to Step 6: Live SLD resolution proof |

---

*PROLOG-PARSE Compiler Lab Studio · Department of Computer Science & Engineering · VNRVJIET*
