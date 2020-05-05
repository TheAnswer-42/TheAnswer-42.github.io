"""6.009 Lab 5 -- Boolean satisfiability solving"""

import sys
import doctest
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


### PART 1: SAT SOLVER


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    # the core of this algorithm is implemented in the `sat_solve` function.
    # this function simply changes the representation of the formula: we
    # implement a clause as a `set` of literals, and literals are converted to
    # tuples if they were given in some other form.
    return sat_solve([{tuple(i) for i in j} for j in formula])


def set_peek(x):
    """
    Helper function to return an arbitrary element from the given set without
    mutating the given set.
    """
    for i in x:
        return i


def propagate(formula, var, val):
    """
    Propagate the effects of setting a given variable to a given value through
    a formula.

    Arguments:
        formula: a list of sets representing a Boolean formula
        var: a string representing the variable to set
        val: a Boolean representing the value to set that variable to

    Returns:
        a new list of sets representing an updated formula, which incorporates
        the effects of setting `var` to `val`
    """
    # the key operations here are:
    #   * clauses containing (var, val) have already been satisfied (and so
    #     should be removed)
    #   * clauses containing (var, not val) must be satisfied by one of the
    #     other literals in the clause (so we should remove that literal from the
    #     clause)
    return [clause - {(var, not val)}
            for clause in formula
            if (var, val) not in clause]


def sat_solve(formula):
    # this dictionary will be our output (mapping names to Boolean values)
    assignments = {}

    # unit propagation
    while True:
        for clause in formula:
            # try to find a clause of length one
            if len(clause) == 1:
                # here, we found a unit clause.  break out of the `for` loop
                # (and execute the remainder of the while loop's body)
                var, val = set_peek(clause)
                break
        else:
            # this break will only happen if we exited the for loop by
            # exhausting the elements in the formula (i.e., if no unit clauses
            # existed).  this will break out of the `while` loop.
            break

        # if we're here, it's because we broke out of the `for` loop.  we'll
        # store this assignment away and propagate it throughout the formula,
        # before jumping back to the top of this while loop (to continue
        # looking for unit literals)
        assignments[var] = val
        formula = propagate(formula, var, val)

    # base case: an empty formula is one that does not need any more
    # assignments to satisfy it
    if not formula:
        return assignments

    # base case: a formula with an empty clause contains a contradiction (there
    # are no possible ways to satisfy that clause)
    if not all(formula):
        return None

    # this section is the core of the algorithm.  we'll try setting a single
    # variable to both True and False, and try to recursively solve the
    # resulting formulae.
    var, val = set_peek(formula[0])
    for polarity in (val, not val):
        # try the recursive solve
        result = sat_solve(propagate(formula, var, polarity))
        if result is not None:
            # if the recursive call gave us a valid result, incorporate the
            # result from the recursive call into our assignments dictionary,
            # and also set the current variable to the appropriate value before
            # returning.
            assignments[var] = polarity
            assignments.update(result)
            return assignments

    # if we get to this point, neither polarity worked for the given variable,
    # which means no possible assignment exists. so we return None.
    return None


### PART 2: SCHEDULING REDUCTION


def boolify_scheduling_problem(student_preferences, session_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of session names (strings) that work for that student
    session_capacities: a dictionary mapping each session name to a positive
                        integer for how many students can fit in that session

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up
    We assume no student or session names contain underscores.
    """
    out = []
    # the core implementation of these rules is implemented in helper functions
    # rule_1, rule_2, and rule_3
    # this function simply takes the resulting formulae from those rules and
    # combines them together to make a single formula for the whole problem.
    for rule in rule_1, rule_2, rule_3:
        out.extend(rule(student_preferences, session_capacities))
    return out


def rule_1(prefs, caps):
    return [[('%s_%s' % (s, p), True) for p in prefs[s]] for s in prefs]


def all_combinations_helper(source, N):
    if N == 0:
        yield frozenset()
        return
    for c in all_combinations(source, N-1):
        for s in source:
            if s not in c:
                yield c | frozenset([s])


def all_combinations(source, N):
    return set(all_combinations_helper(source, N))


def rule_2(prefs, caps):
    room_pairs = all_combinations(caps, 2)
    return [[('%s_%s' % (s, r), False) for r in p]
            for s in prefs for p in room_pairs]


def rule_3(prefs, caps):
    out = []
    for room, cap in caps.items():
        if cap >= len(prefs):
            continue
        student_combinations = all_combinations(prefs, cap+1)
        for group in student_combinations:
            out.append([('%s_%s' % (s, room), False) for s in group])
    return out
