"""
Curated Pure Prolog Knowledge Bases for Compiler Design & Logic Visualizer Studio.
"""

SAMPLE_PROGRAMS = {
    "ancestor_tree": {
        "title": "Classical Recursive Ancestry & Relationships",
        "description": "Exemplifies Horn Clauses, Recursive Rules, and Transitive Closure in First-Order Logic.",
        "code": """% ==========================================================
% CLASSICAL RECURSIVE LOGIC: ANCESTRY & FAMILY RELATIONS
% Demonstrates: Horn Clauses, Recursive Rules, Transitive Closure
% ==========================================================

% Facts: parent(Parent, Child)
parent(george, john).
parent(george, mary).
parent(helen, john).    
parent(helen, mary).
parent(john, james).
parent(john, alice).
parent(mary, tom).

% Facts: male(Person), female(Person)
male(george).
male(john).
male(james).
male(tom).
female(helen).
female(mary).
female(alice).

% Rule 1: Father relation
father(Father, Child) :-
    parent(Father, Child),
    male(Father).

% Rule 2: Mother relation
mother(Mother, Child) :-
    parent(Mother, Child),
    female(Mother).

% Rule 3: Sibling relation
sibling(Child1, Child2) :-
    parent(P, Child1),
    parent(P, Child2),
    Child1 \\= Child2.

% Rule 4: Grandfather relation
grandfather(GF, GC) :-
    parent(GF, Parent),
    parent(Parent, GC),
    male(GF).

% Rule 5: Recursive Base Case - Direct Ancestor
ancestor(Ancestor, Descendant) :-
    parent(Ancestor, Descendant).

% Rule 6: Recursive Transitive Step - Multi-generational Ancestor
ancestor(Ancestor, Descendant) :-
    parent(Ancestor, Intermediate),
    ancestor(Intermediate, Descendant).
""",
        "default_query": "?- ancestor(george, X)."
    },

    "graph_network": {
        "title": "Directed Network Reachability & Graph Paths",
        "description": "Models directed networks with transitive path closure and detour reachability.",
        "code": """% ==========================================================
% DIRECTED GRAPH REACHABILITY (TOPOLOGY ROUTING ENGINE)
% Demonstrates: Multi-hop Traversal and Cycle-Safe Path Proof
% ==========================================================

% Directed Links: edge(From, To)
edge(router0, switch0).
edge(switch0, pc0).
edge(switch0, pc1).
edge(router0, router1).
edge(router1, server0).
edge(server0, server1).
edge(server1, cloud).

% Base case: Single-hop direct connection
path(From, To) :-
    edge(From, To).

% Recursive multi-hop transitive step
path(From, To) :-
    edge(From, NextHop),
    path(NextHop, To).

% Two-hop detour connection
two_hop(From, To) :-
    edge(From, Intermediate),
    edge(Intermediate, To).
""",
        "default_query": "?- path(router0, Target)."
    },

    "list_algorithms": {
        "title": "List Processing (Member, Append, Reverse)",
        "description": "Standard recursive list unification using ISO Prolog [Head|Tail] pattern matching.",
        "code": """% ==========================================================
% RECURSIVE LIST PROCESSING & PATTERN MATCHING
% Demonstrates: [Head|Tail] Cons cells, Base Cases, Accumulators
% ==========================================================

% member(Element, List)
member(X, [X|_]).
member(X, [_|Tail]) :-
    member(X, Tail).

% append(List1, List2, ResultList)
append([], L, L).
append([H|T], L2, [H|Rest]) :-
    append(T, L2, Rest).

% prefix(Prefix, FullList)
prefix(P, L) :-
    append(P, _, L).

% reverse(List, ReversedList) using accumulator
reverse(List, Reversed) :-
    rev_acc(List, [], Reversed).

rev_acc([], Acc, Acc).
rev_acc([H|T], Acc, Reversed) :-
    rev_acc(T, [H|Acc], Reversed).
""",
        "default_query": "?- member(X, [alpha, beta, gamma, delta])."
    },

    "expr_evaluator": {
        "title": "Symbolic Arithmetic & Expression Evaluator",
        "description": "Interprets and evaluates nested symbolic arithmetic expressions in logic.",
        "code": """% ==========================================================
% SYMBOLIC ARITHMETIC EVALUATOR & INFERENCE
% Demonstrates: Expression Decomposition, AST Evaluation
% ==========================================================

% Base case: Numbers evaluate to themselves
eval(num(N), N).

% Addition: add(A, B)
eval(add(A, B), Result) :-
    eval(A, ValA),
    eval(B, ValB),
    Result is ValA + ValB.

% Subtraction: sub(A, B)
eval(sub(A, B), Result) :-
    eval(A, ValA),
    eval(B, ValB),
    Result is ValA - ValB.

% Multiplication: mul(A, B)
eval(mul(A, B), Result) :-
    eval(A, ValA),
    eval(B, ValB),
    Result is ValA * ValB.
""",
        "default_query": "?- eval(mul(add(num(3), num(4)), num(5)), Value)."
    }
}

import os
_base_dir = os.path.dirname(os.path.abspath(__file__))
_large_file = os.path.join(_base_dir, "examples", "large_nlp_and_expert_system.pl")
if os.path.exists(_large_file):
    with open(_large_file, "r", encoding="utf-8") as _f:
        _large_code = _f.read()
    SAMPLE_PROGRAMS["nlp_expert"] = {
        "title": "Large-Scale Multi-Domain NLP Parser & Clinical Expert System (160+ Rules)",
        "description": "Massive 160+ clause industrial knowledge base covering English CFG parsing, clinical diagnosis, degree audit, and network topology.",
        "code": _large_code,
        "default_query": "?- sentence([the, smart, student, compiles, the, program], [])."
    }

