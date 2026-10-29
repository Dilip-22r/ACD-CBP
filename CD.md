# 🏛️ Compiler Design (CD) Implementation & Viva Defense Guide

**Course:** Compiler Design and Computer Networks Laboratory (22PC2CS301)  
**Project Title:** PROLOG-C: A Full-Phase Compiler, Static Analyzer, and WAM Logic Engine for ISO Prolog  
**Department:** Computer Science and Engineering, VNRVJIET  

---

## 📌 Executive Summary for the Examiner

While typical academic Compiler Design projects stop at trivial arithmetic expression calculators or simple lexers, **PROLOG-C** tackles the complete formal compilation pipeline for **ISO Prolog (First-Order Logic Horn Clauses)**.

The project demonstrates all classical phases of compiler engineering:
1. **Phase 1 — Lexical Analysis (Lexer):** Deterministic Finite Automaton (DFA) tokenizer for Atoms, Logic Variables, Numbers, Functors, Comments (`%`, `/* */`), and Neck/Query operators (`:-`, `?-`).  
2. **Phase 2 — Syntax Analysis (Parser):** Predictive Recursive Descent Parser with Panic-Mode Error Recovery, constructing both Concrete Syntax Trees (CST) and Abstract Syntax Trees (AST). Complete with formal **FIRST & FOLLOW sets**.
3. **Phase 3 — Semantic Analysis & Symbol Table:** Predicate Signature Indexing (`functor/arity`), Clause-Level Lexical Scope tracking, and **Singleton Variable Detection** (catching typos where a variable appears only once in a clause).
4. **Phase 4 — Intermediate Code Generation (ICG):** Compiles AST into standard **Warren Abstract Machine (WAM)** bytecode instructions (`get_structure`, `unify_variable`, `put_value`, `call`, `proceed`) and **Three-Address Code (TAC) Quadruples**.
5. **Phase 5 — Code Optimization:** Peep-hole register allocation optimization, redundant instruction elimination, and constant propagation.
6. **Phase 6 — Execution & Resolution Engine:** Validates compiler correctness using **Robinson's First-Order Unification Algorithm** (with occurs-check) and **SLD Resolution with Chronological Backtracking**.

---

## 🗺️ The 6 Classical Compiler Phases Implemented in PROLOG-C

```
+───────────────────────────────────────────────────────────────────────────────+
| [1] LEXICAL ANALYZER (lexer.py)                                               |
|     Input: Prolog Source Code (.pl)                                           |
|     Output: Linear Token Stream (Type, Lexeme, Line, Col)                     |
|     Tokens: ATOM, VARIABLE, ANON_VAR, NUMBER, OP_RULE (:-), OP_QUERY (?-), .  |
+───────────────────────────────────────────────────────────────────────────────+
                                        │
                                        ▼
+───────────────────────────────────────────────────────────────────────────────+
| [2] SYNTAX ANALYZER / PARSER (parser.py)                                      |
|     CFG: Program -> Clause* EOF; Clause -> Fact | Rule | Query               |
|     Technique: Predictive Recursive Descent with Error Recovery               |
|     Output: Abstract Syntax Tree (AST) & Derivation Steps                     |
+───────────────────────────────────────────────────────────────────────────────+
                                        │
                                        ▼
+───────────────────────────────────────────────────────────────────────────────+
| [3] SEMANTIC ANALYZER & SYMBOL TABLE (semantic.py)                            |
|     Symbol Table: Indexes Predicate Signatures (functor/arity)                |
|     Scope Rules: Clause-local variable namespaces                             |
|     Diagnostics: Singleton Variable Warnings, Arity Mismatches, Undefined Preds|
+───────────────────────────────────────────────────────────────────────────────+
                                        │
                                        ▼
+───────────────────────────────────────────────────────────────────────────────+
| [4] INTERMEDIATE CODE GENERATOR (wam_compiler.py)                             |
|     Warren Abstract Machine (WAM) Bytecode: allocate, get_structure, call     |
|     Three-Address Code (TAC) Quadruples: (OP, ARG1, ARG2, RESULT)             |
+───────────────────────────────────────────────────────────────────────────────+
                                        │
                                        ▼
+───────────────────────────────────────────────────────────────────────────────+
| [5] CODE OPTIMIZATION PASS (wam_compiler.py)                                  |
|     Peep-hole instruction rewriting (get_variable -> put_value chaining)      |
|     Dead code & unused argument elimination                                   |
+───────────────────────────────────────────────────────────────────────────────+
                                        │
                                        ▼
+───────────────────────────────────────────────────────────────────────────────+
| [6] EXECUTION ENGINE & UNIFIER (engine.py)                                    |
|     Robinson's Unification Algorithm (MGU computation with Occurs-Check)      |
|     SLD Resolution & Backtracking Proof Search                                |
+───────────────────────────────────────────────────────────────────────────────+
```

---

## 📐 Formal Context-Free Grammar (CFG) for ISO Prolog

The language grammar is defined formally by $G = (V_N, V_T, P, S)$:

### 1. Variables / Non-Terminals ($V_N$):
$$\{ \text{Program}, \text{ClauseList}, \text{Clause}, \text{Fact}, \text{Rule}, \text{Query}, \text{Head}, \text{GoalList}, \text{ConjGoalList}, \text{Goal}, \text{CutGoal}, \text{RelExpr}, \text{RelOp}, \text{AddExpr}, \text{AddOp}, \text{MulExpr}, \text{MulOp}, \text{Term}, \text{GroupExpr}, \text{AtomicTerm}, \text{VariableTerm}, \text{CompoundTerm}, \text{ArgList}, \text{ListTerm}, \text{EmptyList}, \text{BracketList}, \text{ListElements}, \text{TailTerm} \}$$

### 2. Terminals ($V_T$):
$$\{ \text{ATOM}, \text{VARIABLE}, \text{NUMBER}, \text{STRING}, \text{ANON\_VAR}, \text{':-'}, \text{'?-'}, \text{'.'}, \text{','}, \text{';'}, \text{'('}, \text{')'}, \text{'['}, \text{']'}, \text{'|'}, \text{'!'}, \text{'is'}, \text{'='}, \text{'\='}, \text{'=='}, \text{'\=='}, \text{'<'}, \text{'>'}, \text{'=<'}, \text{'>='}, \text{'+'}, \text{'-'}, \text{'*'}, \text{'/'}, \text{'mod'}, \text{EOF} \}$$

### 3. Production Rules ($P$):
```ebnf
/* 1. Program & Clause Sequencing */
Program          ::= ClauseList EOF
ClauseList       ::= Clause ClauseList | ε
Clause           ::= Fact | Rule | Query

/* 2. Clause Forms */
Fact             ::= Head '.'
Rule             ::= Head ':-' GoalList '.'
Query            ::= '?-' GoalList '.'

/* 3. Predicate Head */
Head             ::= CompoundTerm | ATOM

/* 4. Goal Sequencing & Conjunction/Disjunction */
GoalList         ::= Goal ConjGoalList
ConjGoalList     ::= ',' Goal ConjGoalList | ';' Goal ConjGoalList | ε
Goal             ::= RelExpr | CutGoal
CutGoal          ::= '!'

/* 5. Relational & Arithmetic Operator Precedence */
RelExpr          ::= AddExpr ( RelOp AddExpr )*
RelOp            ::= 'is' | '=' | '\=' | '==' | '\==' | '<' | '>' | '=<' | '>='
AddExpr          ::= MulExpr ( AddOp MulExpr )*
AddOp            ::= '+' | '-'
MulExpr          ::= Term ( MulOp Term )*
MulOp            ::= '*' | '/' | 'mod'

/* 6. Terms & Data Structures */
Term             ::= CompoundTerm | AtomicTerm | VariableTerm | ListTerm | GroupExpr
GroupExpr        ::= '(' RelExpr ')'
AtomicTerm       ::= ATOM | NUMBER | STRING
VariableTerm     ::= VARIABLE | ANON_VAR

/* 7. Functors & Compound Predicates */
CompoundTerm     ::= ATOM '(' ArgList ')'
ArgList          ::= RelExpr ( ',' RelExpr )*

/* 8. Lists & Head/Tail Splitting */
ListTerm         ::= EmptyList | BracketList
EmptyList        ::= '[' ']'
BracketList      ::= '[' ListElements ']'
ListElements     ::= RelExpr ( ',' RelExpr )* ( '|' TailTerm )?
TailTerm         ::= Term
```

---

## 📊 FIRST & FOLLOW Sets Table

Essential for LL(1) parsing validation:

| Non-Terminal | FIRST Set | FOLLOW Set |
| :--- | :--- | :--- |
| **Program** | `{ ATOM, VARIABLE, '?-', ε }` | `{ $ }` |
| **Clause** | `{ ATOM, VARIABLE, '?-' }` | `{ ATOM, VARIABLE, '?-', $ }` |
| **Fact** | `{ ATOM }` | `{ ATOM, VARIABLE, '?-', $ }` |
| **Rule** | `{ ATOM }` | `{ ATOM, VARIABLE, '?-', $ }` |
| **Query** | `{ '?-' }` | `{ ATOM, VARIABLE, '?-', $ }` |
| **Head** | `{ ATOM }` | `{ '.', ':-' }` |
| **GoalList** | `{ ATOM, VARIABLE, NUMBER, STRING, '[', '(', '!' }` | `{ '.' }` |
| **Goal** | `{ ATOM, VARIABLE, NUMBER, STRING, '[', '(', '!' }` | `{ ',', ';', '.' }` |
| **Expr** | `{ ATOM, VARIABLE, NUMBER, STRING, '[', '(' }` | `{ ',', ';', '.', ')', ']' }` |
| **Term** | `{ ATOM, VARIABLE, NUMBER, STRING, '[', '(' }` | `{ ',', ')', ']', '\|', '.', ':-', ';', OPERATOR, $ }` |
| **CompoundTerm** | `{ ATOM }` | `{ '.', ':-', ',', ';', ')', ']', '\|', OPERATOR, $ }` |
| **ArgList** | `{ ATOM, VARIABLE, NUMBER, STRING, '[', '(' }` | `{ ')' }` |
| **ListTerm** | `{ '[' }` | `{ ',', ')', ']', '\|', '.', ':-', ';', OPERATOR, $ }` |

---

## ⚙️ Compiler Phases: In-Depth Breakdown

### 1. Lexical Analyzer (`lexer.py`)
- **DFA States:**
  - `START`: Reads leading character.
  - `IN_ATOM`: Reads lowercase letters/digits.
  - `IN_VARIABLE`: Reads uppercase letters or leading `_`.
  - `IN_NUMBER`: Handles digits and decimal point lookahead (`.`).
  - `IN_COMMENT`: Skips characters until newline (`%`) or closing `*/`.
- **Lookahead Resolution:**
  - Differentiates the clause terminator dot `.` from a floating-point number `3.14` by checking if the subsequent character is whitespace, newline, or EOF.

### 2. Syntax Analyzer (`parser.py`)
- Employs **Predictive Recursive Descent**.
- Produces a strictly typed Abstract Syntax Tree (`ast_nodes.py`).
- Implements **Panic-Mode Error Recovery**: upon encountering a syntax error, the parser emits a descriptive diagnostic with line/col coordinates and advances tokens until the next `.` (clause terminator) to continue parsing subsequent clauses.

### 3. Semantic Analysis & Symbol Table (`semantic.py`)
- **Predicate Signatures:** Prolog functions by arity. `parent(X, Y)` is registered as `parent/2`. It is strictly distinct from `parent(X, Y, Z)` (`parent/3`).
- **Clause-Local Scope:** Unlike C/Java where variables have block scope, in Prolog, variable names (`X`, `Student`) are scoped strictly to the clause in which they appear.
- **Singleton Variable Warning:** If a variable appears only once in a rule or fact (e.g. `p(X, Y) :- q(X).`), `Y` is flagged as a Singleton Variable because it contributes nothing to the relation and usually indicates a spelling mistake.

### 4. Intermediate Code Generation (WAM & TAC) (`wam_compiler.py`)
- **Warren Abstract Machine (WAM):** The standard virtual architecture for logic languages.
  - `get_constant C, Ai`: Asserts that argument register `Ai` contains constant `C`.
  - `get_variable X, Ai`: Copies register `Ai` into local variable `X`.
  - `put_value X, Ai`: Sets up argument register `Ai` with value of `X` before calling a subgoal.
  - `call Pred/N`: Invokes predicate `Pred` with arity `N`.
  - `proceed`: Returns successfully from fact or rule.
- **Three-Address Code (TAC):** Quadruple format `(OP, ARG1, ARG2, RESULT)`.

### 5. Execution Engine (`engine.py`)
- **Robinson's First-Order Unification Algorithm:**
  - Computes the Most General Unifier (MGU) $\theta$.
  - Includes **Occurs-Check** to prevent circular infinite terms like $X = f(X)$.
- **SLD Resolution:** Selects leftmost subgoal, searches matching clauses, performs variable standardization (renaming apart), and backtracks upon failure.

---

## 🎯 Top 15 Examiner Viva Questions & Model Answers

### Q1: What makes parsing Prolog different from parsing C or Java?
> **Answer:** In C or Java, statements are procedural and variables have nested block scopes. In Prolog, programs are collections of **Horn Clauses** (facts and rules) without explicit type declarations. Variables are dynamically typed and **strictly clause-scoped**. Additionally, compound terms serve dual purposes: they represent both data structures and callable goals.

### Q2: Why is the grammar of Prolog LL(1) friendly?
> **Answer:** Each clause begins with a distinct token type (an Atom for facts/rules or `?-` for queries). Subgoals in the rule body are separated deterministically by `,` (AND) or `;` (OR), and every clause ends with a terminating period `.`. With 1 token of lookahead, the parser can predict whether it is encountering a fact, rule, or query.

### Q3: What is a "Singleton Variable" and why does your compiler flag it?
> **Answer:** A singleton variable is a variable that appears only once inside a given clause. In logic programming, variables express constraints or relationships between terms. If a variable is mentioned only once, it either has no effect on the logic or is a typographical error (e.g., typing `Stundet` instead of `Student`). Our semantic analyzer issues a warning and suggests prefixing it with an underscore `_`.

### Q4: Explain the difference between `f/2` and `f/3` in the Symbol Table.
> **Answer:** In Prolog, predicates are identified by their **functor and arity** pair (`functor/arity`). Thus, `course(cse, 101)` is stored under key `course/2`, while `course(cse, 101, 4)` is stored under key `course/3`. They are completely distinct predicates and can coexist without naming collisions.

### Q5: What is the Warren Abstract Machine (WAM)?
> **Answer:** The Warren Abstract Machine, designed by David H. D. Warren in 1983, is the universal intermediate representation and virtual machine architecture for Prolog compilers. It decomposes logic clauses into specialized register-based instructions for argument passing (`put_*`), pattern matching (`get_*`), and goal execution (`call`, `proceed`).

### Q6: What is a Three-Address Code Quadruple? Show an example from your compiler.
> **Answer:** A quadruple is an intermediate representation record with four fields: `(OP, ARG1, ARG2, RESULT)`. For example, matching an atom argument `cse` in register `A1` generates the quadruple:
> `(EQ_ATOM, cse, A1, match_flag)`
> And calling a subgoal generates:
> `(CALL, needs_counselling/2, 2, t1)`

### Q7: How does Robinson's Unification Algorithm work?
> **Answer:** Given two terms $T_1$ and $T_2$, unification finds a substitution $\theta$ such that $T_1\theta = T_2\theta$.
> 1. If both are identical constants or atoms, it succeeds with $\theta$.
> 2. If one is a variable $V$, it binds $V \to T$ after running the **occurs-check** (ensuring $V$ does not appear inside $T$).
> 3. If both are compound terms, their functors and arities must match, and all corresponding arguments must recursively unify.

### Q8: What is the Occurs-Check and why is it important?
> **Answer:** The occurs-check verifies that a variable $X$ does not appear within the term it is being unified with (e.g., trying to unify $X$ with $f(X)$). Without the occurs-check, the unifier would construct a cyclic, infinite data structure that causes compiler or runtime crashes.

### Q9: How does Panic-Mode Error Recovery work in your parser?
> **Answer:** When an unexpected token is encountered during parsing of a clause, the parser logs a `SyntaxError` with the line number and column, then enters panic-mode: it discards incoming tokens until it detects a `.` (the clause synchronization token) or `EOF`. This prevents cascading syntax errors and allows the compiler to analyze the rest of the source file.

### Q10: How does your lexer distinguish between a period as a clause terminator and a period in a float?
> **Answer:** The lexer uses 1-character lookahead. If the dot `.` is preceded by digits and immediately followed by digits (e.g. `3.14`), it is tokenized as a `NUMBER`. If the dot is followed by whitespace, newline, comment `%`, or EOF, it is tokenized as a `DOT` clause terminator.

### Q11: What is the difference between Concrete Syntax Tree (CST) and Abstract Syntax Tree (AST)?
> **Answer:** The CST (Parse Tree) contains every grammar detail including punctuation tokens (`(`, `)`, `,`, `.`, `:-`). The AST discards extraneous syntax noise and retains only semantic nodes: `Fact`, `Rule`, `CompoundTerm`, `Variable`, and `Atom`.

### Q12: How are lists represented internally in your AST?
> **Answer:** A list `[a, b | T]` is represented in the AST by a `ListTerm` node storing a list of head elements `[Atom('a'), Atom('b')]` and an optional tail term `Variable('T')`. An empty list `[]` has an empty elements list and `None` tail.

### Q13: What optimization is performed in the intermediate code generation phase?
> **Answer:** PROLOG-C performs peep-hole optimization on argument registers. For example, if a head parameter reads argument register $A_1$ (`get_variable X, A1`) and immediately prepares that same variable as the first argument of the first subgoal (`put_value X, A1`), the compiler eliminates the redundant `put_value` instruction.

### Q14: How does variable renaming (Standardizing Apart) prevent bugs during recursive rule evaluation?
> **Answer:** When a rule like `ancestor(A, D) :- parent(A, P), ancestor(P, D).` calls itself recursively, variables named `A`, `P`, and `D` appear at multiple recursion levels. If they were not standardized apart, variables from the parent frame would accidentally bind to variables in the child frame. Our engine renames variables to `A_depth_counter` before each resolution step.

### Q15: How does this project relate to EduTrack?
> **Answer:** PROLOG-C includes an **Academic Risk Knowledge Base** (`edutrack_rules.pl`) directly modeling student records, GPA thresholds, and attendance rules. While EduTrack used Machine Learning for statistical dropout scoring, PROLOG-C uses formal logic compilation to parse, verify, and infer academic policy rules through a rigorous 6-phase compiler pipeline!
