import numpy as np
from process_board import *

def in_bounds(board, x, y=None):
  if type(x) == type(tuple()):
    if x[0] in range(board.shape[0]) and x[1] in range(board.shape[0]):
      return True
    else:
      return False
  else:
    if x in range(board.shape[0]) and y in range(board.shape[1]):
      return True
    else:
      return False
def contents(board, x, y):
  return board[x, y]

def is_safe_move(board, x, y):
  if in_bounds(board, x, y) and board[x][y] <= SAFE_SPACE:
    return True
  else:
    return False

def move_up(x, y):
  return x, y+1
def move_down(x, y):
  return x, y-1
def move_left(x, y):
  return x-1, y
def move_right(x, y):
  return x+1, y

def get_move(move_name, x, y):
  if move_name == "left":
    return move_left(x, y)
  if move_name == "right":
    return move_right(x, y)
  if move_name == "down":
    return move_down(x, y)
  if move_name == "up":
    return move_up(x, y)
  return None