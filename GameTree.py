from sys import maxsize
from random import randint

class Node:

    def __init__(self,state,action=None,depth=0,parent=None):
        self.point_ = 0
        self.parent = parent
        self.children = []
        self.depth = depth
        self.state = state
        self.action = action
        self.candidates = []

    def add_child(self,state,action):
        child = Node(state,action,self.depth+1,self)
        self.children.append(child)


    def calculate(self):
        if self.depth%2 == 0:
            self.point = max([child.point for child in self.children])
        else:
            self.point = min([child.point for child in self.children])
        self.candidates = []
        if self.depth == 0:
            self.candidates = [child.action for child in self.children if child.point == self.point]
            # for child in self.children:
            #     if self.point == child.point:
            #         self.candidates.append(child.action)

    @property
    def point(self):
        return self.point_

    @point.setter
    def point(self,value):
        self.point_ = value
        if self.parent:
            self.parent.calculate()

    def show(self):
        indent = "     "
        print(indent*self.depth,self.point)
        for child in self.children:
            child.show()
