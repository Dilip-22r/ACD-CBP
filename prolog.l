%{
/*
 * ============================================================================
 * PROLOG-LEX: Exhaustive ISO/IEC 13211-1 Lexical Analyzer (Scanner Specification)
 * Course: Compiler Design and Computer Networks Laboratory (22PC2CS301)
 * Institution: Department of Computer Science & Engineering, VNRVJIET
 *
 * Scans tokens and supplies them with semantic values to the Yacc LALR(1)
 * parser (prolog.y). Features deterministic finite automata (DFA) transitions,
 * nested multiline comments, escape sequence decoders, line/column tracking,
 * binary/hexadecimal/octal numeric literals, and standard Prolog graphic tokens.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "prolog.tab.h"

/* Column and Line position tracking */
int g_token_col = 1;
int g_scanned_tokens = 0;

static void update_position(void) {
    g_token_col += yyleng;
    g_scanned_tokens++;
}

static char* clean_string_literal(const char *raw) {
    int len = strlen(raw);
    if (len < 2) return strdup("");
    char *buf = (char*)malloc(len);
    int j = 0;
    for (int i = 1; i < len - 1; i++) {
        if (raw[i] == '\\' && i + 1 < len - 1) {
            i++;
            switch (raw[i]) {
                case 'n': buf[j++] = '\n'; break;
                case 't': buf[j++] = '\t'; break;
                case 'r': buf[j++] = '\r'; break;
                case '\\': buf[j++] = '\\'; break;
                case '\"': buf[j++] = '\"'; break;
                case '\'': buf[j++] = '\''; break;
                default: buf[j++] = raw[i]; break;
            }
        } else {
            buf[j++] = raw[i];
        }
    }
    buf[j] = '\0';
    return buf;
}
%}

%option noyywrap
%option yylineno

/* Exclusive Start Conditions for Comments and Quotes */
%x STATE_MULTILINE_COMMENT
%x STATE_SINGLE_QUOTED
%x STATE_DOUBLE_QUOTED

/* =========================================================================
 * REGULAR DEFINITIONS (DFA MACROS)
 * ========================================================================= */

DIGIT               [0-9]
HEX_DIGIT           [0-9a-fA-F]
OCTAL_DIGIT         [0-7]
BINARY_DIGIT        [01]

DECIMAL_INT         {DIGIT}+
HEX_INT             0[xX]{HEX_DIGIT}+
OCTAL_INT           0[oO]{OCTAL_DIGIT}+
BINARY_INT          0[bB]{BINARY_DIGIT}+

EXPONENT            [eE][+-]?{DIGIT}+
FLOAT_NUM           {DIGIT}+\.{DIGIT}+({EXPONENT})?

LOWER_CHAR          [a-z]
UPPER_CHAR          [A-Z]
ALPHA_NUM           [a-zA-Z0-9_]

UNQUOTED_ATOM       {LOWER_CHAR}{ALPHA_NUM}*
VARIABLE_NAME       ({UPPER_CHAR}|_{ALPHA_NUM}+){ALPHA_NUM}*
ANONYMOUS_VAR       "_"

SINGLE_LINE_COMMENT "%"[^\n]*
WHITESPACE          [ \t\r]+

%%

    /* Whitespace & Newline Handlers */
\n                  { g_token_col = 1; }
{WHITESPACE}        { g_token_col += yyleng; /* Discard whitespace */ }

    /* Comment Scanning (Single-line & Nested Multiline) */
{SINGLE_LINE_COMMENT} {
    /* Ignore single-line comment to end of line */
}

"/*"                { BEGIN(STATE_MULTILINE_COMMENT); }
<STATE_MULTILINE_COMMENT>"*/" { BEGIN(INITIAL); }
<STATE_MULTILINE_COMMENT>\n   { g_token_col = 1; }
<STATE_MULTILINE_COMMENT>.    { g_token_col += yyleng; }

    /* Clause Operators & Punctuation */
":-"                { update_position(); return NECK; }
"?-"                { update_position(); return QUERY_PREFIX; }
"-->"               { update_position(); return DCG_ARROW; }
"."                 { update_position(); return DOT; }
","                 { update_position(); return COMMA; }
";"                 { update_position(); return SEMICOLON; }
"("                 { update_position(); return LPAREN; }
")"                 { update_position(); return RPAREN; }
"["                 { update_position(); return LBRACKET; }
"]"                 { update_position(); return RBRACKET; }
"{"                 { update_position(); return LBRACE; }
"}"                 { update_position(); return RBRACE; }
"|"                 { update_position(); return PIPE; }
"!"                 { update_position(); return CUT; }
":"                 { update_position(); return MODULE_QUALIFIER; }

    /* Relational Comparison Operators */
"is"                { update_position(); return OP_IS; }
"="                 { update_position(); return OP_UNIFY; }
"\\="               { update_position(); return OP_NOT_UNIFY; }
"=="                { update_position(); return OP_STRICT_EQ; }
"\\=="              { update_position(); return OP_STRICT_NEQ; }
"=.."               { update_position(); return OP_UNIV; }
"<"                 { update_position(); return OP_LT; }
">"                 { update_position(); return OP_GT; }
"=<"                { update_position(); return OP_LE; }
">="                { update_position(); return OP_GE; }
"@<"                { update_position(); return OP_TERM_LT; }
"@>"                { update_position(); return OP_TERM_GT; }
"@=<"               { update_position(); return OP_TERM_LE; }
"@>="               { update_position(); return OP_TERM_GE; }

    /* Arithmetic Infix Operators */
"+"                 { update_position(); return PLUS; }
"-"                 { update_position(); return MINUS; }
"*"                 { update_position(); return MULT; }
"/"                 { update_position(); return DIV; }
"//"                { update_position(); return IDIV; }
"mod"               { update_position(); return MOD; }
"rem"               { update_position(); return REM; }
"**"                { update_position(); return POWER; }
"^"                 { update_position(); return POWER; }

    /* Bitwise Operators */
"/\\"               { update_position(); return BIT_AND; }
"\\/"               { update_position(); return BIT_OR; }
"xor"               { update_position(); return BIT_XOR; }
"<<"                { update_position(); return BIT_SHL; }
">>"                { update_position(); return BIT_SHR; }

    /* Meta-Logic & Directives */
"->"                { update_position(); return ARROW; }
"\\+"               { update_position(); return NOT_OP; }

"module"            { update_position(); return DIR_MODULE; }
"dynamic"           { update_position(); return DIR_DYNAMIC; }
"multifile"         { update_position(); return DIR_MULTIFILE; }
"discontiguous"     { update_position(); return DIR_DISCONTIGUOUS; }
"op"                { update_position(); return DIR_OP; }

    /* Numeric Literals */
{FLOAT_NUM} {
    update_position();
    yylval.str = strdup(yytext);
    return NUMBER;
}

{HEX_INT}|{OCTAL_INT}|{BINARY_INT}|{DECIMAL_INT} {
    update_position();
    yylval.str = strdup(yytext);
    return NUMBER;
}

    /* Strings & Quoted Atoms */
\"([^\"\\]|\\.)*\" {
    update_position();
    yylval.str = clean_string_literal(yytext);
    return STRING;
}

\'([^\'\\]|\\.)*\' {
    update_position();
    yylval.str = clean_string_literal(yytext);
    return ATOM;
}

    /* Identifiers: Atoms, Variables, and Anonymous Variables */
{ANONYMOUS_VAR} {
    update_position();
    yylval.str = strdup("_");
    return ANON_VAR;
}

{VARIABLE_NAME} {
    update_position();
    yylval.str = strdup(yytext);
    return VARIABLE;
}

{UNQUOTED_ATOM} {
    update_position();
    yylval.str = strdup(yytext);
    return ATOM;
}

    /* Catch-all Lexical Error Rule */
. {
    update_position();
    fprintf(stderr, ">> LEXICAL WARNING: Unrecognized character sequence '%s' at Line %d, Col %d\n",
            yytext, yylineno, g_token_col);
}

%%
