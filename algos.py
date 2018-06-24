from random import choice
from copy import deepcopy
from GameTree import Node
import pandas as pd

BLACK, WHITE = "BLACK", "WHITE"

##############################
#  basic algos
##############################

def check_reversible(board,x,y,player):
    from Game import Stone
    isReversible = False
    reversibles = []
    if isinstance(board[x][y],Stone):
        return isReversible,reversibles
    directions = iter([(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)])
    for direction in directions:
        stones = []
        for i in range(1,len(board)):
            x_ = direction[0]
            y_ = direction[1]
            if not(0 <= x+x_*i < len(board) and  0 <= y+y_*i < len(board)):
                break
            else:
                target = board[x+x_*i][y+y_*i]
                if i == 1:
                    if not(isinstance(target,Stone)):
                        break
                    else:
                        if target.player == player:
                            break
                        else:
                            stones.append(target)
                else:
                    if not(isinstance(target,Stone)):
                        break
                    else:
                        if target.player == player:
                            isReversible =  True
                            reversibles.extend(stones)

                            break
                        else:
                            stones.append(target)
    reversibles = list(set(reversibles))
    return isReversible,reversibles

def check_puttable(board,player):
    N = len(board)
    puttables = [(i,j) for i in range(N) for j in range(N) if check_reversible(board,i,j,player)[0]]
    isPuttable = bool(len(puttables))
    return isPuttable, puttables

##############################
#  romdom algo
##############################

def random_algo(game,puttables):
        return choice(puttables)

##############################
#  get corner algo
##############################

def get_corner(board,player,puttables):
    N = len(board) - 1
    for candidate in puttables:
        if candidate in ((0,0),(0,N),(N,0),(N,N)):
            return candidate
    return False

def corner_algo(game,puttables):
    board = game.board.board
    player = game.on_player
    corner = get_corner(board,player,puttables)
    if corner:
        return corner
    else:
        return random_algo(game,puttables)

##############################
#  maxmize reversibles algo
##############################

def get_maximums(game,puttables):
    board = game.board.board
    player = game.on_player
    maximum = 0
    candidates = []
    for puttable in puttables:
        x,y = puttable
        reversibles = check_reversible(board,x,y,player)[1]
        if len(reversibles) > maximum:
            maximum = len(reversibles)
            candidates = [puttable]
        elif len(reversibles) == maximum:
            candidates.append(puttable)
    return candidates

def maximum_algo(game,puttables):
    maximums = get_maximums(game,puttables)
    return random_algo(game,maximums)

def corner_maximum_algo(game,puttables):
    board = game.board.board
    player = game.on_player
    corner = get_corner(board,player,puttables)
    if corner:
        return corner
    else:
        return maximum_algo(game,puttables)

##############################
#  minimax algo(game tree)
##############################

def populate_tree(node,i=0,depth=3):
    game = node.state
    isPuttable,puttables = check_puttable(game.board.board,game.on_player)
    if not(isPuttable):
        if node.state.on_player == WHITE:
            node.point = next(node.state.players).point
            next(node.state.players)
        else:
            node.point = node.state.on_player.point
        return
    for puttable in puttables:
        x,y = puttable
        new_game = deepcopy(game)
        reversibles = check_reversible(new_game.board.board,x,y,new_game.on_player)[1]
        new_game.put_stone(x,y)
        for stone in reversibles:
            stone.reverse(new_game.on_player)
        new_game.on_player = next(new_game.players)
        node.add_child(new_game,puttable)
    i += 1
    for child in node.children:
        if i < depth:
            populate_tree(child,i,depth)
        elif i == depth:
            child.point = next(child.state.players).point
            next(child.state.players)

def minimax_algo(game,puttables):
    tree = Node(game)
    populate_tree(tree)
    candidates = tree.candidates
    return choice(candidates)

##############################
#  Q_learning algo
##############################

def action_values_black4_algo(game,puttables):
    action_values = pd.read_csv("action_values/av_b_4.csv",index_col=0)
    state = game.board.id_num
    if state in action_values.index:
        row = action_values.ix[state]
        posi = choice(row[row.values == row.max()].index)
        x,y =int(posi[1]),int(posi[4])
    else:
        x,y = random_algo(game,puttables)
    return x,y

def action_values_white4_algo(game,puttables):
    action_values = pd.read_csv("action_values/av_w_4.csv",index_col=0)
    state = game.board.id_num
    if state in action_values.index:
        row = action_values.ix[state]
        posi = choice(row[row.values == row.max()].index)
        x,y =int(posi[1]),int(posi[4])
    else:
        x,y = random_algo(game,puttables)
    return x,y
