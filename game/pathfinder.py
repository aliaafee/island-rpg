import math

from .math import Vector3


class Pathfinder:
    def __init__(self, grid_size, grid_cell_count) -> None:
        self.grid_size = grid_size
        self.grid_cell_count = grid_cell_count

        self.cell_size = (
            grid_size[0]/grid_cell_count[0],
            grid_size[1]/grid_cell_count[1]
        )

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
        if self.grid[y][x] == 0:
            return False
        return True


    def get_adjacent_diag_pos(self, pos) -> tuple:
        for offset in [(1,0), (1, 1), (0,1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
            yield pos[0] + offset[0], pos[1] + offset[1]


    def get_adjacent_perp_pos(self, pos) -> tuple:
        for offset in [(1,0), (0,1), (-1, 0), (0, -1)]:
            yield pos[0] + offset[0], pos[1] + offset[1]            


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
        
        if diagonal:
            get_adjacent = self.get_adjacent_diag_pos
        else:
            get_adjacent = self.get_adjacent_perp_pos

        #a node is a tuple defined as ((x, y), g, h, f, parent)
        POS = 0; G = 1; H = 2; F = 3; PARENT = 4

        open_list = {}
        closed_list = {}

        #add start node to open list
        open_list[start] = (start, 0, 0, 0, None)

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
                return path, run

            #look at all the adjacent nodes
            for child_pos in get_adjacent(current_node[POS]):
                if self.in_grid(*child_pos):
                    #check to see if the node is closed
                    if not child_pos in closed_list.keys():
                        child_g = current_node[G] + 1
                        child_h = (end[0]-child_pos[0])**2 + (end[1] - child_pos[1])**2
                        if not child_pos in open_list.keys():
                            #add to open_list if not done already
                            open_list[child_pos] = (child_pos, child_g, child_h, child_g + child_h, current_node)
                        else:
                            #if current child is furthur from origin than the one in
                            #the open list, switch to current child
                            if open_list[child_pos][G] > child_g:
                                open_list[child_pos] = (child_pos, child_g, child_h, child_g + child_h, current_node)
        return [], run


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