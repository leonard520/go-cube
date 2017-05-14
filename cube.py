import sys
import time
import copy

class Cube:
    def __init__(self, s):
        self.status = s
    def __eq__(self, other):
        for i in range(0, len(self.status)):
            if self.status[i] != other.status[i]:
                return False
        return True
    def f(self):
        hamming = 0
        for value in self.status:
            if value == 1:
                hamming += 1
        return hamming
    def g(self):
        self.f(self)
    def rotate(self, dir):
        if dir == 'l':
            tmp = self.status[1]
            self.status[1] = self.status[0]
            self.status[0] = self.status[3]
            self.status[3] = self.status[5]
            self.status[5] = tmp

        elif dir == 'r':
            tmp = self.status[1]
            self.status[1] = self.status[5]
            self.status[5] = self.status[3]
            self.status[3] = self.status[0]
            self.status[0] = tmp

        elif dir == 'u':
            tmp = self.status[0]
            self.status[0] = self.status[4]
            self.status[4] = self.status[5]
            self.status[5] = self.status[2]
            self.status[2] = tmp

        elif dir == 'd':
            tmp = self.status[0]
            self.status[0] = self.status[2]
            self.status[2] = self.status[5]
            self.status[5] = self.status[4]
            self.status[4] = tmp
    def dump(self):
        for i in range(0, 6):
            print str(self.status[i]) + ' ',
        print '\n'

class Chess:
    def __init__(self, s, p):
        self.status = s;
        self.position = p
    def __eq__(self, other):
        for i in range(0, 25):
            if self.status[i] != other.status[i]:
                return False
        return self.position == other.position
    def dump(self):
        for i in range(0, 5):
            for j in range(0, 5):
                print str(self.status[i * 5 + j]) + ' ',
            print '\n'
        print self.position
class CubeChess:
    def __init__(self, cube_status, chess_status):
        self.cube_status = cube_status
        self.chess_status = chess_status
        self.value = 0
    def __eq__(self, other):
        return self.cube_status == other.cube_status and self.chess_status == other.chess_status
    def f(self):
        return self.cube_status.f()
    def g(self):
        return self.cube_status.g()
    def is_done(self):
        return self.f() == 6
    def dump(self):
        self.value = self.f()
        self.cube_status.dump()
        self.chess_status.dump()

class GoCube:
    open_list = []
    close_list = []

    def dump(self):
        print "below is open list"
        for v in self.open_list:
            v.dump()
        print "below is close list"
        for v in self.close_list:
            v.dump()

    def next(self):
        status = self.open_list[0]
        if status.is_done() == True:
            return True
        cube = status.cube_status
        chess = status.chess_status

        self.open_list.remove(status)
        self.close_list.append(status)

        [x, y] = [chess.position % 5, chess.position / 5]
        #time.sleep(1)
        if x > 0: # left
            obj_chess = copy.copy(chess)
            obj_cube = copy.copy(cube)

            tmp = obj_chess.status[y * 5 + x - 1]
            obj_chess.status[y * 5 + x - 1] = obj_cube.status[2]
            obj_cube.status[2] = tmp
            obj_cube.rotate('l')
            obj_chess.position = y * 5 + x - 1
            next_item = CubeChess(obj_cube, obj_chess)
            next_item.value = next_item.f()
            #print "left " + str(next_item.value)
            #next_item.dump()
            if next_item not in self.close_list:
                self.open_list.append(next_item)

        #time.sleep(1)
        if y > 0: # up
            obj_chess = copy.copy(chess)
            obj_cube = copy.copy(cube)

            tmp = obj_chess.status[(y - 1) * 5 + x]
            obj_chess.status[(y - 1) * 5 + x] = obj_cube.status[3]
            obj_cube.status[3] = tmp
            obj_cube.rotate('u')
            obj_chess.position = (y - 1) * 5 + x
            next_item = CubeChess(obj_cube, obj_chess)
            next_item.value = next_item.f()
            #print "up " + str(next_item.value)
            #next_item.dump()
            if next_item not in self.close_list:
                self.open_list.append(next_item)

        #time.sleep(1)
        if x < 4: # right
            obj_chess = copy.copy(chess)
            obj_cube = copy.copy(cube)

            tmp = obj_chess.status[y * 5 + x + 1]
            obj_chess.status[y * 5 + x + 1] = obj_cube.status[4]
            obj_cube.status[4] = tmp
            obj_cube.rotate('r')
            obj_chess.position = y * 5 + x + 1
            next_item = CubeChess(obj_cube, obj_chess)
            next_item.value = next_item.f()
            #print "right " + str(next_item.value)
            #next_item.dump()
            if next_item not in self.close_list:
                self.open_list.append(next_item)

        #time.sleep(1)
        if y < 4: # down
            obj_chess = copy.copy(chess)
            obj_cube = copy.copy(cube)

            tmp = obj_chess.status[(y + 1) * 5 + x]
            obj_chess.status[(y + 1) * 5 + x] = obj_cube.status[5]
            obj_cube.status[5] = tmp
            obj_cube.rotate('d')
            obj_chess.position = (y + 1) * 5 + x
            next_item = CubeChess(obj_cube, obj_chess)
            next_item.value = next_item.f()
            #print "down " + str(next_item.value)
            #next_item.dump()
            if next_item not in self.close_list:
                self.open_list.append(next_item)

        self.open_list.sort(key=lambda x: x.value)
        return False


    def run(self, chess_start_status, p):
        cube_zero = Cube([0, 0, 0, 0, 0, 0])
        chess_zero = Chess(chess_start_status, p)
        start = CubeChess(cube_zero, chess_zero)
        start.value = start.f()
        self.open_list.append(start)
        flag = self.next()
        while flag == False and len(self.open_list) > 0:
            flag = self.next()

def testCube():
    c = Cube([0, 1, 0, 1, 0, 1])
    c.rotate('d')
    c.dump()

    c.rotate('u')
    c.dump()

    c.rotate('l')
    c.dump()

    c.rotate('r')
    c.dump()

if __name__ == "__main__":
    start = time.clock()
    s = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0]
    #s = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    puzzle = GoCube()
    puzzle.run(s, 11)

    end = time.clock()
    print end-start
