---
layout: post
title: Bacon Number
subtitle: MIT OCW 6.009 (2019 Fall) Lab 2
date: 2020-04-15
description: # Add post description (optional)
img: 20200415-bacon-number.jpg # Add image post (optional)
tags: [Python, MIT OCW, 6.009]
author: # Add name author (optional)
---
Python으로 [MIT OCW 6.009] Fundamentals of Programming (2019년 가을) 강의의 두 번째 문제, [Lab 2: Bacon Number][bacon-number]를 풀어보자 (<a href="{{site.baseurl}}/assets/files/6.009-lab2.zip" download>문제 템플릿</a>).

*Six Degrees of Separation* 이란 지구상의 한 사람과 다른 한 사람 간에는 최대 6명의 사람이 있다는 이론이다. 본 이론의 할리우드 버전이 바로 *Bacon number* 다. 배우 Kevin Bacon은 0의 Bacon number를 갖는다. Kevin Bacon과 같은 영화에 출연한 배우는 1의 Bacon number를 갖는다. Kevin Bacon과 같은 영화에 출연한 배우와 같은 영화에 출연한 배우는 2의 Bacon number를 갖는다. 즉, 어떤 배우의 Bacon number는 *그 배우를 Kevin Bacon과 떨어뜨려 놓는 최소 영화 수* 로 정의된다.

배우-영화 데이터는 `list`로 제공된다. 이 list는 `[actor_id_1, actor_id_2, film_id]` 형태의 list를 원소로 가지며, 이는 `actor_id_1`의 배우와 `actor_id_2`의 배우가 `film_id`의 영화에 출연했다는 의미이다. 본 문제에서는 `small.json`과 `large.json`의 두 데이터가 제공된다.

한편, 배우 ID-배우 이름 데이터는 `{actor_name: actor_id}` 형태의 `dictionary`로 제공된다. 본 문제에서는 `names.json`이 제공된다.<br/><br/>

### 1. Acting Together
> `did_x_and_y_act_together` 함수를 작성하라.
>> <span style="color:#2d8659">**Parameters:**</span>
* `data`: 배우-영화 데이터.<br>
* `actor_id_1`, `actor_id_2`: 두 배우의 ID.<br>

>> <span style="color:#2d8659">**Return:**</span>
* 두 배우가 같은 영화에 출연했으면 `True`, 아니면 `False`.

예를 들어, Kevin Bacon (`id=4724`)과 Steve Park (`id=4025`)은 같은 영화에 출연하지 않았으므로, `did_x_and_y_act_together(..., 4724, 4025)`는 `False`를 반환해야 한다.

우선 다음과 같이 배우-영화 데이터로부터 `{film_id: {actor_id_1, actor_id_2, ...}}` 꼴의 `dictionary`를 반환하는 코드를 작성하였다.
{% highlight ruby linenos=table %}
def data_into_film_dict(data):
    """
        아이템 탐색이 list에서보다 dictionary에서 훨씬 빠르며,
        같은 영화에 나온 배우들을 모두 묶기 위해,
        배우-영화 데이터 ([[actor_id_1, actor_id_2, film_id]])를 dictionary로 변환하자.

        Return:
            * filmDict: Dictionary ({film_id: {actor_id_1, actor_id_2, ...}})
                        Key: integer; Value: set
    """
    filmDict = {}
    for IDs in data:
        if IDs[2] not in filmDict:      # 각 영화의 첫 번째
            filmDict[IDs[2]] = set(IDs[:2])     # filmDict[film_id] = {actor_id_1, actor_id_2}
        else:       # set는 반복되는 원소를 허용하지 않는다
            filmDict[IDs[2]] = filmDict[IDs[2]] | set(IDs[:2])
    return filmDict
{% endhighlight %}

그 후 다음 코드를 작성하였다.
{% highlight ruby linenos=table %}
def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    """
        Parameter:
            * data: 배우-영화 데이터 ([[actor_id_1, actor_id_2, film_id]])

        Return:
            * 두 배우가 같은 영화에 출연했으면 True
            * 아니면 False
    """
    filmDict = data_into_film_dict(data)
    act_together = False
    for actor_ids in filmDict.values():
        if actor_id_1 in actor_ids and actor_id_2 in actor_ids:
            act_together = True
    return act_together
{% endhighlight %}

다음과 같이 위 코드를 테스트하였다.
{% highlight ruby linenos=table %}
import json

with open('resources/names.json') as f:
    namesDict = json.load(f)

with open('resources/small.json') as f:
    smalldb = json.load(f)

# Steve Park과 Craig Bierko가 같이 연기했는가?
print('Steve Park and Craig Bierko acted together:',
      did_x_and_y_act_together(smalldb, namesDict['Steve Park'], namesDict['Craig Bierko']))

# Rex Linn과 Samuel L. Jackson이 같이 연기했는가?
print('Rex Linn and Samuel L. Jackson acted together:',
      did_x_and_y_act_together(smalldb, namesDict['Rex Linn'], namesDict['Samuel L. Jackson']))
{% endhighlight %}

{% highlight language %}
  >>   Steve Park and Craig Bierko acted together: False
  >>   Rex Linn and Samuel L. Jackson acted together: True
{% endhighlight %}<br/>

### 2. Bacon Number
> `get_actors_with_bacon_number` 함수를 작성하라.
>> <span style="color:#2d8659">**Parameters:**</span>
* `data`: 배우-영화 데이터.<br>
* `n`: Bacon number.<br>

>> <span style="color:#2d8659">**Return:**</span>
* 입력한 Bacon number를 갖는 모든 배우들의 ID를 포함하는 `set`.

Bacon number가 1인 배우들을 다음과 같이 나타낼 수 있다.
<center><img src="{{site.baseurl}}/assets/img/20200415-bacon-number-1.png" width="400" height="400"></center>
그렇다면 Bacon number가 2인 배우들은 다음과 같이 나타내어진다.
<center><img src="{{site.baseurl}}/assets/img/20200415-bacon-number-2.png" width="400" height="400"></center>
Bacon number가 `i`인 배우들로부터 Bacon number가 `i+1`인 배우들을 구하도록 재귀 함수를 작성하여야 한다.

우선 다음과 같이 배우-영화 데이터로부터 `{actor_id: {film_id_1, film_id_2, ...}}`꼴의 `dictionary`를 반환하는 코드를 작성하였다.
{% highlight ruby linenos=table %}
def data_into_actor_dict(data):
    """
        한 배우의 영화를 모두 묶기 위해,
        영화-배우 데이터 ([[actor_id_1, actor_id_2, film_id]])를 dictionary로 변환하자.

        Return:
            * actorDict: Dictionary ({actor_id: {film_id_1, film_id_2, ...}})
                         Key: integer; Value: set
    """
    actorDict = {}
    for IDs in data:
        for actor_id in IDs[:2]:    # IDs[0]와 IDs[1] (actor_ids)
            if actor_id not in actorDict:
                actorDict[actor_id] = set([IDs[2]])     # actorDict[actor_id] = {film_id}
            else:       # a set doesn't allow duplicated elements
                actorDict[actor_id] = actorDict[actor_id] | set([IDs[2]])
    return actorDict
{% endhighlight %}

또한 영화-배우 데이터로부터 `{actor_id: {coactor_id_1, coactor_id_2, ...}}` 꼴의 `dictionary`를 반환하는 코드를 작성하였다. 위에서 작성한 `data_into_film_dict`와 `data_into_actor_dict`를 사용하였다.
{% highlight ruby linenos=table %}
def data_into_coactor_dict(data):
    """
        한 배우의 동료 배우 (같은 영화에 출연한 배우)를 모두 묶기 위해,
        영화-배우 데이터 ([[actor_id_1, actor_id_2, film_id]])를 dictionary로 변환하자.

        Return:
            * coactorDict: Dictionary ({actor_id: {coactor_id_1, coactor_id_2, ...}})
                           Key: integer; Value: set
    """
    filmDict = data_into_film_dict(data)
    actorDict = data_into_actor_dict(data)
    coactorDict = {}
    for actor_id in actorDict:
        for film_id in actorDict[actor_id]:
            if actor_id not in coactorDict:   # 각 배우의 첫 번째
                coactorDict[actor_id] = filmDict[film_id]
            else:
                coactorDict[actor_id] = coactorDict[actor_id] | filmDict[film_id]
        # actor_id's co-actors shouldn't include actor_id itself
        coactorDict[actor_id] = coactorDict[actor_id] - set([actor_id])
    return coactorDict
{% endhighlight %}

그 후 다음 코드를 작성하였다. Kevin Bacon의 ID는 `4724`이다. `get_ids_with_actor_number` 작성 시 Bacon이 아닌 다른 배우로부터도 actor number를 구할 수 있도록 중심 배우의 id를 `center_id`로 두었다.
{% highlight ruby linenos=table %}
def get_ids_with_actor_number(coactorDict, center_id, n):
    """
        Parameter:
            * n: actor number (center_id가 4724일 때 Bacon number)

        Return:
            * (Actor number n의 배우 ID set, actor number 0 ~ n의 배우 ID set) 꼴의 tuple
    """
    if n == 0:
        ids = {center_id}
        ids_so_far = {center_id}
    else:
        # junc_ids (junction ids): actor IDs with Bacon number (n-1)
        junc_ids, junc_ids_so_far = get_ids_with_actor_number(coactorDict, center_id, n - 1)
        idSet = set()
        for junc_id in junc_ids:
            idSet = idSet | coactorDict[junc_id]    # junc_id의 coactor IDs를 append
        ids = idSet - junc_ids_so_far
        ids_so_far = idSet | junc_ids_so_far
    return ids, ids_so_far

def get_actors_with_bacon_number(data, n):
    """
        Parameter:
            * n: Bacon number

        Return:
            * Bacon number n을 갖는 배우들의 ID set
    """
    coactorDict = data_into_coactor_dict(data)
    return get_ids_with_actor_number(coactorDict, 4724, n)[0]   # Kevin Bacon의 ID는 4724
{% endhighlight %}

이에 추가로, 배우 ID를 이름으로 바꾸는 함수도 작성하였다.
{% highlight ruby linenos=table %}
import json

with open('resources/names.json') as f:
    namesDict = json.load(f)

def ids_into_names(ids):
    nameList = list(namesDict.keys())
    idList = list(namesDict.values())
    names = set()
    for id in ids:
        names.add(nameList[idList.index(id)])
    if len(names) == 0:
        return None
    else:
        return names
{% endhighlight %}

다음과 같이 위 코드를 테스트하였다. `Lenovo Ideapad S340 (Ryzen 5)`으로 실행한 결과 70초 ~ 75초가 소요된다.
{% highlight ruby linenos=table %}
import time
import json

with open('resources/large.json') as f:
    largedb = json.load(f)

# large.json에서, 누가 Bacon number 6를 갖는가?
start = time.time()
print('Actors of BN 6 in large.json:', ids_into_names(get_actors_with_bacon_number(largedb, 6)))
end = time.time()
print('get_actors_with_bacon_number (BN 6) in large.json:', end-start, 's')    # 70 ~ 75 s
{% endhighlight %}

{% highlight language %}
  >>   Actors of BN 6 in large.json: {'Iva Ilakovac', 'Sven Batinic', 'Vjeran Tin Turk', 'Anton Radacic'}
  >>   get_actors_with_bacon_number (BN 6) in large.json: 72.103125 s
{% endhighlight %}<br/>

### 3. Paths
> `get_bacon_path` 함수를 작성하라.
>> <span style="color:#2d8659">**Parameters:**</span>
* `data`: 배우-영화 데이터.<br>
* `actor_id`: 배우 ID.<br>

>> <span style="color:#2d8659">**Return:**</span>
* Kevin Bacon으로부터 입력한 배우로 이어지는 배우 ID들의 `list`, 즉 'Bacon path'. Path가 존재하지 않으면 `None`.

예를 들어, Julia Roberts의 Bacon path는 `[4724, 3087, 1204]`이다. 이는 Kevin Bacon (`id=4724`)은 Julia Roberts (`id=1204`)와 같은 영화에 출연한 Robert Duvall (`id=3087`)과 같은 영화에 출연했다는 의미이다. Bacon path는 고유하지 않으며, 도착 배우가 같은 어떤 최단 경로라도 답이 될 수 있다.

> `get_path` 함수를 작성하라.
>> <span style="color:#2d8659">**Parameters:**</span>
* `data`: 배우-영화 데이터.<br>
* `actor_id_1`, `actor_id_2`: 두 배우의 ID.<br>

>> <span style="color:#2d8659">**Return:**</span>
* 입력한 한 배우로부터 입력한 다른 배우로 이어지는 배우 ID들의 `list`. Path가 존재하지 않으면 `None`.

Kevin Bacon은 사실 특별한 사람이 아니며, 다른 어떤 배우를 중심으로도 path를 찾을 수 있다. 역시 출발 배우와 도착 배우가 같은 어떤 최단 경로라도 답이 될 수 있다.

다음과 같이 코드를 작성하였다. 위에서 작성한 `data_into_coactor_dict`와 `get_ids_with_actor_number`를 사용하였다.
{% highlight ruby linenos=table %}
def get_bacon_path(data, actor_id):
    return get_path(data, 4724, actor_id)   # Kevin Bacon의 ID는 4724

def get_path(data, center_id, actor_id):
    """
        Parameter:
            * center_id: center_id가 4724일 때는 Bacon path

        Return:
            * path: center_id로 시작하여 actor_id로 끝나는 list
    """
    coactorDict = data_into_coactor_dict(data)

    ANactorList = []    # ANactorList[i]: AN i를 갖는 배우 ID의 set ({actor_id_1, actor_id_2, ...})
    n = 0
    pathExist = True
    while True:     # ANactorList를 만들자; len(ANactorList) = actor_id의 AN
        junc_ids = get_ids_with_actor_number(coactorDict, center_id, n)[0]
        if actor_id in junc_ids:
            break
        elif len(junc_ids) == 0:    # path가 존재하지 않으면
            pathExist = False
            break
        ANactorList.append(junc_ids)
        n += 1

    if not pathExist:   # path가 존재하지 않으면
        return None
    else:
        path = [actor_id]     # path를 거꾸로 탐색하자
        for i in range(n):
            for id in ANactorList[-(i+1)]:
                if id in coactorDict[path[i]]:
                    path.append(id)
                    break
        path.reverse()    # path는 center_id로 시작하고 actor_id로 끝난다
        return path
{% endhighlight %}

다음과 같이 `get_bacon_path`를 테스트하였다. `large.json`에서 Kevin Bacon - Malena Alterio path를 구하는 코드는 `Lenovo Ideapad S340 (Ryzen 5)`으로 실행한 결과 135초 ~ 140초가 소요된다.
{% highlight ruby linenos=table %}
import jason
import time

with open('resources/small.json') as f:
    smalldb = json.load(f)

print(get_bacon_path(smalldb, 6908))    # BN 1 (len(bacon_path) should be 2)
print(get_bacon_path(smalldb, 2561))    # BN 2 (len(bacon_path) should be 3)
print(get_bacon_path(smalldb, 10500))   # BN 3 (len(bacon_path) should be 4)

with open('resources/large.json') as f:
    largedb = json.load(f)

# What is the path of actors from Kevin Bacon to Malena Alterio (BN 5) in large.json?
start = time.time()
print('\nThe path from Kevin Bacon - Melana Alterio in large.json:',
      get_bacon_path(largedb, namesDict['Malena Alterio']))
end = time.time()
print('get_bacon_path (BN 5) in large.json:', end-start, 's')   # 135 ~ 140 s
{% endhighlight %}

{% highlight language %}
  >>   [4724, 6908]
  >>   [4724, 1532, 2561]
  >>   [4724, 2876, 16927, 10500]
  >>
  >>   The path from Kevin Bacon - Melana Alterio in large.json: [4724, 6159, 3872, 16441, 34020, 96428]
  >>   get_bacon_path (BN 5) in large.json: 136.328125 s
{% endhighlight %}

또, 다음과 같이 `get_path`를 테스트하였다. `Lenovo Ideapad S340 (Ryzen 5)`으로 실행한 결과 35초 ~ 40초가 소요된다.
{% highlight ruby linenos=table %}
import jason
import time

with open('resources/large.json') as f:
    largedb = json.load(f)

# What is the minimal path of actors from Al Hoxie to Betsy Palmer in large.json?
start = time.time()
print('The path from Al Hoxie - Betsy Palmer in large.json:',
      get_path(largedb, namesDict['Al Hoxie'], namesDict['Betsy Palmer']))
end = time.time()
print('get_path (AN 6) in large.json:', end-start, 's')   # 35 ~ 40 s
{% endhighlight %}

{% highlight language %}
  >>   The path from Al Hoxie - Betsy Palmer in large.json: [1408949, 14664, 8841, 11147, 32, 4724, 37469]
  >>   get_path (AN 6) in large.json: 37.790527 s
{% endhighlight %}<br/>

### 4. 끝맺음
이것으로 [MIT OCW 6.009] Fundamentals of Programming (2019년 가을) 강의의 두 번째 문제, [Lab 2: Bacon Number][bacon-number] 풀이를 완료하였다. 상술한 테스트 외에, 문제 템플릿에서 주어진 테스트도 모두 통과하는 것을 확인하였다. 시간 단축을 위해 최대한 `list` 대신 `dictionary` 및 `set`를 활용하였다. 추가 시간 단축을 위해서는 어떻게 더 효율적으로 재귀 호출을 할지 고민해야 할 것 같다. 사실 breadth-first search (BFS) 개념을 이 뒤에 알게 되어 미흡한 부분이 있다. MIT에서 제공한 <a href="{{site.baseurl}}/assets/files/6.009-lab2-solution.py" download>solution</a>을 참고하자. 이 solution은 2020 봄 버전이라 `json` 대신 `pickle` 파일을 사용한다.

[bacon-number]: https://py.mit.edu/fall19/labs/lab2
