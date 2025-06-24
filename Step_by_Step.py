import pygame
from copy import deepcopy
# from module import (classes, *functions*, or variables)
# you can directly use (specific_component) in your code without prefixing it with the module name.

# Initialize Pygame
pygame.init()

WINDOW_SIZE = 460
GRID_SIZE = 3
TILE_SIZE = 300 // GRID_SIZE
FONT_SIZE = TILE_SIZE // 2
BACKGROUND_COLOR = (50, 50, 50)
TILE_COLOR = (100, 200, 200) #light cyan
EMPTY_TILE_COLOR = (200, 50, 50) #red
FONT_COLOR = (0, 0, 0)
COUNTER_COLOR = (255, 255, 255)
FPS = 1

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

#"U": [row, col]
# [ (0, 0)   (0, 1)   (0, 2) ]
# [ (1, 0)   (1, 1)   (1, 2) ]
# [ (2, 0)   (2, 1)   (2, 2) ]

GoalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Pygame setup
screen = pygame.display.set_mode((WINDOW_SIZE, 310))
pygame.display.set_caption("8-Puzzle Solver with Step Counter")
font = pygame.font.Font(None, FONT_SIZE) #(FontName, FontSize)


def draw_grid(puzzle, steps):
    screen.fill(BACKGROUND_COLOR)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = puzzle[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            #Rect(x-topleft corner, y-topleft corner, width, height)
            color = TILE_COLOR if value != 0 else EMPTY_TILE_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Grid lines
            if value != 0:
                text = font.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    # Draw step counter
    counter_text = font.render(f"Steps: {steps}", True, COUNTER_COLOR)
    counter_rect = counter_text.get_rect(center=(380, 150))
    screen.blit(counter_text, counter_rect)

    pygame.display.flip()


def get_pos(puzzle, element):
    for row in range(len(puzzle)):
        if element in puzzle[row]:
            return row, puzzle[row].index(element)


def heuristic(current_state): #Manhattan Distance
    h = 0
    for row in range(len(current_state)):
        for col in range(len(current_state)):
            pos = get_pos(GoalState, current_state[row][col])
            h += abs(row - pos[0]) + abs(col - pos[1])
    return h


def get_adj_nodes(node):
    list_nodes = []
    empty_pos = get_pos(node["current_node"], 0)

    for dir in DIRECTIONS.keys():
        new_pos = (empty_pos[0] + DIRECTIONS[dir][0], empty_pos[1] + DIRECTIONS[dir][1])
        if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
        # if the empty tile in the 1st row, it can't go up and so on
            new_state = deepcopy(node["current_node"])
            new_state[empty_pos[0]][empty_pos[1]] = node["current_node"][new_pos[0]][new_pos[1]]
            new_state[new_pos[0]][new_pos[1]] = 0
            list_nodes.append({
                "current_node": new_state,
                "previous_node": node["current_node"],
                "g": node["g"] + 1,
                "h": heuristic(new_state),
                "dir": dir
            })
    return list_nodes

# def get_best_node(open_set):
#     best_node = None
#     best_f = float("inf")  # Start with an infinitely large value for comparison
#
#     for node in open_set.values():
#         f = node["g"] + node["h"]  # Calculate f = g + h
#         if f < best_f:  # Check if this node has a smaller f value
#             best_f = f
#             best_node = node
#
#     return best_node

def get_best_node(open_set):
    return min(open_set.values(), key=lambda node: node["g"] + node["h"])
    #The word node represents each dictionary from open_set.values() during iteration.

def build_path(closed_set):
    node = closed_set[str(GoalState)]
    path = []
    while node["dir"]:
        path.append(node)
        node = closed_set[str(node["previous_node"])] #node--
    path.reverse()
    return path


def solve_puzzle(puzzle):
    open_set = {
        str(puzzle): {"current_node": puzzle, "previous_node": puzzle, "g": 0, "h": heuristic(puzzle), "dir": ""}}
    closed_set = {}

    while open_set:
        current_node = get_best_node(open_set)
        closed_set[str(current_node["current_node"])] = current_node

        if current_node["current_node"] == GoalState:
            return build_path(closed_set)

        adj_nodes = get_adj_nodes(current_node)
        for node in adj_nodes:
            if str(node["current_node"]) in closed_set or str(node["current_node"]) in open_set:
                continue
            open_set[str(node["current_node"])] = node

        del open_set[str(current_node["current_node"])]
    return []


def animate_solution(path):
    steps = 0
    for step in path:
        steps += 1
        draw_grid(step["current_node"], steps)
        pygame.time.delay(300)


def main():
    running = True
    puzzle = [[3,8,0],[1,7,6],[5,4,2]]
    #puzzle = [[4, 1, 3],[2, 5, 6],[7, 8, 0]]

    steps = 0  # Initial steps counter
    draw_grid(puzzle, steps)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  #K_s Press 'S' to solve
                    solution_path = solve_puzzle(puzzle)
                    animate_solution(solution_path)

    pygame.quit()


if __name__ == "__main__":
    main()
