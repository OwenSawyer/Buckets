# - 2 Empty buckets A & B, having M & N Litres
# - k litres goal (either bucket), k <= max(m,n)
# - Moves:
#    -Fill
#    -Empty
#    -Move water b/w buckets (a->b or b->a) (only as much as possible!)
#
import copy
from random import randint

class Stack():
    def __init__(self):
        self.stack = []
        
    def isempty(self):
        return self.stack == []    

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            print ("Sorry, cannot pop an empty stack")
            
    def top(self):
        return self.stack[-1]
            
class Queue:
    def __init__(self):
        self.items = []

    def isempty(self):
        return self.items == []

    def push(self, item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop()

def BucketMeasure(m,n,k):
    path = Stack()    #items -> (state, move)
    
    path = BFS((0,0), path, m, n, k)
    path = pathfix(path)
    if path.isempty():
        return NIL
    else:
        while not (path.isempty()):
            current = path.pop()    #tuple
            tuplestate = current[0]   #state is a tuple (m,n)
            state = str(tuplestate)
            rule = current[1]    #move is between 0-6
            
            if (rule==0):
                print('\nbegin:             ' + state) 
            elif (rule==1):
                print('fill A:            ' + state) 
            elif (rule==2):
                print('fill B:            ' + state) 
            elif (rule==3):
                print('empty A:           ' + state) 
            elif (rule==4):
                print('empty B:           ' + state) 
            elif (rule==5):
                print('pour B into A:     ' + state) 
            elif (rule==6):
                print('pour A into B:     ' + state) 
    
                    
                    
def BFS(start, path, m, n, k):
    Q = Queue()
    goal = (-1,-1)       #initial value

    parent = {}     #dictionary
    #key-> current state    
    #value-> tuple (state,move) of parent that led to current state
    
    Q.push(start)   #(0,0)
    parent[start] = (start,0)
    while not (Q.isempty()):
        state = Q.pop()        #front item (tuple)
        if (state[0] == k or state[1] == k):    #current is target state
            goal = state
            break
        
        if (state[0] < m):           #fill bucket A
            new = (m, state[1])
            if not (new in parent):      #only visit if not visited before
                Q.push(new)
                parent[new] = (state, 1)
                
        if (state[1] < n):           #fill bucket B
            new = (state[0], n)
            if not (new in parent):     
                Q.push(new)
                parent[new] = (state, 2)        
        
        if (state[0] > 0):           #empty bucket A
            new = (0, state[1])
            if not (new in parent):    
                Q.push(new)
                parent[new] = (state, 3)               
                                       
        if (state[1] > 0):           #fill bucket B
            new = (state[0], 0)
            if not (new in parent):     
                Q.push(new)
                parent[new] = (state, 4)             
                

        if (state[1] > 0):           #pour B into A
            new = (min(state[0]+state[1], m), max(state[0]+state[1]-m, 0))
               #fill A as much as possible, leave remainder in B
            if not (new in parent):     
                Q.push(new)
                parent[new] = (state, 5)        
                                                         
        if (state[0] > 0):           #pour A into B
            new = (max(state[0]+state[1] - n,0), min(state[0]+state[1], n))
            if not (new in parent):     
                Q.push(new)
                parent[new] = (state, 6)         
    
  

    if (goal != (-1,-1)):     #target was found
        path.push((goal,0))
            # generate the path through previous parents of goal   
            # state (in the dict) that led to goal state.
        while (parent[path.top()[0]][1] != 0):
            path.push(parent[path.top()[0]])
    return path

#path = [((2, 4), 0), ((3, 3), 6), ((0, 3), 1), ((3, 0), 6), ((0, 0), 1)]
#pathfix(path)
def pathfix(path):
    for item in range(len(path.stack)):
        if (item == (len(path.stack)-1)):
            path.stack[item] = (path.stack[item][0],0)
            break
        else:
            path.stack[item] = (path.stack[item][0],path.stack[item+1][1])
    return path

def reroll(illegal):
    new = randint(1,9)
    if new == illegal:
        new = reroll(illegal)
    return new


class Buckets: #initialize a bucket game
    
    def __init__(self: 'Buckets') -> None:
        self.m = randint(1,10)
        self.n = randint(1,10)
        if (self.n == self.m):
            self.n = reroll(self.m)
        maximum = max(self.m,self.n)
        self.k = randint(1,maximum)
        self.path = Stack()
        self.path = BFS((0,0), self.path, self.m, self.n, self.k)
        self.optimal_moves = len(self.path.stack) - 1
        self.state = (0,0)
        self.move_counter = 0
        self.m_frac = (self.m)/(self.state[0]) if self.state[0] != 0 else 0
        self.n_frac = (self.n)/(self.state[1]) if self.state[1] != 0 else 0
        if (self.optimal_moves== -1):
            self.fix()
        if (self.k == self.m) or (self.k == self.n):
            self.fix()
    
    def fix(self):
        self.m = randint(1,10)
        self.n = randint(1,10)
        if (self.n == self.m):
            self.n = reroll(self.m)
        maximum = max(self.m,self.n)
        self.k = randint(1,maximum)
        self.path = Stack()
        self.path = BFS((0,0), self.path, self.m, self.n, self.k)
        self.optimal_moves = len(self.path.stack) - 1
        if (self.optimal_moves == -1):
            self.fix()
        elif (self.k == self.m) or (self.k == self.n):
            self.fix()        
        else:
            self.state = (0,0)
            self.move_counter = 0
            self.m_frac = (self.m)/(self.state[0]) if self.state[0] != 0 else 0
            self.n_frac = (self.n)/(self.state[1]) if self.state[1] != 0 else 0
            
    
    def re_frac(self):
        self.m_frac = (self.m)/(self.state[0]) if self.state[0] != 0 else 0
        self.n_frac = (self.n)/(self.state[1]) if self.state[1] != 0 else 0        
        
    def fill(self, bucket):
        if bucket == self.m:
            self.state = (m, self.state[1])
        else:
            self.state = (self.state[0], n)
        self.move_counter += 1
        
    def empty(self, bucket):
        if bucket == self.m:
            self.state = (0, self.state[1])
        else:
            self.state = (self.state[0], 0)
        self.move_counter += 1        
        
        
    def exchange(self, bucket_from, bucket_to):
        if bucket_from == self.m:   #m to n
            self.state = (max(self.state[0]+self.state[1] - self.n,0), 
                          min(self.state[0]+self.state[1], self.n))
        else: #n to m
            self.state = (min(self.state[0]+self.state[1], self.m), 
                          max(self.state[0]+self.state[1]-self.m, 0))
        self.move_counter += 1         
    