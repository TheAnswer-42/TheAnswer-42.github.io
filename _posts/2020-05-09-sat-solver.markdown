---
layout: post
title: SAT Solver
subtitle: MIT OCW 6.009 (2020 Spring) Lab 5
date: 2020-05-09
description: # Add post description (optional)
img: 20200509-sat-solver.png # Add image post (optional)
tags: [Python, MIT OCW, 6.009]
author: # Add name author (optional)
---
Python으로 [MIT OCW 6.009] Fundamentals of Programming (2020년 봄) 강의의 다섯 번째 문제, [Lab 5: SAT Solver][sat-solver]를 풀어보자 (<a href="{{site.baseurl}}/assets/files/6.009-lab5 (2020S).zip" download>문제 템플릿</a>).

이번 문제에서는 [Boolean satisfiability problem][bsp-wiki]을 다룰 것이다. Python에서는 `not`이 `or`에 우선하는 것을 주의하라. 즉, `not p or q`는 `(not p) or q`이다.<br><br>

### **1. SAT Solver**
Boolean 식은 [Conjunctive normal form (CNF)][cnf-wiki]으로 나타낼 수 있다. CNF에서 *literal* 은 변수 또는 변수의 `not`, *clause* 는 `or`로 연결된 literals, *formula* 는 `and`로 연결된 clauses다. 본 문제에서는 변수를 `string`으로, literal을 (변수, `True`/`False`) 꼴의 `tuple` 또는 `list`로, clause를 literals의 `list`로, formula를 clauses의 `list`로 나타낸다. 예를 들어,
{% highlight ruby %}
(a or c) and (a or not d) and (b or c)
{% endhighlight %}
와 같은 CNF Boolean 식을
{% highlight ruby %}
[[('a', True), ('c', True)], [('a', True), ('d', False)], [('b', True), ('c', True)]]
{% endhighlight %}
로 나타낸다.

Boolean 식을 푸는 전통적인 도구는 satisfiability solver, 또는 SAT solver이다. 변수에 가능한 모든 Boolean 조합을 대입하는 brute-force 방법은 바람직하지 않다. Boolean 변수가 $$N$$개일 때 조합은 $$2^N$$개가 될 것이다. 대신 다음과 같은 방법을 쓰자.

Formula $$F$$에서 변수 `x`를 고른다. 그 후 `x`가 `True`일 때 도출되는 formula $$F_1$$을 얻는다. $$F_1$$을 성공적으로 풀 수 있으면 `x`가 `True`임을 답에 포함한다. $$F_1$$을 풀 수 없으면 `x`를 `False`로 놓고 재시도한다. 두 경우 모두에서 답을 얻을 수 없으면 $$F$$를 만족할 수 없다고 결론짓는다. 예를 들어, 다음과 같은 CNF formula를 보자.
{% highlight ruby %}
(a or b or not c) and (c or d)
{% endhighlight %}
`c`를 `True`로 놓으면 위 식은 다음과 같이 변한다.
{% highlight ruby %}
(a or b)
{% endhighlight %}
이렇게 식을 변형함으로써 보다 효율적인 SAT solver를 작성할 수 있다.<br><br>

> `satisfying_assignment` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `formula`: 상술한 `list` 형태의 CNF formula.

>> <span style="color:#2d8659">**Return:**</span>
* 변수와 `True`/`False`를 연결하는 `dictionary`. 해가 존재하지 않으면 `None`.

우선 `satisfying_assignment`은 다음과 같이 작성하였다. 단순히 `formula`를 `list`, `clause`를 `set`, `literal`을 `tuple`로 형식을 변경하여 전달하는 역할을 한다.
{% highlight ruby linenos=table %}
def satisfying_assignment(formula):
    return sat_solve([{tuple(literal) for literal in clause} for clause in formula])
{% endhighlight %}

그 후 한 변수에 대한 `True`/`False` 가정을 바탕으로 단순화한 `formula`를 반환하는 `simplify_formula`를 작성하였다.
{% highlight ruby linenos=table %}
def simplify_formula(formula, var, val):
    """var의 val (T/F)를 바탕으로 변형한 formula 반환"""
    return [clause - {(var, not val)} for clause in formula if (var, val) not in clause]
{% endhighlight %}

최종적으로 `sat_solve`를 다음과 같이 작성하였다. 효율을 위해, unit clause (literal이 한 개인 clause)가 있으면 먼저 그 clause의 literal을 사용하여 `formula`를 풀도록 하였다.
{% highlight ruby linenos=table %}
def sat_solve(formula):
    """reformatted된 CNF formula를 가지고 SAT를 푼다"""
    assignment = {}

    # 효율을 위해, unit clause (literal이 한 개인 clause)가 있으면 먼저 그 clause에 대해 푼다
    while True:
        for clause in formula:
            if len(clause) == 1:
                var, val = list(clause)[0]
                formula = simplify_formula(formula, var, val)
                if not all(formula):    # formula에 빈 set 있으면 틀린 clause가 있다는 뜻이므로 해가 없다
                    return None
                assignment[var] = val
                break
        else:
            break   # unit clause 없으면 while문 나간다

    # base case
    if not formula:
        return assignment

    # recursive case
    # left-first search: 첫 clause의 첫 literal이 옳다고 가정 후 (left branch) 해 있으면 반환,
    #                    아니면 틀리다고 가정 후 (right branch) 해 있으면 반환
    var, b = list(formula[0])[0]
    for val in (b, not b):
        result = sat_solve(simplify_formula(formula, var, val))
        if result is not None:
            assignment.update(result)
            assignment[var] = val
            return assignment
{% endhighlight %}

문제 템플릿과 함께 주어진 `test.py` 중 `Test_1_Sat`와 `Test_2_PuzzleSudoku`의 테스트를 모두 통과하는 것을 확인하였다.<br><br>


### **2. Scheduling by Reduction**
이제 CNF formula가 주어지면 `satisfying_assignment`로 풀 수 있게 되었다. 그렇다면 Boolean 식을 CNF formula로 만들어보자.

학생들이 시험을 치기 위해 방을 배정받아야 한다고 하자. 각 학생이 선호하는 방이 있으며, 각 방은 수용 인원이 정해져 있다. 이때 모든 조건을 만족하도록 학생을 방에 배정하는 경우 (schedule)를 찾아라.<br>

> `boolify_scheduling_problem` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `student_preferences`: 학생 이름 (string)과 그 학생이 선호하는 방 이름 (string)의 `set`를 연결하는 `dictionary`.
* `session_capacities`: 방 이름 (string)과 그 방의 수용 인원 (integer)을 연결하는 `dictionary`.

>> <span style="color:#2d8659">**Return:**</span>
* `student_preferences`와 `session_capacities`를 고려한 CNF formula.

반환되는 CNF formula의 변수는 `student_session`의 형태이다 (`student`는 학생 이름, `session`은 방 이름).

호출 예시는 다음과 같다.
{% highlight ruby linenos=table %}
boolify_scheduling_problem({'Alice': {'basement', 'penthouse'},
                            'Bob': {'kitchen'},
                            'Charles': {'basement', 'kitchen'},
                            'Dana': {'kitchen', 'penthouse', 'basement'}},
                           {'basement': 1,
                            'kitchen': 2,
                            'penthouse': 4})
{% endhighlight %}<br>

#### **2.1. Students Only in Desired Rooms**
CNF formula를 만들기 위한 규칙을 세 가지로 나눌 수 있다. 그 첫 번째로, 한 학생이 선호하는 방 중 하나에 그 학생을 배정해야 한다. 예를 들어, 위의 예시에서 Charles는 basement 또는 kitchen에 배정되어야 하며, Alice는 basement 또는 penthouse에 배정되어야 한다.<br>

#### **2.2. Each Student in Exactly One Session**
두 번째 규칙으로, 각 학생은 한 방에만 배정되어야 한다. 즉 각 학생은 최소 한 방에 배정되어야 하며, 최대 한 방에 배정되어야 한다. 전자는 위의 **2.1** 규칙으로 만족되므로 후자만 고려하면 된다. 예를 들어, 위의 예시에서 `Bob_kitchen`과 `Bob_basement`는 동시에 `True`일 수 없다 (하나는 `False`여야 한다).<br>

#### **2.3. No Oversubscribed Sections**
마지막 규칙으로, 방의 수용 인원을 넘어서 배정될 수 없다. 이를 다음과 같이 생각할 수 있다. 방의 수용 인원이 $$N$$명일 때, 모든 $$N + 1$$명의 학생 조합에서, 한 조합당 최소 한 명은 그 방에 배정될 수 없다.<br>

#### **2.4. 문제 풀이**
첫 번째로 **2.1** 규칙으로 CNF formula를 만드는 함수를 작성하였다.
{% highlight ruby linenos=table %}
def rule1(student_preferences):
    """Rule 1: Students Only In Desired Rooms"""
    return [{(student + '_' + session, True) for session in student_preferences[student]}
            for student in student_preferences]
{% endhighlight %}

두 번째로 **2.2** 규칙으로 CNF formula를 만드는 함수를 작성하였다. 조합을 생성하는 generator `comb`도 작성하였다.
{% highlight ruby linenos=table %}
def comb(L, n):
    """list L에서 n개 원소를 뽑는 모든 조합을 생성하는 generator"""
    if not n:
        yield []
    else:
        for i in range(len(L)):
            for subcomb in comb(L[i+1:], n-1):
                yield [L[i]] + subcomb

def rule2(student_preferences):
    """Rule 2: Each Student In Exactly One Session (각 학생이 최대 한 개의 session에 있어야 한다)"""
    return [{(student + '_' + session, False) for session in session_comb}
            for student in student_preferences for session_comb in comb(list(student_preferences[student]), 2)]
{% endhighlight %}

세 번째로 **2.3** 규칙으로 CNF formula를 만드는 함수를 작성하였다. 위에서 작성한 `comb`을 사용하였다.
{% highlight ruby linenos=table %}
def rule3(student_preferences, session_capacities):
    """Rule 3: No Oversubscribed Sections"""
    formula = []
    students = list(student_preferences.keys())
    for session, capacity in session_capacities.items():
        if capacity >= len(students):   # capacity가 학생 수 이상이면 rule3 필요 없다
            continue
        for student_comb in comb(students, capacity + 1):
            formula.append({(student + '_' + session, False) for student in student_comb})
    return formula
{% endhighlight %}

최종적으로 위 세 함수로 만든 CNF formula를 합치는 함수 `boolify_scheduling_problem`을 작성하였다.
{% highlight ruby linenos=table %}
def boolify_scheduling_problem(student_preferences, session_capacities):
    return rule1(student_preferences) +
           rule2(student_preferences) +
           rule3(student_preferences, session_capacities)
{% endhighlight %}

문제 템플릿과 함께 주어진 `test.py` 중 `Test_3_Scheduling`의 테스트를 모두 통과하는 것을 확인하였다.<br><br>

### **3. 끝맺음**
이것으로 [MIT OCW 6.009] Fundamentals of Programming (2020년 봄) 강의의 다섯 번째 문제, [Lab 5: SAT Solver][sat-solver] 풀이를 완료하였다. 백트래킹을 연습할 수 있는 문제였다.

[sat-solver]: https://py.mit.edu/spring20/labs/lab5
[bsp-wiki]: https://en.wikipedia.org/wiki/Boolean_satisfiability_problem
[cnf-wiki]: https://en.wikipedia.org/wiki/Conjunctive_normal_form
