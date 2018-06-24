

```python
from Game import *

# 戦略アルゴリズム
from algos import random_algo,corner_algo,maximum_algo,corner_maximum_algo # ルールベースAI
from algos import minimax_algo                                             # minimax法AI
from algos import action_values_black4_algo                                # Q学習AI（4*4マス、黒番用）
from algos import action_values_white4_algo                                # Q学習AI（4*4マス、白番用）
```


```python
# gameの初期化
game = Game(N=4,                    #　ボードのマス数
            black_algo=corner_algo, #　黒番のAI
            white_algo=random_algo) #　白番のAI

```


```python
game.turn(show=True) # show:盤面の表示
```

    - - - -
    - ○ ● -
    - ● ● -
    - - ● -



```python
for i in range(5):
    print("----------")
    game.turn(show=True)
```

    ----------
    - - - -
    - ○ ● -
    - ○ ● -
    - ○ ● -
    ----------
    ● - - -
    - ● ● -
    - ○ ● -
    - ○ ● -
    ----------
    ● - - -
    - ● ● -
    - ○ ● -
    - ○ ○ ○
    ----------
    ● - - -
    - ● ● -
    - ● ● -
    ● ○ ○ ○
    ----------
    ● - - -
    - ● ● ○
    - ● ○ -
    ● ○ ○ ○



```python
# ゲームセットまでプレイ
game.play_all(show=True) # show:最終局面の表示
```

    --------------------
    ● ● ● ●
    ○ ● ● ●
    ○ ○ ○ ●
    ● ○ ○ ○



```python
# 100プレイ試行した結果を表示
results = {"WHITE":0,"BLACK":0}
for i in range(100):
    game = Game(N=4,black_algo=action_values_black4_algo,white_algo=random_algo)
    game.play_all()
    results[game.winner.color] += 1
results
```




    {'BLACK': 60, 'WHITE': 40}




```python

```
