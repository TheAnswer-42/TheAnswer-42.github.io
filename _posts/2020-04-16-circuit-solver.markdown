---
layout: post
title: Circuit Solver
subtitle: MIT OCW 6.009 Lab 3
date: 2020-04-16
description: # Add post description (optional)
img: 20200416-circuit.png # Add image post (optional)
tags: [Python, MIT OCW, 6.009]
author: # Add name author (optional)
---
Python으로 [MIT OCW 6.009] Fundamentals of Programming 강의의 세 번째 문제, [Lab 3: Circuit Solver][circuit-solver]를 풀어보자 (<a href="{{site.baseurl}}/assets/files/6.009-lab3.zip" download>문제 템플릿</a>).<br><br>

### 1. A System of Linear Equations
각 선형 식은 변수와 계수를 연결하는 `dictionary`로 표현된다. 상수항은 key `1`로 표현된다. 예를 들어, $$2x + 3.5y + 4z + 5 = 0$$은 `{'x': 2, 'y': 3.5, 'z': 4, 1: 5}`로 표현된다. 연립방정식은 식 dictionaries의 `list`로 표현된다.

본 문제에서는 연립방정식을 풀기 위해 substitution method를 쓰는 것을 추천한다. 모든 연립방정식의 식은 서로 독립이라고 가정한다. 다음과 같은 연립방정식이 있다고 하자.<br>
<center>$$ \begin{matrix}
x + 2y + 4z - 1 = 0 \\
2x + y = 0 \\
2x + 3y + 4z + 5 = 0
\end{matrix} $$</center>
**Step 1.**<br>
대입할 식, *substitution equation* 을 고른다. 어떤 식이어도 되지만, 속도를 위해서 가장 변수가 적은 식을 고른다. 이 경우에는 $$2x + y = 0$$을 고르게 된다.

**Step 2.**<br>
이 식의 변수 중 *substituted variable* 을 고른다. 어떤 변수여도 되지만, 정확도를 위해서 계수의 절댓값이 가장 큰 변수를 고른다. 이 경우에는 $$2$$를 계수로 가지는 $$x$$를 고르게 된다.

**Step 3.**<br>
*Substitution equation* 을 *substituted variable* 에 대해 정리한다. 이 경우에는 $$x = -0.5y$$가 된다.

**Step 4.**<br>
*Substituted variable* 에 대한 식을 다른 식들에 대입한다. 즉, *substituted variable* 을 소거한다. 이 경우에는 다음과 같이 소거된다.
<center>$$ \begin{matrix}
(-0.5y) + 2y + 4z - 1 = 0 \\
2(-0.5y) + 3y + 4z + 5 = 0
\end{matrix} $$</center>
즉,
<center>$$ \begin{matrix}
1.5y + 4z - 1 = 0 \\
2y + 4z + 5 = 0
\end{matrix} $$</center>
가 된다.

**Step 5.**<br>
새로운 연립방정식은 변수가 하나 소거되었으며 식이 하나 적다. 따라서 재귀적으로 연립방정식의 해를 구할 수 있다. 이 경우에는 재귀 연산 끝에 다음과 같은 해를 얻는다.
<center>$$ \begin{matrix}
y = -12 \\
z = 4.75
\end{matrix} $$</center>

**Step 6.**<br>
마지막으로, *substitution equation* 을 이용해서 *substituted variable* 의 값을 계산한다. 즉, 위의 해를 *substitution equation* 에 대입한다. 이 경우에는 다음과 같은 해를 얻는다.
<center>$$x = 6$$</center>
본 연립방정식의 해는 `{'x': 6, 'y': -12, 'z': 4.75}`로 표현된다.<br><br>

> `substituteEquation` 함수를 작성하라.
>> <span style="color:#2d8659">**Input:**</span>
* `equation`: 정리할 식.
* `substitutedVariable`: 대입할 변수.
* `substitutionEquation`: 대입할 식.

>> <span style="color:#2d8659">**Return:**</span>
* 상술한 `dictionary` 형태의, substituted variable의 소거가 완료된 후의 식.

`substituteEquation`은 위의 **step 1** ~ **step 4** 과정을 수행하는 함수이다.

다음과 같은 코드를 작성하였다. 향후 재귀 호출 시 전체 연립방정식을 계속 복사하는 것은 메모리 에러를 초래할 수 있으므로, 본 함수가 소거가 완료된 식을 반환할 뿐 아니라 `equation` 자체를 수정하게끔 하였다.
{% highlight ruby linenos=table %}
def substituteEquation(equation, substitutedVariable, substitutionEquation):
    """
        Input:
            * equation: 변수 또는 1 (상수항)을 계수와 연결하는 dictionary.
                        e.g., {1: 2, 'x': 2, 'y': 3}은 2 + 2x + 3y = 0 의미.
            * substitutedVariable: equation에서 소거될 변수.
                                   정확도를 위해, substitutionEquation에서
                                   계수의 절댓값이 가장 큰 변수이다.
            * substitutionEquation: 소거에 사용될 식. 속도를 위해, 가장 변수가 적은 식이다.

        Return:
            * equation: 정리된 equation.
                        이 함수는 정리된 equation을 반환할 뿐 아니라, equation 자체를 수정한다.
    """
    if substitutedVariable in equation:    # substitutedVariable이 equation에 없다면, equation 변화 X
        for var in substitutionEquation:
            coefficient = equation[substitutedVariable] * substitutionEquation[var]
            if var in equation:
                equation[var] += coefficient
            else:
                equation[var] = coefficient
        del(equation[substitutedVariable])      # substitutedVariable은 소거된다
    return equation
{% endhighlight %}<br>

> `solveLinear` 함수를 작성하라.
>> <span style="color:#2d8659">**Input:**</span>
* `variables`: 연립방정식의 모든 변수의 `set`. 각 변수는 `string` 또는 `tuple`이다.
* `equations`: 상술한 `dictionary` 형태의 식을 원소로 갖는 `list`. 이 list의 길이는 `variables`의 길이와 같으며, 식은 서로 독립적이다.

>> <span style="color:#2d8659">**Return:**</span>
* 각 변수를 그 값과 연결하는 `dictionary`. 즉, 연립방정식의 해.

`solveLinear`는 위의 **step 1** ~ **step 6** 과정을 수행하는 함수이다. `1e-5` 내의 계산 오차는 허용된다.

다음과 같은 코드를 작성하였다. 위에서 작성한 `substituteEquation`을 사용하였다.
{% highlight ruby linenos=table %}
def solveLinear(variables, equations):
    """
        Input:
            * variables: 변수를 나타내는 strings 또는 tuples의 set.
                         e.g., {'x', 'y', 'z'}
            * equations: 선형 식들의 list. 각 식은 dictionary로 표현되며, 서로 독립적이다.

        Return:
            * result: 각 변수와 그 값을 연결하는 dictionary (solution).
                      하나의 해가 있다고 가정한다 (len(variables) = len(equations)).
                      1e-5 미만의 오차는 허용된다.
    """

    def rearrange(variable, equation):
    """ equation을 variable에 대해 정리한다.
        e.g., variable이 'x', equation이 {'x': 2, 'y': 1}일 때,
              equation을 {'y': -0.5}로 만든다 (x = -0.5*y). """
        variable_coefficient = equation[variable]
        del (equation[variable])    # variable은 소거된다
        for left_var in equation:
            # 나머지 변수들의 계수를 수정한다
            equation[left_var] = -equation[left_var] / variable_coefficient

    if len(equations) == 1:  # 풀이 완료 (남은 변수의 수가 1)
        variable = list(variables)[0]
        equation = equations[0]
        rearrange(variable, equation)
        solution = {variable: list(equation.values())[0]}   # e.g., x = 2이면 {'x': 2}
    else:
        # substitutionEquation: 변수가 가장 적은 식
        num_var = []  # num_var[i]: i-th 식의 변수 갯수 (equations[i])
        for equation in equations:
            num_var.append(len(equation))
        substitutionEquation = equations[num_var.index(min(num_var))]

        # substitutedVariable: substitutionEquation에서 계수의 절댓값이 가장 큰 변수
        forSubstitutedVariable = substitutionEquation.copy()
        if 1 in forSubstitutedVariable:     # substitutedVariable 고를 때 상수항은 제외해야 한다
            del(forSubstitutedVariable[1])
        for var in forSubstitutedVariable:
            forSubstitutedVariable[var] = abs(forSubstitutedVariable[var])      # 절댓값
        vars = list(forSubstitutedVariable.keys())
        values = list(forSubstitutedVariable.values())
        substitutedVariable = vars[values.index(max(values))]
        variables -= set([substitutedVariable])     # len(variables)이 1 감소

        # substitutionEquation을 substitutedVariable에 대해 rearrange
        rearrange(substitutedVariable, substitutionEquation)

        equations.remove(substitutionEquation)  # len(equations)이 1 감소
        for equation in equations:
            # modify equation and substitutionEquation
            substituteEquation(equation, substitutedVariable, substitutionEquation)

        solution = solveLinear(variables, equations)  # 소거된 equations로 재귀 호출
        substitutedVariable_sol = 0
        for var in solution:
            if var in substitutionEquation:
                substitutedVariable_sol += substitutionEquation[var] * solution[var]
        if 1 in substitutionEquation:
            substitutedVariable_sol += substitutionEquation[1]      # 상수항
        solution[substitutedVariable] = substitutedVariable_sol     # solution에 변수 하나 더 추가

    return solution
{% endhighlight %}

다음과 같이 위 코드를 테스트하였다.
{% highlight ruby linenos=table %}
# Solve the system of equations given below.
equations = [{'x': 1, 'y': -1, 'z': 2, 1: 2},
             {'x': 1, 'y': 1, 'z': 3, 1: 1},
             {'x': 11, 'z': -13, 1: -20}]
print('Solution for x - y + 2z + 2 = 0, x + y + 3z + 1 = 0, 11x - 13z - 20 = 0:\n',
       solveLinear({'x', 'y', 'z'}, equations), '\n')
{% endhighlight %}

{% highlight language %}
  >>   Solution for x - y + 2z + 2 = 0, x + y + 3z + 1 = 0, 11x - 13z - 20 = 0:
  >>   {'y': 0.9506172839506175, 'x': 0.7530864197530864, 'z': -0.9012345679012347}
{% endhighlight %}<br/>

### 2. Circuit Solver
회로는 $$J$$개 연결점과 $$W$$개 전선으로 표현할 수 있다. 전류, 전압, 저항은 각각 $$I, V, R$$로 표현된다.

*Kirchhoff's Current Law* 는 전류가 보존된다는 법칙이다. 즉, 각 연결점에서 들어오는 전류의 양은 나가는 전류와 양과 같다. $$J$$개 연결점에 각각 이 법칙을 적용하여 $$J$$개 식을 도출할 수 있으며, 이 중 한 식이 독립적이지 않다. 결과적으로 $$J - 1$$개의 독립적인 식을 얻을 수 있다.

*Ohm's Law* 는 전선에 걸리는 전압과 전선의 저항을 연결한다. 연결점 $$A$$와 연결점 $$B$$를 연결하는 전선 $$W$$에 대해 다음이 성립한다.
<center>$$V_B - V_A = V_W - I_W R_W$$</center>

Kirchhoff's Current Law 와 Ohm's Law를 결합하면 $$(J + W - 1)$$개 식을 얻으며, 이 식들은 서로 독립적임이 알려져 있다. 이에 더해, 한 연결점의 전압을 $$0$$으로 두는 *grounding* 을 통해 총 $$(J + W)$$개 식을 얻을 수 있다.

예를 들어, 다음과 같은 회로를 보자.
<center><img src="{{site.baseurl}}/assets/img/20200416-circuit-example.png" width="400" height="400"></center>

변수는 7개로, 다음과 같다: $$V_A, V_B, V_C, I_{W0}, I_{W1}, I_{W2}, I_{W3}$$. Kirchhoff's Current Law와 Ohm's Law를 적용하면 6개 식을 얻으며, 연결점 A에 grounding을 하면 총 식은 7개가 된다. 식은 다음과 같다:

<center>$$ \begin{matrix}
I_{W0} = I_{W1} \\
I_{W1} = I_{W2} + I_{W3} \\
V_A - V_C = 5 \\
V_B - V_A = -3I_{W1} \\
V_C - V_B = -2I_{W2} \\
V_C - V_B = -10 -7I_{W3} \\
V_A = 0
\end{matrix} $$</center>
이 연립방정식을 풀면 다음과 같은 해를 얻을 수 있다.
<center>$$ \begin{matrix}
I_{W0} = 0.60976 A \\
I_{W1} = 0.60976 A \\
I_{W2} = 1.58537 A \\
I_{W3} = -0.97561 A
\end{matrix} $$</center><br>

> `solveCircuit` 함수를 작성하라.
>> <span style="color:#2d8659">**Input:**</span>
* `junctions`: 회로에 있는 모든 연결점의 `set`. 각 연결점은 `string` 또는 `tuple`로 표현된다.
* `wires`: 전선 ID (`string` 또는 `tuple`)와 (시작 연결점, 끝 연결점) 꼴의 tuple을 연결하는 `dictionary`. 전선들을 따라가면 한 연결점에서 다른 연결점을 이을 수 있도록 제공된다. 각 전선은 한 번씩만 나타난다.
* `resistances`: 전선 ID와 전선의 저항 (단위는 $$\Omega$$)을 연결하는 `dictionary`. 저항이 없는 경우 `0`으로 표시된다.
* `voltages`: 전선 ID와 전선 상의 배터리에 의한 전압차 (단위는 $$V$$)를 연결하는 `dictionary`. 양이면 배터리의 양극이 끝 연결점 옆에 있다는 것을, 음이면 배터리의 양극이 시작 연결점에 있다는 것을 의미한다. 전압차가 없는 경우 `0`으로 표시된다.

>> <span style="color:#2d8659">**Return:**</span>
* 전선 ID와 그 전선의 전류 (양이면 `wires` dictionary 상의 시작 연결점에서 끝 연결점으로 흐른다는 것을 의미)를 연결하는 `dictionary`.

`1e-5` 내의 계산 오차는 허용된다.

다음과 같은 코드를 작성하였다. 위에서 작성한 `solveLinear`을 사용하였다.
{% highlight ruby linenos=table %}
def solveCircuit(junctions, wires, resistances, voltages):
    """
        Input:
            * junctions: 연결점의 set. 각 연결점은 string 또는 tuple이다.
            * wires: {wire ID: (start J, end J)} 형태의 dictionary.
            * resistances: {wire ID: R} 형태의 dictionary. 저항이 없으면 0.
            * voltages: {wire ID: V} 형태의 dictionary. 전압차가 없으면 0.

        Return:
            * result: {wire ID: I} 형태의 dictionary.
    """
    variables = junctions.copy()        # 연결점은 전압을 나타낸다
    equations = []
    for W in wires:
        variables = variables | {W}     # 전선은 전류를 나타낸다; 총 (J+W)개 변수

        # Ohm's Law로 W개 식을 얻는다
        volt_term = -voltages[W]
        res_term = resistances[W]
        # wires[W][0]: 시작 연결점 (전압), wires[W][1]: 끝 연결점 (전압), W: 전선 ID (전류)
        equations.append({wires[W][0]: -1, wires[W][1]: 1, W: res_term, 1: volt_term})

    # 한 연결점을 grounding해 1개 식을 얻는다
    junctionsList = list(junctions)
    equations.append({junctionsList[0]: 1})

    # Kirchhoff's Current Law로 (J-1)개 식을 얻는다
    for J in junctionsList[:-1]:  # (J-1)개의 독립적인 전류 식이 존재한다; 마지막 식은 필요없다
        equation = {}
        for W in wires:
            if wires[W][1] == J:    # 전선 W의 끝 연결점이 J일 때
                equation[W] = 1
            if wires[W][0] == J:    # 전선 W의 시작 연결점이 J일 때
                equation[W] = -1
        equations.append(equation)

    solution = solveLinear(variables, equations)    # (J+W)개 변수의 해
    result = {}
    for variable in solution:
        # result는 W개 변수 (전류)의 해이다; J개 변수 (전압)은 필요없다
        if variable not in junctions:
            result[variable] = solution[variable]
    return result
{% endhighlight %}

다음과 같이 위 코드를 테스트하였다. 테스트 회로는 상술한 회로와 같다.
{% highlight ruby linenos=table %}
# Solve the circuit given below.
    junctions = {'A', 'B', 'C'}
    wires = {'0': ('C', 'A'), '1': ('A', 'B'), '2': ('B', 'C'), '3': ('B', 'C')}
    resistances = {'0': 0, '1': 3, '2': 2, '3': 7}
    voltages = {'0': 5, '1': 0, '2': 0, '3': -10}
    print('Solution for the circuit (current of each wire):\n',
          '\t', solveCircuit(junctions, wires, resistances, voltages))
{% endhighlight %}

{% highlight language %}
  >>   Solution for the circuit (current of each wire):
  >>   {'0': 0.6097560975609754, '3': -0.975609756097561, '2': 1.5853658536585367, '1': 0.6097560975609755}
{% endhighlight %}<br/>

### 4. 끝맺음
이것으로 [MIT OCW 6.009] Fundamentals of Programming 강의의 세 번째 문제, [Lab 3: Circuit Solver][circuit-solver] 풀이를 완료하였다. 상술한 테스트 외에, 문제 템플릿에서 주어진 테스트도 모두 통과하는 것을 확인하였다.

[circuit-solver]: https://py.mit.edu/fall19/labs/lab3
