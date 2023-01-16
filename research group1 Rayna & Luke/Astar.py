import heapq
from algorithm import Algorithm
import time
class Astar(Algorithm):
    def __init__(self,grid,markup):
        self.grid = grid
        self.markup = markup
        self.path = []
        self.visited = []

    def search(self,start_cell,goal_cell):
        visited=[]
        frontier = []
        came_from = {}
        cost_so_far = {}
        found_target = False
        heapq.heappush(frontier, (0, start_cell))
        cost_so_far[start_cell] = 0
        while frontier:
            priority, current = heapq.heappop(frontier)
            if current not in visited:
                visited.append(current)
            if current == goal_cell:
                # early exit
                found_target = True
                break
            for each in current.neighbors():
                new_cost = cost_so_far[current] + current.octile_distance(each)
                if (self.markup[each] != '*' and (each not in cost_so_far.keys() or new_cost < cost_so_far[each])):
                    cost_so_far[each] = new_cost
                    priority = each.octile_distance(goal_cell)
                    priority += new_cost
                    heapq.heappush(frontier, (priority, each))
                    came_from[each] = current
        if found_target:
            path = []
            current = goal_cell
            while current != start_cell:
                path.insert(0, current)
                current = came_from[current]
            path.insert(0, current)
        return visited,path

    def run(self,start,goal):
        print("A* Algorithm")
        time1 = time.time()
        self.visited,self.path = self.search(start,goal)
        time2 = time.time()
        print("Running time(ms):", (time2 - time1) * 1000)

    def show_result(self):
        for cell in self.grid.each_cell():
            if self.markup[cell] != '*' and self.markup[cell] != '!':
                if cell in self.visited:
                    self.markup[cell] = '?'
                if self.path:
                    if cell in self.path[1:-1]:
                        self.markup[cell] = '.'
        if self.path:
            distance = 0
            for i in range(len(self.path) - 1):
                distance += self.path[i].octile_distance(self.path[i + 1])
            print("Length of path::",distance)


