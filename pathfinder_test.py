import pygame
import sys
from timeit import default_timer as timer

from game.pathfinder import Pathfinder

CELL_SIZE = 10

# grid = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
#     [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
#     [1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
#     [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]

grid = [
    [1 for x in range(100)] for y in range(100)
]

grid[1][0] = 0
grid[1][1] = 0
grid[0][1] = 0

start = None
end = (0, 0)

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("OrthoGame")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 12)


def spos(x, y):
    return x*CELL_SIZE, y*CELL_SIZE

def cpos(x, y):
    return int(x / CELL_SIZE), int(y / CELL_SIZE)


def sposc(x, y):
    return x*CELL_SIZE + CELL_SIZE/2, y*CELL_SIZE + CELL_SIZE/2


def update_grid(x, y, val):
    global grid
    try:
        grid[y][x] = val
    except:
        pass


def draw_grid(grid, start, end):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                pygame.draw.rect(screen,'black', (*spos(x, y), CELL_SIZE, CELL_SIZE))
            else:
                pass
                pygame.draw.rect(screen,'grey', (*spos(x, y), CELL_SIZE, CELL_SIZE))
    if start:
        pygame.draw.circle(screen, 'purple', sposc(*start), CELL_SIZE/2.5)
    if end:
        pygame.draw.circle(screen, 'orange', sposc(*end), CELL_SIZE/2.5)


def draw_path(path):
    points = [sposc(*p) for p in path]
    pygame.draw.lines(screen, 'red', False,
            points
            , 1
    )
    for p in points:
        pygame.draw.circle(screen, 'purple', p, CELL_SIZE/10)


def highlight_nodes(nodes):
    for pos in nodes:
        pygame.draw.circle(screen, 'green', sposc(*pos), CELL_SIZE/3)



def onMouseUp(event):
    global start, end

    if event.button == pygame.BUTTON_LEFT:
        end = cpos(*event.pos)
    # if event.button == pygame.BUTTON_RIGHT:
    #     end = cpos(*event.pos)

    screen.fill('white')
    draw_grid(grid, start, end)

    # if start and end:
    #     pfinder = Pathfinder(grid=grid)
    #     path, runs = pfinder.astar_findpath(start, end, diagonal=True)
        
    #     if 'closed_list' in pfinder.debug.keys():
    #         highlight_nodes(pfinder.debug['closed_list'])

    #     if path:
    #         print("Path found in {} runs".format(runs))
    #         draw_path(path)
    #     else:
    #         print("Path not found after {} runs".format(runs))
        



def main():
    global start, end
    
    pfinder = Pathfinder(grid=grid)
    screen.fill('white')
    draw_grid(grid, start, end)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                onMouseUp(event)

        keys = pygame.key.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        if keys[pygame.K_a]:
            x,y = cpos(*mouse_position)
            update_grid(x, y, 0)
            screen.fill('white')
            draw_grid(grid, start, end)
        if keys[pygame.K_d]:
            x,y = cpos(*mouse_position)
            update_grid(x, y, 1)
            screen.fill('white')
            draw_grid(grid, start, end)
        if keys[pygame.K_s]:
            start = cpos(*mouse_position)
            screen.fill('white')
            draw_grid(grid, start, end)
            if start and end:
                t_s = timer()
                path, runs = pfinder.astar_findpath(start, end, diagonal=True)
                t_e = timer()
                new_time = t_e - t_s

                t_s = timer()
                path, runs = pfinder.astar_findpath_previous_version(start, end, diagonal=True)
                t_e = timer()
                old_time = t_e - t_s

                if 'closed_list' in pfinder.debug.keys():
                    highlight_nodes(pfinder.debug['closed_list'])
                if path:
                    print("Path found in {} runs, {} s".format(runs, (new_time, old_time)))
                    draw_path(path)
                else:
                    print("Path not found after {} runs, {} s".format(runs, (new_time, old_time)))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()