% ==========================================================
% CLASSICAL RECURSIVE LOGIC: ANCESTOR & FAMILY RELATIONSHIPS
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

% Rule 3: Sibling relation (X \= Y ensures someone is not sibling to themselves)
sibling(Child1, Child2) :-
    parent(P, Child1),
    parent(P, Child2),
    Child1 \= Child2.

% Rule 4: Grandfather
grandfather(GF, GC) :-
    parent(GF, Parent),
    parent(Parent, GC),
    male(GF).

% Rule 5: Recursive Base Case - Direct Ancestor
ancestor(Ancestor, Descendant) :-
    parent(Ancestor, Descendant).

% Rule 6: Recursive Transitive Step - Indirect Ancestor
ancestor(Ancestor, Descendant) :-
    parent(Ancestor, Intermediate),
    ancestor(Intermediate, Descendant).
