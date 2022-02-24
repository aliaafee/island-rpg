import math
import heapq

from .math import Vector3

#a node is a tuple defined as ((x, y), g, h, f, parent)
POS = 0; G = 1; H = 2; F = 3; PARENT = 4


class Pathfinder:
    def __init__(self, grid_size=(10, 10), grid_cell_count=(10, 10), grid=None) -> None:
        self.grid_size = grid_size
        self.grid_cell_count = grid_cell_count

        self.cell_size = (
            grid_size[0]/grid_cell_count[0],
            grid_size[1]/grid_cell_count[1]
        )

        self.debug = {}

        if grid:
            self.grid = grid
            return

        self.clear()


    def _add_obstacle(self, position: Vector3, size: Vector3):
        topleft = position - size/2.0
        cell = (
            math.floor(topleft.x / self.cell_size[0]),
            math.floor(topleft.y / self.cell_size[1])
        )

        cell_size = (
            math.ceil(size.x / self.cell_size[0]),
            math.ceil(size.y / self.cell_size[1])
        )

        for x in range(cell[0], cell[0] + cell_size[0]):
            for y in range(cell[1], cell[1] + cell_size[1]):
                if x < self.grid_cell_count[0] and y < self.grid_cell_count[1]:
                    self.grid[y][x] = 0
        
        
    def clear(self):
        self.grid = []
        for y in range(self.grid_cell_count[1]):
            self.grid.append([])
            for x in range(self.grid_cell_count[0]):
                self.grid[y].append(1)


    def add_obstacles(self, obstacles):
        """Each obstacle as a tuple (position, size) in
            world space, as Vector3"""
        for position, size in obstacles:
            self._add_obstacle(position, size)


    def in_grid(self, x, y):
        if x < 0:
            return False
        if x > len(self.grid[0]) - 1 :
            return False
        if y < 0:
            return False
        if y > len(self.grid) - 1:
            return False
        return True


    def is_valid_cell(self, x, y):
        if not(self.in_grid(x, y)):
            return False
        if self.grid[y][x] == 0:
            return False
        return True


    def get_adjacent_diag_pos(self, pos) -> tuple:
        for offset in [(1,0), (1, 1), (0,1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
            yield pos[0] + offset[0], pos[1] + offset[1]


    def get_adjacent_perp_pos(self, pos) -> tuple:
        for offset in [(1,0), (0,1), (-1, 0), (0, -1)]:
            yield pos[0] + offset[0], pos[1] + offset[1]

    
    def get_adjacent_conditional(self, pos) -> tuple:
        """
        Does not move diagonally if there is a nearby obstacle
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x or y:
                    if abs(x) == abs(y):
                        adj_x = (
                            x + (0 - x) + pos[0], 
                            y + pos[1]
                        )
                        adj_y = (
                            x + pos[0], 
                            y + (0 - y) + pos[1]
                        )
                        adj_v = []
                        if self.in_grid(*adj_x):
                            adj_v.append(self.grid[adj_x[1]][adj_x[0]])
                        if self.in_grid(*adj_y):
                            adj_v.append(self.grid[adj_y[1]][adj_y[0]])
                        
                        if not(0 in adj_v):
                            yield pos[0] + x, pos[1] + y
                    else:
                        yield pos[0] + x, pos[1] + y


    def astar_findpath_previous_version(self, start, end, diagonal = False):
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

        if not(self.is_valid_cell(*start) and self.is_valid_cell(*end)):
            return None, 0
        
        if diagonal:
            get_adjacent = self.get_adjacent_conditional
        else:
            get_adjacent = self.get_adjacent_perp_pos

        open_list = {}
        closed_list = {}

        #add start node to open list
        open_list[start] = (start, 0, 0, 0, None)

        runs = 0
        while open_list:
            #keep track of number of runs
            runs += 1

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
                if len(path) == 1:
                    return None, runs
                self.debug['closed_list'] = closed_list
                return path, runs

            #look at all the adjacent nodes
            for child_pos in get_adjacent(current_node[POS]):
                if self.is_valid_cell(*child_pos):
                    #check to see if the node is closed
                    if not child_pos in closed_list.keys():
                        child_g = current_node[G] + 1
                        child_h = math.sqrt((end[0]-child_pos[0])**2 + (end[1] - child_pos[1])**2)
                        if not child_pos in open_list.keys():
                            #add to open_list if not done already
                            open_list[child_pos] = (child_pos, child_g, child_h, child_g + child_h, current_node)
                        else:
                            #if current child is furthur from origin than the one in
                            #the open list, switch to current child
                            if open_list[child_pos][G] > child_g:
                                open_list[child_pos] = (child_pos, child_g, child_h, child_g + child_h, current_node)
        self.debug['closed_list'] = closed_list
        return [], runs


    def astar_findpath(self, start, end, diagonal = False):
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

        self.debug['closed_list'] = []

        if not(self.is_valid_cell(*start) and self.is_valid_cell(*end)):
            return None, 0
        
        if diagonal:
            get_adjacent = self.get_adjacent_conditional
        else:
            get_adjacent = self.get_adjacent_perp_pos

        open_list = {}
        closed_list = {}
        
        #add start node to open list
        open_list[start] = (start, 0, 0, 0, None)
        open_list_heap = [(0, start)]
        heapq.heapify(open_list_heap)

        runs = 0
        while open_list_heap:
            #keep track of number of runs
            runs += 1

            #let current node be the node with smallest f in the open list
            f, current_node_pos = heapq.heappop(open_list_heap)
            
            #make sure the node has not been closed yet
            if not current_node_pos in closed_list: #current_node_pos in closed_list.keys():
                #move current_node from open_list to closed_list
                current_node = open_list.pop(current_node_pos)
                closed_list[current_node[POS]] = current_node

                if current_node[POS] == end:
                    #we have reached the end, back track and make the path
                    path = [end]
                    while current_node[PARENT]:
                        path.insert(0, current_node[PARENT][POS])
                        current_node = current_node[PARENT]
                    if len(path) == 1:
                        return None, runs
                    self.debug['closed_list'] = closed_list
                    return path, runs

                #look at all the adjacent nodes
                for child_pos in get_adjacent(current_node[POS]):
                    if self.is_valid_cell(*child_pos):
                        #check to see if the node is closed
                        if not child_pos in closed_list:
                            child_g = current_node[G] + 1
                            child_h = math.sqrt((end[0]-child_pos[0])**2 + (end[1] - child_pos[1])**2)
                            child_f = child_g + child_h
                            if not child_pos in open_list:
                                #add to open_list if not done already
                                open_list[child_pos] = (child_pos, child_g, child_h, child_f, current_node)
                                heapq.heappush(open_list_heap, (child_f, child_pos))
                            else:
                                #if current child is furthur from origin than the one in
                                #the open list, switch to current child
                                if open_list[child_pos][G] > child_g:
                                    open_list[child_pos] = (child_pos, child_g, child_h, child_f, current_node)
                                    heapq.heappush(open_list_heap, (child_f, child_pos))
        self.debug['closed_list'] = closed_list
        return [], runs


    def find_path(self, start: Vector3, end: Vector3, diagonal=True):
        """start and end as Vector3 in world space"""
        start_cell = (
            math.floor(start.x/self.cell_size[0]),
            math.floor(start.y/self.cell_size[1])
        )

        end_cell = (
            math.floor(end.x/self.cell_size[0]),
            math.floor(end.y/self.cell_size[1])
        )

        if not (self.in_grid(*start_cell) and self.in_grid(*end_cell)):
            return None

        path, runs = self.astar_findpath(start_cell, end_cell, diagonal=diagonal)

        print('operations:', runs, 'path length:', len(path))

        if not path:
            return None

        return [
            Vector3(node[0] * self.cell_size[0] + self.cell_size[0]/2, node[1] * self.cell_size[1] + self.cell_size[1]/2, 0)
            for node in path[1:-1]
        ] + [end]