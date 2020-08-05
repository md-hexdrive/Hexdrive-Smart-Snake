import numpy as np

def sidewind(board, board_width, board_height, my_head, possible_moves):
    x = my_head['x']
    y = my_head['y']
    if(y==board_height-1 and 'right' in possible_moves):
        return 'right'
    elif(y==board_height-1 and 'down' in possible_moves):
        return 'down'
    
    if (x>0 and ((y==board_height-2 and 'down' not in possible_moves) or (y==0 and 'up' not in possible_moves)) and 'left' in possible_moves):
        return 'left'
    if(y==board_height-1 and x<board_width and "right" in possible_moves):
        return "right"
    
    if((x==0 and 'up' in possible_moves) or 'down' not in possible_moves) and 'up' in possible_moves:
        return 'up'
    if(x > 0 and y < board_height-1 and "down" in possible_moves):
        return "down"
    
#     if((y==board_height-2 or y==0) and "left" in possible_moves and "down" not in possible_moves):
#         return "left"
#     
    #if((x > 0 and y < board_height-2 and "up" in possible_moves) or (x==0 and y==board_height-2 and "up" in possible_moves)):
    #    return "up"
    
    elif("left" in possible_moves):
        return "left"
    else:
        return ""