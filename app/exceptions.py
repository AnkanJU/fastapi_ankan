class TodoNotFoundException(Exception):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id