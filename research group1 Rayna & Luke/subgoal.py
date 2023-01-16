import heapq
from algorithm import Algorithm
import time

DIRECTIONS = ['N','S','E','W','NE','NW','SE','SW']
CARDINAL = ['N','S','W','E']
DIAGONAL = {'NE':['N','E'],'NW':['N','W'],'SE':['S','E'],'SW':['S','W']}
# each diagonal direction has two corresponding cardinal direction

class SubgoalGraph(Algorithm):
    def __init__(self,grid,markup):
        self.grid = grid
        self.markup = markup
        self.subgoal_graph = {}
        self.clearances = {}
        self.path = []

    def ConstructSubgoalGraph(self):
        graph = {}
        for cell in self.grid.each_cell():
            if self.markup[cell] != '*':
                for each in CARDINAL:
                    if each == 'N':
                        if cell.north and cell.east:
                            if self.markup[cell.northeast] == '*':
                                if self.markup[cell.north] != '*' and self.markup[cell.east] != '*':
                                    graph[cell] = []
                    elif each == 'E':
                        if cell.south and cell.east:
                            if self.markup[cell.southeast] == '*':
                                if self.markup[cell.south] != '*' and self.markup[cell.east] != '*':
                                    graph[cell] = []
                    elif each == 'S':
                        if cell.south and cell.west:
                            if self.markup[cell.southwest] == '*':
                                if self.markup[cell.south] != '*' and self.markup[cell.west] != '*':
                                    graph[cell] = []
                    elif each == 'W':
                        if cell.west and cell.north:
                            if self.markup[cell.northwest] == '*':
                                if self.markup[cell.north] != '*' and self.markup[cell.west] != '*':
                                    graph[cell] = []
        for vertex in graph.keys():
            DHRpoints = self.GetDirectHReachable(vertex,graph)
            for each in DHRpoints:
                graph[vertex].append(each)
        return graph

    def ConnectToGraph(self, s):
        if s not in self.subgoal_graph.keys():
            self.subgoal_graph[s] = []
            DHRpoints = self.GetDirectHReachable(s,self.subgoal_graph)
            for each in DHRpoints:
                self.subgoal_graph[s].append(each)
                self.subgoal_graph[each].append(s)

    def FindAbstractPath(self,start_cell,goal_cell):
        abstract_path = []
        original_graph = self.subgoal_graph.copy()
        self.ConnectToGraph(start_cell)
        self.ConnectToGraph(goal_cell)
        '''
        using A* algorithm to find a shortest path on the modified subgoal graph
        '''
        frontier = []
        came_from = {}
        cost_so_far = {}
        found_target = False
        heapq.heappush(frontier,(0,start_cell))
        cost_so_far[start_cell] = 0
        while frontier:
            priority,current = heapq.heappop(frontier)
            if current == goal_cell:
                #early exit
                found_target = True
                break
            for each in self.subgoal_graph[current]:
                new_cost = cost_so_far[current] + current.octile_distance(each)
                if(each not in cost_so_far.keys() or new_cost < cost_so_far[each]):
                    cost_so_far[each] = new_cost
                    priority = each.octile_distance(goal_cell)
                    priority += new_cost
                    heapq.heappush(frontier,(priority,each))
                    came_from[each] = current
        self.subgoal_graph = original_graph
        if found_target:
            current = goal_cell
            while current != start_cell:
                abstract_path.insert(0,current)
                current = came_from[current]
            abstract_path.insert(0, current)
            return abstract_path
        else:
            return None

    def FindPath(self,start_cell,goal_cell):
        path = self.TryDirectPath(start_cell,goal_cell)
        if path:
            return path
        abstract_path = self.FindAbstractPath(start_cell,goal_cell)
        if not abstract_path:
            return None
        path = []
        for i in range(len(abstract_path)-1):
            cell1 = abstract_path[i]
            cell2 = abstract_path[i+1]
            mid_path = self.FindHReachablePath(cell1,cell2)
            if mid_path:
                for cell in mid_path:
                    if cell not in path:
                        path.append(cell)
        return path

    def FindHReachablePath(self,start,goal):
        '''
        use DFS to find path between 2 cells
        '''
        path = []
        frontier = [start]
        came_from = {}
        came_from[start] = None
        while frontier:
            current = frontier.pop()
            if current == goal:
                find_target = True
                break
            for neighbor in current.quater_neighbors(goal):
                if neighbor not in came_from and self.markup[neighbor] != '*':
                    frontier.append(neighbor)
                    came_from[neighbor] = current
        if find_target:
            while current != start:
                path.insert(0,current)
                current = came_from[current]
            path.insert(0,current)
        return path

    def IsSubgoal(self,cell,graph):
        if cell in graph:
            return True
        else:
            return False

    def Clearance(self,cell,d,graph):
        if self.markup[cell] == '*':
            return None
        i = 0
        if d == 'E':
            while True:
                if cell.east == None:
                    return i
                if self.markup[cell.east] == '*':
                    return i
                i = i + 1
                cell = cell.east
                if self.IsSubgoal(cell,graph):
                    return i
        elif d == 'SE':
            while True:
                if cell.southeast == None:
                    return i
                if self.markup[cell.southeast] == '*':
                    return i
                if self.markup[cell.south] == '*' or self.markup[cell.east] == '*':
                    return i
                i = i + 1
                cell = cell.southeast
                if self.IsSubgoal(cell,graph):
                    return i
        elif d == 'S':
            while True:
                if cell.south == None:
                    return i
                if self.markup[cell.south] == '*':
                    return i
                i = i + 1
                cell = cell.south
                if self.IsSubgoal(cell,graph):
                    return i
        elif d == 'SW':
            while True:
                if cell.southwest == None:
                    return i
                if self.markup[cell.southwest] == '*':
                    return i
                if self.markup[cell.south] == '*' or self.markup[cell.west] == '*':
                    return i
                i = i + 1
                cell = cell.southwest
                if self.IsSubgoal(cell,graph):
                    return i
        elif d == 'W':
            while True:
                if cell.west == None:
                    return i
                if self.markup[cell.west] == '*':
                    return i
                i = i + 1
                cell = cell.west
                if self.IsSubgoal(cell,graph):
                    return i
        elif d == 'NW':
            while True:
                if cell.northwest == None:
                    return i
                if self.markup[cell.northwest] == '*':
                    return i
                if self.markup[cell.north] == '*' or self.markup[cell.west] == '*':
                    return i
                i = i + 1
                cell = cell.northwest
                if self.IsSubgoal(cell,graph):
                    return i
        elif d == 'N':
            while True:
                if cell.north == None:
                    return i
                if self.markup[cell.north] == '*':
                    return i
                i = i + 1
                cell = cell.north
                if self.IsSubgoal(cell,graph):
                    return i
        elif d == 'NE':
            while True:
                if cell.northeast == None:
                    return i
                if self.markup[cell.northeast] == '*':
                    return i
                if self.markup[cell.north] == '*' or self.markup[cell.east] == '*':
                    return i
                i = i + 1
                cell = cell.northeast
                if self.IsSubgoal(cell,graph):
                    return i


    def calculate_clearance(self):
        clearances = {'E':{},'SE':{},'S':{},'SW':{},'W':{},'NW':{},'N':{},'NE':{}}
        for cell in self.grid.each_cell():
            clearances['E'][cell] = self.Clearance(cell,'E',self.subgoal_graph)
            clearances['SE'][cell] = self.Clearance(cell, 'SE',self.subgoal_graph)
            clearances['S'][cell] = self.Clearance(cell, 'S',self.subgoal_graph)
            clearances['SW'][cell] = self.Clearance(cell, 'SW',self.subgoal_graph)
            clearances['W'][cell] = self.Clearance(cell, 'W',self.subgoal_graph)
            clearances['NW'][cell] = self.Clearance(cell, 'NW',self.subgoal_graph)
            clearances['N'][cell] = self.Clearance(cell, 'N',self.subgoal_graph)
            clearances['NE'][cell] = self.Clearance(cell, 'NE',self.subgoal_graph)
        return clearances

    def GetDirectHReachable(self,cell,graph):
        s = []
        for d in DIRECTIONS:
            if self.clearances:
                value = self.clearances[d][cell]
            else:
                value = self.Clearance(cell,d,graph)
            cell2 = cell.move(d, value)
            if self.IsSubgoal(cell2,graph) and value != 0:
                s.append(cell2)
        for d in DIAGONAL.keys():
            for c in DIAGONAL[d]:
                max = self.Clearance(cell,c,graph)
                diag = self.Clearance(cell,d,graph)
                if self.IsSubgoal(cell.move(c,max),graph):
                    max -= 1
                if self.IsSubgoal(cell.move(d,diag),graph):
                    diag -= 1
                for i in range(1,diag+1):
                    current = cell.move(d,i)
                    j = self.Clearance(current,c,graph)
                    cell2 = current.move(c,j)
                    if j <= max and self.IsSubgoal(cell2,graph):
                        s.append(cell2)
                        j -= 1
                    if j < max:
                        max = j
        return s


    def TryDirectPath(self,start_cell,goal_cell):
        dy = goal_cell.row-start_cell.row
        dx = goal_cell.column-start_cell.column
        abs_dy = abs(dy)
        abs_dx = abs(dx)
        row_step = 1 if dy > 0 else -1
        col_step = 1 if dx > 0 else -1
        row,col = start_cell.row,start_cell.column
        flag = True
        for i in range(0,dy,row_step):
            if not flag:
                break
            for j in range(0,dx,col_step):
                cell = self.grid.cell_at(row+i,col+j)
                if self.markup[cell] == '*':
                    flag = False
                    break
        if flag:
            if abs_dx > abs_dy:
                if (dy>0 and dx >0): # goal cell is southeast of start cell
                    path = [start_cell]
                    current = start_cell
                    for i in range(abs_dy):
                        if self.markup[current] == '*':
                            flag = False
                            break
                        current = current.southeast
                        path.append(current)
                    if flag:
                        for j in range(abs_dx-abs_dy):
                            if self.markup[current] == '*':
                                flag = False
                                break
                            current = current.southeast
                            path.append(current)
                elif (dy<=0 and dx >=0): # goal cell is northeast of start cell
                    path = [start_cell]
                    current = start_cell
                    for i in range(abs_dy):
                        if self.markup[current] == '*':
                            flag = False
                            break
                        current = current.northeast
                        path.append(current)
                    if flag:
                        for j in range(abs_dx-abs_dy):
                            if self.markup[current] == '*':
                                flag = False
                                break
                            current = current.east
                            path.append(current)
                elif (dy<0 and dx <=0): # goal cell is northwest of start cell
                    path = [start_cell]
                    current = start_cell
                    for i in range(abs_dy):
                        if self.markup[current] == '*':
                            flag = False
                            break
                        current = current.northwest
                        path.append(current)
                    if flag:
                        for j in range(min(abs_dx,abs_dy)):
                            if self.markup[current] == '*':
                                flag = False
                                break
                            current = current.west
                            path.append(current)
                else: # goal cell is southwest of start cell
                    path = [start_cell]
                    current = start_cell
                    for i in range(abs_dy):
                        if self.markup[current] == '*':
                            flag = False
                            break
                        current = current.southwest
                        path.append(current)
                    if flag:
                        for j in range(abs_dx-abs_dy):
                            if self.markup[current] == '*':
                                flag = False
                                break
                            current = current.west
                            path.append(current)
            else:
                if (dy>0 and dx >0): # goal cell is southeast of start cell
                    path = [start_cell]
                    current = start_cell
                    for i in range(abs_dx):
                        if self.markup[current] == '*':
                            flag = False
                            break
                        current = current.southeast
                        path.append(current)
                    if flag:
                        for j in range(abs_dy-abs_dx):
                            if self.markup[current] == '*':
                                flag = False
                                break
                            current = current.south
                            path.append(current)
                elif (dy<=0 and dx >=0): # goal cell is northeast of start cell
                    path = [start_cell]
                    current = start_cell
                    for i in range(abs_dx):
                        if self.markup[current] == '*':
                            flag = False
                            break
                        current = current.northeast
                        path.append(current)
                    if flag:
                        for j in range(abs_dy-abs_dx):
                            if self.markup[current] == '*':
                                flag = False
                                break
                            current = current.north
                            path.append(current)
                elif (dy<0 and dx <=0): # goal cell is northwest of start cell
                    path = [start_cell]
                    current = start_cell
                    for i in range(abs_dx):
                        if self.markup[current] == '*':
                            flag = False
                            break
                        current = current.northwest
                        path.append(current)
                    if flag:
                        for j in range(abs_dy-abs_dx):
                            if self.markup[current] == '*':
                                flag = False
                                break
                            current = current.north
                            path.append(current)
                else: # goal cell is southwest of start cell
                    path = [start_cell]
                    current = start_cell
                    for i in range(abs_dx):
                        if self.markup[current] == '*':
                            flag = False
                            break
                        current = current.southwest
                        path.append(current)
                    if flag:
                        for j in range(abs_dy-abs_dx):
                            if self.markup[current] == '*':
                                flag = False
                                break
                            current = current.south
                            path.append(current)
        if flag:
            return path
        else:
            return None

    def get_ready(self):
        '''
        Preprocess:
        1.Build up the subgoal graph
        2.Store the clearance for each cell
        '''
        print("Subgoal Graph Algorithm")
        time1 = time.time()
        self.subgoal_graph = self.ConstructSubgoalGraph()
        self.clearances = self.calculate_clearance()
        time2 = time.time()
        print("Preprocessing time(ms):",(time2- time1)*1000)

    def run(self,start,goal):
        time1 = time.time()
        self.path = self.FindPath(start,goal)
        time2 = time.time()
        print("Running time(ms):",(time2 - time1)*1000)

    def show_result(self):
        for cell in self.grid.each_cell():
            if self.markup[cell] == ' ' or self.markup[cell] =='':
                if self.IsSubgoal(cell,self.subgoal_graph):
                    self.markup[cell] = '?'
                if self.path:
                    if cell in self.path[1:-1]:
                        self.markup[cell] = '.'
                        #if self.IsSubgoal(cell, self.subgoal_graph):
                        #    self.markup[cell] = '?.'
        if self.path:
            distance = 0
            for i in range(len(self.path) - 1):
                distance += self.path[i].octile_distance(self.path[i + 1])
            print("Length of path:",distance)




















