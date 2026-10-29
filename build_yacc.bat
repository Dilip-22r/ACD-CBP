@echo off
echo ========================================================
echo Compiling Prolog Formal Grammar with Flex, Bison, and GCC
echo Course: Compiler Design Laboratory (22PC2CS301)
echo ========================================================

set BISON="C:\MinGW\msys\1.0\bin\bison.exe"
set FLEX="C:\MinGW\msys\1.0\bin\flex.exe"
set GCC="C:\MinGW\bin\gcc.exe"

echo [1/3] Running Bison (Yacc) on prolog.y...
%BISON% -d -o prolog.tab.c prolog.y
if %ERRORLEVEL% NEQ 0 (
    echo Error: Bison compilation failed.
    exit /b %ERRORLEVEL%
)

echo [2/3] Running Flex (Lex) on prolog.l...
%FLEX% -o lex.yy.c prolog.l
if %ERRORLEVEL% NEQ 0 (
    echo Error: Flex compilation failed.
    exit /b %ERRORLEVEL%
)

echo [3/3] Compiling C source files with GCC into prolog_yacc.exe...
%GCC% -o prolog_yacc.exe prolog.tab.c lex.yy.c
if %ERRORLEVEL% NEQ 0 (
    echo Error: GCC compilation failed.
    exit /b %ERRORLEVEL%
)

echo ========================================================
echo BUILD SUCCESSFUL: prolog_yacc.exe generated!
echo Run tests with: prolog_yacc.exe examples\family.pl
echo ========================================================
