
def create_snake(snake_data):
    pass
class Snake:
    
    def __init__(self, snake_id, name, head, body):
        self.snake_id = snake_id
        self.name = name
        self.head = head
        self.body = body
    
    def cur_pos(self, head, body):
        self.head = head
        self.body = body