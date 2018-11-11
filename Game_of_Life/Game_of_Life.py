
from time import sleep
from graphics import *

BLOCK_SIZE = 10
BLOCK_OUTLINE_WIDTH = 2
BOARD_WIDTH  = 30
BOARD_HEIGHT = 30

neighbor_test_blocklist = [(0,0), (1,1)]
toad_blocklist = [(4,4), (3,5), (3,6), (5,7), (6,5), (6,6)]
beacon_blocklist = [(2,3), (2,4), (3,3), (3,4), (4,5), (4,6), (5,5), (5,6)]
glider_blocklist = [(1,2), (2,3), (3,1), (3,2), (3,3)]
pulsar_blocklist = [(2,4), (2,5), (2,6), (4,2), (4,7), (5,2), (5,7),
                    (6,2), (6,7), (7,4), (7,5), (7,6), ]
# for diehard, make board at least 25x25, might need to change block size
diehard_blocklist = [(5,7), (6,7), (6,8), (10,8), (11,8), (12,8), (11,6)]
simple_test = [(4,2), (2,3), (5,3), (2,4), (5,4), (3,5)]
another_list = []


class Block(Rectangle):

    BLOCK_SIZE = 10
    OUTLINE_WIDTH = 1

    def __init__(self,pos, color):
        self.x = pos.x
        self.y = pos.y
        self.color = color
        super().__init__(Point(Block.BLOCK_SIZE*self.x,Block.BLOCK_SIZE*self.y), Point(Block.BLOCK_SIZE*(self.x+1),Block.BLOCK_SIZE*(self.y+1)))
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)
        self.live=False
        self.new_live=False


class Cell(Block):
    """ 
    creates object cell live/dead
    """

    def __init__(self, pos, status=False):
        self.x = pos.x
        self.y = pos.y
        self.pos = pos
        self.status = status
        if self.status:
            self.color = "green"
        else: 
            self.color = "lightgrey"
        super().__init__(self.pos,self.color)

    def get_cell_status(self):
        return self.status

    def get_cell_pos(self):
        return self.pos

    def set_cell_status(self,status):
        self.status = status
        if self.status:
            self.setFill("green")
        else: 
            self.setFill("lightgrey")

    def draw(self, win):
      super().draw(win)

    def undraw(self):
      super().undraw()


class Board():


    def __init__(self, win, x, y, live_status_list):
        self.x = x+1
        self.y = y+1
        self.win = win
        self.status_board={}
        for i in range(1,self.x):
            for j in range(1,self.y): self.status_board[(i,j)] = (Cell(Point(i,j),((i,j) in live_status_list)))

                
    def set_cells_starting_status(self, live_status_list):
        new_dict={}
        for item in self.status_board.keys():
            new_dict.update({item:((item[0],item[1]) in live_status_list)})
        return new_dict

############################## algorithm ##################################################
    def testx(self, item, maxx, status, old_dict):
#    testing neighbours in x coord
        neighbour = 0
        if item[0] > 1.0:
            if (old_dict[(item[0]-1,item[1])]==status):
                neighbour += 1
        if item[0] < maxx: 
            if (old_dict[(item[0]+1,item[1])]==status):
                neighbour += 1
        return neighbour

    def testy(self, item, maxy, status, old_dict):
#    testing neighbours in y coord
        neighbour = 0
        if item[1] > 1.0:
            if (old_dict[(item[0],item[1]-1)]==status):
                neighbour += 1
        if item[1] < maxy: 
            if (old_dict[(item[0],item[1]+1)]==status):
                neighbour += 1
        return neighbour

    def testcorners(self, item, maxx, maxy, status, old_dict):
#    testing neighbours in corners
        neighbour = 0
        if item[0] > 1.0 and item[1] > 1.0:
            if (old_dict[(item[0]-1,item[1]-1)]==status):
               neighbour += 1
        if item[0] < maxx and item[1] > 1:
            if (old_dict[(item[0]+1,item[1]-1)]==status):
                neighbour += 1
        if item[0] > 1.0 and item[1] < maxy:
            if (old_dict[(item[0]-1,item[1]+1)]==status):
                neighbour += 1
        if item[0] < maxx and item[1] < maxy:
            if (old_dict[(item[0]+1,item[1]+1)]==status):
                neighbour += 1
        return neighbour


    def set_new_list(self, maxx, maxy, old_dict):
############## apply neigbourgs test results and set up new dictinary with new values  ########
        new_dict={}
        for item in self.status_board:
            new_dict.update({(item[0],item[1]):False})
            total_live = 0
            total_dead = 0
            total_live = (self.testx((item[0],item[1]),maxx,True,old_dict)\
                         +self.testy((item[0],item[1]),maxy,True,old_dict))\
                         +self.testcorners((item[0],item[1]),maxx,maxy,True,old_dict)
            total_dead = (self.testx((item[0],item[1]),maxx,False,old_dict)\
                         +self.testy((item[0],item[1]),maxy,False,old_dict))\
                         +self.testcorners((item[0],item[1]),maxx,maxy,False,old_dict)
# rule no. 1
            if old_dict[(item[0],item[1])] and total_live  < 2:
                self.status_board[(item[0],item[1])].set_cell_status(False)   
                new_dict[(item[0],item[1])] = False
# rule no. 2
            if old_dict[(item[0],item[1])] and total_live  > 3: 
                self.status_board[(item[0],item[1])].set_cell_status(False) 
                new_dict[(item[0],item[1])] = False
# rule no. 3
            if old_dict[(item[0],item[1])] and (total_live == 2 or total_live == 3): 
                self.status_board[(item[0],item[1])].set_cell_status(True) 
                new_dict[(item[0],item[1])] = True
# rule no. 4
            if not old_dict[(item[0],item[1])] and total_live == 3: 
                self.status_board[(item[0],item[1])].set_cell_status(True)
                new_dict[(item[0],item[1])] = True
        return new_dict

     
    def draw(self, win):
        for item in self.status_board:
           self.status_board[item].draw(win)

    def undraw(self):
        for item in self.status_board:
           self.status_board[item].undraw()


if __name__ == '__main__':    
    # Initalize board

    new_win=GraphWin('Game of Life', 1000, 1000)
    life = Board(new_win, BOARD_WIDTH, BOARD_HEIGHT, diehard_blocklist)
    new_d=life.set_cells_starting_status(diehard_blocklist)
    life.draw(new_win)
    n = 100
    while n > 0:
      sleep(.2)
      new_d=life.set_new_list(BOARD_WIDTH, BOARD_HEIGHT, new_d)
      n -= 1
    
    new_win.mainloop()


    
  





