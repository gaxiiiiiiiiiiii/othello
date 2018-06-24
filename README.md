
# 基本的な使い方


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
    - ● ● ●
    - - - -



```python
for i in range(5):
    print("----------")
    game.turn(show=True)
```

    ----------
    - - - -
    - ○ ○ ○
    - ● ● ●
    - - - -
    ----------
    ● - - -
    - ● ○ ○
    - ● ● ●
    - - - -
    ----------
    ● - - -
    - ● ○ ○
    - ● ● ○
    - - - ○
    ----------
    ● - - ●
    - ● ● ○
    - ● ● ○
    - - - ○
    ----------
    ● - - ●
    ○ ○ ○ ○
    - ● ● ○
    - - - ○



```python
# ゲームセットまでプレイ
game.play_all(show=True) # show:最終局面の表示
```

    --------------------
    ● ● ● ●
    ● ● ● ○
    ● ● ● ○
    ○ ○ ● ○



```python
# 100プレイ試行した結果を表示
results = {"WHITE":0,"BLACK":0}
for i in range(100):
    game = Game(N=4,black_algo=action_values_black4_algo,white_algo=random_algo)
    game.play_all()
    results[game.winner.color] += 1
results
```




    {'BLACK': 64, 'WHITE': 36}



# Q学習AIの作り方


```python
from Q_learning import Q_learning
```


```python
#Q学習の初期化
learner = Q_learning(N=4,            # ボードのマス数
                    player="BLACK") # プレイヤーの色
```


```python
# 学習用対戦相手の戦略アルゴリズム
white_algo = random_algo
```


```python
# 学習の実行
learner.learn(trial_num=10,            # 学習回数
             white_algo = white_algo, # 相手の戦略アルゴリズム
             show=True)               # 学習結果の表示

```

    {'WHITE': 7, 'BLACK': 3}



```python
# 学習結果の保存
learner.save_action_values("action_values/test_data.csv")　# action_valusフォルダの利用を推奨
```


```python
# 学習結果を実装した関数を作成
def test_algo(game,puttables):
    action_values = pd.read_csv("action_values/test_data.csv",index_col=0) # 学習結果の読み込み
    state = game.board.id_num
    if state in action_values.index:
        row = action_values.ix[state]
        posi = choice(row[row.values == row.max()].index)
        x,y =int(posi[1]),int(posi[4])
    else:
        x,y = random_algo(game,puttables)
    return x,y
```


```python
# 作成したAIで対戦
game = Game(N=4,black_algo=test_algo,white_algo=random_algo)
game.play_all(show=True)
```

    --------------------
    ○ ○ ○ ●
    ○ ○ ● ○
    ○ ○ ○ ○
    ● ○ ○ ○


# Q学習同士での学習


```python
# 黒白両方のlearnerを用意
learner_black = Q_learning(N=4,player="BLACK")
learner_white = Q_learning(N=4,player="WHITE")
```


```python
# 黒番のlearner.learnを実行
# white_algoとして、learner_white.evaluatorを使用
learner_black.learn(trial_num=10,white_algo = learner_white.evaluator)
```


```python
# learner_blackとlearner_white両方のaction_valuesが学習結果として利用可能
# 既存のaction_values_black4_algoとaction_values_white4_algoは、
# Q学習同士を5万回程対戦させた学習結果を利用している
```

# 参考動画

[全力で人工知能に対決を挑んでみた（理論編）](http://www.nicovideo.jp/watch/sm30440714)


```python

```
