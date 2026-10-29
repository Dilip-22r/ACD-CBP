% ==============================================================================
% LARGE-SCALE MULTI-DOMAIN PROLOG KNOWLEDGE BASE & PARSER SYSTEM (150+ RULES & FACTS)
% Domain 1: Natural Language Processing (Context-Free Grammar & Morphological Agreement)
% Domain 2: Clinical Medical Diagnosis Expert System
% Domain 3: University Course Prerequisite Hierarchy & Degree Audit Engine
% Domain 4: Directed Distributed Topology & Routing Paths
% Domain 5: Functional List Operations & Combinatorial Math
% ==============================================================================

% ==============================================================================
% DOMAIN 1: NATURAL LANGUAGE PROCESSING (CFG IN DIFFERENCE LIST FORM)
% ==============================================================================

% Grammar Rule 1: A complete sentence consists of a Noun Phrase followed by a Verb Phrase
sentence(S0, S) :-
    noun_phrase(Num, S0, S1),
    verb_phrase(Num, S1, S).

% Grammar Rule 2: Noun Phrase with Determiner, optional Adjective, and Noun
noun_phrase(Num, S0, S) :-
    det(Word, Num),
    S0 = [Word | S1],
    noun_body(Num, S1, S).

% Grammar Rule 3: Noun Phrase with only Noun (Bare Plural / Mass Noun)
noun_phrase(Num, S0, S) :-
    noun(Word, Num),
    S0 = [Word | S].

% Grammar Rule 4: Noun Phrase with Relative Clause attached
noun_phrase(Num, S0, S) :-
    det(D, Num),
    S0 = [D | S1],
    noun(N, Num),
    S1 = [N | S2],
    rel_clause(S2, S).

% Grammar Rule 5: Noun Body: Single Noun
noun_body(Num, S0, S) :-
    noun(Word, Num),
    S0 = [Word | S].

% Grammar Rule 6: Noun Body: Adjective followed by Noun
noun_body(Num, S0, S) :-
    adj(A),
    S0 = [A | S1],
    noun(N, Num),
    S1 = [N | S].

% Grammar Rule 7: Verb Phrase: Intransitive Verb (no object)
verb_phrase(Num, S0, S) :-
    verb_intr(Word, Num),
    S0 = [Word | S].

% Grammar Rule 8: Verb Phrase: Transitive Verb with Direct Object Noun Phrase
verb_phrase(Num, S0, S) :-
    verb_tr(Word, Num),
    S0 = [Word | S1],
    noun_phrase(_, S1, S).

% Grammar Rule 9: Verb Phrase with Prepositional Phrase Modifier
verb_phrase(Num, S0, S) :-
    verb_intr(Word, Num),
    S0 = [Word | S1],
    prep_phrase(S1, S).

% Grammar Rule 10: Verb Phrase: Transitive Verb + Object + Prepositional Modifier
verb_phrase(Num, S0, S) :-
    verb_tr(Word, Num),
    S0 = [Word | S1],
    noun_phrase(_, S1, S2),
    prep_phrase(S2, S).

% Grammar Rule 11: Prepositional Phrase: Preposition followed by Noun Phrase
prep_phrase(S0, S) :-
    prep(P),
    S0 = [P | S1],
    noun_phrase(_, S1, S).

% Grammar Rule 12: Relative Clause (e.g. "that compiles the program")
rel_clause(S0, S) :-
    rel_pronoun(RP),
    S0 = [RP | S1],
    verb_phrase(_, S1, S).

% --- English Lexicon Facts (Morphology & Parts of Speech) ---

% Determiners: det(Word, NumberAgreement)
det(the, sing).
det(the, plur).
det(a, sing).
det(an, sing).
det(every, sing).
det(each, sing).
det(some, plur).
det(all, plur).
det(many, plur).
det(two, plur).
det(three, plur).

% Relative Pronouns
rel_pronoun(that).
rel_pronoun(which).
rel_pronoun(who).

% Nouns: noun(Word, NumberAgreement)
noun(student, sing).
noun(students, plur).
noun(professor, sing).
noun(professors, plur).
noun(doctor, sing).
noun(doctors, plur).
noun(patient, sing).
noun(patients, plur).
noun(compiler, sing).
noun(compilers, plur).
noun(parser, sing).
noun(parsers, plur).
noun(program, sing).
noun(programs, plur).
noun(algorithm, sing).
noun(algorithms, plur).
noun(computer, sing).
noun(computers, plur).
noun(cat, sing).
noun(cats, plur).
noun(dog, sing).
noun(dogs, plur).
noun(hospital, sing).
noun(university, sing).
noun(laboratory, sing).

% Adjectives: adj(Word)
adj(quick).
adj(smart).
adj(efficient).
adj(recursive).
adj(declarative).
adj(deterministic).
adj(complex).
adj(lazy).
adj(brown).
adj(young).
adj(senior).
adj(correct).

% Intransitive Verbs: verb_intr(Word, NumberAgreement)
verb_intr(sleeps, sing).
verb_intr(sleep, plur).
verb_intr(runs, sing).
verb_intr(run, plur).
verb_intr(works, sing).
verb_intr(work, plur).
verb_intr(fails, sing).
verb_intr(fail, plur).
verb_intr(thinks, sing).
verb_intr(think, plur).

% Transitive Verbs: verb_tr(Word, NumberAgreement)
verb_tr(compiles, sing).
verb_tr(compile, plur).
verb_tr(parses, sing).
verb_tr(parse, plur).
verb_tr(reads, sing).
verb_tr(read, plur).
verb_tr(writes, sing).
verb_tr(write, plur).
verb_tr(teaches, sing).
verb_tr(teach, plur).
verb_tr(helps, sing).
verb_tr(help, plur).
verb_tr(chases, sing).
verb_tr(chase, plur).
verb_tr(diagnoses, sing).
verb_tr(diagnose, plur).
verb_tr(treats, sing).
verb_tr(treat, plur).

% Prepositions: prep(Word)
prep(in).
prep(on).
prep(at).
prep(by).
prep(with).
prep(from).
prep(into).
prep(about).

% ==============================================================================
% DOMAIN 2: CLINICAL MEDICAL DIAGNOSIS EXPERT SYSTEM
% ==============================================================================

% Patient Symptom Facts: symptom(Patient, Symptom)
symptom(alice, fever).
symptom(alice, cough).
symptom(alice, fatigue).

symptom(bob, rash).
symptom(bob, itching).
symptom(bob, sneezing).

symptom(charlie, headache).
symptom(charlie, fever).
symptom(charlie, chills).
symptom(charlie, muscle_pain).

symptom(david, nausea).
symptom(david, stomach_ache).
symptom(david, fatigue).

symptom(emma, sore_throat).
symptom(emma, cough).
symptom(emma, congestion).

% Clinical Diagnosis Inference Rules
diagnosis(Patient, influenza) :-
    symptom(Patient, fever),
    symptom(Patient, cough),
    symptom(Patient, fatigue).

diagnosis(Patient, allergic_reaction) :-
    symptom(Patient, rash),
    symptom(Patient, itching).

diagnosis(Patient, common_cold) :-
    symptom(Patient, sore_throat),
    symptom(Patient, cough),
    symptom(Patient, congestion).

diagnosis(Patient, bacterial_infection) :-
    symptom(Patient, fever),
    symptom(Patient, chills),
    symptom(Patient, muscle_pain).

diagnosis(Patient, gastroenteritis) :-
    symptom(Patient, nausea),
    symptom(Patient, stomach_ache).

% Medical Treatment Recommendation Rules
prescribe(Patient, oseltamivir) :-
    diagnosis(Patient, influenza).

prescribe(Patient, antihistamine) :-
    diagnosis(Patient, allergic_reaction).

prescribe(Patient, amoxicillin) :-
    diagnosis(Patient, bacterial_infection).

prescribe(Patient, oral_rehydration) :-
    diagnosis(Patient, gastroenteritis).

prescribe(Patient, rest_and_vitamins) :-
    diagnosis(Patient, common_cold).

% Quarantine & Isolation Safety Protocol
requires_isolation(Patient) :-
    diagnosis(Patient, influenza).

requires_isolation(Patient) :-
    diagnosis(Patient, bacterial_infection).

% High-Risk Patient Evaluation
high_risk(Patient) :-
    symptom(Patient, fever),
    symptom(Patient, fatigue),
    symptom(Patient, chills).

% ==============================================================================
% DOMAIN 3: ACADEMIC DEGREE AUDIT & PREREQUISITE HIERARCHY
% ==============================================================================

% Direct Prerequisites: prereq(PrereqCourse, AdvancedCourse)
prereq(cs101, cs102).
prereq(cs102, data_structures).
prereq(data_structures, algorithms).
prereq(data_structures, operating_systems).
prereq(data_structures, database_systems).
prereq(algorithms, compiler_design).
prereq(operating_systems, computer_networks).
prereq(compiler_design, advanced_compilers).
prereq(compiler_design, program_analysis).
prereq(computer_networks, distributed_systems).

% Course Credits: credits(Course, CreditHours)
credits(cs101, 3).
credits(cs102, 3).
credits(data_structures, 4).
credits(algorithms, 4).
credits(operating_systems, 4).
credits(database_systems, 3).
credits(computer_networks, 3).
credits(compiler_design, 4).
credits(advanced_compilers, 3).
credits(distributed_systems, 3).

% Student Completion History: completed(Student, Course)
completed(john, cs101).
completed(john, cs102).
completed(john, data_structures).
completed(john, algorithms).

completed(mary, cs101).
completed(mary, cs102).
completed(mary, data_structures).
completed(mary, operating_systems).
completed(mary, computer_networks).

completed(peter, cs101).
completed(peter, cs102).

completed(sarah, cs101).
completed(sarah, cs102).
completed(sarah, data_structures).
completed(sarah, algorithms).
completed(sarah, compiler_design).

% Rule: Direct or Indirect Prerequisite (Transitive Closure)
depends_on(Course, Prereq) :-
    prereq(Prereq, Course).

depends_on(Course, Prereq) :-
    prereq(Intermediate, Course),
    depends_on(Intermediate, Prereq).

% Rule: Eligibility to Enroll in an Advanced Course
can_enroll(Student, Course) :-
    prereq(Pre, Course),
    completed(Student, Pre).

% Rule: Graduated Senior Status (Has Completed Compiler Design & Networks)
eligible_for_capstone(Student) :-
    completed(Student, compiler_design),
    completed(Student, computer_networks).

% ==============================================================================
% DOMAIN 4: NETWORK TOPOLOGY & ROUTING PATHS
% ==============================================================================

% Directed Network Links: link(NodeA, NodeB)
link(gateway, router1).
link(gateway, router2).
link(router1, switch1).
link(router1, switch2).
link(router2, switch3).
link(switch1, workstation1).
link(switch1, workstation2).
link(switch2, compute_server1).
link(switch2, compute_server2).
link(switch3, database_server).

% Transitive Route Discovery
route(From, To) :-
    link(From, To).

route(From, To) :-
    link(From, Next),
    route(Next, To).

% Multi-Hop Intermediate Transit
via_router(From, To, Router) :-
    link(From, Router),
    route(Router, To).

% ==============================================================================
% DOMAIN 5: LIST PROCESSING UTILITIES & ALGORITHMS
% ==============================================================================

% Element membership
elem(X, [X | _]).
elem(X, [_ | Tail]) :-
    elem(X, Tail).

% List Concatenation (append/3)
concat_list([], L, L).
concat_list([H | T], L2, [H | Rest]) :-
    concat_list(T, L2, Rest).

% List Length Computation
list_len([], 0).
list_len([_ | Tail], N) :-
    list_len(Tail, N1),
    N is N1 + 1.

% List Reversal using an Accumulator
reverse_acc([], Acc, Acc).
reverse_acc([H | T], Acc, Result) :-
    reverse_acc(T, [H | Acc], Result).

rev(List, Reversed) :-
    reverse_acc(List, [], Reversed).
