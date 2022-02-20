import math
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.finder import ExecutionRunsException

from .math import Vector3


class Pathfinder:
    def __init__(self, grid_size, grid_cell_count) -> None:
        self.grid_size = grid_size
        self.grid_cell_count = grid_cell_count

        self.cell_size = (
            grid_size[0]/grid_cell_count[0],
            grid_size[1]/grid_cell_count[1]
        )
        
        self.finder = AStarFinder(
            diagonal_movement=DiagonalMovement.only_when_no_obstacle,
            max_runs=2000
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
                    self.matrix[y][x] = 0
        
        
    def clear(self):
        self.matrix = []
        for y in range(self.grid_cell_count[1]):
            self.matrix.append([])
            for x in range(self.grid_cell_count[0]):
                self.matrix[y].append(1)
        
        self.grid = Grid(matrix=self.matrix)


    def add_obstacles(self, obstacles):
        """Each obstacle as a tuple (position, size) in
            world space, as Vector3"""
        for position, size in obstacles:
            self._add_obstacle(position, size)

        self.grid = Grid(matrix=self.matrix)




    def find_path(self, start: Vector3, end: Vector3):
        """start and end as Vector3 in world space"""
        print(start, end)
        start_cell = (
            math.floor(start.x/self.cell_size[0]),
            math.floor(start.y/self.cell_size[1])
        )

        end_cell = (
            math.floor(end.x/self.cell_size[0]),
            math.floor(end.y/self.cell_size[1])
        )

        if not (self.grid.inside(*start_cell) and self.grid.inside(*end_cell)):
            return None

        self.grid.cleanup()

        try:
            path, runs = self.finder.find_path(
                self.grid.node(*start_cell),
                self.grid.node(*end_cell),
                self.grid
            )
        except ExecutionRunsException:
            print("Out of Runs")
            return None

        print('operations:', runs, 'path length:', len(path))
        print(self.grid.grid_str(
            path=path, 
            start=self.grid.node(*start_cell), 
            end=self.grid.node(*end_cell)
        ))

        if not path:
            return None

        return [
            Vector3(node[0] * self.cell_size[0] + self.cell_size[0]/2, node[1] * self.cell_size[1] + self.cell_size[1]/2, 0)
            for node in path[1:-2]
        ] + [end]