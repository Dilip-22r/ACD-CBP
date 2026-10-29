# ⚡ Quick Faculty Cheat-Sheet: How Grammar is Implemented in PROLOG-C

**Course:** Compiler Design Laboratory (22PC2CS301)  
**Project:** PROLOG-PARSE / PROLOG-C — Logic Compiler & Visual Studio  
**Purpose:** 60-Second Viva Guide for Answering "Where and How is Grammar Implemented?"

---

## 📌 1. The 30-Second Summary to Speak to Faculty

> *"Sir/Madam, our compiler implements grammar at **two synchronized layers**:*
> 1. ***Formal YACC/Bison Layer (`prolog.y` & `prolog.l`):** Contains the official declarative Context-Free Grammar (CFG) in Yacc BNF syntax with `%token` declarations and ISO operator precedence (`%left`, `%right`). It is compiled via Flex and Bison into a native executable `prolog_yacc.exe`.*
> 2. ***Visual Studio Python Layer (`parser.py` & `lexer.py`):** Implements the exact same CFG productions using **Predictive Recursive Descent with Operator Precedence Climbing** and panic-mode error recovery, driving the interactive web studio."*

---

## 📁 2. Which Files Contain the Grammar? (Exact File Map)

| File Name | Compiler Phase | Lines | What Grammar is Inside? |
| :--- | :--- | :---: | :--- |
| [`prolog.y`](file:///d:/CBPS/Prolog_Compiler_CD/prolog.y) | **Syntax (YACC)** | **~1,000** | **Formal YACC/Bison BNF productions:** `program`, `clause`, `fact`, `rule`, `head`, `body`, `compound_term`, `list_term`, and `%left`/`%right` operator precedence tables. |
| [`prolog.l`](file:///d:/CBPS/Prolog_Compiler_CD/prolog.l) | **Lexical (LEX)** | **~220** | **Flex DFA regular expressions:** Tokens for atoms, variables, numbers, strings, operators, comments (`%` and `/* */`), feeding `prolog.y`. |
| [`parser.py`](file:///d:/CBPS/Prolog_Compiler_CD/parser.py) | **Syntax (Python)** | **~400** | **Predictive Recursive Descent:** Methods `parse_program()`, `parse_clause()`, `parse_head()`, `parse_body()`, `parse_term()` with precedence climbing and panic-mode `synchronize()`. |
| [`lexer.py`](file:///d:/CBPS/Prolog_Compiler_CD/lexer.py) | **Lexical (Python)** | **~320** | **Python DFA Scanner:** Recognizes 20+ token types with exact line and column tracking. |
| [`semantic.py`](file:///d:/CBPS/Prolog_Compiler_CD/semantic.py) | **Semantic Check** | **~240** | **Symbol Table & Scope Rules:** Functor/arity indexing, clause counts, and singleton variable warning detection. |
| [`wam_compiler.py`](file:///d:/CBPS/Prolog_Compiler_CD/wam_compiler.py) | **Intermediate Code**| **~300** | **WAM Code Gen:** Lowers grammar AST nodes into Warren Abstract Machine instructions (`put_*`, `get_*`, `unify_*`, `call`, `proceed`). |
| [`GRAMMAR_SPEC_1000.md`](file:///d:/CBPS/Prolog_Compiler_CD/GRAMMAR_SPEC_1000.md) | **Documentation** | **~500** | **Full 1,000-Rule Catalog:** Exhaustive formal reference of every production across all 8 compiler phases. |

---

## ⚙️ 3. How the Grammar Rules Actually Work

```
Source Code (.pl)
       │
       ▼
[Phase 1: Lexer (prolog.l / lexer.py)] 
   ➔ Scans text into Tokens: ATOM("parent"), LPAREN, VAR("X"), COMMA, VAR("Y"), RPAREN, DOT
       │
       ▼
[Phase 2: Parser (prolog.y / parser.py)]
   ➔ Applies Grammar Productions:
      • Program   ::= Clause*
      • Clause    ::= Fact | Rule | Query
      • Fact      ::= Head '.'
      • Rule      ::= Head ':-' Body '.'
      • Head      ::= Atom | Functor(Args...)
      • Body      ::= Goal (',' Goal | ';' Goal)*
      • Term      ::= Atom | Var | Number | List | InfixExpr
       │
       ▼
[Phase 3: Semantic Analysis (semantic.py / prolog.y symtab)]
   ➔ Builds Predicate Symbol Table (e.g. parent/2, ancestor/2)
   ➔ Detects Singleton Variables (linting)
       │
       ▼
[Phase 4: Intermediate Code Generation (wam_compiler.py)]
   ➔ Generates WAM Bytecode + TAC Quadruples
       │
       ▼
[Phase 5: SLD Resolution Engine (engine.py)]
   ➔ Robinson Unification with Occurs-Check + Chronological Backtracking
```

---

## 🚨 4. How Wrong Grammar is Handled (Error Recovery)

When bad Prolog syntax is provided:

1. **YACC Parser (`prolog_yacc.exe`):**
   * Employs the error production: `clause : error DOT`
   * Catches syntax errors (e.g., missing closing parenthesis `parent(a, b.` or bad operators `X is * 5.`).
   * Discards invalid tokens up to the clause boundary `.` (panic-mode resynchronization).
   * Generates an `[ERROR_CLAUSE_RESYNC]` AST node and **continues parsing subsequent valid clauses**!

2. **Python Parser (`parser.py`):**
   * Uses the method `synchronize()` in `parser.py:L85`.
   * Skips tokens until encountering `DOT ('.')` or `EOF`.
   * Records clean line/column error diagnostics without crashing.

**Try it in terminal:**
```bash
prolog_yacc.exe examples\bad_syntax_suite.pl
```
*Result: Catches all 4 syntax errors, resynchronizes, parses the remaining 5 valid clauses cleanly!*

---

## 🎯 5. How to Run & Verify for Faculty (Commands to Show)

```bash
# 1. Compile the Yacc Grammar and Lex Scanner into native binary:
build_yacc.bat

# 2. Run the Yacc Parser on sample code:
prolog_yacc.exe examples\ancestor.pl

# 3. Test Panic-Mode Error Recovery with bad grammar:
prolog_yacc.exe examples\bad_syntax_suite.pl

# 4. Run the 36 automated unit tests:
python tests_edge_cases.py

# 5. Launch the Web Studio UI:
python app.py
# (Open http://127.0.0.1:5050 in browser)
```
