"""
behaviour.py
Controls the battlesnakes logic and behaviour
"""

import server
from sidewind import *
from process_board import *
from flood_fill import *

import numpy as np
import random

"""
TODO: Have the snake move toward the most free area
TODO: Ingnore food that an enemy is closer to than you

"""
# find the best available move and have the snake perform it
def find_best_move(data):
    board, board_width, board_height, my_head, my_snake, other_snakes, food, hazards = process_board(data)
    
    move = safe_move(board, board_width, board_height, my_head, my_snake, other_snakes, food, hazards)
    return move

# find and return a move this snake can make safely
def safe_move(board, board_width, board_height, my_head, my_snake, other_snakes, food, hazards):    
    possible_moves = ["up", "down", "left", "right"]
    x = my_head['x']
    y = my_head['y']
    
    move_right = (x+1, y)
    move_left = (x-1, y)
    move_up = (x, y+1)
    move_down = (x, y-1)
    
    move = ""
    
    possible_moves = find_illegal_moves(x, y, possible_moves, board, board_width, board_height)
    if len(possible_moves) == 1:
        return possible_moves[0]
    
    #if len(possible_moves) > 1:
    #    possible_moves = find_traps(my_head, board, board_width, board_height, possible_moves)
    if len(possible_moves) > 1:
        possible_moves = flood_fill_board(x, y, board, possible_moves)
#     if my_snake["length"] >= board_width:
#         move = sidewind(board, board_width, board_height, my_head, possible_moves)
#         if move != "":
#             return move
    if len(possible_moves) > 1:
        possible_moves = watch_heads(my_head, my_snake, board, possible_moves, other_snakes)
    
    if len(other_snakes) == 1 and my_snake['health'] < 20 or (my_snake['health'] < 40) or len(other_snakes) == 2:
        move = find_food(board, my_snake, food, possible_moves, other_snakes)
    
    #if len(possible_moves) > 1:
    #    possible_moves = best_free_space(x, y, board, possible_moves)
    possible_moves = move_to_most_open_area(board, x, y, possible_moves)
    
    
    #possible_moves = find_trap_point(x, y, board_width, board_height, board, possible_moves)
    #if (my_snake['health'] <= 50):
    
    
    if move == "" and len(possible_moves) > 0:
        move = random.choice(possible_moves)
        return move
    if len(possible_moves) == 0 and move == "":
        if ENEMY_NEXT_MOVE == board[x+1,y]:
            move = "right"
        elif ENEMY_NEXT_MOVE == board[x-1,y]:
            move = "left"
        elif ENEMY_NEXT_MOVE == board[x, y-1]:
            move = "down"
        elif ENEMY_NEXT_MOVE == board[x, y+1]:
            move = "up"
    else:
        if ENEMY_MOST_LIKELY_MOVE == board[x+1,y]:
            move = "right"
        elif ENEMY_MOST_LIKELY_MOVE == board[x-1,y]:
            move = "left"
        elif ENEMY_MOST_LIKELY_MOVE == board[x, y-1]:
            move = "down"
        elif ENEMY_MOST_LIKELY_MOVE == board[x, y+1]:
            move = "up"
    
#     if len(possible_moves) == 1:
#         move = possible_moves[0]
#     elif len(possible_moves) == 2:
#         move = best_free_space(x, y, board, possible_moves)
    
    if move == "" and len(possible_moves) == 0:
        move = random.choice(["up", "down", "left", "right"])
    return move

def move_to_most_open_area(board, x, y, possible_moves):
    if len(possible_moves) > 1:
        occupied = []
        total = []
        percent_occupied = []
        
        if 'up' in possible_moves:
            occupied_up = np.count_nonzero(board[:,y+1:] > SAFE_SPACE)
            occupied.append(occupied_up)
            total_up = board[:,y+1:].size - occupied_up
            total.append(total_up)
            percent_occupied.append(occupied_up / total_up)
        
        if 'down' in possible_moves:
            occupied_down = np.count_nonzero(board[:,:y] > SAFE_SPACE)
            occupied.append(occupied_down)
            total_down = board[:,:y].size - occupied_down
            total.append(total_down)
            percent_occupied.append(occupied_down / total_down)
        
        if 'left' in possible_moves:
            occupied_left = np.count_nonzero(board[:x,:] > SAFE_SPACE)
            occupied.append(occupied_left)
            total_left = board[:x,:].size - occupied_left
            total.append(total_left)
            percent_occupied.append(occupied_left / total_left)
        
        if 'right' in possible_moves:
            occupied_right = np.count_nonzero(board[x+1:,:] > SAFE_SPACE)
            occupied.append(occupied_right)
            total_right = board[x+1:,:].size - occupied_right
            total.append(total_right)
            percent_occupied.append(occupied_right / total_right)
        
        most_occupied_direction = percent_occupied.index(max(percent_occupied))
        del possible_moves[most_occupied_direction]
    """    
    if 'up' in possible_moves and 'down' in possible_moves:
        occupied_up = np.count_nonzero(board[:,y+1:] > SAFE_SPACE)
        occupied_down = np.count_nonzero(board[:,:y] > SAFE_SPACE)
        total_up = board[:,y+1:].size - occupied_up
        total_down = board[:,:y].size - occupied_down
        print("Percent Occupied up vs Down: ")
        print("Up:", occupied_up / total_up, ", Down:", occupied_down / total_down)
        if free_room(board[x,y+1:]) < free_room(np.flip(board[x,:y])) or abs(occupied_up / total_up) > abs(occupied_down / total_down):
            possible_moves.remove('up')
        elif free_room(board[x,y+1:]) > free_room(np.flip(board[x,:y])) or abs(occupied_up / total_up) < abs(occupied_down / total_down):
            possible_moves.remove('down')
    
    if 'left' in possible_moves and 'right' in possible_moves:
        occupied_right = np.count_nonzero(board[x+1:,:] > SAFE_SPACE)
        occupied_left = np.count_nonzero(board[:x,:] > SAFE_SPACE)
        total_left = board[:x,:].size - occupied_left
        total_right = board[x+1:,:].size - occupied_right
        
        if free_room(board[x+1:,y]) < free_room(np.flip(board[:x,y])) or abs(occupied_right / total_right) > abs(occupied_left / total_left):
            possible_moves.remove('right')
        elif free_room(board[x+1:,y]) > free_room(np.flip(board[:x,y])) or abs(occupied_right / total_right) < abs(occupied_left / total_left):
            possible_moves.remove('left')
    """
    return possible_moves

"""
try to avoid moving towards the head of a bigger snake within a specific distance
"""
def watch_heads(my_head, my_snake, board, possible_moves, other_snakes):
    heads_to_avoid = []
    heads_to_chase = []
    
    for snake in other_snakes:
        if snake['id'] == my_snake['id']:
            continue
        if my_snake['length'] <= snake['length']:
            heads_to_avoid.append(snake['head'])
        if my_snake['length'] > snake['length']:
            heads_to_chase.append(snake['head'])
    print("\n\nheads to avoid", heads_to_avoid, "\n\n")
    distances = []
    for head in heads_to_avoid:
        distances.append(distance(my_head, head))
    print("\n\ndistances until heads to avoid", distances, "\n\n")
    if len(distances) == 0:
        return possible_moves
    closest_head = min(distances)
    if closest_head > 2:
        return possible_moves
    ind = distances.index(closest_head)
    directions = direction(my_head, heads_to_avoid[ind])
    print('enemy snake head directions', directions)
    if len(directions) > 0:
        if directions[0] in possible_moves and len(possible_moves) > 1:
            possible_moves.remove(directions[0])
        if len(directions) > 1 and directions[1] in possible_moves and len(possible_moves) > 1:
            possible_moves.remove(directions[1])
    
    return possible_moves


def find_traps(my_head, board, board_width, board_height, possible_moves):
    x = my_head['x']
    y = my_head['y']
    
    next_moves = []
    if 'up' in possible_moves:
        next_moves.append(len(find_illegal_moves(x, y+1, ["up", "down", "left", "right"], board, board_width, board_height)))
    if 'down' in possible_moves:
        next_moves.append(len(find_illegal_moves(x, y-1, ["up", "down", "left", "right"], board, board_width, board_height)))
    if 'left' in possible_moves:
        next_moves.append(len(find_illegal_moves(x-1, y, ["up", "down", "left", "right"], board, board_width, board_height)))
    if 'right' in possible_moves:
        next_moves.append(len(find_illegal_moves(x+1, y, ["up", "down", "left", "right"], board, board_width, board_height)))
    most_moves_avail = max(next_moves)
    returned_moves = []
    if most_moves_avail <= 1:
        for i in range(len(next_moves)):
            if next_moves[i] < 1:
                continue
            else:
                returned_moves.append(possible_moves[i])
        
    for i in range(len(next_moves)):
        if next_moves[i] <= 1:
            continue
        else:
            returned_moves.append(possible_moves[i])
    return returned_moves

# can you move into this point without dying?
def is_illegal_move(point, board, board_width, board_height):
    
    if point[0] not in range(board_width):
        return True
    elif point[1] not in range(board_height):
        return True
    elif board[point] > SAFE_SPACE:
        return True
    else:
        return False

"""
Find and eliminate moves from consideration that would cause this snake to die.
"""
def find_illegal_moves(x, y, possible_moves, board, board_width, board_height):
    move_right = (x+1, y)
    move_left = (x-1, y)
    move_up = (x, y+1)
    move_down = (x, y-1)
    
    if is_illegal_move(move_right, board, board_width, board_height):
        possible_moves.remove('right')
    
    if is_illegal_move(move_left, board, board_width, board_height):
        possible_moves.remove('left')
    
    if is_illegal_move(move_up, board, board_width, board_height):
        possible_moves.remove('up')
    
    if is_illegal_move(move_down, board, board_width, board_height):
        possible_moves.remove('down')
    
    return possible_moves

# find moves that lead to most safe area to move into
def best_free_space(x, y, board, possible_moves):
    clear_space = []
    most_room = 0
    space_up = free_room(board[x,y+1:])
    space_down = free_room(np.flip(board[x,:y]))
    space_left = free_room(np.flip(board[:x,y]))
    space_right = free_room(board[x+1:,y])
    
    if "up" in possible_moves:
        clear_space.append(space_up)
    if "down" in possible_moves:
        clear_space.append(space_down)
    if "left" in possible_moves:
        clear_space.append(space_left)
    if "right" in possible_moves:
        clear_space.append(space_right)
        
    print("possible moves before free space analyzed\n", possible_moves, clear_space)
    clear_moves = []
    
    longest_dist = max(clear_space)
    move = possible_moves[clear_space.index(longest_dist)]
    for i in range(len(clear_space)):
        if (longest_dist / clear_space[i]) >= 2:
            continue
        else:
            clear_moves.append(possible_moves[i])
    #for it in range(len(possible_moves)):
    print("possible moves after free space analyzed\n", clear_moves)    
    return move



def free_room(board_slice):
    if np.count_nonzero(board_slice > SAFE_SPACE) == 0:
        return board_slice.size
    else:
        b = board_slice.tolist()
        free_space = 0
        for space in b:
            if space > SAFE_SPACE:
                return free_space
            free_space += 1

"""
find the closest piece of food your snake can eat
"""
def find_food(board, my_snake, food, possible_moves, other_snakes):
    food_dists = []
    my_head=my_snake['head']
    
    for f in food:
        food_dists.append(distance(my_head, f))
    
    while len(food_dists) > 0:
        my_dist = min(food_dists)
        index = food_dists.index(my_dist)
        target = food[index]
        directions = direction(my_head, target)
        
        if not is_closer_snake(my_dist, my_snake, other_snakes, target):
            
            if len(directions) == 2:
                if directions[0] in possible_moves:
                    return directions[0]
                if directions[1] in possible_moves:
                    return directions[1]
            elif len(directions) == 1:
                if directions[0] in possible_moves:
                    return directions[0]
            
        food.remove(target)
        food_dists.remove(food_dists[index])
    return ""

"""
find if there is another closer snake that can get to the target (i.e., a piece of food) sooner
(don't bother going for it in that case)
"""
def is_closer_snake(my_dist, my_snake, other_snakes, target):
    for snake in other_snakes:
        if snake['id'] == my_snake['id']:
            continue
        dist = distance(snake['head'], target)
        if dist < my_dist: # another snake could get there sooner
            return True
        elif dist == my_dist:
            if snake['length'] >= my_snake['length']:
                return True
    return False

"""
Get the directions between a source point and a target point.
"""
def direction(source, target):
    x1 = source['x']
    y1 = source['y']
    x2 = target['x']
    y2 = target['y']
    
    directions = []
    
    if y1 > y2:
        directions.append("down")
    elif y1 < y2:
        directions.append("up")
    
    if x1 > x2:
        directions.append("left")
    elif x1 < x2:
        directions.append("right")
    
    return directions

"""
get the pythagorean distance between points a and b
"""
def distance(a, b):
    x1 = a['x']
    y1 = a['y']
    x2 = b['x']
    y2 = b['y']
    
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    return dist

if __name__ == "__main__":
    pass
