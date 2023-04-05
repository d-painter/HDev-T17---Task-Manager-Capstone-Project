### Research and references ###

# Using int to round: https://stackoverflow.com/questions/3398410/python-get-number-without-decimal-places

class User:

    tasks_complete = 0

    def __init__(self, username, password, tasks_assigned, tasks_overdue):
        self.username = username
        self.password = password
        self.tasks_assigned = int(tasks_assigned)
        self.tasks_overdue = int(tasks_overdue)

    # User overview
    def __str__(self) -> str:
        return f"""\n{self.username} Overview:
    Total user tasks:       {self.tasks_assigned}
    Total completed tasks:  {self.tasks_complete}
    Overdue tasks:          {self.tasks_overdue}
    Percentage 
        To complete:        {self.percentage_to_complete()}%
        Remaining, overdue: {self.remaining_overdue()}%"""

    # Adds 1 tasks complete count
    def add_to_complete_count(self):
        self.tasks_complete +=1
        return
    
    # Adds 1 to the tasks assigned count
    def add_to_task_count(self):
        self.tasks_assigned += 1
        return
    
    # Adds 1 if a task is overdue
    def has_overdue_task(self):
        self.tasks_overdue += 1
        return

    # Calculate overdue percentage of remaining tasks
    def remaining_overdue(self):
        try:
            return int((self.tasks_overdue/(self.tasks_assigned-self.tasks_complete))*100)
        except ZeroDivisionError:
            return 0

    # Calculate percentage of tasks complete
    def percentage_to_complete(self):
        try:
            return int(((self.tasks_assigned-self.tasks_complete)/self.tasks_assigned)*100)
        except ZeroDivisionError:
            return 0

    # Create a string to write to a file
    def string_to_file(self):
        return f"{self.username};{self.password};{self.tasks_assigned};{self.tasks_overdue}\n"
    
    # Resets user data before metrics are updated from the task file
    def task_reset(self):
        self.tasks_assigned = 0
        self.tasks_overdue = 0
        self.tasks_complete = 0
        return
