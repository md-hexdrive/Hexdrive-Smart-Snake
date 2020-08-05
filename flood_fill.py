from process_board import *
import numpy as np
import time
def generate_test_board(width, height):
    test_board = np.zeros((width, height), dtype=np.int32)
    
    for i in range(1, 4):
        test_board[i][height-1] = 4
    test_board[5][height-1] = 5
    for i in range(3, 6):
        test_board[i][height-2] = 4
    #np.fill_diagonal(test_board, 4)
    #np.fill_diagonal(np.fliplr(test_board), 5)
    return test_board

def flood_fill_board(x, y, board, possible_moves):
    print("flood fill")
    filled_boards = []
    space_in_each_dir=[]
    
    if "up" in possible_moves:
        filled_board, free_space = flood_fill(x, y+1, board)
        filled_boards.append(filled_board)
        space_in_each_dir.append(free_space)
        print("up", free_space)
        
    if "down" in possible_moves:
        filled_board, free_space = flood_fill(x, y-1, board)
        filled_boards.append(filled_board)
        space_in_each_dir.append(free_space)
        print("down", free_space)
        
    if "left" in possible_moves:
        filled_board, free_space = flood_fill(x-1, y, board)
        filled_boards.append(filled_board)
        space_in_each_dir.append(free_space)
        print("left", free_space)
        
    if "right" in possible_moves:
        filled_board, free_space = flood_fill(x+1, y, board)
        filled_boards.append(filled_board)
        space_in_each_dir.append(free_space)
        print("right", free_space)
    
    
    returned_moves = []
    most_space = max(space_in_each_dir)
    """
    TODO: Wondering if when two areas that have the same amount of free space in them
    but less than the most amount of available free space given in a set of possible moves,
    if it would be better to move into one of the two smaller areas instead of the biggest one
    (because they are both connected, whereas the larger area isn't?)
    """
    for i in range(len(possible_moves)):
        free_space = space_in_each_dir[i]
        if free_space < most_space:
            continue
        else:
            returned_moves.append(possible_moves[i])
    
    return returned_moves
def flood_fill(start_x, start_y, board):
    board_copy = board.copy()
    
    free_spaces = []
    free_space_count = 0
    queue = []
    queue.append((start_x, start_y))
    #free_space_count += 1
    
    while len(queue) > 0:
        x, y = queue[0]
        del queue[0]
        
        if y > 0 and y < board.shape[1]-1:
            move_up = (x, y+1)
            if board_copy[move_up] <= SAFE_SPACE and move_up not in queue:
                board_copy[move_up] = 255
                queue.append(move_up)
                free_space_count += 1            
        if y > 0 and y < board.shape[1]-1:
            move_down = (x, y-1)
            if board_copy[move_down] <= SAFE_SPACE and move_down not in queue:
                board_copy[move_down] = 255
                queue.append(move_down)
                free_space_count += 1
        if x > 0 and x < board.shape[0]-2:
            #print(x, y)
            move_left = (x-1, y)
            if board_copy[move_left] <= SAFE_SPACE and move_left not in queue:
                board_copy[move_left] = 255
                queue.append(move_left)
                free_space_count += 1
        if x > 0 and x < board.shape[0]-2:
            move_right = (x+1, y)
            if board_copy[move_right] <= SAFE_SPACE and move_right not in queue:
                board_copy[move_right] = 255
                queue.append(move_right)
                free_space_count += 1
        

        

    return board_copy, free_space_count

if __name__ == "__main__":
    x, y = 5, 10
    #def test_fill(x, y, test_board):    

    test_board = generate_test_board(11, 11)
    test_board[6, 6] = 0
    print(test_board)
    t1 = time.time()
    #board_copy, free_space = flood_fill(x, y, test_board)
    moves = flood_fill_board(x, y, test_board, [#"up",
                                                "down", "left", "right"])
    #time.sleep(0.1)
    t2 = time.time()
    print(moves)
    #print(board_copy)
    #print(free_space)
    print("duration", t2-t1)
