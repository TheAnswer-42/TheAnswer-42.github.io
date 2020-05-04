---
layout: post
title: Frugal Maps
subtitle: MIT OCW 6.009 (2020 Spring) Lab 3
date: 2020-05-01
description: # Add post description (optional)
img: 20200501-frugal-maps.jpg # Add image post (optional)
tags: [Python, MIT OCW, 6.009]
author: # Add name author (optional)
---
Python으로 [MIT OCW 6.009] Fundamentals of Programming (2020년 봄) 강의의 세 번째 문제, [Lab 3: Frugal Maps][frugal-maps]를 풀어보자 (<a href="{{site.baseurl}}/assets/files/6.009-lab3 (2020S).zip" download>문제 템플릿</a>).

본 문제에서는 실제 지도 데이터를 다룬다. Nodes의 `list`와 ways의 `list`가 파일로 제공된다. MIT 데이터 세트 (`resources/mit.nodes`, `resources/mit.ways`), Midwest 데이터 세트 (`resources/midwest.nodes`, `resources/midwest.ways`), Cambridge 데이터 세트 (`resources/cambridge.nodes`, `resources/cambridge.ways`)의 세 데이터 세트가 주어진다. 문제 템플릿과 함께 제공된 `util.py`의 `osm_to_serial_pickles`로 파일을 읽을 수 있다.

각 node는 위치를 나타내며, 다음 keys를 가지는 `dictionary`이다.
* `id`: node의 정수 ID.
* `lat`: node의 위도.
* `lon`: node의 경도.
* `tags`: node의 추가 정보를 포함하는 `dictionary`.

각 way는 연결된 nodes의 배열을 나타내며, 다음 keys를 가지는 `dictionary`이다.
* `id`: way의 정수 ID.
* `nodes`: node를 나타내는 정수의 `list`.
* `tags`: way의 추가 정보 (일방통행인지 양방통행인지, 고속도로인지 도보인지 등)를 포함하는 `dictionary`.

Cambridge, Midwest, MIT 데이터 세트 순으로 데이터 크기가 크다. 아래와 같이 Cambridge 데이터 세트는 매우 크므로 효율적으로 코드를 작성해야 한다.
{% highlight ruby linenos=table %}
num_nodes, num_ways = 0, 0

for node in read_osm_data('resources/cambridge.nodes'):
    num_nodes += 1

for way in read_osm_data('resources/cambridge.ways'):
    num_ways += 1

print('In Cambridge data set...')
print('\tTotal number of nodes:', num_nodes)
print('\tTotal number of ways:', num_ways)
{% endhighlight %}

{% highlight language %}
  >>   In Cambridge data set...
  >>      Total number of nodes: 6337751
  >>      Total number of ways: 838004
{% endhighlight %}<br>

### 1. Shortest Paths
> `find_short_path` 함수를 작성하라.
>> <span style="color:#2d8659">**Parameters:**</span>
* `aux_structures`: 특정 자료 구조 (밑 참고).<br>
* `loc1`: 출발 지점의 (위도, 경도) `tuple`. <br>
* `loc2`: 도착 지점의 (위도, 경도) `tuple`.<br>

>> <span style="color:#2d8659">**Return:**</span>
* (위도, 경도) tuple의 `list`로 나타낸 두 지점 사이의 최단 경로. 경로가 존재하지 않으면 `None`.

제공된 데이터에는 차도뿐 아니라 자전거 도로, 인도, 빌딩 등이 포함되어 있다. 우리는 자동차 경로만을 고려할 것이다. 즉, 경로 설계 시 `highway` tag가 있고, 문제 템플릿 상단에 제공된 `ALLOWED_HIGHWAY_TYPES`에 `highway` tag가 포함되어 있는 way만을 고려한다.

둘을 연결하는 way가 있을 경우에만 한 node에서 다른 node로 갈 수 있다. 예를 들어, 다음 두 ways가 있다고 하자.
{% highlight ruby linenos=table %}
w1 = {'id': 1, 'nodes': [1, 2, 3], 'tags': {}}
w2 = {'id': 2, 'nodes': [5, 6, 7], 'tags': {'oneway': 'yes'}}
{% endhighlight %}

이때 `w1`은 양방통행이므로 node `1`에서 `2`, `2`에서 `3`, `3`에서 `2`, `2`에서 `1`이 가능하다. 반면 `w2`는 일방통행이므로 node `5`에서 `6`, `6`에서 `7`은 가능하지만, `7`에서 `6`, `6`에서 `5`는 불가능하다. `tags`에 `oneway` key가 있으면 일방통행, 아니면 양방통행으로 간주한다. 또, node `1`과 `3`을 바로 연결하는 다른 way가 없는 한 `1`에서 `3`으로 바로 가는 것은 불가능하다.

지구의 곡률을 고려하여 두 위치 사이의 거리 (miles)를 구하는 함수가 `util.py`의 `great_circle_distance`로 제공되며, 최단 경로를 구할 때 이 함수를 사용하라.

`find_short_path`에 우리가 고려하지 않는 way (`highway` tag가 없거나 `ALLOWED_HIGHWAY_TYPES`에 속하지 않는 way)에 속한 node도 `loc1`, `loc2`로 들어올 수 있다. 이때는 다음과 같은 과정을 거친다.
1. 우리가 취급하는 ways의 nodes 중, `loc1`에 가장 가까운 node를 구한다.
2. 우리가 취급하는 ways의 nodes 중, `loc2`에 가장 가까운 node를 구한다.
3. 두 nodes 간의 최단 경로를 구한다.

즉, 두 nodes를 구한 뒤에는 처음에 받은 `loc1`, `loc2`를 완전히 무시한다.

`find_short_path`의 arguments인 `aux_structures`는 직접 만들어야 하는 자료 구조이다. 자료 구조가 프로그램 효율에 매우 중요하므로 이를 잘 설계해야 한다. 즉, 최단 경로를 구할 때 전체 데이터를 다 살펴보지 않고도 필요한 질문에 답을 얻을 수 있도록 설계해야 한다. 또한 필요 없는 nodes나 ways는 저장하지 않도록 하는 것이 좋을 것이다.<br><br>

### 2. Improving Runtime with Heuristics
> Heuristic을 사용하여 `find_short_path` 함수의 효율을 높여라.

출발 node로부터 node $$n$$까지의 path cost, $$g(n)$$을 최소화하는 경로가 최단 경로이다. 그러나 $$g(n)$$을 기준으로 경로를 탐색할 경우 최단 경로일 가능성이 없는 경로 (예를 들면 도착 node로부터 멀어지는 경로)를 탐색하느라 시간을 허비하게 된다. 이를 개선하기 위해 heuristic 함수, $$h(n)$$을 도입하라. $$h(n)$$은 node $$n$$에서 도착 node까지의 예측 cost이다. 이로부터 새로운 함수, $$f(n) = g(n) + h(n)$$을 계산할 수 있다. $$f(n)$$은 node $$n$$을 포함하는 최소 cost 경로의 예측 cost이다. 이 $$f(n)$$을 최소화하는 경로를 탐색함으로써 더 효율적으로 최단 경로를 찾을 수 있다. 본 문제에서는 $$h(n)$$ = `great_circle_distance(n, goal)`이 좋은 heuristic 함수가 된다. Heuristic 도입이 경로의 cost를 바꾸면 안 되며, 여러 경로 중 무엇을 먼저 탐색할지, 그 순서만 바꿔야 한다는 것에 주의하자.<br><br>

### 3. Need for Speed (Limits)
> `find_fast_path` 함수를 작성하라.
>> <span style="color:#2d8659">**Parameters:**</span>
* `aux_structures`: 특정 자료 구조 (위 참고).<br>
* `loc1`: 출발 지점의 (위도, 경도) `tuple`. <br>
* `loc2`: 도착 지점의 (위도, 경도) `tuple`.<br>

>> <span style="color:#2d8659">**Return:**</span>
* (위도, 경도) tuple의 `list`로 나타낸 두 지점 사이의 가장 빠른 경로. 경로가 존재하지 않으면 `None`.

위의 `find_short_path`는 거리에 의존하는 최단 경로지만, 사실 경로 설정 시에 우리는 거리가 아닌 시간에 관심이 있다. `find_fast_path`는 거리상 최단 경로가 아닌 가장 빠른 경로를 찾는다. 본 함수의 경우에는 heuristic 함수를 쓰지 않아도 좋다.

Way가 `maxspeed_mph` tag를 가지고 있으면 해당 값이 그 way의 제한 속도 (mph)이다. `maxspeed_mph` tag가 없으면, 문제 템플릿 상단에 제공된 `DEFAULT_SPEED_LIMIT_MPH`에서 그 way의 `highway` 타입을 찾으면 된다.<br><br>

### 4. 문제 풀이
이번 포스트에서는 문제 풀이를 한꺼번에 하겠다.

우선 다음과 같이 nodes, ways 데이터 세트로부터 `{node ID: (경도, 위도), ...}` 꼴의 `dictionary` (`nodeDict`)와 `{node ID: {(way 1 상의 다음 node ID, way 1의 제한 속도), (way 2 상의 다음 node ID, way 2의 제한 속도), ...}}` 꼴의 `dictionary` (`wayDict`)를 만드는 `build_auxiliary_structures`를 작성하였다. 취급하는 `highway`가 아닌 ways는 제외하였고, 그 ways의 nodes도 제외하였다. 이 데이터를 `find_fast_path`에도 사용해야 하기 때문에, 이때 필요한 제한 속도 정보도 포함시켰다.
{% highlight ruby linenos=table %}
from util import read_osm_data, great_circle_distance

ALLOWED_HIGHWAY_TYPES = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified',
    'residential', 'living_street', 'motorway_link', 'trunk_link',
    'primary_link', 'secondary_link', 'tertiary_link',
}

DEFAULT_SPEED_LIMIT_MPH = {
    'motorway': 60,
    'trunk': 45,
    'primary': 35,
    'secondary': 30,
    'residential': 25,
    'tertiary': 25,
    'unclassified': 25,
    'living_street': 10,
    'motorway_link': 30,
    'trunk_link': 30,
    'primary_link': 30,
    'secondary_link': 30,
    'tertiary_link': 25,
}

def build_auxiliary_structures(nodes_filename, ways_filename):
    wayDict = {}
    for way in read_osm_data(ways_filename):
        highway_type = way['tags'].get('highway', None)
        if highway_type in ALLOWED_HIGHWAY_TYPES:               # ALLOWED_HIGHWAY_TYPES가 아니면 무시
            if 'maxspeed_mph' in way['tags']:
                speed_limit = way['tags']['maxspeed_mph']
            else:
                speed_limit = DEFAULT_SPEED_LIMIT_MPH[highway_type]
            for node_id, next_node_id in zip(way['nodes'], way['nodes'][1:]):
                # wayDict: {node_id: {(way 1의 다음 node_id, way 1의 speed_limit),
                #                     (way 2의 다음 node_id, way 2의 speed_limit), ...}, ...}
                #          다음 node_id 없으면 {node_id: set()}
                wayDict.setdefault(node_id, set()).add((next_node_id, speed_limit))
                if way['tags'].get('oneway', 'no') != 'yes':    # 'oneway'가 'yes'가 아니면 two-way
                    # two-way면 반대 way도 추가
                    wayDict.setdefault(next_node_id, set()).add((node_id, speed_limit))
            # path의 마지막 node가 wayDict에 없어도 (다음 node_id 없어도)
            # relevant node이므로 추가해주어야 한다 (node_id: set())
            wayDict.setdefault(way['nodes'][-1], set())

    nodeDict = {}
    for node in read_osm_data(nodes_filename):
        if node['id'] in wayDict:                               # wayDict에 없는 node는 irrelevant node이므로 무시
            nodeDict[node['id']] = (node['lat'], node['lon'])   # nodeDict: {node_id: (node_lat, node_lon), ...}

    return nodeDict, wayDict
{% endhighlight %}

또, 고려하는 way의 nodes 중 고려하지 않는 way의 node에서 가장 가까운 node를 구하는 `find_nearest_node_id`와 node ID의 `list`를 받아 node (위도, 경도)의 `list`를 반환하는 `node_ids_into_locs`를 작성하였다.
{% highlight ruby linenos=table %}
from util import read_osm_data, great_circle_distance

def find_nearest_node_id(loc, nodeDict):
    best = (None, float('inf'))     # 초기값은 무한
    for node_id in nodeDict:
        dist = great_circle_distance(loc, nodeDict[node_id])    # nodeDict[node_id]는 (node_lat, node_lon)
        if dist < best[1]:
            best = (node_id, dist)
    return best[0]

def node_ids_into_locs(path, nodeDict):
    return [nodeDict[node_id] for node_id in path]
{% endhighlight %}

이에 더해, `agenda` (고려 대상인 경로들(과 그 cost)의 목록)에서 cost가 최소인 경로를 반환하는 함수 `get_next_path_and_cost`를 작성하였다. 이렇게 함으로써 도착 node에 도달하는 경로 중 가장 먼저 찾은 경로가 cost가 최소인 경로라는 것이 보장된다.
{% highlight ruby linenos=table %}
def get_next_path_and_cost(agenda, heuristic=False):
    """
    agenda: (heuristic 쓸 때)    {f(n): (path, cost)}
            (heuristic 안 쓸 때) {cost: path}
    agenda에서 가장 f(n) 또는 cost 작은 path와 그 cost 제거 후 반환 (path, cost)
    """
    smallest_f = min(agenda.keys())         # heuristic 쓸 때 f(n), 안 쓸 때 cost
    smallest_f_path = agenda[smallest_f]    # heuristic 쓸 때 (path, cost), 안 쓸 때 path
    del agenda[smallest_f]
    if heuristic:
        return smallest_f_path
    return smallest_f_path, smallest_f
{% endhighlight %}

그 후 이 함수들을 이용하여 `find_optimal_path`를 작성하였다.
{% highlight ruby linenos=table %}
from util import read_osm_data, great_circle_distance

def find_optimal_path(aux_structures, loc1, loc2, cost_function, heuristic=False):
    nodeDict, wayDict = aux_structures

    # loc1_id, loc2_id: 각각 loc1, loc2의 nearest relevant node의 ID
    loc1_id = find_nearest_node_id(loc1, nodeDict)
    loc2_id = find_nearest_node_id(loc2, nodeDict)

    if heuristic:
        agenda = {0: ([loc1_id], 0)}                    # loc1_id가 출발점; agenda = {f(n): (path, cost)}
    else:
        agenda = {0: [loc1_id]}                         # agenda = {cost: path}
    expanded = set()                                    # 이미 분기점으로 쓰인 nodes 저장할 것

    # loc2_id에 도달하지 못하고 cycle 만들면 while문 나가게 되어 None 반환
    while not len(agenda) == 0:
        path, cost = get_next_path_and_cost(agenda, heuristic)
        junc_node_id = path[-1]                         # path의 마지막 node가 junction node가 된다

        if junc_node_id in expanded:                    # cycle 피한다
            continue

        if junc_node_id == loc2_id:                     # loc2_id에 도달하면 path 반환
            return node_ids_into_locs(path, nodeDict)

        expanded.add(junc_node_id)

        # wayDict[node_id]: {(next_node_id, speed_limit), ...}
        for next_node_id, speed_limit in wayDict[junc_node_id]:
            next_cost = cost + cost_function(junc_node_id, next_node_id, speed_limit)
            # heuristic: f(n) = g(n) (지금까지의 cost) + h(n) (앞으로 예측되는 cost)을
            #            최소화하는 path를 다음에 선택할 것
            if heuristic:
                f = next_cost + cost_function(next_node_id, loc2_id, speed_limit)
                agenda[f] = (path + [next_node_id], next_cost)
            else:   # heuristic 쓰지 않으면 cost를 최소화하는 path를 다음에 선택할 것
                agenda[next_cost] = path + [next_node_id]
{% endhighlight %}

다음과 같이 `find_short_path`와 `find_fast_path`를 작성하였다. `find_short_path`에는 heuristic을 도입했고, `find_fast_path`에는 하지 않았다.
{% highlight ruby linenos=table %}
def find_short_path(aux_structures, loc1, loc2):
    nodeDict, _ = aux_structures
    return find_optimal_path(aux_structures, loc1, loc2,
                             lambda id1, id2, _ : great_circle_distance(nodeDict[id1], nodeDict[id2]), True)

def find_fast_path(aux_structures, loc1, loc2):
    nodeDict, _ = aux_structures
    # heuristic 안 쓸 것
    return find_optimal_path(aux_structures, loc1, loc2,
                             lambda id1, id2, speed : great_circle_distance(nodeDict[id1], nodeDict[id2]) / speed)
{% endhighlight %}

문제 템플릿과 함께 주어진 테스트를 모두 통과하는 것을 확인하였다. `Lenovo Ideapad S340 (Ryzen 5)`으로 실행할 때, `find_short_path`의 경우 heuristic을 쓰지 않을 때는 14개 테스트를 72.326초만에 실행하며, heuristic을 쓸 때는 54.358초만에 실행한다. `find_fast_path`의 경우 13개 테스트를 heuristic 없이 75.311초만에 실행하였다.<br><br>


### 5. 끝맺음
이것으로 [MIT OCW 6.009] Fundamentals of Programming (2020년 봄) 강의의 세 번째 문제, [Lab 3: Frugal Maps][frugal-maps] 풀이를 완료하였다. 경로 탐색 시 heuristic 함수의 사용이 프로그램 효율화에 효과적이라는 것을 확인하게 되었다. Weighted shortest path 문제에서 breadth-first search (BFS)도, depth-first search (DFS)도 아닌 새로운 경로 탐색 방법을 시도해 볼 수 있어서 좋았다. 더 궁금한 점은 MIT에서 제공한 <a href="{{site.baseurl}}/assets/files/6.009-lab3-solution (2020S).py" download>solution</a>을 참고하자.

[frugal-maps]: https://py.mit.edu/spring20/labs/lab3
