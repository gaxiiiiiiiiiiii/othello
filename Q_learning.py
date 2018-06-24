from Game import Game,random_algo
import pandas as pd
from random import choice
from random import random
from copy import deepcopy
from datetime import datetime
from itertools import cycle

class Q_learning:

    def __init__(self,action_values=None,N=8,alpha=0.2,myu=0.9,rand_rate=0.9,r=100,player="BLACK"):
        self.N     = N
        self.alpha = alpha
        self.myu   = myu
        self.rand_rate = rand_rate
        self.r     = r
        self.last_action = None
        self.last_state  = None
        self.player = player
        if type(action_values) == type(None):
            columns = [(x,y) for x in range(self.N) for y in range(self.N)]
            self.action_values = pd.DataFrame(columns=columns)
        else:
            self.action_values = action_values

    def play_game(self,white_algo=random_algo):
        game = Game(N=self.N,black_algo=self.evaluator,white_algo=white_algo)
        while True:
            game.turn()
            if game.game_set:
                # blackの処理
                self.add_reward(game)
                # whiteの処理
                if game.white_player.algo.__name__ == self.evaluator.__name__:
                    game.white_player.play(game,[])
                break
        return game.winner.color

    def add_reward(self,game):
        Q0 = self.action_values.ix[self.last_state][self.last_action]
        if game.winner.color == self.player:
            Q0 += self.alpha*(self.r - Q0)
        else:
            Q0 += self.alpha*((-1*self.r) - Q0)
        self.action_values.ix[self.last_state,self.last_action] = Q0
        self.last_action,self.last_action = None,None



    def evaluator(self,game,puttables):
        if game.game_set:
            self.add_reward(game)
            return
        state = game.board.id_num
        if state not in self.action_values.index:
            row = {action:0 for action in puttables}
            row = pd.DataFrame(row,index=[state],columns=self.action_values.columns)
            self.action_values = self.action_values.append(row)
        row = self.action_values.ix[state]
        if random() > self.rand_rate:
            x,y = choice(row.dropna().index)
        else:
            x,y = choice(row[row.values == row.max()].index)
        if self.last_action != None and self.last_state != None:
            Q0 = self.action_values.ix[self.last_state,self.last_action]
            Q1 = self.action_values.ix[state,(x,y)]
            value = self.alpha*(self.myu*Q1 - Q0)
            self.action_values.ix[self.last_state,self.last_action] += value
        self.last_state = state
        self.last_action = (x,y)
        return x,y

    def learn(self,trial_num,white_algo=random_algo,show=False):
        result = {"BLACK":0,"WHITE":0}
        for i in range(trial_num):
            winner = self.play_game(white_algo=white_algo)
            result[winner] += 1
        print(result)

    def save_acton_values(self, filename):
        self.action_values.to_csv(filename)
