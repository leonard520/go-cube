import sys

class Cube:
    def __init__(self, s):
        self.status = s;
    def f(self):
        hamming = 0
        for value in self.status:
            if value == 0:
                hamming += 1
        return hamming
    def g(self):
        self.f(self)

class Chess:
    def __init__(self, s):
        self.status = s;
    def f(self):
        hamming = 0
        for value in self.status:
            if value == 0:
                hamming += 1
        return hamming
    def g(self):
        self.f(self)
