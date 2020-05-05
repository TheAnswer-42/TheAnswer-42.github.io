---
layout: post
title: Bacon Number (Revisited)
subtitle: MIT OCW 6.009 (2020 Spring) Lab 2
date: 2020-04-30
description: # Add post description (optional)
img: 20200430-bacon-number.png # Add image post (optional)
tags: [Python, MIT OCW, 6.009]
author: # Add name author (optional)
---
Python으로 [MIT OCW 6.009] Fundamentals of Programming (2020년 봄) 강의의 두 번째 문제, [Lab 2: Bacon Number][bacon-number]를 다시 풀어보자 (<a href="{{site.baseurl}}/assets/files/6.009-lab2 (2020S).zip" download>문제 템플릿</a>). [저번 풀이][20200415-bacon-number]는 2019년 가을 버전이며, 두 버전은 다음을 제외하고 동일하다:<br>
1. 데이터가 `json` 파일이 아닌 `pickle` 파일로 제공된다.
2. 배우-영화 데이터가 `list`의 list가 아닌 `tuple`의 list로 제공된다.
3. Goal 함수에 맞는 path를 구하는 문제가 추가되었다.
4. 소소하게, 함수 이름이 약간 바뀌었다.<br><br>

*Six Degrees of Separation* 이란 지구상의 한 사람과 다른 한 사람 간에는 최대 6명의 사람이 있다는 이론이다. 본 이론의 할리우드 버전이 바로 *Bacon number* 다. 배우 Kevin Bacon은 0의 Bacon number를 갖는다. Kevin Bacon과 같은 영화에 출연한 배우는 1의 Bacon number를 갖는다. Kevin Bacon과 같은 영화에 출연한 배우와 같은 영화에 출연한 배우는 2의 Bacon number를 갖는다. 즉, 어떤 배우의 Bacon number는 *그 배우를 Kevin Bacon과 떨어뜨려 놓는 최소 영화 수* 로 정의된다.

배우-영화 데이터는 `list`로 제공된다. 이 list는 `(actor_id_1, actor_id_2, film_id)` 형태의 tuple을 원소로 가지며, 이는 `actor_id_1`의 배우와 `actor_id_2`의 배우가 `film_id`의 영화에 출연했다는 의미이다. 본 문제에서는 `small.pickle`과 `large.pickle`의 두 데이터가 제공된다.

한편, 배우 ID-배우 이름 데이터는 `{actor_name: actor_id}` 형태의 `dictionary`로 제공된다. 본 문제에서는 `names.pickle`이 제공된다.<br/><br/>

### **1. Acting Together**
> `acted_together` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `data`: 배우-영화 데이터.<br>
* `actor_id_1`, `actor_id_2`: 두 배우의 ID.<br>

>> <span style="color:#2d8659">**Return:**</span>
* 두 배우가 같은 영화에 출연했으면 `True`, 아니면 `False`.

예를 들어, Kevin Bacon (`id=4724`)과 Steve Park (`id=4025`)은 같은 영화에 출연하지 않았으므로, `acted_together(..., 4724, 4025)`는 `False`를 반환해야 한다.

우선 다음과 같이 영화-배우 데이터로부터 `{actor_id: {coactor_id_1, coactor_id_2, ...}}` 꼴의 `dictionary`를 반환하는 코드를 작성하였다.
{% highlight ruby linenos=table %}
def make_coactorDict(data):
    coactorDict = {}
    for actor_id_1, actor_id_2, _ in data:
        coactorDict.setdefault(actor_id_1, set()).add(actor_id_2)
        coactorDict.setdefault(actor_id_2, set()).add(actor_id_1)
    return coactorDict
{% endhighlight %}

그 후 다음 코드를 작성하였다.
{% highlight ruby linenos=table %}
def acted_together(data, actor_id_1, actor_id_2):
    coactorDict = make_coactorDict(data)
    if actor_id_2 in coactorDict[actor_id_1]:
        return True
    return False
{% endhighlight %}

다음과 같이 위 코드를 테스트하였다.
{% highlight ruby linenos=table %}
import pickle

with open('resources/names.pickle', 'rb') as f:
    nameDict = pickle.load(f)

with open('resources/small.pickle', 'rb') as f:
    smalldb = pickle.load(f)

# Joseph McKenna와 Dan Warry-Smith가 같이 연기했는가?
print('Joseph McKenna and Dan Warry-Smith acted together:',
      acted_together(smalldb, nameDict['Joseph McKenna'], nameDict['Dan Warry-Smith']))

# Josef Sommer와 Stig Olin이 같이 연기했는가?
print('Josef Sommer and Stig Olin acted together:',
      acted_together(smalldb, nameDict['Josef Sommer'], nameDict['Stig Olin']))
{% endhighlight %}

{% highlight language %}
  Joseph McKenna and Dan Warry-Smith acted together: True
  Josef Sommer and Stig Olin acted together: False
{% endhighlight %}<br/>

### **2. Bacon Number**
> `actors_with_bacon_number` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `data`: 배우-영화 데이터.<br>
* `n`: Bacon number.<br>

>> <span style="color:#2d8659">**Return:**</span>
* 입력한 Bacon number를 갖는 모든 배우들의 ID를 포함하는 `set`.

Bacon number가 1인 배우들을 다음과 같이 나타낼 수 있다.
<center><img src="{{site.baseurl}}/assets/img/20200415-bacon-number-1.png" width="400" height="400"></center>
그렇다면 Bacon number가 2인 배우들은 다음과 같이 나타내어진다.
<center><img src="{{site.baseurl}}/assets/img/20200415-bacon-number-2.png" width="400" height="400"></center>
Bacon number가 `i`인 배우들로부터 Bacon number가 `i+1`인 배우들을 구해야 한다.

다음과 같이 코드를 작성하였다. 위에서 작성한 `make_coactorDict`를 사용하였다. Kevin Bacon의 ID는 `4724`이다.
{% highlight ruby linenos=table %}
BACON = 4724

def actors_with_bacon_number(data, n):
    coactorDict = make_coactorDict(data)
    agenda = {BACON}
    seen = {BACON}
    for i in range(n):
        current_actors = set()
        for actor in agenda:    # agenda: Bacon number가 i인 actor IDs의 set
            for coactor in coactorDict[actor]:
                if coactor not in seen:
                    current_actors.add(coactor)
                    seen.add(coactor)
        agenda = current_actors
        if agenda == set():     # Bacon number가 i인 actor가 없으면 i+1인 actor도 없다
            return set()
    return agenda
{% endhighlight %}

이에 추가로, 배우 ID를 이름으로 바꾸는 함수도 작성하였다.
{% highlight ruby linenos=table %}
def ids_into_names(nameDict, ids):
    return [name for name, ID in nameDict.items() if ID in ids]
{% endhighlight %}

다음과 같이 위 코드를 테스트하였다. 저번 풀이에서는 `Lenovo Ideapad S340 (Ryzen 5)`으로 실행할 때 70초 ~ 75초가 소요되었다. 이번 코드로는 약 2초가 소요된다.
{% highlight ruby linenos=table %}
import pickle

with open('resources/large.pickle', 'rb') as f:
    largedb = pickle.load(f)

# large.pickle에서, 누가 Bacon number 6를 갖는가?
start = time.time()
print('Actors of BN 6 in large.pickle:', ids_into_names(nameDict, actors_with_bacon_number(largedb, 6)))
end = time.time()
print('actors_with_bacon_number (BN 6) in large.pickle:', end - start, 's')   # 2019F 풀 때는 70 ~ 75 s
{% endhighlight %}

{% highlight language %}
  Actors of BN 6 in large.pickle: ['Sven Batinic', 'Anton Radacic', 'Vjeran Tin Turk', 'Iva Ilakovac']
  actors_with_bacon_number (BN 6) in large.pickle: 1.9572618007659912 s
{% endhighlight %}<br/>

### **3. Paths**
> `bacon_path` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `data`: 배우-영화 데이터.<br>
* `actor_id`: 배우 ID.<br>

>> <span style="color:#2d8659">**Return:**</span>
* Kevin Bacon으로부터 입력한 배우로 이어지는 배우 ID들의 `list`, 즉 'Bacon path'. Path가 존재하지 않으면 `None`.

예를 들어, Julia Roberts의 Bacon path는 `[4724, 3087, 1204]`이다. 이는 Kevin Bacon (`id=4724`)은 Julia Roberts (`id=1204`)와 같은 영화에 출연한 Robert Duvall (`id=3087`)과 같은 영화에 출연했다는 의미이다. Bacon path는 고유하지 않으며, 도착 배우가 같은 어떤 최단 경로라도 답이 될 수 있다.

> `actor_to_actor_path` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `data`: 배우-영화 데이터.<br>
* `actor_id_1`, `actor_id_2`: 두 배우의 ID.<br>

>> <span style="color:#2d8659">**Return:**</span>
* 입력한 한 배우로부터 입력한 다른 배우로 이어지는 배우 ID들의 `list`. Path가 존재하지 않으면 `None`.

Kevin Bacon은 사실 특별한 사람이 아니며, 다른 어떤 배우를 중심으로도 path를 찾을 수 있다. 역시 출발 배우와 도착 배우가 같은 어떤 최단 경로라도 답이 될 수 있다.

> `actor_path` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `data`: 배우-영화 데이터.<br>
* `actor_id`: 출발점으로 삼을 배우의 ID.<br>
* `goal_test`: 배우 ID를 입력받아 조건에 맞으면 `True`, 아니면 `False`를 반환하는 `function`.<br>

>> <span style="color:#2d8659">**Return:**</span>
* 입력한 한 배우로부터 `goal_test`를 만족하는 다른 배우로 이어지는 배우 ID들의 `list`. Path가 존재하지 않으면 `None`.

`Dictionary` 형태의 first-in first-out (FIFO) queue를 이용한 breadth-first search (BFS)를 수행하기 위해 우선 다음과 같이 코드를 작성하였다.
{% highlight ruby linenos=table %}
def get_next_in_queue(queue):
    """Dictionary queue에서 가장 오래된 원소를 제거하고 반환 (FIFO)"""
    next_key = queue['oldest']
    next_item = queue[next_key]
    del queue[next_key]
    queue['oldest'] += 1
    return next_item

def add_to_queue(queue, item):
    """Dictionary queue에 새로운 원소를 추가"""
    queue['newest'] += 1
    queue[queue['newest']] = item
{% endhighlight %}

그 후 다음 코드를 작성하였다. 위에서 작성한 `make_coactorDict`를 사용하였다.
{% highlight ruby linenos=table %}
BACON = 4724

def bacon_path(data, actor_id):
    return actor_to_actor_path(data, BACON, actor_id)

def actor_to_actor_path(data, actor_id_1, actor_id_2):
    return actor_path(data, actor_id_1, lambda ID: ID == actor_id_2)

def actor_path(data, actor_id, goal_test):
    coactorDict = make_coactorDict(data)
    pathQueue = {'oldest': 0, 'newest': 0, 0: [actor_id]}
    seen = {actor_id}
    # add_to_queue를 안 하고 계속 get_next_in_queue를 하면 (모든 coactor들이 seen에 있으면)
    # 'oldest'의 value가 'newest'의 value를 초과하게 되어 None 반환
    while pathQueue['oldest'] <= pathQueue['newest']:
        path = get_next_in_queue(pathQueue)     # pathQueue에서 다음 path 받는다
        node = path[-1]                         # 각 path의 마지막 ID가 node가 된다
        if goal_test(node):
            return path
        for coactor in coactorDict[node]:
            if coactor not in seen:
                add_to_queue(pathQueue, path + [coactor])
                seen.add(coactor)
{% endhighlight %}

다음과 같이 `bacon_path`를 테스트하였다. 저번 풀이에서는 `Lenovo Ideapad S340 (Ryzen 5)`으로 실행할 때 135초 ~ 140초가 소요되었다. 이번 코드로는 약 2초가 소요된다.
{% highlight ruby linenos=table %}
import pickle
import time

with open('resources/large.pickle', 'rb') as f:
    largedb = pickle.load(f)

# large.pickle에서, Kevin Bacon에서 Malena Alterio (BN 5)를 잇는 path는 무엇인가?
start = time.time()
print('The path from Kevin Bacon - Melana Alterio in large.pickle:',
      bacon_path(largedb, nameDict['Malena Alterio']))
end = time.time()
print('bacon_path (BN 5) in large.pickle:', end - start, 's')     # 2019F 풀 때는 135 ~ 140 s
{% endhighlight %}

{% highlight language %}
  The path from Kevin Bacon - Melana Alterio in large.pickle: [4724, 4610, 49895, 107254, 151162, 96428]
  bacon_path (BN 5) in large.pickle: 2.1766457557678223 s
{% endhighlight %}

또, 다음과 같이 `actor_to_actor_path`를 테스트하였다. 저번 풀이에서는 `Lenovo Ideapad S340 (Ryzen 5)`으로 실행할 때 35초 ~ 40초가 소요되었다. 이번 코드로는 역시 약 2초가 소요된다.
{% highlight ruby linenos=table %}
import pickle
import time

with open('resources/large.pickle', 'rb') as f:
    largedb = pickle.load(f)

# large.pickle에서, Al Hoxie에서 Betsy Palmer (AN 6)를 잇는 path는 무엇인가?
start = time.time()
print('The path from Al Hoxie - Betsy Palmer in large.pickle:',
      actor_to_actor_path(largedb, nameDict['Al Hoxie'], nameDict['Betsy Palmer']))
end = time.time()
print('actor_to_actor_path (AN 6) in large.pickle:', end - start, 's')    # 2019F 풀 때는 35 ~ 40 s
{% endhighlight %}

{% highlight language %}
  The path from Al Hoxie - Betsy Palmer in large.pickle: [1408949, 14664, 8841, 19968, 14999, 107373, 37469]
  actor_to_actor_path (AN 6) in large.pickle: 2.04034423828125 s
{% endhighlight %}<br/>

### **4. 끝맺음**
이것으로 [MIT OCW 6.009] Fundamentals of Programming (2020년 봄) 강의의 두 번째 문제, [Lab 2: Bacon Number][bacon-number] 풀이를 완료하였다. 상술한 테스트 외에, 문제 템플릿에서 주어진 테스트도 모두 통과하는 것을 확인하였다. 시간 단축을 위해 최대한 `list` 대신 `dictionary` 및 `set`를 활용하였다. 보름 전의 풀이와 달리 이번에는 recursion을 사용하지 않고 BFS를 적용하였고, 프로그램이 훨씬 효율적인 것을 확인할 수 있었다. 이에 더해 list comprehension 등을 사용해 코드가 간단해지고 가독성도 훨씬 향상되었으므로 장족의 발전을 한 것 같다. 더 궁금한 점은 MIT에서 제공한 <a href="{{site.baseurl}}/assets/files/6.009-lab2-solution.py" download>solution</a>을 참고하자.

[bacon-number]: https://py.mit.edu/spring20/labs/lab2
[20200415-bacon-number]: https://theanswer-42.github.io/bacon-number/
