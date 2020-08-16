import server
import behaviour
from game_board import *
import numpy as np
import random
import math
"""
These constants stand for what currently occupies each space on the board, and are used to id the
snake's environment.
"""
EMPTY = 0
FOOD = 1

"""
any space with a value > SAFE_SPACE is dangerous, likely fatal, for our snake to move into.
Stay out of it!
"""
SAFE_SPACE = 1

ENEMY_SNAKE = 2
ENEMY_SNAKE_HEAD = 3
ENEMY_NEXT_MOVE = 6
ENEMY_MOST_LIKELY_MOVE = 9
ENEMY_TAIL = 8

MY_SNAKE = 4
MY_HEAD = 5
MY_TAIL = 7

HAZARD = 10
def process_board(data):
    board_width, board_height, my_head, my_snake, other_snakes, food, hazards = parse_json(data)
    board = fill_board(board_width, board_height, my_head, my_snake, other_snakes, food, hazards)
    return board, board_width, board_height, my_head, my_snake, other_snakes, food, hazards

def parse_json(data):
    board_width = data['board']['width']
    board_height = data['board']['height']
    my_head = data['you']['head']
    my_snake = data['you']
    other_snakes = data['board']['snakes']
    food = data['board']['food']
    hazards = data['board']['hazards']
    print("board_width", board_width)
    print('my_head', my_head)
    print('my health', data['you']['health'])
    
    return board_width, board_height, my_head, my_snake, other_snakes, food, hazards
    


def fill_board(board_width, board_height, my_head, my_snake, other_snakes, food, hazards):
    board = np.zeros((board_width, board_height), dtype=np.int8)
    
    for square in food:
        x = square['x']
        y = square['y']
        board[x][y] = FOOD
    for square in hazards:
        x = square['x']
        y = square['y']
        board[x][y] = HAZARD
    for snake in other_snakes:
        if snake['id'] == my_snake['id']:
            continue
        
        x = snake['head']['x']
        y = snake['head']['y']
        board[x][y] = ENEMY_SNAKE_HEAD
        
        if snake['length'] >= my_snake['length']: # Todo: change this comparision >= if snake runs headlong into other snakes
            last_enemy_pos = snake['body'][1]
            enemy_travel_dir = behaviour.direction(last_enemy_pos, snake['head'])
            if in_bounds(board, get_move("left", x, y)):
              if enemy_travel_dir == "left":
                  board[x-1][y] = ENEMY_MOST_LIKELY_MOVE
              else:
                  board[x-1][y] = ENEMY_NEXT_MOVE
            if in_bounds(board, get_move("right", x, y)):
              if enemy_travel_dir == "right":
                  board[x+1][y] = ENEMY_MOST_LIKELY_MOVE
              else:
                  board[x+1][y] = ENEMY_NEXT_MOVE
            if in_bounds(board, get_move("down", x, y)):
              if enemy_travel_dir == "down":
                  board[x][y-1] = ENEMY_MOST_LIKELY_MOVE
              else:
                  board[x][y-1] = ENEMY_NEXT_MOVE
            if in_bounds(board, get_move("up", x, y)):
              if enemy_travel_dir == "up":
                  board[x][y+1] = ENEMY_MOST_LIKELY_MOVE
              else:
                  board[x][y+1] = ENEMY_NEXT_MOVE
            
        
        for square in snake['body']:
            x = square['x']
            y = square['y']
            board[x][y] = ENEMY_SNAKE
            if square == snake['body'][-1]:
                if snake['length'] == len(snake['body']) and snake['health'] < 100 and (ENEMY_SNAKE_HEAD not in board[x-1:x+2,y] and ENEMY_SNAKE_HEAD not in board[x,y-1:y+2]):
                    board[x][y] = EMPTY
        
        x = snake['head']['x']
        y = snake['head']['y']
        board[x][y] = ENEMY_SNAKE_HEAD
        
    for square in my_snake['body']:
        x = square['x']
        y = square['y']
        
        if square == my_snake['body'][-1]:
            if my_snake['length'] == len(my_snake['body']) and my_snake['length'] > 3 and my_snake['health'] < 100:
                board[x][y] = EMPTY
            else:
                board[x][y] = MY_TAIL
        else:
            board[x][y] = MY_SNAKE
    

    board[my_head['x']][my_head['y']] = MY_HEAD
    
    
    
    return board


if __name__ == "__main__":
    pass
