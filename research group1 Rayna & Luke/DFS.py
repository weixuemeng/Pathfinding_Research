from algorithm import Algorithm
import time

class DFS(Algorithm):
    def __init__(self,grid,markup):
        self.grid = grid
        self.markup = markup
        self.path = []
        self.visited = []

    def search(self,start,goal):
        visited = []
        path = []
        frontier = [start]
        came_from = {}
        came_from[start] = None
        while frontier:
            current = frontier.pop()
            visited.append(current)
            if current == goal:
                find_target = True
                break
            for neighbor in current.neighbors():
                if neighbor not in came_from and self.markup[neighbor] != '*':
                    frontier.append(neighbor)
                    came_from[neighbor] = current
        if find_target:
            while current != start:
                path.insert(0, current)
                current = came_from[current]
            path.insert(0, current)
        return visited,path

    def run(self,start,goal):
        print("DFS")
        time1 = time.time()
        self.visited,self.path = self.search(start,goal)
        time2 = time.time()
        print("Running time:",(time2 - time1)*1000)

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
            print("Length of path:",distance)