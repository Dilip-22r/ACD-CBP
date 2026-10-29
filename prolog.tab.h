/* A Bison parser, made by GNU Bison 2.4.2.  */

/* Skeleton interface for Bison's Yacc-like parsers in C
   
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

/* Line 1685 of yacc.c  */
#line 341 "prolog.y"

    int ival;
    double dval;
    char *str;
    struct ASTNode *ast;



/* Line 1685 of yacc.c  */
#line 117 "prolog.tab.h"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE yylval;


