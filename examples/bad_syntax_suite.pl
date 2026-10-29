% =============================================================================
% BAD SYNTAX TEST SUITE: Deliberate Grammar Violations for Error Recovery
% Course: Compiler Design Laboratory (22PC2CS301)
% Tests panic-mode synchronization, error reporting, and resynchronization.
% =============================================================================

% Valid Clause 1: Ground Fact
parent(george, john).

% Error 1: Missing Closing Parenthesis in compound head
parent(george, mary.

% Valid Clause 2: Fact after error (Should recover and parse successfully)
parent(helen, john).

% Error 2: Dangling neck with empty body
ancestor(X, Y) :- .

% Valid Clause 3: Ground Fact
parent(john, james).

% Error 3: Unclosed list bracket
path(start, [node1, node2, node3).

% Valid Clause 4: Valid Rule
father(F, C) :- parent(F, C), male(F).

% Error 4: Malformed arithmetic operator sequence
bad_math(X) :- X is * / 5.

% Valid Clause 5: Ground Fact
male(george).
