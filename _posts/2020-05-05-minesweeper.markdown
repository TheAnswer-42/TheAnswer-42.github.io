---
layout: post
title: Minesweeper
subtitle: MIT OCW 6.009 (2020 Spring) Lab 4
date: 2020-05-05
description: # Add post description (optional)
img: 20200505-minesweeper.png # Add image post (optional)
tags: [Python, MIT OCW, 6.009]
author: # Add name author (optional)
---
Python으로 [MIT OCW 6.009] Fundamentals of Programming (2020년 봄) 강의의 네 번째 문제, [Lab 4: Minesweeper][minesweeper]를 풀어보자 (<a href="{{site.baseurl}}/assets/files/6.009-lab4 (2020S).zip" download>문제 템플릿</a>).

*Mines* 는 $$1 \times 1$$의 타일들로 덮인 $$n \times m$$의 직사각형 보드 ($$n$$은 행 수, $$m$$은 열 수)에서 수행하는 게임이다. 타일의 일부는 숨겨진 지뢰를 갖고 있다. 각 턴마다 플레이어는 지뢰가 아닌 타일을 소거한다 (판다). 지뢰를 파면 게임에서 지게 되며, 지뢰를 파지 않고 모든 안전한 타일을 소거하면 이긴다. 안전한 타일을 팔 경우 그 타일에 `0`에서 `8`까지의 숫자가 나타나며, 이는 인접한 타일 중 지뢰를 가진 타일의 수이다. 이에 더해 `0` 타일을 팔 경우 인접한 타일에는 지뢰가 없으므로, 자동으로 소거된다.<br><br>

### **1. An Implementation of *Mines***
본 문제에서, *Mines* `game`은 다음 keys와 values를 갖는 dictionary로 나타낸다.
* `dimensions`: 보드의 치수 `(행 수, 열 수)`의 tuple.
* `board`: 2-D array (lists의 list). `game['board'][r][c]`는 타일 $$(r, c)$$가 폭탄을 가지면 `'.'`, 폭탄을 가지지 않으면 인접 폭탄의 수를 나타내는 정수이다.
* `mask`: 2-D array (lists의 list). `game['mask'][r][c]`는 타일 $$(r, c)$$가 플레이어에게 보이면 `True`, 아니면 `False`이다.
* `state`: 게임의 상태를 나타내는 string. 게임이 진행 중이면 `'ongoing'`, 승리했으면 `'victory'`, 졌으면 `'defeat'`이다. 새로운 게임의 state는 항상 `'ongoing'`이다.

`new_game_2d`를 호출하면 다음 예와 같이 새로운 게임이 생성된다.
{% highlight language %}
  >>>  game = new_game_2d(6, 6, [(3, 0), (0, 5), (1, 3), (2, 3)])
  >>>  dump(game)
  board:
      [0, 0, 1, 1, 2, '.']
      [0, 0, 2, '.', 3, 1]
      [1, 1, 2, '.', 2, 0]
      ['.', 1, 1, 1, 1, 0]
      [1, 1, 0, 0, 0, 0]
      [0, 0, 0, 0, 0, 0]
  dimensions: (6, 6)
  mask:
      [False, False, False, False, False, False]
      [False, False, False, False, False, False]
      [False, False, False, False, False, False]
      [False, False, False, False, False, False]
      [False, False, False, False, False, False]
      [False, False, False, False, False, False]
  state: ongoing
  >>>  render_2d(game)
  [['_', '_', '_', '_', '_', '_'],
   ['_', '_', '_', '_', '_', '_'],
   ['_', '_', '_', '_', '_', '_'],
   ['_', '_', '_', '_', '_', '_'],
   ['_', '_', '_', '_', '_', '_'],
   ['_', '_', '_', '_', '_', '_']]
{% endhighlight %}

플레이어가 `dig_2d`를 호출하여 타일 `(1, 0)`을 파면 다음처럼 된다. 반환 값 `9`는 타일 9개가 밝혀졌다는 의미이다.
{% highlight language %}
  >>>  dig_2d(game, 1, 0)
  9
  >>>  dump(game)
  board:
      [0, 0, 1, 1, 2, '.']
      [0, 0, 2, '.', 3, 1]
      [1, 1, 2, '.', 2, 0]
      ['.', 1, 1, 1, 1, 0]
      [1, 1, 0, 0, 0, 0]
      [0, 0, 0, 0, 0, 0]
  dimensions: (6, 6)
  mask:
      [True, True, True, False, False, False]
      [True, True, True, False, False, False]
      [True, True, True, False, False, False]
      [False, False, False, False, False, False]
      [False, False, False, False, False, False]
      [False, False, False, False, False, False]
  state: ongoing
  >>>  render_2d(game)
  [[' ', ' ', '1', '_', '_', '_'],
   [' ', ' ', '2', '_', '_', '_'],
   ['1', '1', '2', '_', '_', '_'],
   ['_', '_', '_', '_', '_', '_'],
   ['_', '_', '_', '_', '_', '_'],
   ['_', '_', '_', '_', '_', '_']]
{% endhighlight %}<br>

#### **1.1. Render**
> `render_2d` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `game`: 위에서 설명한 구조의 *Mines* 게임.<br>
* `xray`: `True`면 모든 타일을 보이게 하고, `False`면 `game['mask']`가 `True`인 타일만 보이게 한다.<br>

>> <span style="color:#2d8659">**Return:**</span>
* 2D array (lists의 list). 가려진 타일은 `'_'`, 폭탄은 `'.'`, `0` 타일은 `' '`, 인접한 폭탄이 있는 타일은 `'1'`, `'2'` 등으로 나타낸다.

`render_2d`의 예시는 다음과 같다.
{% highlight language %}
  >>>  render_2d({'dimensions': (2, 4),
  ...             'state': 'ongoing',
  ...             'board': [['.', 3, 1, 0],
  ...                       ['.', '.', 1, 0]],
  ...             'mask':  [[False, True, True, False],
  ...                       [False, False, True, False]]}, False)
  [['_', '3', '1', '_'], ['_', '_', '1', '_']]

  >>>  render_2d({'dimensions': (2, 4),
  ...             'state': 'ongoing',
  ...             'board': [['.', 3, 1, 0],
  ...                       ['.', '.', 1, 0]],
  ...             'mask':  [[False, True, False, True],
  ...                       [False, False, False, True]]}, True)
  [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
{% endhighlight %}<br>

> `render_ascii` 함수를 작성하라.
>> <span style="color:#2d8659">**Arguments:**</span>
* `game`: 위에서 설명한 구조의 *Mines* 게임.<br>
* `xray`: `True`면 모든 타일을 보이게 하고, `False`면 `game['mask']`가 `True`인 타일만 보이게 한다.<br>

>> <span style="color:#2d8659">**Return:**</span>
* string-based로 나타낸 게임.

`render_ascii`의 예시는 다음과 같다.
{% highlight language %}
  >>>  print(render_ascii({'dimensions': (2, 4),
  ...                      'state': 'ongoing',
  ...                      'board': [['.', 3, 1, 0],
  ...                                ['.', '.', 1, 0]],
  ...                      'mask':  [[True, True, True, False],
  ...                                [False, False, True, False]]}))
  .31_
  __1_
{% endhighlight %}

위의 두 함수를 모두 작성한 다음, 문제 템플릿과 함께 제공된 `server_2d.py`를 실행하고 `localhost:6009`에 접속하면 게임을 해볼 수 있다.<br><br>

#### **1.2. Refactor**
> 문제 템플릿에 작성되어 있는 함수 `new_game_2d`와 `dig_2d`는 옳게 작성되었으나 가독성과 효율이 좋지 않다. 이 두 함수를 개선해라.<br>

<br>
### **2. *HyperMines* (N-dimensional Mines)**
*HyperMines*는 인접 타일이 8개가 아닌 $$3^n - 1$$ ($$n$$은 차원)이라는 점만 제외하면 2-D *Mines*와 똑같다.

`new_game_nd`를 호출하면 다음 예와 같이 새로운 게임이 생성된다.
{% highlight language %}
  >>>  game = new_game_nd((3, 3, 2), [(1, 2, 0)])
  >>>  dump(game)
  board:
      [[0, 0], [1, 1], [1, 1]]
      [[0, 0], [1, 1], ['.', 1]]
      [[0, 0], [1, 1], [1, 1]]
  dimensions: (3, 3, 2)
  mask:
      [[False, False], [False, False], [False, False]]
      [[False, False], [False, False], [False, False]]
      [[False, False], [False, False], [False, False]]
  state: ongoing
{% endhighlight %}

플레이어가 `dig_nd`를 호출하여 타일 `(2, 1, 0)`을 파면 다음처럼 된다. 반환 값 `1`은 타일 1개가 밝혀졌다는 의미이다.
{% highlight language %}
  >>>  dig_nd(game, (2, 1, 0))
  1
  >>>  dump(game)
  board:
      [[0, 0], [1, 1], [1, 1]]
      [[0, 0], [1, 1], ['.', 1]]
      [[0, 0], [1, 1], [1, 1]]
  dimensions: (3, 3, 2)
  mask:
      [[True, True], [True, True], [False, False]]
      [[True, True], [True, True], [False, False]]
      [[True, True], [True, True], [False, False]]
  state: ongoing
{% endhighlight %}<br>

> `new_game_nd`와 `dig_nd`, `render_nd`를 작성하라.

위의 함수를 모두 작성한 다음, 문제 템플릿과 함께 제공된 `server_nd.py`를 실행하고 `localhost:6009`에 접속하면 게임을 해볼 수 있다.<br><br>

### **3. 문제 풀이**
이번 포스트에서는 문제 풀이를 한꺼번에 하겠다.

우선 2-D *Mines*를 위한 함수들은 다음과 같이 작성하였다. `new_game_2d`, `dig_2d`, `render_2d`는 *HyperMines*를 위한 함수들을 이용하였다.
{% highlight ruby linenos=table %}
def new_game_2d(num_rows, num_cols, bombs):
    return new_game_nd((num_rows, num_cols), bombs)

def dig_2d(game, row, col):
    return dig_nd(game, (row, col))

def render_2d(game, xray=False):
    return render_nd(game, xray=xray)

def render_ascii(game, xray=False):
    return '\n'.join([''.join(row) for row in render_2d(game, xray=xray)])      # row끼리는 \n으로 연결
{% endhighlight %}

다음으로 N-D *HyperMines*를 위한 보조 함수들을 작성하였다. 본 함수들은 모두 재귀적으로 작성되었다. 이는 임의의 차원에 적용할 수 있어야 하므로, iteration이 불가하기 때문이다 (이 경우 차원만큼 for문을 중첩해야 한다).
{% highlight ruby linenos=table %}
def neighbor_indices(loc, dimensions):
    """이웃 타일의 index를 반환하는 generator (귀퉁이 타일에서, 이웃 타일이 없는 경우 반환 X)"""
    if len(dimensions) == 0:
        yield ()
    else:
        yield from ((i,) + j for j in neighbor_indices(loc[1:], dimensions[1:])
                    for i in [loc[0]-1, loc[0], loc[0]+1] if 0 <= i < dimensions[0])

def create_board(fill, dimensions):
    """
    board나 mask를 initialize한다.
    fill은 0 ('board') 또는 False ('mask').
    """
    if len(dimensions) == 1:
        return [fill] * dimensions[0]
    return [create_board(fill, dimensions[1:]) for _ in range(dimensions[0])]

def set_tile(board, loc, val):
    """board 상에서 좌표 loc인 타일을 val로 set"""
    if len(loc) == 1:
        board[loc[0]] = val
    else:
        set_tile(board[loc[0]], loc[1:], val)

def get_tile(board, loc):
    """board 상에서 좌표 loc인 타일을 반환"""
    if len(loc) == 1:
        return board[loc[0]]
    else:
        return get_tile(board[loc[0]], loc[1:])

def all_locs(dimensions):
    """dimensions의 모든 locs를 반환하는 generator"""
    if len(dimensions) == 0:
        yield ()
    else:
        for j in all_locs(dimensions[1:]):
            yield from ((i,) + j for i in range(dimensions[0]))

def is_masked_bomb(board, mask, loc):
    """board 상의 좌표 loc 타일이 가려진 폭탄인지 True/False 반환"""
    if len(loc) == 1:
        return board[loc[0]] != '.' and not mask[loc[0]]
    return is_masked_bomb(board[loc[0]], mask[loc[0]], loc[1:])
{% endhighlight %}

그 후 위 보조 함수들을 이용하여 N-D *HyperMines*를 위한 `new_game_nd`, `dig_nd`, `render_nd`를 작성하였다.
{% highlight ruby linenos=table %}
def new_game_nd(dimensions, bombs):
    board = create_board(0, dimensions)
    for bomb_loc in bombs:
        set_tile(board, bomb_loc, '.')
    mask = create_board(False, dimensions)

    for loc in all_locs(dimensions):
        tile = get_tile(board, loc)
        if tile == 0:   # 폭탄은 무시
            set_tile(board, loc, [get_tile(board, neighbor_loc)
                                  for neighbor_loc in neighbor_indices(loc, dimensions)].count('.'))

    return {'dimensions': dimensions,
            'board': board,
            'mask': mask,
            'state': 'ongoing'}

def dig_nd(game, coordinates):
    if get_tile(game['mask'], coordinates) or game['state'] != 'ongoing':
        return 0

    set_tile(game['mask'], coordinates, True)
    revealed = 1

    if get_tile(game['board'], coordinates) == '.':
        game['state'] = 'defeat'
        return revealed         # return 1

    if get_tile(game['board'], coordinates) == 0:
        for neighbor_loc in neighbor_indices(coordinates, game['dimensions']):
            revealed += dig_nd(game, neighbor_loc)

    for loc in all_locs(game['dimensions']):
        if is_masked_bomb(game['board'], game['mask'], loc):
            return revealed     # 아직 가려진 폭탄이 있으면 계속 'ongoing'
    game['state'] = 'victory'   # 모든 폭탄이 밝혀졌으면 'victory'
    return revealed

def render_nd(game, xray=False):
    rendered_board = create_board(None, game['dimensions'])
    for loc in all_locs(game['dimensions']):
        tile = get_tile(game['board'], loc)
        tile_mask = get_tile(game['mask'], loc)
        # xray와 tile_mask가 False일 때 '_'로 set
        set_tile(rendered_board, loc, '_' if not xray and not tile_mask else ' ' if tile == 0 else str(tile))
    return rendered_board
{% endhighlight %}

문제 템플릿과 함께 주어진 `test.py`의 테스트를 모두 통과하는 것을 확인하였다.<br><br>


### **4. 끝맺음**
이것으로 [MIT OCW 6.009] Fundamentals of Programming (2020년 봄) 강의의 네 번째 문제, [Lab 4: Minesweeper][minesweeper] 풀이를 완료하였다. 재귀 호출을 연습할 수 있는 문제였다. 더 궁금한 점은 MIT에서 제공한 <a href="{{site.baseurl}}/assets/files/6.009-lab4-solution (2020S).py" download>solution</a>을 참고하자.

[minesweeper]: https://py.mit.edu/spring20/labs/lab4
