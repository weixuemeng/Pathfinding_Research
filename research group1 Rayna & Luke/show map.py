import pygame
import pygame.gfxdraw
from pygame.locals import *
from prepare import Cell
from prepare import Grid
from prepare import Markup
import map_design
import subgoal
import Astar
import DFS
import JPS
import time

def main():
    pygame.init()
    running = True
    screen = pygame.display.set_mode([770,770])
    pygame.display.set_caption('Navigation')
    g = Grid(50,50)
    markup = None
    big_map = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == K_q:  # Quit
                    running = False
                elif event.key == K_f:  # Save to FILE
                    pygame.image.save(screen, 'maze.png')
                elif event.key == K_1: # map1
                    start,goal,g,markup,big_map = map_design.map1()
                elif event.key == K_2: # map2
                    start,goal,g,markup,big_map = map_design.map2()
                elif event.key == K_3: # map3
                    start,goal,g,markup,big_map = map_design.map3()
                elif event.key == K_4: # map4
                    start,goal,g,markup,big_map = map_design.map4()
                elif event.key == K_5: # map5
                    start,goal,g,markup,big_map = map_design.map5()
                elif event.key == K_6: # map6
                    start,goal,g,markup,big_map = map_design.map6()
                elif event.key == K_7: # map7
                    start,goal,g,markup,big_map = map_design.map7()
                elif event.key == K_8: # map8
                    start,goal,g,markup,big_map = map_design.map8()
                elif event.key == K_s: # subgoal
                    s = subgoal.SubgoalGraph(g,markup)
                    s.get_ready()
                    s.run(start,goal)
                    s.show_result()
                elif event.key == K_a: # A*
                    a = Astar.Astar(g,markup)
                    a.get_ready()
                    a.run(start,goal)
                    a.show_result()
                elif event.key == K_d: # DFS
                    d = DFS.DFS(g,markup)
                    d.get_ready()
                    d.run(start,goal)
                    d.show_result()
                elif event.key == K_j: #JPS
                    j = JPS.JPS(start,goal,markup)
                    j.run()
                    route = j.implement()
                    j.show_result(route)
        display_grid(g, markup, screen,big_map)
        pygame.display.flip()
    
    

def display_grid(g, markup, screen,big_map):
    screen.fill((255,255,255))
    if big_map:
        r = 15
        n = 10
    else:
        r = 37
        n =15
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            c = g.cell_at(row, col)
            cell_x = col * r + n
            cell_y = row * r + n
            # Draw top row
            if markup:
                value = markup.get_item_at(row, col)
                if not value: # normal
                    pygame.draw.rect(screen,
                                     (222,194,155),  # color
                                     (cell_x, cell_y, r, r))
                if value == '*':  # obstacle
                    pygame.draw.rect(screen,
                                     (34,28,18),  # color
                                     (cell_x, cell_y, r, r))
                if value =='!':  #start, goal
                    pygame.draw.rect(screen,
                                     (202,255,112),  # color
                                     (cell_x, cell_y, r, r))
                if value == '?': # keypoint
                    pygame.draw.rect(screen,
                                       (202,225,255),
                                       (cell_x,cell_y,r,r))  #filled
                if value == '?.': # keypoint & path
                    pygame.draw.rect(screen,
                                       (202,225,255),
                                       (cell_x,cell_y,r,r))  #filled
                    pygame.draw.circle(screen,
                                       (255, 118, 118),
                                       (cell_x + r//2, cell_y + r//2),
                                       r//4,  # radius
                                       0)  # filled
                if value == '.': # path marker
                    pygame.draw.rect(screen,
                                     (245, 245, 220),  # color
                                     (cell_x, cell_y, r, r))
                    pygame.draw.circle(screen,
                                       (255, 118, 118),
                                       (cell_x + r//2, cell_y + r//2),
                                       r//4,  # radius
                                       0)  # filled

            if  not c.north or not c.is_linked(c.north):
                pygame.gfxdraw.hline(screen, 
                                     cell_x, cell_x+r-1, cell_y,
                                     (100,100,100))
            if not c.south or not c.is_linked(c.south):
                pygame.gfxdraw.hline(screen, 
                                     cell_x, cell_x+r-1, cell_y+r-1,
                                     (100,100,100))
            if not c.east or not c.is_linked(c.east):
                pygame.gfxdraw.vline(screen, 
                                     cell_x+r-1, cell_y, cell_y+r-1,
                                     (100,100,100))
            if not c.west or not c.is_linked(c.west):
                pygame.gfxdraw.vline(screen, 
                                     cell_x, cell_y, cell_y+r-1,
                                     (100,100,100))
            
if __name__ == "__main__":
    main()


