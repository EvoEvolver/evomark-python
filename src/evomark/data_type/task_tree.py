

class Task:
    def __init__(self, content: str):
        self.sub_tasks: list[Task] = []
        self.content = content

    def add_sub_task(self, task: Task):
        self.sub_tasks.append(task)