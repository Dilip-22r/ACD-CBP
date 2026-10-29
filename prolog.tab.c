/* A Bison parser, made by GNU Bison 2.4.2.  */

/* Skeleton implementation for Bison's Yacc-like parsers in C
   
      Copyright (C) 1984, 1989-1990, 2000-2006, 2009-2010 Free Software
   Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "2.4.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1

/* Using locations.  */
#define YYLSP_NEEDED 0



/* Copy the first part of user declarations.  */

/* Line 189 of yacc.c  */
#line 1 "prolog.y"

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



/* Line 189 of yacc.c  */
#line 410 "prolog.tab.c"

/* Enabling traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* Enabling the token table.  */
#ifndef YYTOKEN_TABLE
# define YYTOKEN_TABLE 0
#endif


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     ATOM = 258,
     VARIABLE = 259,
     ANON_VAR = 260,
     NUMBER = 261,
     STRING = 262,
     NECK = 263,
     QUERY_PREFIX = 264,
     DCG_ARROW = 265,
     DOT = 266,
     COMMA = 267,
     SEMICOLON = 268,
     LPAREN = 269,
     RPAREN = 270,
     LBRACKET = 271,
     RBRACKET = 272,
     LBRACE = 273,
     RBRACE = 274,
     PIPE = 275,
     CUT = 276,
     OP_IS = 277,
     OP_UNIFY = 278,
     OP_NOT_UNIFY = 279,
     OP_STRICT_EQ = 280,
     OP_STRICT_NEQ = 281,
     OP_UNIV = 282,
     OP_LT = 283,
     OP_GT = 284,
     OP_LE = 285,
     OP_GE = 286,
     OP_TERM_LT = 287,
     OP_TERM_GT = 288,
     OP_TERM_LE = 289,
     OP_TERM_GE = 290,
     PLUS = 291,
     MINUS = 292,
     MULT = 293,
     DIV = 294,
     IDIV = 295,
     MOD = 296,
     REM = 297,
     POWER = 298,
     BIT_AND = 299,
     BIT_OR = 300,
     BIT_XOR = 301,
     BIT_SHL = 302,
     BIT_SHR = 303,
     ARROW = 304,
     NOT_OP = 305,
     MODULE_QUALIFIER = 306,
     DIR_MODULE = 307,
     DIR_DYNAMIC = 308,
     DIR_MULTIFILE = 309,
     DIR_DISCONTIGUOUS = 310,
     DIR_OP = 311,
     UMINUS = 312
   };
#endif



#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 214 of yacc.c  */
#line 341 "prolog.y"

    int ival;
    double dval;
    char *str;
    struct ASTNode *ast;



/* Line 214 of yacc.c  */
#line 512 "prolog.tab.c"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif


/* Copy the second part of user declarations.  */


/* Line 264 of yacc.c  */
#line 524 "prolog.tab.c"

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#elif (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
typedef signed char yytype_int8;
#else
typedef short int yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(e) ((void) (e))
#else
# define YYUSE(e) /* empty */
#endif

/* Identity function, used to suppress warnings about constant conditions.  */
#ifndef lint
# define YYID(n) (n)
#else
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static int
YYID (int yyi)
#else
static int
YYID (yyi)
    int yyi;
#endif
{
  return yyi;
}
#endif

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#     ifndef _STDLIB_H
#      define _STDLIB_H 1
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's `empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (YYID (0))
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined _STDLIB_H \
       && ! ((defined YYMALLOC || defined malloc) \
	     && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef _STDLIB_H
#    define _STDLIB_H 1
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
	 || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

/* Copy COUNT objects from FROM to TO.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(To, From, Count) \
      __builtin_memcpy (To, From, (Count) * sizeof (*(From)))
#  else
#   define YYCOPY(To, From, Count)		\
      do					\
	{					\
	  YYSIZE_T yyi;				\
	  for (yyi = 0; yyi < (Count); yyi++)	\
	    (To)[yyi] = (From)[yyi];		\
	}					\
      while (YYID (0))
#  endif
# endif

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)				\
    do									\
      {									\
	YYSIZE_T yynewbytes;						\
	YYCOPY (&yyptr->Stack_alloc, Stack, yysize);			\
	Stack = &yyptr->Stack_alloc;					\
	yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
	yyptr += yynewbytes / sizeof (*yyptr);				\
      }									\
    while (YYID (0))

#endif

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  43
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   363

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  58
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  22
/* YYNRULES -- Number of rules.  */
#define YYNRULES  82
/* YYNRULES -- Number of states.  */
#define YYNSTATES  161

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   312

#define YYTRANSLATE(YYX)						\
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[YYLEX] -- Bison symbol number corresponding to YYLEX.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint16 yyprhs[] =
{
       0,     0,     3,     5,     6,     9,    11,    13,    15,    17,
      19,    21,    24,    27,    32,    36,    40,    45,    52,    55,
      58,    61,    70,    72,    76,    78,    82,    84,    86,    88,
      92,    96,    98,   100,   102,   105,   107,   109,   117,   123,
     125,   127,   129,   131,   133,   135,   137,   141,   145,   149,
     153,   157,   161,   165,   169,   173,   177,   181,   185,   189,
     193,   197,   201,   205,   209,   213,   217,   221,   225,   229,
     233,   237,   241,   245,   249,   252,   256,   261,   264,   268,
     274,   278,   282
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int8 yyrhs[] =
{
      59,     0,    -1,    60,    -1,    -1,    60,    61,    -1,    61,
      -1,    62,    -1,    63,    -1,    64,    -1,    65,    -1,    66,
      -1,     1,    11,    -1,    70,    11,    -1,    70,     8,    71,
      11,    -1,     9,    71,    11,    -1,     8,    67,    11,    -1,
      70,    10,    71,    11,    -1,    52,    14,     3,    12,    77,
      15,    -1,    53,    68,    -1,    54,    68,    -1,    55,    68,
      -1,    56,    14,     6,    12,     3,    12,     3,    15,    -1,
      73,    -1,    68,    12,    69,    -1,    69,    -1,     3,    39,
       6,    -1,     3,    -1,    76,    -1,    72,    -1,    72,    12,
      73,    -1,    72,    13,    73,    -1,    73,    -1,    75,    -1,
      21,    -1,    50,    73,    -1,    74,    -1,    78,    -1,    14,
      73,    49,    73,    13,    73,    15,    -1,    14,    73,    49,
      73,    15,    -1,     3,    -1,     4,    -1,     5,    -1,     6,
      -1,     7,    -1,    76,    -1,    77,    -1,    75,    51,    75,
      -1,    75,    22,    75,    -1,    75,    23,    75,    -1,    75,
      24,    75,    -1,    75,    25,    75,    -1,    75,    26,    75,
      -1,    75,    27,    75,    -1,    75,    28,    75,    -1,    75,
      29,    75,    -1,    75,    30,    75,    -1,    75,    31,    75,
      -1,    75,    32,    75,    -1,    75,    33,    75,    -1,    75,
      34,    75,    -1,    75,    35,    75,    -1,    75,    36,    75,
      -1,    75,    37,    75,    -1,    75,    38,    75,    -1,    75,
      39,    75,    -1,    75,    40,    75,    -1,    75,    41,    75,
      -1,    75,    42,    75,    -1,    75,    43,    75,    -1,    75,
      44,    75,    -1,    75,    45,    75,    -1,    75,    46,    75,
      -1,    75,    47,    75,    -1,    75,    48,    75,    -1,    37,
      75,    -1,    14,    75,    15,    -1,     3,    14,    79,    15,
      -1,    16,    17,    -1,    16,    79,    17,    -1,    16,    79,
      20,    75,    17,    -1,    18,    72,    19,    -1,    79,    12,
      75,    -1,    75,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   474,   474,   501,   514,   518,   531,   536,   541,   546,
     551,   556,   571,   587,   603,   616,   629,   644,   648,   651,
     654,   657,   661,   667,   671,   678,   692,   697,   709,   721,
     725,   729,   741,   744,   748,   752,   755,   767,   771,   784,
     788,   793,   798,   802,   808,   811,   816,   822,   826,   830,
     834,   838,   842,   846,   850,   854,   858,   862,   866,   870,
     874,   880,   884,   888,   892,   896,   900,   904,   908,   912,
     916,   920,   924,   928,   934,   940,   952,   976,   981,   986,
    1001,  1012,  1016
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "ATOM", "VARIABLE", "ANON_VAR", "NUMBER",
  "STRING", "NECK", "QUERY_PREFIX", "DCG_ARROW", "DOT", "COMMA",
  "SEMICOLON", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "LBRACE",
  "RBRACE", "PIPE", "CUT", "OP_IS", "OP_UNIFY", "OP_NOT_UNIFY",
  "OP_STRICT_EQ", "OP_STRICT_NEQ", "OP_UNIV", "OP_LT", "OP_GT", "OP_LE",
  "OP_GE", "OP_TERM_LT", "OP_TERM_GT", "OP_TERM_LE", "OP_TERM_GE", "PLUS",
  "MINUS", "MULT", "DIV", "IDIV", "MOD", "REM", "POWER", "BIT_AND",
  "BIT_OR", "BIT_XOR", "BIT_SHL", "BIT_SHR", "ARROW", "NOT_OP",
  "MODULE_QUALIFIER", "DIR_MODULE", "DIR_DYNAMIC", "DIR_MULTIFILE",
  "DIR_DISCONTIGUOUS", "DIR_OP", "UMINUS", "$accept", "program",
  "clause_sequence", "clause", "fact_clause", "rule_clause",
  "query_clause", "directive_clause", "dcg_rule_clause", "directive_spec",
  "predicate_indicator_list", "predicate_indicator", "head", "body",
  "goal_sequence", "goal", "if_then_else_goal", "term", "compound_term",
  "list_term", "curly_term", "arg_sequence", 0
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[YYLEX-NUM] -- Internal token number corresponding to
   token YYLEX-NUM.  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    58,    59,    59,    60,    60,    61,    61,    61,    61,
      61,    61,    62,    63,    64,    65,    66,    67,    67,    67,
      67,    67,    67,    68,    68,    69,    70,    70,    71,    72,
      72,    72,    73,    73,    73,    73,    73,    74,    74,    75,
      75,    75,    75,    75,    75,    75,    75,    75,    75,    75,
      75,    75,    75,    75,    75,    75,    75,    75,    75,    75,
      75,    75,    75,    75,    75,    75,    75,    75,    75,    75,
      75,    75,    75,    75,    75,    75,    76,    77,    77,    77,
      78,    79,    79
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     0,     2,     1,     1,     1,     1,     1,
       1,     2,     2,     4,     3,     3,     4,     6,     2,     2,
       2,     8,     1,     3,     1,     3,     1,     1,     1,     3,
       3,     1,     1,     1,     2,     1,     1,     7,     5,     1,
       1,     1,     1,     1,     1,     1,     3,     3,     3,     3,
       3,     3,     3,     3,     3,     3,     3,     3,     3,     3,
       3,     3,     3,     3,     3,     3,     3,     3,     3,     3,
       3,     3,     3,     3,     2,     3,     4,     2,     3,     5,
       3,     3,     1
};

/* YYDEFACT[STATE-NAME] -- Default rule to reduce with in state
   STATE-NUM when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       0,     0,    26,     0,     0,     0,     0,     5,     6,     7,
       8,     9,    10,     0,    27,    11,     0,    39,    40,    41,
      42,    43,     0,     0,     0,    33,     0,     0,     0,     0,
       0,     0,     0,     0,    22,    35,    32,    44,    45,    36,
       0,    28,    31,     1,     4,     0,     0,    12,     0,    82,
       0,     0,    32,    77,     0,     0,    74,    34,     0,     0,
      18,    24,    19,    20,     0,    15,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,    14,     0,     0,     0,     0,     0,
       0,    76,     0,    75,    78,     0,    80,     0,     0,     0,
       0,    47,    48,    49,    50,    51,    52,    53,    54,    55,
      56,    57,    58,    59,    60,    61,    62,    63,    64,    65,
      66,    67,    68,    69,    70,    71,    72,    73,    46,    29,
      30,    13,    16,    81,     0,     0,     0,    25,    23,     0,
       0,    38,    79,     0,     0,     0,    17,     0,    37,     0,
      21
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
      -1,     5,     6,     7,     8,     9,    10,    11,    12,    33,
      60,    61,    13,    40,    41,    42,    35,    36,    37,    38,
      39,    50
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -16
static const yytype_int16 yypact[] =
{
      37,    -2,     0,    98,    -1,    12,    79,   -16,   -16,   -16,
     -16,   -16,   -16,    73,   -16,   -16,   215,     0,   -16,   -16,
     -16,   -16,    -1,   104,    -1,   -16,   215,    -1,    18,    40,
      40,    40,    36,    75,   -16,   -16,   231,   -16,   -16,   -16,
      87,    82,   -16,   -16,   -16,    -1,    -1,   -16,   215,   231,
       6,    57,   134,   -16,    27,    29,   -16,   -16,    97,    74,
     103,   -16,   103,   103,   111,   -16,   215,   215,   215,   215,
     215,   215,   215,   215,   215,   215,   215,   215,   215,   215,
     215,   215,   215,   215,   215,   215,   215,   215,   215,   215,
     215,   215,   215,   215,   -16,    -1,    -1,   125,   126,   134,
     215,   -16,    -1,   -16,   -16,   215,   -16,   127,   132,    40,
     128,   261,   261,   261,   288,   288,   288,   312,   312,   312,
     312,   200,   200,   200,   200,   -13,   -13,    99,    99,    99,
      99,    99,    99,    99,   -13,   -13,    99,    99,    86,   -16,
     -16,   -16,   -16,   231,    76,   166,   129,   -16,   -16,   140,
      -1,   -16,   -16,   131,   143,   169,   -16,   141,   -16,   171,
     -16
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
     -16,   -16,   -16,   181,   -16,   -16,   -16,   -16,   -16,   -16,
      -8,   106,   -16,    51,   192,    -3,   -16,   -15,    10,    77,
     -16,   201
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If zero, do what YYDEFACT says.
   If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -4
static const yytype_int16 yytable[] =
{
      34,    49,    17,    18,    19,    20,    21,    52,    49,    15,
      14,    56,    43,    22,    16,    23,    14,    24,   100,    51,
      25,   101,    62,    63,    57,    82,    83,    84,    85,    86,
      87,    88,    58,    99,    91,    92,    26,    -3,     1,   100,
       2,    95,    96,    59,   104,     3,     4,   105,   106,    27,
      64,   111,   112,   113,   114,   115,   116,   117,   118,   119,
     120,   121,   122,   123,   124,   125,   126,   127,   128,   129,
     130,   131,   132,   133,   134,   135,   136,   137,   138,    -2,
       1,    45,     2,    46,    47,   143,    65,     3,     4,   150,
     145,   151,   139,   140,    95,    96,    97,    98,    94,   144,
     107,    17,    18,    19,    20,    21,   102,    17,    18,    19,
      20,    21,    22,   108,    23,   109,    24,   110,    48,    25,
      23,    53,    80,    81,    82,    83,    84,    85,    86,    87,
      88,    89,    90,    91,    92,    26,   141,   142,   147,   146,
     149,    26,    87,   154,   159,    23,   156,   155,    27,   103,
      28,    29,    30,    31,    32,   157,    66,    67,    68,    69,
      70,    71,    72,    73,    74,    75,    76,    77,    78,    79,
      80,    81,    82,    83,    84,    85,    86,    87,    88,    89,
      90,    91,    92,   152,   158,    93,   160,    44,    66,    67,
      68,    69,    70,    71,    72,    73,    74,    75,    76,    77,
      78,    79,    80,    81,    82,    83,    84,    85,    86,    87,
      88,    89,    90,    91,    92,   148,    55,    93,    17,    18,
      19,    20,    21,   153,    54,     0,     0,     0,     0,    48,
       0,    23,    -4,    -4,    -4,    -4,    80,    81,    82,    83,
      84,    85,    86,    87,    88,    89,    90,    91,    92,     0,
       0,    93,    26,    66,    67,    68,    69,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
       0,     0,    93,    -4,    -4,    -4,    69,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
       0,     0,    93,    -4,    -4,    -4,    72,    73,    74,    75,
      76,    77,    78,    79,    80,    81,    82,    83,    84,    85,
      86,    87,    88,    89,    90,    91,    92,     0,     0,    93,
      -4,    -4,    -4,    -4,    76,    77,    78,    79,    80,    81,
      82,    83,    84,    85,    86,    87,    88,    89,    90,    91,
      92,     0,     0,    93
};

static const yytype_int16 yycheck[] =
{
       3,    16,     3,     4,     5,     6,     7,    22,    23,    11,
       0,    26,     0,    14,    14,    16,     6,    18,    12,    22,
      21,    15,    30,    31,    27,    38,    39,    40,    41,    42,
      43,    44,    14,    48,    47,    48,    37,     0,     1,    12,
       3,    12,    13,     3,    17,     8,     9,    20,    19,    50,
      14,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,     0,
       1,     8,     3,    10,    11,   100,    11,     8,     9,    13,
     105,    15,    95,    96,    12,    13,    45,    46,    11,   102,
       3,     3,     4,     5,     6,     7,    49,     3,     4,     5,
       6,     7,    14,    39,    16,    12,    18,     6,    14,    21,
      16,    17,    36,    37,    38,    39,    40,    41,    42,    43,
      44,    45,    46,    47,    48,    37,    11,    11,     6,    12,
      12,    37,    43,     3,     3,    16,    15,   150,    50,    15,
      52,    53,    54,    55,    56,    12,    22,    23,    24,    25,
      26,    27,    28,    29,    30,    31,    32,    33,    34,    35,
      36,    37,    38,    39,    40,    41,    42,    43,    44,    45,
      46,    47,    48,    17,    15,    51,    15,     6,    22,    23,
      24,    25,    26,    27,    28,    29,    30,    31,    32,    33,
      34,    35,    36,    37,    38,    39,    40,    41,    42,    43,
      44,    45,    46,    47,    48,   109,    24,    51,     3,     4,
       5,     6,     7,   146,    23,    -1,    -1,    -1,    -1,    14,
      -1,    16,    32,    33,    34,    35,    36,    37,    38,    39,
      40,    41,    42,    43,    44,    45,    46,    47,    48,    -1,
      -1,    51,    37,    22,    23,    24,    25,    26,    27,    28,
      29,    30,    31,    32,    33,    34,    35,    36,    37,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    47,    48,
      -1,    -1,    51,    22,    23,    24,    25,    26,    27,    28,
      29,    30,    31,    32,    33,    34,    35,    36,    37,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    47,    48,
      -1,    -1,    51,    25,    26,    27,    28,    29,    30,    31,
      32,    33,    34,    35,    36,    37,    38,    39,    40,    41,
      42,    43,    44,    45,    46,    47,    48,    -1,    -1,    51,
      28,    29,    30,    31,    32,    33,    34,    35,    36,    37,
      38,    39,    40,    41,    42,    43,    44,    45,    46,    47,
      48,    -1,    -1,    51
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     1,     3,     8,     9,    59,    60,    61,    62,    63,
      64,    65,    66,    70,    76,    11,    14,     3,     4,     5,
       6,     7,    14,    16,    18,    21,    37,    50,    52,    53,
      54,    55,    56,    67,    73,    74,    75,    76,    77,    78,
      71,    72,    73,     0,    61,     8,    10,    11,    14,    75,
      79,    73,    75,    17,    79,    72,    75,    73,    14,     3,
      68,    69,    68,    68,    14,    11,    22,    23,    24,    25,
      26,    27,    28,    29,    30,    31,    32,    33,    34,    35,
      36,    37,    38,    39,    40,    41,    42,    43,    44,    45,
      46,    47,    48,    51,    11,    12,    13,    71,    71,    75,
      12,    15,    49,    15,    17,    20,    19,     3,    39,    12,
       6,    75,    75,    75,    75,    75,    75,    75,    75,    75,
      75,    75,    75,    75,    75,    75,    75,    75,    75,    75,
      75,    75,    75,    75,    75,    75,    75,    75,    75,    73,
      73,    11,    11,    75,    73,    75,    12,     6,    69,    12,
      13,    15,    17,    77,     3,    73,    15,    12,    15,     3,
      15
};

#define yyerrok		(yyerrstatus = 0)
#define yyclearin	(yychar = YYEMPTY)
#define YYEMPTY		(-2)
#define YYEOF		0

#define YYACCEPT	goto yyacceptlab
#define YYABORT		goto yyabortlab
#define YYERROR		goto yyerrorlab


/* Like YYERROR except do call yyerror.  This remains here temporarily
   to ease the transition to the new meaning of YYERROR, for GCC.
   Once GCC version 2 has supplanted version 1, this can go.  However,
   YYFAIL appears to be in use.  Nevertheless, it is formally deprecated
   in Bison 2.4.2's NEWS entry, where a plan to phase it out is
   discussed.  */

#define YYFAIL		goto yyerrlab
#if defined YYFAIL
  /* This is here to suppress warnings from the GCC cpp's
     -Wunused-macros.  Normally we don't worry about that warning, but
     some users do, and we want to make it easy for users to remove
     YYFAIL uses, which will produce warnings from Bison 2.5.  */
#endif

#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)					\
do								\
  if (yychar == YYEMPTY && yylen == 1)				\
    {								\
      yychar = (Token);						\
      yylval = (Value);						\
      yytoken = YYTRANSLATE (yychar);				\
      YYPOPSTACK (1);						\
      goto yybackup;						\
    }								\
  else								\
    {								\
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;							\
    }								\
while (YYID (0))


#define YYTERROR	1
#define YYERRCODE	256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#define YYRHSLOC(Rhs, K) ((Rhs)[K])
#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)				\
    do									\
      if (YYID (N))                                                    \
	{								\
	  (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;	\
	  (Current).first_column = YYRHSLOC (Rhs, 1).first_column;	\
	  (Current).last_line    = YYRHSLOC (Rhs, N).last_line;		\
	  (Current).last_column  = YYRHSLOC (Rhs, N).last_column;	\
	}								\
      else								\
	{								\
	  (Current).first_line   = (Current).last_line   =		\
	    YYRHSLOC (Rhs, 0).last_line;				\
	  (Current).first_column = (Current).last_column =		\
	    YYRHSLOC (Rhs, 0).last_column;				\
	}								\
    while (YYID (0))
#endif


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
#  define YY_LOCATION_PRINT(File, Loc)			\
     fprintf (File, "%d.%d-%d.%d",			\
	      (Loc).first_line, (Loc).first_column,	\
	      (Loc).last_line,  (Loc).last_column)
# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


/* YYLEX -- calling `yylex' with the right arguments.  */

#ifdef YYLEX_PARAM
# define YYLEX yylex (YYLEX_PARAM)
#else
# define YYLEX yylex ()
#endif

/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)			\
do {						\
  if (yydebug)					\
    YYFPRINTF Args;				\
} while (YYID (0))

# define YY_SYMBOL_PRINT(Title, Type, Value, Location)			  \
do {									  \
  if (yydebug)								  \
    {									  \
      YYFPRINTF (stderr, "%s ", Title);					  \
      yy_symbol_print (stderr,						  \
		  Type, Value); \
      YYFPRINTF (stderr, "\n");						  \
    }									  \
} while (YYID (0))


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# else
  YYUSE (yyoutput);
# endif
  switch (yytype)
    {
      default:
	break;
    }
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
#else
static void
yy_stack_print (yybottom, yytop)
    yytype_int16 *yybottom;
    yytype_int16 *yytop;
#endif
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)				\
do {								\
  if (yydebug)							\
    yy_stack_print ((Bottom), (Top));				\
} while (YYID (0))


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_reduce_print (YYSTYPE *yyvsp, int yyrule)
#else
static void
yy_reduce_print (yyvsp, yyrule)
    YYSTYPE *yyvsp;
    int yyrule;
#endif
{
  int yynrhs = yyr2[yyrule];
  int yyi;
  unsigned long int yylno = yyrline[yyrule];
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
	     yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr, yyrhs[yyprhs[yyrule] + yyi],
		       &(yyvsp[(yyi + 1) - (yynrhs)])
		       		       );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, Rule); \
} while (YYID (0))

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef	YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif



#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static YYSIZE_T
yystrlen (const char *yystr)
#else
static YYSIZE_T
yystrlen (yystr)
    const char *yystr;
#endif
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static char *
yystpcpy (char *yydest, const char *yysrc)
#else
static char *
yystpcpy (yydest, yysrc)
    char *yydest;
    const char *yysrc;
#endif
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
	switch (*++yyp)
	  {
	  case '\'':
	  case ',':
	    goto do_not_strip_quotes;

	  case '\\':
	    if (*++yyp != '\\')
	      goto do_not_strip_quotes;
	    /* Fall through.  */
	  default:
	    if (yyres)
	      yyres[yyn] = *yyp;
	    yyn++;
	    break;

	  case '"':
	    if (yyres)
	      yyres[yyn] = '\0';
	    return yyn;
	  }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into YYRESULT an error message about the unexpected token
   YYCHAR while in state YYSTATE.  Return the number of bytes copied,
   including the terminating null byte.  If YYRESULT is null, do not
   copy anything; just return the number of bytes that would be
   copied.  As a special case, return 0 if an ordinary "syntax error"
   message will do.  Return YYSIZE_MAXIMUM if overflow occurs during
   size calculation.  */
static YYSIZE_T
yysyntax_error (char *yyresult, int yystate, int yychar)
{
  int yyn = yypact[yystate];

  if (! (YYPACT_NINF < yyn && yyn <= YYLAST))
    return 0;
  else
    {
      int yytype = YYTRANSLATE (yychar);
      YYSIZE_T yysize0 = yytnamerr (0, yytname[yytype]);
      YYSIZE_T yysize = yysize0;
      YYSIZE_T yysize1;
      int yysize_overflow = 0;
      enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
      char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
      int yyx;

# if 0
      /* This is so xgettext sees the translatable formats that are
	 constructed on the fly.  */
      YY_("syntax error, unexpected %s");
      YY_("syntax error, unexpected %s, expecting %s");
      YY_("syntax error, unexpected %s, expecting %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s");
# endif
      char *yyfmt;
      char const *yyf;
      static char const yyunexpected[] = "syntax error, unexpected %s";
      static char const yyexpecting[] = ", expecting %s";
      static char const yyor[] = " or %s";
      char yyformat[sizeof yyunexpected
		    + sizeof yyexpecting - 1
		    + ((YYERROR_VERBOSE_ARGS_MAXIMUM - 2)
		       * (sizeof yyor - 1))];
      char const *yyprefix = yyexpecting;

      /* Start YYX at -YYN if negative to avoid negative indexes in
	 YYCHECK.  */
      int yyxbegin = yyn < 0 ? -yyn : 0;

      /* Stay within bounds of both yycheck and yytname.  */
      int yychecklim = YYLAST - yyn + 1;
      int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
      int yycount = 1;

      yyarg[0] = yytname[yytype];
      yyfmt = yystpcpy (yyformat, yyunexpected);

      for (yyx = yyxbegin; yyx < yyxend; ++yyx)
	if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR)
	  {
	    if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
	      {
		yycount = 1;
		yysize = yysize0;
		yyformat[sizeof yyunexpected - 1] = '\0';
		break;
	      }
	    yyarg[yycount++] = yytname[yyx];
	    yysize1 = yysize + yytnamerr (0, yytname[yyx]);
	    yysize_overflow |= (yysize1 < yysize);
	    yysize = yysize1;
	    yyfmt = yystpcpy (yyfmt, yyprefix);
	    yyprefix = yyor;
	  }

      yyf = YY_(yyformat);
      yysize1 = yysize + yystrlen (yyf);
      yysize_overflow |= (yysize1 < yysize);
      yysize = yysize1;

      if (yysize_overflow)
	return YYSIZE_MAXIMUM;

      if (yyresult)
	{
	  /* Avoid sprintf, as that infringes on the user's name space.
	     Don't have undefined behavior even if the translation
	     produced a string with the wrong number of "%s"s.  */
	  char *yyp = yyresult;
	  int yyi = 0;
	  while ((*yyp = *yyf) != '\0')
	    {
	      if (*yyp == '%' && yyf[1] == 's' && yyi < yycount)
		{
		  yyp += yytnamerr (yyp, yyarg[yyi++]);
		  yyf += 2;
		}
	      else
		{
		  yyp++;
		  yyf++;
		}
	    }
	}
      return yysize;
    }
}
#endif /* YYERROR_VERBOSE */


/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
#else
static void
yydestruct (yymsg, yytype, yyvaluep)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
#endif
{
  YYUSE (yyvaluep);

  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  switch (yytype)
    {

      default:
	break;
    }
}

/* Prevent warnings from -Wmissing-prototypes.  */
#ifdef YYPARSE_PARAM
#if defined __STDC__ || defined __cplusplus
int yyparse (void *YYPARSE_PARAM);
#else
int yyparse ();
#endif
#else /* ! YYPARSE_PARAM */
#if defined __STDC__ || defined __cplusplus
int yyparse (void);
#else
int yyparse ();
#endif
#endif /* ! YYPARSE_PARAM */


/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;

/* Number of syntax errors so far.  */
int yynerrs;



/*-------------------------.
| yyparse or yypush_parse.  |
`-------------------------*/

#ifdef YYPARSE_PARAM
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void *YYPARSE_PARAM)
#else
int
yyparse (YYPARSE_PARAM)
    void *YYPARSE_PARAM;
#endif
#else /* ! YYPARSE_PARAM */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void)
#else
int
yyparse ()

#endif
#endif
{


    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       `yyss': related to states.
       `yyvs': related to semantic values.

       Refer to the stacks thru separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yytoken = 0;
  yyss = yyssa;
  yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */

  /* Initialize stack pointers.
     Waste one element of value and location stack
     so that they stay on the same level as the state stack.
     The wasted elements are never initialized.  */
  yyssp = yyss;
  yyvsp = yyvs;

  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
	/* Give user a chance to reallocate the stack.  Use copies of
	   these so that the &'s don't force the real ones into
	   memory.  */
	YYSTYPE *yyvs1 = yyvs;
	yytype_int16 *yyss1 = yyss;

	/* Each stack pointer address is followed by the size of the
	   data in use in that stack, in bytes.  This used to be a
	   conditional around just the two extra args, but that might
	   be undefined if yyoverflow is a macro.  */
	yyoverflow (YY_("memory exhausted"),
		    &yyss1, yysize * sizeof (*yyssp),
		    &yyvs1, yysize * sizeof (*yyvsp),
		    &yystacksize);

	yyss = yyss1;
	yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
	goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
	yystacksize = YYMAXDEPTH;

      {
	yytype_int16 *yyss1 = yyss;
	union yyalloc *yyptr =
	  (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
	if (! yyptr)
	  goto yyexhaustedlab;
	YYSTACK_RELOCATE (yyss_alloc, yyss);
	YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
	if (yyss1 != yyssa)
	  YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
		  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
	YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yyn == YYPACT_NINF)
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = YYLEX;
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yyn == 0 || yyn == YYTABLE_NINF)
	goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  *++yyvsp = yylval;

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     `$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 2:

/* Line 1464 of yacc.c  */
#line 474 "prolog.y"
    {
          (yyval.ast) = ast_create_node(AST_PROGRAM, "PROGRAM_ROOT", "root", 1, 1);
          ast_add_child((yyval.ast), (yyvsp[(1) - (1)].ast));

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
          ast_print_tree((yyval.ast), 0, "", 1);

          /* Dump Embedded Symbol Table */
          symtab_dump();
      ;}
    break;

  case 3:

/* Line 1464 of yacc.c  */
#line 501 "prolog.y"
    {
          (yyval.ast) = ast_create_node(AST_PROGRAM, "EMPTY_PROGRAM", "empty", 1, 0);
          printf(">> Compiler Warning: Source file contains zero valid Prolog clauses.\n");
      ;}
    break;

  case 4:

/* Line 1464 of yacc.c  */
#line 514 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (2)].ast);
          ast_add_child((yyval.ast), (yyvsp[(2) - (2)].ast));
      ;}
    break;

  case 5:

/* Line 1464 of yacc.c  */
#line 518 "prolog.y"
    {
          (yyval.ast) = ast_create_node(AST_CLAUSE_LIST, "CLAUSE_LIST", "seq", (yyvsp[(1) - (1)].ast) ? (yyvsp[(1) - (1)].ast)->line : 1, 4);
          ast_add_child((yyval.ast), (yyvsp[(1) - (1)].ast));
      ;}
    break;

  case 6:

/* Line 1464 of yacc.c  */
#line 531 "prolog.y"
    {
          g_total_clauses++;
          g_fact_count++;
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 7:

/* Line 1464 of yacc.c  */
#line 536 "prolog.y"
    {
          g_total_clauses++;
          g_rule_count++;
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 8:

/* Line 1464 of yacc.c  */
#line 541 "prolog.y"
    {
          g_total_clauses++;
          g_query_count++;
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 9:

/* Line 1464 of yacc.c  */
#line 546 "prolog.y"
    {
          g_total_clauses++;
          g_directive_count++;
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 10:

/* Line 1464 of yacc.c  */
#line 551 "prolog.y"
    {
          g_total_clauses++;
          g_dcg_rule_count++;
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 11:

/* Line 1464 of yacc.c  */
#line 556 "prolog.y"
    {
          g_error_count++;
          (yyval.ast) = ast_make_leaf(AST_ERROR_NODE, "ERROR_CLAUSE_RESYNC", "resync", yylineno);
          printf(">> [SYNTAX RECOVERY] Error in clause before line %d; resynchronized on '.'\n", yylineno);
      ;}
    break;

  case 12:

/* Line 1464 of yacc.c  */
#line 571 "prolog.y"
    {
          (yyval.ast) = ast_make_unary(AST_FACT, "FACT", (yyvsp[(1) - (2)].ast) ? (yyvsp[(1) - (2)].ast)->value : "", (yyvsp[(1) - (2)].ast), (yyvsp[(1) - (2)].ast) ? (yyvsp[(1) - (2)].ast)->line : yylineno);
          if ((yyvsp[(1) - (2)].ast)) {
              symtab_record_predicate((yyvsp[(1) - (2)].ast)->value, (yyvsp[(1) - (2)].ast)->arity, 0, (yyvsp[(1) - (2)].ast)->line);
          }
      ;}
    break;

  case 13:

/* Line 1464 of yacc.c  */
#line 587 "prolog.y"
    {
          (yyval.ast) = ast_make_binary(AST_RULE, "RULE", ":-", (yyvsp[(1) - (4)].ast), (yyvsp[(3) - (4)].ast), (yyvsp[(1) - (4)].ast) ? (yyvsp[(1) - (4)].ast)->line : yylineno);
          if ((yyvsp[(1) - (4)].ast)) {
              symtab_record_predicate((yyvsp[(1) - (4)].ast)->value, (yyvsp[(1) - (4)].ast)->arity, 1, (yyvsp[(1) - (4)].ast)->line);
          }
      ;}
    break;

  case 14:

/* Line 1464 of yacc.c  */
#line 603 "prolog.y"
    {
          (yyval.ast) = ast_make_unary(AST_QUERY, "QUERY", "?-", (yyvsp[(2) - (3)].ast), yylineno);
      ;}
    break;

  case 15:

/* Line 1464 of yacc.c  */
#line 616 "prolog.y"
    {
          (yyval.ast) = ast_make_unary(AST_DIRECTIVE, "DIRECTIVE", ":-", (yyvsp[(2) - (3)].ast), yylineno);
      ;}
    break;

  case 16:

/* Line 1464 of yacc.c  */
#line 629 "prolog.y"
    {
          (yyval.ast) = ast_make_binary(AST_DCG_RULE, "DCG_RULE", "-->", (yyvsp[(1) - (4)].ast), (yyvsp[(3) - (4)].ast), (yyvsp[(1) - (4)].ast) ? (yyvsp[(1) - (4)].ast)->line : yylineno);
          if ((yyvsp[(1) - (4)].ast)) {
              symtab_record_predicate((yyvsp[(1) - (4)].ast)->value, (yyvsp[(1) - (4)].ast)->arity + 2, 1, (yyvsp[(1) - (4)].ast)->line);
          }
      ;}
    break;

  case 17:

/* Line 1464 of yacc.c  */
#line 644 "prolog.y"
    {
          (yyval.ast) = ast_make_binary(AST_DIRECTIVE_MODULE, "DIR_MODULE", (yyvsp[(3) - (6)].str),
                               ast_make_leaf(AST_ATOM, "MODULE_NAME", (yyvsp[(3) - (6)].str), yylineno), (yyvsp[(5) - (6)].ast), yylineno);
      ;}
    break;

  case 18:

/* Line 1464 of yacc.c  */
#line 648 "prolog.y"
    {
          (yyval.ast) = ast_make_unary(AST_DIRECTIVE_DYNAMIC, "DIR_DYNAMIC", "dynamic", (yyvsp[(2) - (2)].ast), yylineno);
      ;}
    break;

  case 19:

/* Line 1464 of yacc.c  */
#line 651 "prolog.y"
    {
          (yyval.ast) = ast_make_unary(AST_DIRECTIVE_MULTIFILE, "DIR_MULTIFILE", "multifile", (yyvsp[(2) - (2)].ast), yylineno);
      ;}
    break;

  case 20:

/* Line 1464 of yacc.c  */
#line 654 "prolog.y"
    {
          (yyval.ast) = ast_make_unary(AST_DIRECTIVE_DISCONTIGUOUS, "DIR_DISCONTIGUOUS", "discontiguous", (yyvsp[(2) - (2)].ast), yylineno);
      ;}
    break;

  case 21:

/* Line 1464 of yacc.c  */
#line 657 "prolog.y"
    {
          (yyval.ast) = ast_make_leaf(AST_DIRECTIVE_OP, "DIR_OP", (yyvsp[(7) - (8)].str), yylineno);
          g_operator_count++;
      ;}
    break;

  case 22:

/* Line 1464 of yacc.c  */
#line 661 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 23:

/* Line 1464 of yacc.c  */
#line 667 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (3)].ast);
          ast_add_child((yyval.ast), (yyvsp[(3) - (3)].ast));
      ;}
    break;

  case 24:

/* Line 1464 of yacc.c  */
#line 671 "prolog.y"
    {
          (yyval.ast) = ast_create_node(AST_ARG_LIST, "PRED_SPEC_LIST", "specs", yylineno, 2);
          ast_add_child((yyval.ast), (yyvsp[(1) - (1)].ast));
      ;}
    break;

  case 25:

/* Line 1464 of yacc.c  */
#line 678 "prolog.y"
    {
          char buf[64];
          snprintf(buf, sizeof(buf), "%s/%s", (yyvsp[(1) - (3)].str), (yyvsp[(3) - (3)].str));
          (yyval.ast) = ast_make_leaf(AST_ATOM, "PREDICATE_INDICATOR", buf, yylineno);
      ;}
    break;

  case 26:

/* Line 1464 of yacc.c  */
#line 692 "prolog.y"
    {
          g_term_count++;
          (yyval.ast) = ast_make_leaf(AST_HEAD, "HEAD_ATOM", (yyvsp[(1) - (1)].str), yylineno);
          (yyval.ast)->arity = 0;
      ;}
    break;

  case 27:

/* Line 1464 of yacc.c  */
#line 697 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 28:

/* Line 1464 of yacc.c  */
#line 709 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 29:

/* Line 1464 of yacc.c  */
#line 721 "prolog.y"
    {
          (yyval.ast) = ast_make_binary(AST_CONJUNCTION, "CONJUNCTION", ",", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
          g_operator_count++;
      ;}
    break;

  case 30:

/* Line 1464 of yacc.c  */
#line 725 "prolog.y"
    {
          (yyval.ast) = ast_make_binary(AST_DISJUNCTION, "DISJUNCTION", ";", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
          g_operator_count++;
      ;}
    break;

  case 31:

/* Line 1464 of yacc.c  */
#line 729 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 32:

/* Line 1464 of yacc.c  */
#line 741 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 33:

/* Line 1464 of yacc.c  */
#line 744 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_leaf(AST_CUT, "CUT_OPERATOR", "!", yylineno);
      ;}
    break;

  case 34:

/* Line 1464 of yacc.c  */
#line 748 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_unary(AST_NEGATION, "NEGATION", "\\+", (yyvsp[(2) - (2)].ast), yylineno);
      ;}
    break;

  case 35:

/* Line 1464 of yacc.c  */
#line 752 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 36:

/* Line 1464 of yacc.c  */
#line 755 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 37:

/* Line 1464 of yacc.c  */
#line 767 "prolog.y"
    {
          g_operator_count += 2;
          (yyval.ast) = ast_make_ternary(AST_IF_THEN_ELSE, "IF_THEN_ELSE", "->;", (yyvsp[(2) - (7)].ast), (yyvsp[(4) - (7)].ast), (yyvsp[(6) - (7)].ast), yylineno);
      ;}
    break;

  case 38:

/* Line 1464 of yacc.c  */
#line 771 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_IF_THEN, "IF_THEN", "->", (yyvsp[(2) - (5)].ast), (yyvsp[(4) - (5)].ast), yylineno);
      ;}
    break;

  case 39:

/* Line 1464 of yacc.c  */
#line 784 "prolog.y"
    {
          g_term_count++;
          (yyval.ast) = ast_make_leaf(AST_ATOM, "ATOM", (yyvsp[(1) - (1)].str), yylineno);
      ;}
    break;

  case 40:

/* Line 1464 of yacc.c  */
#line 788 "prolog.y"
    {
          g_term_count++;
          g_variable_count++;
          (yyval.ast) = ast_make_leaf(AST_VARIABLE, "VARIABLE", (yyvsp[(1) - (1)].str), yylineno);
      ;}
    break;

  case 41:

/* Line 1464 of yacc.c  */
#line 793 "prolog.y"
    {
          g_term_count++;
          g_variable_count++;
          (yyval.ast) = ast_make_leaf(AST_ANON_VAR, "ANON_VAR", "_", yylineno);
      ;}
    break;

  case 42:

/* Line 1464 of yacc.c  */
#line 798 "prolog.y"
    {
          g_term_count++;
          (yyval.ast) = ast_make_leaf(AST_INTEGER, "NUMBER", (yyvsp[(1) - (1)].str), yylineno);
      ;}
    break;

  case 43:

/* Line 1464 of yacc.c  */
#line 802 "prolog.y"
    {
          g_term_count++;
          (yyval.ast) = ast_make_leaf(AST_STRING, "STRING", (yyvsp[(1) - (1)].str), yylineno);
      ;}
    break;

  case 44:

/* Line 1464 of yacc.c  */
#line 808 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 45:

/* Line 1464 of yacc.c  */
#line 811 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (1)].ast);
      ;}
    break;

  case 46:

/* Line 1464 of yacc.c  */
#line 816 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_COMPOUND, "MODULE_CALL", ":", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 47:

/* Line 1464 of yacc.c  */
#line 822 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_IS, "IS_EVAL", "is", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 48:

/* Line 1464 of yacc.c  */
#line 826 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_UNIFY, "UNIFY", "=", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 49:

/* Line 1464 of yacc.c  */
#line 830 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_NOT_UNIFY, "NOT_UNIFY", "\\=", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 50:

/* Line 1464 of yacc.c  */
#line 834 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_STRICT_EQ, "STRICT_EQ", "==", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 51:

/* Line 1464 of yacc.c  */
#line 838 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_STRICT_NEQ, "STRICT_NEQ", "\\==", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 52:

/* Line 1464 of yacc.c  */
#line 842 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_UNIV, "UNIV_DECOMPOSE", "=..", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 53:

/* Line 1464 of yacc.c  */
#line 846 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_LT, "LESS_THAN", "<", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 54:

/* Line 1464 of yacc.c  */
#line 850 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_GT, "GREATER_THAN", ">", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 55:

/* Line 1464 of yacc.c  */
#line 854 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_LE, "LESS_OR_EQUAL", "=<", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 56:

/* Line 1464 of yacc.c  */
#line 858 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_GE, "GREATER_OR_EQUAL", ">=", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 57:

/* Line 1464 of yacc.c  */
#line 862 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_LT, "TERM_ORDER_LT", "@<", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 58:

/* Line 1464 of yacc.c  */
#line 866 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_GT, "TERM_ORDER_GT", "@>", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 59:

/* Line 1464 of yacc.c  */
#line 870 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_LE, "TERM_ORDER_LE", "@=<", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 60:

/* Line 1464 of yacc.c  */
#line 874 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_GE, "TERM_ORDER_GE", "@>=", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 61:

/* Line 1464 of yacc.c  */
#line 880 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_ADD, "ADD", "+", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 62:

/* Line 1464 of yacc.c  */
#line 884 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_SUB, "SUB", "-", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 63:

/* Line 1464 of yacc.c  */
#line 888 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_MUL, "MUL", "*", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 64:

/* Line 1464 of yacc.c  */
#line 892 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_DIV, "DIV", "/", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 65:

/* Line 1464 of yacc.c  */
#line 896 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_IDIV, "IDIV", "//", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 66:

/* Line 1464 of yacc.c  */
#line 900 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_MOD, "MOD", "mod", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 67:

/* Line 1464 of yacc.c  */
#line 904 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_REM, "REM", "rem", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 68:

/* Line 1464 of yacc.c  */
#line 908 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_POW, "POW", "^", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 69:

/* Line 1464 of yacc.c  */
#line 912 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_BITWISE_AND, "BIT_AND", "/\\", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 70:

/* Line 1464 of yacc.c  */
#line 916 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_BITWISE_OR, "BIT_OR", "\\/", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 71:

/* Line 1464 of yacc.c  */
#line 920 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_BITWISE_XOR, "BIT_XOR", "xor", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 72:

/* Line 1464 of yacc.c  */
#line 924 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_SHIFT_LEFT, "BIT_SHL", "<<", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 73:

/* Line 1464 of yacc.c  */
#line 928 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_binary(AST_OP_SHIFT_RIGHT, "BIT_SHR", ">>", (yyvsp[(1) - (3)].ast), (yyvsp[(3) - (3)].ast), yylineno);
      ;}
    break;

  case 74:

/* Line 1464 of yacc.c  */
#line 934 "prolog.y"
    {
          g_operator_count++;
          (yyval.ast) = ast_make_unary(AST_OP_UNARY_MINUS, "NEG", "-", (yyvsp[(2) - (2)].ast), yylineno);
      ;}
    break;

  case 75:

/* Line 1464 of yacc.c  */
#line 940 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(2) - (3)].ast);
      ;}
    break;

  case 76:

/* Line 1464 of yacc.c  */
#line 952 "prolog.y"
    {
          g_term_count++;
          g_compound_count++;
          (yyval.ast) = ast_create_node(AST_COMPOUND, "COMPOUND_TERM", (yyvsp[(1) - (4)].str), yylineno, (yyvsp[(3) - (4)].ast) ? (yyvsp[(3) - (4)].ast)->arity : 1);
          if ((yyvsp[(3) - (4)].ast)) {
              (yyval.ast)->arity = (yyvsp[(3) - (4)].ast)->arity;
              for (int i = 0; i < (yyvsp[(3) - (4)].ast)->arity; i++) {
                  (yyval.ast)->children[i] = (yyvsp[(3) - (4)].ast)->children[i];
              }
          }
          symtab_insert((yyvsp[(1) - (4)].str), (yyval.ast)->arity, SYM_FUNCTOR, yylineno);
      ;}
    break;

  case 77:

/* Line 1464 of yacc.c  */
#line 976 "prolog.y"
    {
          g_term_count++;
          g_list_count++;
          (yyval.ast) = ast_make_leaf(AST_LIST_NIL, "NIL_LIST", "[]", yylineno);
      ;}
    break;

  case 78:

/* Line 1464 of yacc.c  */
#line 981 "prolog.y"
    {
          g_term_count++;
          g_list_count++;
          (yyval.ast) = ast_make_unary(AST_LIST_EXPLICIT, "EXPLICIT_LIST", "[...]", (yyvsp[(2) - (3)].ast), yylineno);
      ;}
    break;

  case 79:

/* Line 1464 of yacc.c  */
#line 986 "prolog.y"
    {
          g_term_count++;
          g_list_count++;
          (yyval.ast) = ast_make_binary(AST_LIST_CONS, "HEAD_TAIL_SPLIT", "[H|T]", (yyvsp[(2) - (5)].ast), (yyvsp[(4) - (5)].ast), yylineno);
      ;}
    break;

  case 80:

/* Line 1464 of yacc.c  */
#line 1001 "prolog.y"
    {
          (yyval.ast) = ast_make_unary(AST_CURLY_BLOCK, "DCG_ESCAPE_BLOCK", "{}", (yyvsp[(2) - (3)].ast), yylineno);
      ;}
    break;

  case 81:

/* Line 1464 of yacc.c  */
#line 1012 "prolog.y"
    {
          (yyval.ast) = (yyvsp[(1) - (3)].ast);
          ast_add_child((yyval.ast), (yyvsp[(3) - (3)].ast));
      ;}
    break;

  case 82:

/* Line 1464 of yacc.c  */
#line 1016 "prolog.y"
    {
          (yyval.ast) = ast_create_node(AST_ARG_LIST, "ARG_SEQUENCE", "args", yylineno, 4);
          ast_add_child((yyval.ast), (yyvsp[(1) - (1)].ast));
      ;}
    break;



/* Line 1464 of yacc.c  */
#line 2762 "prolog.tab.c"
      default: break;
    }
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;

  /* Now `shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*------------------------------------.
| yyerrlab -- here on detecting error |
`------------------------------------*/
yyerrlab:
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
      {
	YYSIZE_T yysize = yysyntax_error (0, yystate, yychar);
	if (yymsg_alloc < yysize && yymsg_alloc < YYSTACK_ALLOC_MAXIMUM)
	  {
	    YYSIZE_T yyalloc = 2 * yysize;
	    if (! (yysize <= yyalloc && yyalloc <= YYSTACK_ALLOC_MAXIMUM))
	      yyalloc = YYSTACK_ALLOC_MAXIMUM;
	    if (yymsg != yymsgbuf)
	      YYSTACK_FREE (yymsg);
	    yymsg = (char *) YYSTACK_ALLOC (yyalloc);
	    if (yymsg)
	      yymsg_alloc = yyalloc;
	    else
	      {
		yymsg = yymsgbuf;
		yymsg_alloc = sizeof yymsgbuf;
	      }
	  }

	if (0 < yysize && yysize <= yymsg_alloc)
	  {
	    (void) yysyntax_error (yymsg, yystate, yychar);
	    yyerror (yymsg);
	  }
	else
	  {
	    yyerror (YY_("syntax error"));
	    if (yysize != 0)
	      goto yyexhaustedlab;
	  }
      }
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
	 error, discard it.  */

      if (yychar <= YYEOF)
	{
	  /* Return failure if at end of input.  */
	  if (yychar == YYEOF)
	    YYABORT;
	}
      else
	{
	  yydestruct ("Error: discarding",
		      yytoken, &yylval);
	  yychar = YYEMPTY;
	}
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule which action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;	/* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (yyn != YYPACT_NINF)
	{
	  yyn += YYTERROR;
	  if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
	    {
	      yyn = yytable[yyn];
	      if (0 < yyn)
		break;
	    }
	}

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
	YYABORT;


      yydestruct ("Error: popping",
		  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  *++yyvsp = yylval;


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined(yyoverflow) || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
     yydestruct ("Cleanup: discarding lookahead",
		 yytoken, &yylval);
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  /* Make sure YYID is used.  */
  return YYID (yyresult);
}



/* Line 1684 of yacc.c  */
#line 1022 "prolog.y"


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

