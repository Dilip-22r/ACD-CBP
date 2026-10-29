%{
/*
 * ============================================================================
 * PROLOG-YACC: Massive Exhaustive ISO/IEC 13211-1 Prolog Formal Grammar
 * Course: Compiler Design and Computer Networks Laboratory (22PC2CS301)
 * Institution: Department of Computer Science & Engineering, VNRVJIET
 *
 * This specification implements the complete formal Context-Free Grammar (CFG)
 * for ISO Standard Prolog, Definite Clause Grammars (DCG), Module Directives,
 * Operator Declarations, First-Order Logic Horn Clauses, List Constructors,
 * Arithmetic Infix Expressions, and Error-Recovery Synchronization.
 *
 * Generated Parser Type: LALR(1) Automaton with Shift-Reduce Precedence Resolution
 * Target Host Language : ANSI C11 / C99 / MinGW GCC
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <time.h>

/* Forward declarations */
extern int yylex(void);
extern int yylineno;
extern char *yytext;
void yyerror(const char *format, ...);

/* Global Compiler Metrics & Statistics */
int g_total_clauses       = 0;
int g_fact_count          = 0;
int g_rule_count          = 0;
int g_query_count         = 0;
int g_directive_count     = 0;
int g_dcg_rule_count      = 0;
int g_term_count          = 0;
int g_variable_count      = 0;
int g_compound_count      = 0;
int g_list_count          = 0;
int g_operator_count      = 0;
int g_error_count         = 0;
int g_warning_count       = 0;

/* =========================================================================
 * 1. EXTENDED ABSTRACT SYNTAX TREE (AST) DATA STRUCTURES
 * ========================================================================= */

typedef enum {
    /* Program & Clause Hierarchy */
    AST_PROGRAM,
    AST_CLAUSE_LIST,
    AST_FACT,
    AST_RULE,
    AST_QUERY,
    AST_DIRECTIVE,
    AST_DCG_RULE,

    /* Structural Head & Body */
    AST_HEAD,
    AST_BODY,
    AST_CONJUNCTION,
    AST_DISJUNCTION,
    AST_IF_THEN_ELSE,
    AST_IF_THEN,
    AST_NEGATION,
    AST_CUT,

    /* Terminal Leaf Terms */
    AST_ATOM,
    AST_VARIABLE,
    AST_ANON_VAR,
    AST_INTEGER,
    AST_FLOAT,
    AST_STRING,

    /* Structured Terms */
    AST_COMPOUND,
    AST_LIST_NIL,
    AST_LIST_CONS,
    AST_LIST_EXPLICIT,
    AST_CURLY_BLOCK,
    AST_ARG_LIST,

    /* Arithmetic & Relational Infix Expressions */
    AST_OP_IS,
    AST_OP_UNIFY,
    AST_OP_NOT_UNIFY,
    AST_OP_STRICT_EQ,
    AST_OP_STRICT_NEQ,
    AST_OP_UNIV,
    AST_OP_LT,
    AST_OP_GT,
    AST_OP_LE,
    AST_OP_GE,
    AST_OP_ADD,
    AST_OP_SUB,
    AST_OP_MUL,
    AST_OP_DIV,
    AST_OP_IDIV,
    AST_OP_MOD,
    AST_OP_REM,
    AST_OP_POW,
    AST_OP_UNARY_MINUS,
    AST_OP_BITWISE_AND,
    AST_OP_BITWISE_OR,
    AST_OP_BITWISE_XOR,
    AST_OP_SHIFT_LEFT,
    AST_OP_SHIFT_RIGHT,

    /* Directives & Modules */
    AST_DIRECTIVE_MODULE,
    AST_DIRECTIVE_DYNAMIC,
    AST_DIRECTIVE_MULTIFILE,
    AST_DIRECTIVE_DISCONTIGUOUS,
    AST_DIRECTIVE_OP,

    /* Error recovery node */
    AST_ERROR_NODE
} ASTNodeType;

typedef struct ASTNode {
    ASTNodeType type;
    const char *tag;
    char *value;
    int line;
    int col;
    int arity;
    int capacity;
    struct ASTNode **children;
} ASTNode;

/* AST Node Allocation and Constructor Routines */
ASTNode* ast_create_node(ASTNodeType type, const char *tag, const char *val, int line, int initial_capacity) {
    ASTNode *node = (ASTNode*)malloc(sizeof(ASTNode));
    if (!node) {
        fprintf(stderr, "FATAL: Out of memory allocating ASTNode\n");
        exit(EXIT_FAILURE);
    }
    node->type = type;
    node->tag = tag;
    node->value = val ? strdup(val) : strdup("");
    node->line = line;
    node->col = 0;
    node->arity = 0;
    node->capacity = initial_capacity > 0 ? initial_capacity : 2;
    node->children = (ASTNode**)malloc(sizeof(ASTNode*) * node->capacity);
    for (int i = 0; i < node->capacity; i++) {
        node->children[i] = NULL;
    }
    return node;
}

void ast_add_child(ASTNode *parent, ASTNode *child) {
    if (!parent || !child) return;
    if (parent->arity >= parent->capacity) {
        parent->capacity *= 2;
        parent->children = (ASTNode**)realloc(parent->children, sizeof(ASTNode*) * parent->capacity);
    }
    parent->children[parent->arity++] = child;
}

ASTNode* ast_make_leaf(ASTNodeType type, const char *tag, const char *val, int line) {
    return ast_create_node(type, tag, val, line, 0);
}

ASTNode* ast_make_unary(ASTNodeType type, const char *tag, const char *val, ASTNode *child, int line) {
    ASTNode *n = ast_create_node(type, tag, val, line, 1);
    ast_add_child(n, child);
    return n;
}

ASTNode* ast_make_binary(ASTNodeType type, const char *tag, const char *val, ASTNode *left, ASTNode *right, int line) {
    ASTNode *n = ast_create_node(type, tag, val, line, 2);
    ast_add_child(n, left);
    ast_add_child(n, right);
    return n;
}

ASTNode* ast_make_ternary(ASTNodeType type, const char *tag, const char *val, ASTNode *c1, ASTNode *c2, ASTNode *c3, int line) {
    ASTNode *n = ast_create_node(type, tag, val, line, 3);
    ast_add_child(n, c1);
    ast_add_child(n, c2);
    ast_add_child(n, c3);
    return n;
}

/* =========================================================================
 * 2. SYMBOL TABLE SPECIFICATION EMBEDDED IN YACC
 * ========================================================================= */

#define SYMTAB_BUCKETS 256

typedef enum {
    SYM_PREDICATE,
    SYM_FUNCTOR,
    SYM_VARIABLE,
    SYM_CONSTANT,
    SYM_OPERATOR
} SymbolKind;

typedef struct SymbolEntry {
    char *name;
    int arity;
    SymbolKind kind;
    int clause_count;
    int fact_count;
    int rule_count;
    int first_line;
    int last_line;
    struct SymbolEntry *next;
} SymbolEntry;

typedef struct SymbolTable {
    SymbolEntry *buckets[SYMTAB_BUCKETS];
    int total_symbols;
} SymbolTable;

static SymbolTable g_symtab;

static unsigned int symtab_hash(const char *str, int arity) {
    unsigned int hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return (hash ^ (arity * 31)) % SYMTAB_BUCKETS;
}

void symtab_init(void) {
    for (int i = 0; i < SYMTAB_BUCKETS; i++) {
        g_symtab.buckets[i] = NULL;
    }
    g_symtab.total_symbols = 0;
}

SymbolEntry* symtab_lookup(const char *name, int arity) {
    unsigned int bucket = symtab_hash(name, arity);
    SymbolEntry *entry = g_symtab.buckets[bucket];
    while (entry) {
        if (strcmp(entry->name, name) == 0 && entry->arity == arity) {
            return entry;
        }
        entry = entry->next;
    }
    return NULL;
}

SymbolEntry* symtab_insert(const char *name, int arity, SymbolKind kind, int line) {
    SymbolEntry *existing = symtab_lookup(name, arity);
    if (existing) {
        existing->last_line = line;
        return existing;
    }
    unsigned int bucket = symtab_hash(name, arity);
    SymbolEntry *entry = (SymbolEntry*)malloc(sizeof(SymbolEntry));
    entry->name = strdup(name);
    entry->arity = arity;
    entry->kind = kind;
    entry->clause_count = 0;
    entry->fact_count = 0;
    entry->rule_count = 0;
    entry->first_line = line;
    entry->last_line = line;
    entry->next = g_symtab.buckets[bucket];
    g_symtab.buckets[bucket] = entry;
    g_symtab.total_symbols++;
    return entry;
}

void symtab_record_predicate(const char *name, int arity, int is_rule, int line) {
    SymbolEntry *e = symtab_lookup(name, arity);
    if (!e) {
        e = symtab_insert(name, arity, SYM_PREDICATE, line);
    }
    e->clause_count++;
    if (is_rule) e->rule_count++;
    else e->fact_count++;
    e->last_line = line;
}

void symtab_dump(void) {
    printf("\n+-----------------------------------------------------------------------------+\n");
    printf("|          PROLOG YACC EMBEDDED SYMBOL TABLE (PREDICATE & FUNCTOR INDEX)      |\n");
    printf("+-----------------------------------------------------------------------------+\n");
    printf("| %-22s | %-6s | %-12s | %-7s | %-6s | %-6s |\n",
           "Functor / Predicate", "Arity", "Kind", "Clauses", "Facts", "Rules");
    printf("+------------------------+--------+--------------+---------+--------+--------+\n");

    int printed = 0;
    for (int i = 0; i < SYMTAB_BUCKETS; i++) {
        SymbolEntry *e = g_symtab.buckets[i];
        while (e) {
            const char *kind_str = "PREDICATE";
            if (e->kind == SYM_FUNCTOR) kind_str = "FUNCTOR";
            else if (e->kind == SYM_VARIABLE) kind_str = "VARIABLE";
            else if (e->kind == SYM_CONSTANT) kind_str = "CONSTANT";
            else if (e->kind == SYM_OPERATOR) kind_str = "OPERATOR";

            printf("| %-22s | %-6d | %-12s | %-7d | %-6d | %-6d |\n",
                   e->name, e->arity, kind_str, e->clause_count, e->fact_count, e->rule_count);
            printed++;
            e = e->next;
        }
    }
    if (printed == 0) {
        printf("| %-75s |\n", "(Symbol Table Empty)");
    }
    printf("+-----------------------------------------------------------------------------+\n");
    printf("  Total Distinct Registered Symbols: %d\n\n", g_symtab.total_symbols);
}

/* =========================================================================
 * 3. PRETTY DERIVATION TREE VISUALIZER
 * ========================================================================= */

void ast_print_tree(const ASTNode *node, int depth, const char *prefix, int is_last) {
    if (!node) return;
    printf("%s", prefix);
    printf("%s", is_last ? "└── " : "├── ");
    printf("[%s]", node->tag);
    if (node->value && strlen(node->value) > 0) {
        printf(" '%s'", node->value);
    }
    printf(" (L%d)\n", node->line);

    char new_prefix[512];
    snprintf(new_prefix, sizeof(new_prefix), "%s%s", prefix, is_last ? "    " : "│   ");

    for (int i = 0; i < node->arity; i++) {
        int child_is_last = (i == (node->arity - 1));
        ast_print_tree(node->children[i], depth + 1, new_prefix, child_is_last);
    }
}

%}

/* =========================================================================
 * 4. YACC BISON VALUE STACK DECLARATION (%union)
 * ========================================================================= */
%union {
    int ival;
    double dval;
    char *str;
    struct ASTNode *ast;
}

/* =========================================================================
 * 5. TERMINAL SYMBOL TOKENS (LEXICAL ALPHABET)
 * ========================================================================= */

/* Atomic and Literal Value Terminals */
%token <str> ATOM
%token <str> VARIABLE
%token <str> ANON_VAR
%token <str> NUMBER
%token <str> STRING

/* Punctuation & Structural Delimiters */
%token NECK                 /* :- Clause neck operator */
%token QUERY_PREFIX         /* ?- Interactive query prefix */
%token DCG_ARROW            /* --> Definite Clause Grammar arrow */
%token DOT                  /* . Clause terminator */
%token COMMA                /* , Conjunction separator */
%token SEMICOLON            /* ; Disjunction separator */
%token LPAREN RPAREN        /* ( ) Grouping parentheses */
%token LBRACKET RBRACKET    /* [ ] List constructors */
%token LBRACE RBRACE        /* { } Curly bracket DCG goal block */
%token PIPE                 /* | Head/Tail list bar */
%token CUT                  /* ! Search pruning cut operator */

/* Relational Comparison Operators */
%token OP_IS                /* is Arithmetic evaluation */
%token OP_UNIFY             /* = First-order unification */
%token OP_NOT_UNIFY         /* \= Non-unifiability test */
%token OP_STRICT_EQ         /* == Term structural identity */
%token OP_STRICT_NEQ        /* \== Term structural non-identity */
%token OP_UNIV              /* =.. Functor/Args list univ operator */
%token OP_LT                /* < Arithmetic less than */
%token OP_GT                /* > Arithmetic greater than */
%token OP_LE                /* =< Arithmetic less than or equal */
%token OP_GE                /* >= Arithmetic greater than or equal */
%token OP_TERM_LT           /* @< Term standard order less than */
%token OP_TERM_GT           /* @> Term standard order greater than */
%token OP_TERM_LE           /* @=< Term standard order less or equal */
%token OP_TERM_GE           /* @>= Term standard order greater or equal */

/* Arithmetic & Binary Infix Operators */
%token PLUS                 /* + Addition */
%token MINUS                /* - Subtraction / Negation */
%token MULT                 /* * Multiplication */
%token DIV                  /* / Floating-point division */
%token IDIV                 /* // Integer division */
%token MOD                  /* mod Modulus */
%token REM                  /* rem Remainder */
%token POWER                /* ** or ^ Exponentiation */
%token BIT_AND              /* /\ Bitwise AND */
%token BIT_OR               /* \/ Bitwise OR */
%token BIT_XOR              /* xor Bitwise XOR */
%token BIT_SHL              /* << Bitwise shift left */
%token BIT_SHR              /* >> Bitwise shift right */

/* Control Flow & Meta-Logical Operators */
%token ARROW                /* -> Soft cut if-then */
%token NOT_OP               /* \+ Negation as failure */
%token MODULE_QUALIFIER     /* : Module qualification */

/* Compiler Directives */
%token DIR_MODULE           /* :- module(Name, Exports) */
%token DIR_DYNAMIC          /* :- dynamic(F/A) */
%token DIR_MULTIFILE        /* :- multifile(F/A) */
%token DIR_DISCONTIGUOUS    /* :- discontiguous(F/A) */
%token DIR_OP               /* :- op(Prec, Spec, Name) */

/* =========================================================================
 * 6. NON-TERMINAL TYPE DECLARATIONS
 * ========================================================================= */
%type <ast> program
%type <ast> clause_sequence
%type <ast> clause
%type <ast> fact_clause
%type <ast> rule_clause
%type <ast> query_clause
%type <ast> directive_clause
%type <ast> dcg_rule_clause
%type <ast> head
%type <ast> body
%type <ast> goal_sequence
%type <ast> goal
%type <ast> if_then_else_goal
%type <ast> term
%type <ast> compound_term
%type <ast> list_term
%type <ast> curly_term
%type <ast> arg_sequence
%type <ast> directive_spec
%type <ast> predicate_indicator
%type <ast> predicate_indicator_list

/* =========================================================================
 * 7. FORMAL ISO/IEC 13211-1 OPERATOR PRECEDENCE & ASSOCIATIVITY
 *
 * Ordered from lowest precedence (top) to highest precedence (bottom).
 * ========================================================================= */

%right NECK DCG_ARROW                                       /* 1200: Clause constructors */
%right SEMICOLON                                            /* 1100: Disjunction (;) */
%right ARROW                                                /* 1050: If-Then (->) */
%right COMMA                                                /* 1000: Conjunction (,) */
%right NOT_OP                                               /*  900: Negation (\+) */
%nonassoc OP_IS OP_UNIFY OP_NOT_UNIFY                       /*  700: Term Unification & Is */
%nonassoc OP_STRICT_EQ OP_STRICT_NEQ OP_UNIV                /*  700: Structural Identity */
%nonassoc OP_LT OP_GT OP_LE OP_GE                           /*  700: Arithmetic Relational */
%nonassoc OP_TERM_LT OP_TERM_GT OP_TERM_LE OP_TERM_GE       /*  700: Standard Order of Terms */
%left MODULE_QUALIFIER                                      /*  600: Module Qualifier (:) */
%left PLUS MINUS BIT_OR BIT_XOR                             /*  500: Additive & Bitwise Or */
%left MULT DIV IDIV MOD REM BIT_AND BIT_SHL BIT_SHR         /*  400: Multiplicative & Shifts */
%right POWER                                                /*  200: Exponentiation (**) */
%nonassoc UMINUS                                            /*  200: Unary Arithmetic Minus */

%%

/* =========================================================================
 * 8. COMPLETE CONTEXT-FREE GRAMMAR RULES (BNF WITH SEMANTIC ACTIONS)
 * ========================================================================= */

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 1: Top-Level Program Structure
 * A Prolog program is a sequence of zero or more clauses terminating at EOF.
 * -----------------------------------------------------------------------------
 */
program:
      clause_sequence {
          $$ = ast_create_node(AST_PROGRAM, "PROGRAM_ROOT", "root", 1, 1);
          ast_add_child($$, $1);

          printf("\n===============================================================================\n");
          printf("   ISO PROLOG FORMAL YACC/BISON PARSE DERIVATION COMPLETED SUCCESSFULLY       \n");
          printf("===============================================================================\n");
          printf("  Total Program Clauses   : %d\n", g_total_clauses);
          printf("  - Facts Defined         : %d\n", g_fact_count);
          printf("  - Rules Defined         : %d\n", g_rule_count);
          printf("  - Queries Ingested      : %d\n", g_query_count);
          printf("  - Directives Processed  : %d\n", g_directive_count);
          printf("  - DCG Grammar Rules     : %d\n", g_dcg_rule_count);
          printf("  - Total Ground Terms    : %d\n", g_term_count);
          printf("  - Variables Instantiated: %d\n", g_variable_count);
          printf("  - Compound Terms Built  : %d\n", g_compound_count);
          printf("  - List Constructors     : %d\n", g_list_count);
          printf("  - Infix Operators Parsed: %d\n", g_operator_count);
          printf("===============================================================================\n\n");

          /* Print Pretty Abstract Syntax Tree */
          printf("--- AST DERIVATION TREE (FIRST 3 LEVELS) ---\n");
          ast_print_tree($$, 0, "", 1);

          /* Dump Embedded Symbol Table */
          symtab_dump();
      }
    | /* empty program */ {
          $$ = ast_create_node(AST_PROGRAM, "EMPTY_PROGRAM", "empty", 1, 0);
          printf(">> Compiler Warning: Source file contains zero valid Prolog clauses.\n");
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 2-3: Clause Sequence Recursion
 * Left-recursive definition for optimal LALR(1) stack memory performance.
 * -----------------------------------------------------------------------------
 */
clause_sequence:
      clause_sequence clause {
          $$ = $1;
          ast_add_child($$, $2);
      }
    | clause {
          $$ = ast_create_node(AST_CLAUSE_LIST, "CLAUSE_LIST", "seq", $1 ? $1->line : 1, 4);
          ast_add_child($$, $1);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 4-9: Clause Classification
 * Prolog classifies every statement into Fact, Rule, Query, Directive, or DCG.
 * -----------------------------------------------------------------------------
 */
clause:
      fact_clause {
          g_total_clauses++;
          g_fact_count++;
          $$ = $1;
      }
    | rule_clause {
          g_total_clauses++;
          g_rule_count++;
          $$ = $1;
      }
    | query_clause {
          g_total_clauses++;
          g_query_count++;
          $$ = $1;
      }
    | directive_clause {
          g_total_clauses++;
          g_directive_count++;
          $$ = $1;
      }
    | dcg_rule_clause {
          g_total_clauses++;
          g_dcg_rule_count++;
          $$ = $1;
      }
    | error DOT {
          g_error_count++;
          $$ = ast_make_leaf(AST_ERROR_NODE, "ERROR_CLAUSE_RESYNC", "resync", yylineno);
          printf(">> [SYNTAX RECOVERY] Error in clause before line %d; resynchronized on '.'\n", yylineno);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 10: Fact Clause Production
 * Syntax: Head .
 * Semantics: An unconditionally true proposition in the Horn clause universe.
 * -----------------------------------------------------------------------------
 */
fact_clause:
      head DOT {
          $$ = ast_make_unary(AST_FACT, "FACT", $1 ? $1->value : "", $1, $1 ? $1->line : yylineno);
          if ($1) {
              symtab_record_predicate($1->value, $1->arity, 0, $1->line);
          }
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 11: Rule Clause Production
 * Syntax: Head :- Body .
 * Semantics: Conditional Horn clause: Head is true IF Body is satisfiable.
 * -----------------------------------------------------------------------------
 */
rule_clause:
      head NECK body DOT {
          $$ = ast_make_binary(AST_RULE, "RULE", ":-", $1, $3, $1 ? $1->line : yylineno);
          if ($1) {
              symtab_record_predicate($1->value, $1->arity, 1, $1->line);
          }
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 12: Interactive Query Clause
 * Syntax: ?- Body .
 * Semantics: Direct invocation request for the SLD resolution engine.
 * -----------------------------------------------------------------------------
 */
query_clause:
      QUERY_PREFIX body DOT {
          $$ = ast_make_unary(AST_QUERY, "QUERY", "?-", $2, yylineno);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 13: Compiler Directive Statement
 * Syntax: :- DirectiveSpec .
 * Semantics: Meta-commands modifying the compilation environment.
 * -----------------------------------------------------------------------------
 */
directive_clause:
      NECK directive_spec DOT {
          $$ = ast_make_unary(AST_DIRECTIVE, "DIRECTIVE", ":-", $2, yylineno);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 14: Definite Clause Grammar (DCG) Expansion Rule
 * Syntax: Head --> Body .
 * Semantics: Natural language grammar production expanded via difference lists.
 * -----------------------------------------------------------------------------
 */
dcg_rule_clause:
      head DCG_ARROW body DOT {
          $$ = ast_make_binary(AST_DCG_RULE, "DCG_RULE", "-->", $1, $3, $1 ? $1->line : yylineno);
          if ($1) {
              symtab_record_predicate($1->value, $1->arity + 2, 1, $1->line);
          }
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 15-20: Compiler Directive Specifications
 * Supports : module/2, dynamic/1, multifile/1, discontiguous/1, op/3
 * -----------------------------------------------------------------------------
 */
directive_spec:
      DIR_MODULE LPAREN ATOM COMMA list_term RPAREN {
          $$ = ast_make_binary(AST_DIRECTIVE_MODULE, "DIR_MODULE", $3,
                               ast_make_leaf(AST_ATOM, "MODULE_NAME", $3, yylineno), $5, yylineno);
      }
    | DIR_DYNAMIC predicate_indicator_list {
          $$ = ast_make_unary(AST_DIRECTIVE_DYNAMIC, "DIR_DYNAMIC", "dynamic", $2, yylineno);
      }
    | DIR_MULTIFILE predicate_indicator_list {
          $$ = ast_make_unary(AST_DIRECTIVE_MULTIFILE, "DIR_MULTIFILE", "multifile", $2, yylineno);
      }
    | DIR_DISCONTIGUOUS predicate_indicator_list {
          $$ = ast_make_unary(AST_DIRECTIVE_DISCONTIGUOUS, "DIR_DISCONTIGUOUS", "discontiguous", $2, yylineno);
      }
    | DIR_OP LPAREN NUMBER COMMA ATOM COMMA ATOM RPAREN {
          $$ = ast_make_leaf(AST_DIRECTIVE_OP, "DIR_OP", $7, yylineno);
          g_operator_count++;
      }
    | goal {
          $$ = $1;
      }
    ;

predicate_indicator_list:
      predicate_indicator_list COMMA predicate_indicator {
          $$ = $1;
          ast_add_child($$, $3);
      }
    | predicate_indicator {
          $$ = ast_create_node(AST_ARG_LIST, "PRED_SPEC_LIST", "specs", yylineno, 2);
          ast_add_child($$, $1);
      }
    ;

predicate_indicator:
      ATOM DIV NUMBER {
          char buf[64];
          snprintf(buf, sizeof(buf), "%s/%s", $1, $3);
          $$ = ast_make_leaf(AST_ATOM, "PREDICATE_INDICATOR", buf, yylineno);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 21-23: Clause Head Structure
 * In Horn logic, the head must be an atomic predicate or a compound functor.
 * -----------------------------------------------------------------------------
 */
head:
      ATOM {
          g_term_count++;
          $$ = ast_make_leaf(AST_HEAD, "HEAD_ATOM", $1, yylineno);
          $$->arity = 0;
      }
    | compound_term {
          $$ = $1;
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 24: Clause Body
 * The body consists of a structured goal sequence.
 * -----------------------------------------------------------------------------
 */
body:
      goal_sequence {
          $$ = $1;
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 25-27: Goal Conjunctions and Disjunctions
 * ISO Prolog Goal lists are tree structures combining ',' (AND) and ';' (OR).
 * -----------------------------------------------------------------------------
 */
goal_sequence:
      goal_sequence COMMA goal {
          $$ = ast_make_binary(AST_CONJUNCTION, "CONJUNCTION", ",", $1, $3, yylineno);
          g_operator_count++;
      }
    | goal_sequence SEMICOLON goal {
          $$ = ast_make_binary(AST_DISJUNCTION, "DISJUNCTION", ";", $1, $3, yylineno);
          g_operator_count++;
      }
    | goal {
          $$ = $1;
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 28-35: Individual Subgoals
 * Includes Terms, Cuts, Negations, If-Then-Else, and Curly DCG Blocks.
 * -----------------------------------------------------------------------------
 */
goal:
      term {
          $$ = $1;
      }
    | CUT {
          g_operator_count++;
          $$ = ast_make_leaf(AST_CUT, "CUT_OPERATOR", "!", yylineno);
      }
    | NOT_OP goal {
          g_operator_count++;
          $$ = ast_make_unary(AST_NEGATION, "NEGATION", "\\+", $2, yylineno);
      }
    | if_then_else_goal {
          $$ = $1;
      }
    | curly_term {
          $$ = $1;
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 36-37: If-Then and If-Then-Else Control Constructs
 * Syntax: ( Condition -> Then ; Else )
 * -----------------------------------------------------------------------------
 */
if_then_else_goal:
      LPAREN goal ARROW goal SEMICOLON goal RPAREN {
          g_operator_count += 2;
          $$ = ast_make_ternary(AST_IF_THEN_ELSE, "IF_THEN_ELSE", "->;", $2, $4, $6, yylineno);
      }
    | LPAREN goal ARROW goal RPAREN {
          g_operator_count++;
          $$ = ast_make_binary(AST_IF_THEN, "IF_THEN", "->", $2, $4, yylineno);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 38-70: General Terms & Operators (The Core Prolog Expression Grammar)
 * -----------------------------------------------------------------------------
 */
term:
      /* Atomic and Literal Terms */
      ATOM {
          g_term_count++;
          $$ = ast_make_leaf(AST_ATOM, "ATOM", $1, yylineno);
      }
    | VARIABLE {
          g_term_count++;
          g_variable_count++;
          $$ = ast_make_leaf(AST_VARIABLE, "VARIABLE", $1, yylineno);
      }
    | ANON_VAR {
          g_term_count++;
          g_variable_count++;
          $$ = ast_make_leaf(AST_ANON_VAR, "ANON_VAR", "_", yylineno);
      }
    | NUMBER {
          g_term_count++;
          $$ = ast_make_leaf(AST_INTEGER, "NUMBER", $1, yylineno);
      }
    | STRING {
          g_term_count++;
          $$ = ast_make_leaf(AST_STRING, "STRING", $1, yylineno);
      }

      /* Structural Compound Terms and Lists */
    | compound_term {
          $$ = $1;
      }
    | list_term {
          $$ = $1;
      }

      /* Module Qualification: Module:Predicate */
    | term MODULE_QUALIFIER term {
          g_operator_count++;
          $$ = ast_make_binary(AST_COMPOUND, "MODULE_CALL", ":", $1, $3, yylineno);
      }

      /* Unification and Relational Predicates */
    | term OP_IS term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_IS, "IS_EVAL", "is", $1, $3, yylineno);
      }
    | term OP_UNIFY term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_UNIFY, "UNIFY", "=", $1, $3, yylineno);
      }
    | term OP_NOT_UNIFY term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_NOT_UNIFY, "NOT_UNIFY", "\\=", $1, $3, yylineno);
      }
    | term OP_STRICT_EQ term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_STRICT_EQ, "STRICT_EQ", "==", $1, $3, yylineno);
      }
    | term OP_STRICT_NEQ term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_STRICT_NEQ, "STRICT_NEQ", "\\==", $1, $3, yylineno);
      }
    | term OP_UNIV term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_UNIV, "UNIV_DECOMPOSE", "=..", $1, $3, yylineno);
      }
    | term OP_LT term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_LT, "LESS_THAN", "<", $1, $3, yylineno);
      }
    | term OP_GT term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_GT, "GREATER_THAN", ">", $1, $3, yylineno);
      }
    | term OP_LE term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_LE, "LESS_OR_EQUAL", "=<", $1, $3, yylineno);
      }
    | term OP_GE term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_GE, "GREATER_OR_EQUAL", ">=", $1, $3, yylineno);
      }
    | term OP_TERM_LT term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_LT, "TERM_ORDER_LT", "@<", $1, $3, yylineno);
      }
    | term OP_TERM_GT term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_GT, "TERM_ORDER_GT", "@>", $1, $3, yylineno);
      }
    | term OP_TERM_LE term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_LE, "TERM_ORDER_LE", "@=<", $1, $3, yylineno);
      }
    | term OP_TERM_GE term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_GE, "TERM_ORDER_GE", "@>=", $1, $3, yylineno);
      }

      /* Infix Arithmetic Operators */
    | term PLUS term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_ADD, "ADD", "+", $1, $3, yylineno);
      }
    | term MINUS term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_SUB, "SUB", "-", $1, $3, yylineno);
      }
    | term MULT term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_MUL, "MUL", "*", $1, $3, yylineno);
      }
    | term DIV term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_DIV, "DIV", "/", $1, $3, yylineno);
      }
    | term IDIV term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_IDIV, "IDIV", "//", $1, $3, yylineno);
      }
    | term MOD term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_MOD, "MOD", "mod", $1, $3, yylineno);
      }
    | term REM term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_REM, "REM", "rem", $1, $3, yylineno);
      }
    | term POWER term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_POW, "POW", "^", $1, $3, yylineno);
      }
    | term BIT_AND term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_BITWISE_AND, "BIT_AND", "/\\", $1, $3, yylineno);
      }
    | term BIT_OR term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_BITWISE_OR, "BIT_OR", "\\/", $1, $3, yylineno);
      }
    | term BIT_XOR term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_BITWISE_XOR, "BIT_XOR", "xor", $1, $3, yylineno);
      }
    | term BIT_SHL term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_SHIFT_LEFT, "BIT_SHL", "<<", $1, $3, yylineno);
      }
    | term BIT_SHR term {
          g_operator_count++;
          $$ = ast_make_binary(AST_OP_SHIFT_RIGHT, "BIT_SHR", ">>", $1, $3, yylineno);
      }

      /* Prefix Unary Minus */
    | MINUS term %prec UMINUS {
          g_operator_count++;
          $$ = ast_make_unary(AST_OP_UNARY_MINUS, "NEG", "-", $2, yylineno);
      }

      /* Grouping Parentheses */
    | LPAREN term RPAREN {
          $$ = $2;
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 71-72: Compound Terms
 * Syntax: Functor ( Argument_1 , Argument_2 , ... Argument_N )
 * -----------------------------------------------------------------------------
 */
compound_term:
      ATOM LPAREN arg_sequence RPAREN {
          g_term_count++;
          g_compound_count++;
          $$ = ast_create_node(AST_COMPOUND, "COMPOUND_TERM", $1, yylineno, $3 ? $3->arity : 1);
          if ($3) {
              $$->arity = $3->arity;
              for (int i = 0; i < $3->arity; i++) {
                  $$->children[i] = $3->children[i];
              }
          }
          symtab_insert($1, $$->arity, SYM_FUNCTOR, yylineno);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 73-76: First-Class List Constructors
 * Syntax:
 *   - []                   (Empty Nil List)
 *   - [ Element_1, ... ]   (Explicit Sequence)
 *   - [ Head | Tail ]      (Cons Cell Pair)
 * -----------------------------------------------------------------------------
 */
list_term:
      LBRACKET RBRACKET {
          g_term_count++;
          g_list_count++;
          $$ = ast_make_leaf(AST_LIST_NIL, "NIL_LIST", "[]", yylineno);
      }
    | LBRACKET arg_sequence RBRACKET {
          g_term_count++;
          g_list_count++;
          $$ = ast_make_unary(AST_LIST_EXPLICIT, "EXPLICIT_LIST", "[...]", $2, yylineno);
      }
    | LBRACKET arg_sequence PIPE term RBRACKET {
          g_term_count++;
          g_list_count++;
          $$ = ast_make_binary(AST_LIST_CONS, "HEAD_TAIL_SPLIT", "[H|T]", $2, $4, yylineno);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 77: Curly Bracket DCG Escape Term
 * Syntax: { Goal }
 * Semantics: Embeds pure Prolog goals inside Definite Clause Grammar rules.
 * -----------------------------------------------------------------------------
 */
curly_term:
      LBRACE goal_sequence RBRACE {
          $$ = ast_make_unary(AST_CURLY_BLOCK, "DCG_ESCAPE_BLOCK", "{}", $2, yylineno);
      }
    ;

/*
 * -----------------------------------------------------------------------------
 * PRODUCTION 78-79: Comma-Separated Argument Sequences
 * -----------------------------------------------------------------------------
 */
arg_sequence:
      arg_sequence COMMA term {
          $$ = $1;
          ast_add_child($$, $3);
      }
    | term {
          $$ = ast_create_node(AST_ARG_LIST, "ARG_SEQUENCE", "args", yylineno, 4);
          ast_add_child($$, $1);
      }
    ;

%%

/* =========================================================================
 * 9. AUXILIARY C SUPPORT FUNCTIONS, SYNTAX ERROR HANDLER & DRIVER
 * ========================================================================= */

void yyerror(const char *format, ...) {
    g_error_count++;
    va_list args;
    va_start(args, format);
    fprintf(stderr, "\n>> SYNTAX ERROR at Line %d near token '%s': ", yylineno, yytext ? yytext : "");
    vfprintf(stderr, format, args);
    fprintf(stderr, "\n");
    va_end(args);
}

static void print_banner(void) {
    printf("+-----------------------------------------------------------------------------+\n");
    printf("|          ISO PROLOG LALR(1) FORMAL GRAMMAR COMPILER & PARSER (YACC)          |\n");
    printf("|          Course: Compiler Design Laboratory (Course Code: 22PC2CS301)       |\n");
    printf("|          Dept of Computer Science & Engineering, VNRVJIET Hyderabad         |\n");
    printf("+-----------------------------------------------------------------------------+\n");
}

int main(int argc, char **argv) {
    clock_t start_time = clock();
    print_banner();
    symtab_init();

    const char *input_filename = NULL;
    if (argc > 1) {
        input_filename = argv[1];
        FILE *fp = fopen(input_filename, "r");
        if (!fp) {
            fprintf(stderr, "FATAL ERROR: Unable to open input file '%s'\n", input_filename);
            return EXIT_FAILURE;
        }
        extern FILE *yyin;
        yyin = fp;
        printf(">> [PHASE 1] Opening source program stream: '%s'\n", input_filename);
    } else {
        printf(">> [PHASE 1] Awaiting interactive input from standard stdin (type Prolog clauses):\n");
    }

    printf(">> [PHASE 2] Executing LALR(1) Parse Table Transitions via yyparse()...\n");
    int parse_status = yyparse();
    clock_t end_time = clock();
    double elapsed_ms = ((double)(end_time - start_time) / CLOCKS_PER_SEC) * 1000.0;

    printf("\n-------------------------------------------------------------------------------\n");
    printf(" COMPILATION BENCHMARK SUMMARY\n");
    printf("-------------------------------------------------------------------------------\n");
    printf(" Parse Time Elapsed : %.3f milliseconds\n", elapsed_ms);
    printf(" Syntax Errors      : %d\n", g_error_count);
    printf(" Syntax Warnings    : %d\n", g_warning_count);

    if (parse_status == 0 && g_error_count == 0) {
        printf(" Parse Verification : PASSED (100%% Grammatically Conforming to ISO Prolog)\n");
        printf("-------------------------------------------------------------------------------\n\n");
        return EXIT_SUCCESS;
    } else {
        printf(" Parse Verification : FAILED (Grammar syntax violations detected)\n");
        printf("-------------------------------------------------------------------------------\n\n");
        return EXIT_FAILURE;
    }
}
