from pygame.locals import *
from prepare import Cell
from prepare import Grid
from prepare import Markup
from algorithm import Algorithm
import random
import math
import heapq
import time

class JPS(Algorithm):
    def __init__(self,start,goal,markup):
        super().__init__()
        self.start = start
        self.goal = goal
        self.markup = markup
        
    def implement(self):
        current = self.start
        frontier = []
        heapq.heappush(frontier,(0,current))
        came_from = {}
        cost_so_far = {}
        came_from[current] = None
        cost_so_far[current] = 0
        while len(frontier) != 0:
            cost,current = heapq.heappop(frontier)
        
            if current == self.goal:
                found = True
                break

            successors = self.JPS_search(current, came_from[current])
            for i in successors:
                new_cost = cost_so_far[current]+ self.dist(current,i)
                if i not in cost_so_far or new_cost < cost_so_far[i]:
                    cost_so_far[i] = new_cost
                    heapq.heappush( frontier,(new_cost, i))
                    came_from[i] = current
        current = self.goal
        path = [] # path only with successor

        while current is not None:
            path.insert(0, current)
            current = came_from[current]

        route = self.connect(path)

        return route
    
    def direct(self,current,neib):
        """
        calculate the length between the center of two node
        """
        direction1 = None
        direction2 = None
        norm = math.sqrt(math.pow(neib.row-current.row,2)+ math.pow( neib.column-current.column,2))
        direction_vector = ((neib.row-current.row)/norm, (neib.column-current.column)/norm)

        if norm ==1.0 or norm%1.0 ==0:
            direction1='straight'
            if direction_vector[0]==0 and direction_vector[1]==-1:
                direction2 = 'left'
            elif direction_vector[0]==0 and direction_vector[1]==1:
                direction2 = 'right'
            elif direction_vector[0]==-1 and direction_vector[1]==0:
                direction2 = 'top'
            elif direction_vector[0]==1 and direction_vector[1]==0:
                direction2 = 'bottom'   
            
        else:
            direction1 = 'diagonal'
            if direction_vector[0]<0 and direction_vector[1]<0:
                direction2 = 'left top'
            elif direction_vector[0]<0 and direction_vector[1]>0:
                direction2 = 'right top'
            elif direction_vector[0]>0 and direction_vector[1]<0:
                direction2 = 'left bottom'
            elif direction_vector[0]>0 and direction_vector[1]>0:
                direction2 = 'right bottom'  
            
        return direction1,direction2
    
    def move_direct(self,parent,current):
        norm = math.sqrt(math.pow(current.row-parent.row,2)+math.pow(current.column-parent.column,2))
        if norm==1.0:
            return 'straight'
        else:
            return 'diagonal'
        
    def length(self,path,current):
        
        parent_current = None
        # find the length of the path that include x: dist(parent,x) +dist(x, n)

        if path[1] ==current:
            parent_current = math.sqrt(math.pow(path[1].row-path[0].row,2) + math.pow(path[1].column-path[0].column,2))
        else:
            
            side1 = abs(path[1].row-path[0].row)
            side2 = abs(path[1].column-path[0].column)
            min_side = min(side1,side2)
            max_side = max(side1,side2)
            dia_len = min_side*math.sqrt(2)
            str_len = max_side-min_side
            parent_current = dia_len+str_len
        current_neib = math.sqrt(math.pow(path[2].row-path[1].row,2)+ math.pow(path[2].column- path[1].column,2))
        length = parent_current+ current_neib

        return round(length,5)

    def jump(self,current,direction): # current-x , direction-d, s-start, g-goal

        n = None
        if direction =='left':
            n = self.markup.grid.cell_at(current.row,current.column-1) if current.column-1>=0 else None
        elif direction =='right':
            n = self.markup.grid.cell_at(current.row,current.column+1) if current.column+1<= self.markup.grid.num_columns-1 else None
        elif direction =='top':
            n = self.markup.grid.cell_at(current.row-1,current.column) if current.row-1 >=0 else None
        elif direction =='bottom':
            n = self.markup.grid.cell_at(current.row+1,current.column) if current.row+1<= self.markup.grid.num_rows-1 else None
        elif direction=='left top':
            n = self.markup.grid.cell_at(current.row-1,current.column-1) if current.row-1 >=0 and current.column-1 >=0 else None
        elif direction == 'left bottom':
            n = self.markup.grid.cell_at(current.row+1,current.column-1) if current.row+1 <= self.markup.grid.num_rows-1 and current.column-1 >=0 else None
        elif direction=='right top':
            n = self.markup.grid.cell_at(current.row-1,current.column+1) if current.row-1 >=0 and current.column+1 <= self.markup.grid.num_columns-1 else None
        elif direction =='right bottom':
            n = self.markup.grid.cell_at(current.row+1,current.column+1) if current.row+1 <= self.markup.grid.num_rows-1 and current.column+1 <= self.markup.grid.num_columns-1 else None

        if n is None or self.markup.is_obstacle(n.row,n.column) :
            return None
        if n== self.goal:
            return n

        
        neighbors, forced = self.prune(current,n)# natural- non-grey ??? 8个的，还是只有白色方块算
        if len(forced)!= 0:
            return n
            
        # if d is diagonal
        if direction=='left top':
            for i in ['left','top']:
                if self.jump(n,i) is not None:
                    return n
        elif direction =='left bottom':
            for i in ['left','bottom']:
                if self.jump(n,i) is not None:
                    return n
        elif direction =='right top':
            for i in ['right','top']:
                if self.jump(n,i) is not None:
                    return n
        elif direction =='right bottom':
            for i in ['right','bottom']:
                if self.jump(n,i) is not None:
                    return n
                
        return self.jump(n,direction)
    
    def path_exist(self,current,neib):
        '''decide if path exist'''
        
        if self.direct(current,neib)[1] =='left top':
            if self.markup.get_item_at(current.north.row,current.north.column)=='*' and self.markup.get_item_at(current.west.row,current.west.column)=='*':
                if self.markup.get_item_at(neib.south.row,current.south.column)=='*' and self.markup.get_item_at(current.east.row,current.east.column)=='*':
                    return False
        elif self.direct(current,neib)[1] =='left bottom':
            if self.markup.get_item_at(current.south.row,current.south.column)=='*' and self.markup.get_item_at(current.west.row,current.west.column)=='*':
                if self.markup.get_item_at(neib.north.row,current.north.column)=='*' and self.markup.get_item_at(current.east.row,current.east.column)=='*':
                    return False
        elif self.direct(current,neib)[1] =='right top':
            if self.markup.get_item_at(current.north.row,current.north.column)=='*' and self.markup.get_item_at(current.east.row,current.east.column)=='*':
                if self.markup.get_item_at(neib.south.row,current.south.column)=='*' and self.markup.get_item_at(current.west.row,current.west.column)=='*':
                    return False
        elif self.direct(current,neib)[1] =='right bottom':
            if self.markup.get_item_at(current.south.row,current.south.column)=='*' and self.markup.get_item_at(current.east.row,current.east.column)=='*':
                if self.markup.get_item_at(neib.north.row,current.north.column)=='*' and self.markup.get_item_at(current.west.row,current.west.column)=='*':
                    return False
        else:
            return True
     
                
    def prune(self,parent,current):
        '''
        include :
        copy: the grey cell (non- natural cell)
        forced: list contains the forced neighbors
        neighors: list contains the white cell ( natural cell)
        '''
        
        neighbors = current.neighbors() # initialize neighbor list
        copy = []
        forced = []

        if parent==None: # don't need pruning rules
            neighbors = neighbors

        else : # use pruning rules
            for n in current.neighbors(): # regardless obstacle
                # find the path - this is the roughly methods but could work
                p = []
                for i in n.neighbors():
                    if i is not current:
                        p.append(i) # append the neignbor of neighbor that not obs and not x(current)
                min_value = 10000
                min_cell = None

                for q in p:
                    distance = self.dist(parent,q)
                    if distance < min_value:
                        min_value = min(min_value, distance)
                        min_cell = q # find the min middlecell of the path 
                path1 = [parent,min_cell, n] # not include x ---len(<p(x),...,n>\x)
                path2 = [parent,current, n]  # include x  --- len(<p(x),x,n>)

                direction = self.move_direct(parent,current)
                
                if direction =='straight':
                    if self.length(path1,current)<= self.length(path2,current): # prune rule
                        copy.append(n)
                elif direction =='diagonal':
                    if self.length(path1,current)< self.length(path2,current):
                        copy.append(n)
            

            for n in copy: # find the forced neighbors in non-natural node
                if self.markup.is_obstacle(n.row,n.column)==False:  #forced neighbors is not obstacle
                    # find the path 
                    p = []
                    for i in n.neighbors():
                        if self.markup.is_obstacle(i.row,i.column)==False and i is not current :
                            p.append(i) # append the neignbor of neighbor that not obs and not x
                    min_value = 1000
                    min_cell = None

                    for q in p:
                        distance = self.dist(parent,q)
                        if distance < min_value:
                            min_value = min(min_value, distance)
                            min_cell = q # find the min middlecell of the path
                    path1 = [parent,min_cell, n] # not include x ---len(<p(x),...,n>\x)
                    path2 = [parent,current, n]  # include x  --- len(<p(x),x,n>)

                    if not min_cell or self.length(path1,current)>self.length(path2,current):
                        if n != parent:
                            forced.append(n)

                elif self.markup.is_obstacle(n.row,n.column)==True:
                    neighbors.remove(n)

             # use an empty list, since we cannot modify the item in the list when interate
            copy2=[]
            for n in neighbors:
                copy2.append(n)
            for n in copy2:
                if self.markup.is_obstacle(n.row,n.column) == True:
                    neighbors.remove(n)
                if n in copy and n in neighbors:
                    neighbors.remove(n)
                if n in forced and n not in neighbors:
                    neighbors.append(n)

     
        return neighbors, forced
    
    def JPS_search(self,current,parent):
        '''algorithm1'''
        neighbors = self.prune(parent,current)[0]
        
        successor = [] # empty list
        for n in neighbors:
            s = self.jump( current, self.direct(current,n)[1])
            if isinstance(s,Cell):
                successor.append(s)
            elif isinstance(s,list):
                for jumppoint in s:
                    successor.append(jumppoint)
        return successor
    
    def dist(self,x,y):
        distance =math.sqrt( math.pow(y.row-x.row,2) + math.pow(y.column- x.column,2))

        return distance
    
    def connect(self,path):  # after finding the rough path
        route = []
        for i in range(len(path)-1):   # 0,1
            prev = path[i]
            current= path[i+1]
            prev_row = prev.row
            prev_col= prev.column
            cur_row = current.row
            cur_col = current.column

            if self.direct(prev,current)[1]=='left':
                for i in range(prev_col,cur_col-1,-1):
                    if self.markup.grid.cell_at(prev_row,i) not in route:
                        route.append(self.markup.grid.cell_at(prev_row,i))
            elif self.direct(prev,current)[1] == 'right':
                for i in range(prev_col,cur_col+1):
                    if self.markup.grid.cell_at(prev_row,i) not in route:
                        route.append(self.markup.grid.cell_at(prev_row,i)) 
            elif self.direct(prev,current)[1] =='top':
                for i in range(prev_row,cur_row-1,-1):
                    if self.markup.grid.cell_at(i,prev_col) not in route:
                        route.append(self.markup.grid.cell_at(i,prev_col)) 
            elif self.direct(prev,current)[1] =='bottom':
                for i in range(prev_row,cur_row+1):
                    if self.markup.grid.cell_at(i,prev_col) not in route:
                        route.append(self.markup.grid.cell_at(i,prev_col))
            elif self.direct(prev,current)[1]=='left top':
                i= prev_row
                j = prev_col
                while i>= cur_row and j>= cur_col:
                    if self.markup.grid.cell_at(i,j) not in route:
                        route.append(self.markup.grid.cell_at(i,j)) 
                    i-=1
                    j-=1

            elif self.direct(prev,current)[1]=='left bottom':
                i = prev_row
                j = prev_col
                while i<= cur_row and j>=cur_col:
                    if self.markup.grid.cell_at(i,j) not in route:
                        route.append(self.markup.grid.cell_at(i,j)) 
                    i+=1
                    j-=1

            elif self.direct(prev,current)[1]=='right top':
                i = prev_row
                j = prev_col
                while i>= cur_row and j<=cur_col:
                    if self.markup.grid.cell_at(i,j) not in route:
                        route.append(self.markup.grid.cell_at(i,j)) 
                    i-=1
                    j+=1

            elif self.direct(prev,current)[1]=='right bottom':
                i = prev_row
                j = prev_col
                while i<= cur_row and j<=cur_col:
                    if self.markup.grid.cell_at(i,j) not in route:
                        route.append(self.markup.grid.cell_at(i,j))
                    i+=1
                    j+=1

        return route
    
    def run(self):
        print("JPS")
        time1 = time.time()
        self.implement()
        time2 = time.time()
        print("Running time(ms):",(time2 - time1)*1000)

    def path_length(self,route):
        i = 0
        j = 1
        sumR = 0
        while j<=len(route)-1:
            length = self.dist(route[i],route[j])
            sumR+=length
            i+=1
            j+=1
        return sumR
            
            
        

    def show_result(self,route):
        
        for cell in route:
            self.markup.set_item_at(cell.row,cell.column,'.')

        self.markup.set_item_at(self.start.row, self.start.column,'!')
        self.markup.set_item_at(self.goal.row, self.goal.column, '!')
        length = self.path_length(route)
        print('Length of path:',str(length))
        

        
            
            
        
        
        
    



    
    
