import pygame
import sys
from timeit import default_timer as timer


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("OrthoGame")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 12)

grid = [
    [1 for x in range(10)] for y in range(10)
]

grid = [
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]
]


def print_grid(grid, marks: dict, indent="  "):
    print(indent + "{}x{} grid".format(len(grid[0]), len(grid)))
    print(indent + " " + " ".join("-" for x in range(len(grid[0]))))
    for y, row in enumerate(grid):
        line = []
        for x, cell in enumerate(row):
            if (x, y) in marks.keys():
                line.append(marks[(x, y)])
            else:
                if cell == 0:
                    line.append(".")
                else:
                    line.append(" ")
        print(indent + "|" + " ".join(line))


def findpath_astar(grid, start, end):
    marks = {
        start: "S",
        end: "E"
    }
    visited = []

    runs = 0
    current = start
    visited.append(start)

    def ingrid(cell, grid):
        x, y = cell
        if x < 0:
            return False
        if x > len(grid[0]) - 1 :
            return False
        if y < 0:
            return False
        if y > len(grid) - 1:
            return False
        return True

    while True:
        runs += 1
        if current == end:
            print("found in {} runs".format(runs))
            print_grid(grid, {**marks, **{key: "+" for key in visited[1:-1]}})
            return

        cheapest, cheapest_value = (0, 0), 10000
        for offset in [(1,0), (1, 1), (0,1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
            adj = (current[0] + offset[0], current[1] + offset[1])
            print("checking {}".format(adj))
            if ingrid(adj, grid):
                if not(adj in visited) and grid[adj[1]][adj[0]] != 0:
                    cost = 1 + (end[0] - adj[0])**2 + (end[1] - adj[1])**2
                    if cost < cheapest_value:
                        cheapest, cheapest_value = adj, cost

        print("Cheapest {}, cost {}".format(cheapest, cheapest_value))
        print_grid(grid, {**marks, **{cheapest: "+"}})
        print("")
        current = cheapest
        visited.append(current)


class Node:
    def __init__(self, pos, g=0, h=0, parent=None) -> None:
        self.pos = pos
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent = parent

        self.update_count = 0

    def update(self, g, h, parent):
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent = parent
        self.update_count += 1

    def __repr__(self) -> str:
        return "({}, {}) = {}".format(*self.pos, self.f)

    def get_adjacent_diag_pos(self) -> tuple:
        for offset in [(1,0), (1, 1), (0,1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
            yield self.pos[0] + offset[0], self.pos[1] + offset[1]

    def get_adjacent_pos(self) -> tuple:
        for offset in [(1,0), (0,1), (-1, 0), (0, -1)]:
            yield self.pos[0] + offset[0], self.pos[1] + offset[1]

    def distance2_to(self, target_pos):
        return (target_pos[0]-self.pos[0])**2 + (target_pos[1] - self.pos[1])**2



def findpath_astar2(grid, start, end):
    def ingrid(cell, grid):
        x, y = cell
        if x < 0:
            return False
        if x > len(grid[0]) - 1 :
            return False
        if y < 0:
            return False
        if y > len(grid) - 1:
            return False
        return True


    open_list = []
    closed_list = []

    open_list.append(Node(start))

    run = 0
    while open_list:
        run += 1
        print(run)
        current_node = sorted(open_list, key=lambda node: node.f)[0]
        open_list.pop(open_list.index(current_node))
        closed_list.append(current_node)
        if current_node.pos == end:
            path = [end]
            while current_node.parent:
                path.append(current_node.parent.pos)
                current_node = current_node.parent
            yield path
            return path
        
        for child_pos in current_node.get_adjacent_pos():
            #print("  ")
            if not child_pos in [node.pos for node in closed_list]:
                if ingrid(child_pos, grid):
                    if grid[child_pos[1]][child_pos[0]]:
                        child_node = Node(child_pos)
                        child_node.g = current_node.g + 1
                        child_node.h = child_node.distance2_to(end)
                        child_node.f = child_node.g + child_node.h
                        child_node.parent = current_node
                        for open_node in open_list:
                            if child_node.pos == open_node.pos:
                                if child_node.g > open_node.g:
                                    continue
                        open_list.append(child_node)
                        yield start, end, current_node.pos, open_list, closed_list, child_node
        yield start, end, current_node.pos, open_list, closed_list, None
        #print_grid(grid, {**{current_node.pos: "K"}, **{start: "S", end: "E"}, **{key.pos: "0" for key in open_list}})
    print("could not find a path")


def astar_findpath(grid, start, end):
    """
        grid = [
            [1, 0,...]
            .
            .
        ]
        start, end = (x, y) valid position on grid

        A* search, adapted from implementation by Nicholas Swift
        https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    """
    def is_valid_pos(x, y):
        if x < 0:
            return False
        if x > len(grid[0]) - 1 :
            return False
        if y < 0:
            return False
        if y > len(grid) - 1:
            return False
        if grid[y][x] == 0:
            return False
        return True

    def backtrace(node):
        c = node
        path = []
        while c.parent:
            path.append(c.parent.pos)
            c = c.parent
        return path

    open_list = {}
    closed_list = {}

    #add start node to open list
    open_list[start] = Node(start)

    run = 0
    while open_list:
        #keep track of number of runs
        run += 1
        #print(run)

        #let current node be the node with smallest f in the open list
        current_node = sorted(open_list.values(), key=lambda node: node.f)[0]

        #move current_node from open_list to closed_list
        open_list.pop(current_node.pos)
        closed_list[current_node.pos] = current_node

        if current_node.pos == end:
            #we have reached the end, back track and make the path
            path = [end]
            while current_node.parent:
                path.insert(0, current_node.parent.pos)
                current_node = current_node.parent
            #yield path
            return path

        #look at all the adjacent nodes
        for child_pos in current_node.get_adjacent_pos():
            if is_valid_pos(*child_pos):
                #check to see if the node is closed
                if not child_pos in closed_list.keys():
                    child_g = current_node.g + 1
                    child_h = (end[0]-child_pos[0])**2 + (end[1] - child_pos[1])**2
                    if not child_pos in open_list.keys():
                        #add to open_list if not done already
                        open_list[child_pos] = Node(child_pos, child_g, child_h, parent=current_node)
                        #yield start, end, current_node.pos, open_list.values(), closed_list.values(), open_list[child_pos], backtrace(current_node)
                    else:
                        #if current child is furthur from origin than the one in
                        #the open list, switch to current child
                        if open_list[child_pos].g > child_g:
                            open_list[child_pos].update(child_g, child_h, parent=current_node)
                        #yield start, end, current_node.pos, open_list.values(), closed_list.values(), open_list[child_pos], backtrace(current_node)
        #yield start, end, current_node.pos, open_list.values(), closed_list.values(), None, backtrace(current_node)
    print("could not find a path")
    return None




def astar_findpath2(grid, start, end, diagonal = False):
    """
        grid = [
            [1, 0,...]
            .
            .
        ]
        start, end = (x, y) valid position on grid

        A* search, adapted from implementation by Nicholas Swift
        https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    """
    def is_valid_pos(x, y):
        if x < 0:
            return False
        if x > len(grid[0]) - 1 :
            return False
        if y < 0:
            return False
        if y > len(grid) - 1:
            return False
        if grid[y][x] == 0:
            return False
        return True

    def get_adjacent_diag_pos(pos) -> tuple:
        for offset in [(1,0), (1, 1), (0,1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
            yield pos[0] + offset[0], pos[1] + offset[1]

    def get_adjacent_perp_pos(pos) -> tuple:
        for offset in [(1,0), (0,1), (-1, 0), (0, -1)]:
            yield pos[0] + offset[0], pos[1] + offset[1]

    if diagonal:
        get_adjacent = get_adjacent_diag_pos
    else:
        get_adjacent = get_adjacent_perp_pos

    def backtrace(node):
        path = []
        c = node
        while c[PARENT]:
            path.insert(0, c[PARENT][POS])
            c = c[PARENT]
        return path

    #a node is a tuple defined as ((x, y), g, h, f, parent)
    POS = 0; G = 1; H = 2; F = 3; PARENT = 4

    open_list = {}
    closed_list = {}

    #add start node to open list
    open_list[start] = (start, 0, 0, 0, None)#Node(start)

    run = 0
    while open_list:
        #keep track of number of runs
        run += 1
        #print(run)

        #let current node be the node with smallest f in the open list
        current_node = sorted(open_list.values(), key=lambda node: node[F])[0]

        #move current_node from open_list to closed_list
        open_list.pop(current_node[POS])
        closed_list[current_node[POS]] = current_node

        if current_node[POS] == end:
            #we have reached the end, back track and make the path
            path = [end]
            while current_node[PARENT]:
                path.insert(0, current_node[PARENT][POS])
                current_node = current_node[PARENT]
            #yield path
            return path

        #look at all the adjacent nodes
        for child_pos in get_adjacent(current_node[POS]):
            if is_valid_pos(*child_pos):
                #check to see if the node is closed
                if not child_pos in closed_list.keys():
                    child_g = current_node[G] + 1
                    child_h = (end[0]-child_pos[0])**2 + (end[1] - child_pos[1])**2
                    if not child_pos in open_list.keys():
                        #add to open_list if not done already
                        open_list[child_pos] = (child_pos, child_g, child_h, child_g + child_h, current_node)
                        #yield start, end, current_node[POS], open_list.values(), closed_list.values(), open_list[child_pos], backtrace(current_node)
                    else:
                        #if current child is furthur from origin than the one in
                        #the open list, switch to current child
                        if open_list[child_pos][G] > child_g:
                            #open_list[child_pos].update(child_g, child_h, parent=current_node)
                            open_list[child_pos] = (child_pos, child_g, child_h, child_g + child_h, current_node)
                        #yield start, end, current_node[POS], open_list.values(), closed_list.values(), open_list[child_pos], backtrace(current_node)
        #yield start, end, current_node[POS], open_list.values(), closed_list.values(), None, backtrace(current_node)
    return None
        
        




start = (1, 1)
end = (9, 9)
#gen = astar_findpath2(grid, (1, 1), (9, 1))
#gen = findpath_astar2(grid, (1, 1), (9, 1))
#print(path)
#print_grid(grid, {**{start: "S", end: "E"}, **{key: "+" for key in path[1:-1]}})
#path = astar_findpath(grid, start, end)

GRID_SIZE = 40
def s_pos(x, y):
    return x*GRID_SIZE, y*GRID_SIZE
def s_pos_c(x, y):
    return x*GRID_SIZE + GRID_SIZE/2, y*GRID_SIZE + GRID_SIZE/2

def draw_text(screen, pos, text):
    x,y = pos
    surf = font.render(str(text),True,'black')
    rect = surf.get_rect(center = (x,y))
    screen.blit(surf,rect)

def draw_grid_only(screen, grid, start, end):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                pygame.draw.rect(screen,'black', (*s_pos(x, y), GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen,'black', (*s_pos(x, y), GRID_SIZE, GRID_SIZE), 1)
    pygame.draw.circle(screen, 'purple', s_pos_c(*start), GRID_SIZE/2.5)
    pygame.draw.circle(screen, 'orange', s_pos_c(*end), GRID_SIZE/2.5)

def draw_grid(screen, grid, start, end, current, open_list, closed_list, child_node, backtrace):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                pygame.draw.rect(screen,'black', (*s_pos(x, y), GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen,'black', (*s_pos(x, y), GRID_SIZE, GRID_SIZE), 1)
    for node in open_list:
        pygame.draw.circle(screen, "green", s_pos_c(*node.pos), GRID_SIZE/3)
        text_pos = s_pos_c(*node.pos)
        draw_text(screen, text_pos, node.f)
        draw_text(screen, (text_pos[0], text_pos[1]+10), node.update_count)
    for node in closed_list:
        pygame.draw.circle(screen, "red", s_pos_c(*node.pos), GRID_SIZE/3)
    pygame.draw.circle(screen, 'blue', s_pos_c(*current), GRID_SIZE/3.5)
    pygame.draw.circle(screen, 'purple', s_pos_c(*start), GRID_SIZE/2.5)
    pygame.draw.circle(screen, 'purple', s_pos_c(*end), GRID_SIZE/2.5)
    if child_node:
        pygame.draw.circle(screen, 'grey', s_pos_c(*child_node.pos), GRID_SIZE/3.5)
        draw_text(screen, s_pos_c(*child_node.pos), child_node.f)
        draw_text(screen, (text_pos[0], text_pos[1]+10), node.update_count)
    if backtrace:
        if len(backtrace) > 1:
            pygame.draw.lines(screen, 'Black', False,
                [s_pos_c(*p) for p in backtrace]
                , 4
            )

def draw_grid2(screen, grid, start, end, current, open_list, closed_list, child_node, backtrace):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                pygame.draw.rect(screen,'black', (*s_pos(x, y), GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen,'black', (*s_pos(x, y), GRID_SIZE, GRID_SIZE), 1)
    for node in open_list:
        text_pos = s_pos_c(*node[0])
        pygame.draw.circle(screen, "green", text_pos, GRID_SIZE/3)
        draw_text(screen, text_pos, node[3])
        #draw_text(screen, (text_pos[0], text_pos[1]+10), node.update_count)
    for node in closed_list:
        pygame.draw.circle(screen, "red", s_pos_c(*node[0]), GRID_SIZE/3)
    pygame.draw.circle(screen, 'blue', s_pos_c(*current), GRID_SIZE/3.5)
    pygame.draw.circle(screen, 'purple', s_pos_c(*start), GRID_SIZE/2.5)
    pygame.draw.circle(screen, 'purple', s_pos_c(*end), GRID_SIZE/2.5)
    if child_node:
        pygame.draw.circle(screen, 'grey', s_pos_c(*child_node[0]), GRID_SIZE/3.5)
        draw_text(screen, s_pos_c(*child_node[0]), child_node[3])
        #draw_text(screen, (text_pos[0], text_pos[1]+10), node.update_count)
    if backtrace:
        if len(backtrace) > 1:
            pygame.draw.lines(screen, 'Black', False,
                [s_pos_c(*p) for p in backtrace]
                , 4
            )
    


screen.fill('white')
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            start = (1, 1)
            end = (9, 9)
            
            t_s = timer()
            for i in range(100000):
                path = astar_findpath2(grid, start, end)
            t_e = timer()
            print("astar_findpath2 took {} s".format(t_e - t_s))


            draw_grid_only(screen, grid, start, end)
            pygame.draw.lines(screen, 'red', False,
                 [s_pos_c(*p) for p in path]
                 , 4
            )
            
            t_s = timer()
            for i in range(100000):
                path = astar_findpath(grid, start, end)
            t_e = timer()
            print("astar_findpath took {} s".format(t_e - t_s))


            draw_grid_only(screen, grid, start, end)
            pygame.draw.lines(screen, 'red', False,
                 [s_pos_c(*p) for p in path]
                 , 4
            )
            pass
            #start, end, current, open_list, closed_list = next(gen)
    # try:
    #     item = next(gen)
    #     if type(item) is tuple:
    #         screen.fill("white")
    #         draw_grid2(screen, grid, *item)
    #     else:
    #         pygame.draw.lines(screen, 'Black', False,
    #             [s_pos_c(*p) for p in item]
    #             , 4
    #         )
    # except StopIteration:
    #     pass
                

    

    
    #try:
    #    print(next(gen))
    #except StopIteration:
    #    print("done"


    #debug(round(self.clock.get_fps()))

    pygame.display.update()
    clock.tick(60)