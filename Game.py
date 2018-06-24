from itertools import cycle
from random import choice
from copy import deepcopy
from algos import *

class Game:

    def __init__(self,N=8,black_algo=random_algo,white_algo=random_algo):
        self.black_player = Player(BLACK)
        self.white_player = Player(WHITE)
        self.black_player.algo = black_algo
        self.white_player.algo = white_algo
        self.board = Board(self.black_player,self.white_player,N)
        self.players = cycle([self.black_player,self.white_player])
        self.on_player = next(self.players)
        self.winner = None
        self._game_set = False
        self.passed = False

    def turn(self,show=False):
        isPuttable,puttables = check_puttable(self.board.board,self.on_player)
        if not(isPuttable):
            if self.passed:
                self.game_set = True
            else:
                self.passed = True
        else:
            self.passed = False
            x,y = self.on_player.play(self,puttables)
            reversibles = check_reversible(self.board.board,x,y,self.on_player)[1]
            self.put_stone(x,y)
            for stone in reversibles:
                stone.reverse(self.on_player)
        self.on_player = next(self.players)
        if show:
            self.board.show()

    def put_stone(self,x,y):
        self.board.board[x][y] = Stone(self.on_player)

    def play_all(self,show=False):
        while not(self.game_set):
            self.turn()
        if show:
            print("--------------------")
            self.board.show()

    def judge(self):
        if self.black_player.point > self.white_player.point:
            self.winner = self.black_player
        else:
            self.winner = self.white_player

    @property
    def game_set(self):
        return self._game_set

    @game_set.setter
    def game_set(self,value):
        self._game_set = value
        self.judge()





class Player:

    def __init__(self,color):
        self.color = color
        self.point = 0
        self.algo = None

    def play(self,game,puttables):
        return self.algo(game,puttables)

class Board:

    def __init__(self,black_player,white_player,N=8):
        if N%2 != 0:
            raise ValueError("N must be even numver")
        n = int(N/2)
        self.board = [[[None] for _ in range(N)] for _ in range(N)]
        self.board[n][n - 1] = Stone(black_player)
        self.board[n - 1][n] = Stone(black_player)
        self.board[n][n]     = Stone(white_player)
        self.board[n-1][n-1] = Stone(white_player)

    def show(self):
        output = ([str(cell) if isinstance(cell,Stone) else "-" for cell in row] for row in self.board)
        for row in [" ".join(row) for row in output]:
            print(row)

    @property
    def id_num(self):
        output = [[str(cell) if isinstance(cell,Stone) else "-" for cell in row] for row in self.board]
        num = ""
        for row in ["".join(row) for row in output]:
            num += row
        num = num.replace("-","0").replace("○","1").replace("●","2")
        num = int(num,3)

        return hex(num)

class Stone:

    def __init__(self, player):
        self.player = player
        self.player.point += 1

    def reverse(self, new_player):
        self.player.point -= 1
        self.player = new_player
        self.player.point += 1


    def __str__(self):
        if self.player.color == BLACK:
            return "●"
        else:
            return "○"



# def trial(num,black_algo,white_algo=None,N=8,show=False):
#     result = {"BLACK":0,"WHITE":0,"DRAW":0}
#     for _ in range(num):
#         print(_)
#         if white_algo:
#             game = Game(N=N,black_algo=black_algo,white_algo=white_algo)
#         else:
#             game = Game(black_algo=black_algo)
#         game.play_all(show)
#         winner = game.winner
#         if winner:
#             result[game.winner.color] += 1
#         else:
#             result["DRAW"] += 1
#     return result
