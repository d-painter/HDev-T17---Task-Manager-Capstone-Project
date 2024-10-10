from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


class Task:
    """Task class"""

    # Set whether a task is overdue to false
    is_overdue = False


    def __init__(self, task_id, owner, created_by, title, description, date_raised, date_due, is_complete):
        self.task_id = int(task_id)
        self.owner = owner
        self.created_by = created_by
        self.title = title
        self.description = description
        self.date_raised = date_raised
        self.date_due = date_due
        self.is_complete = is_complete.strip("\n")

    def __str__(self) -> str:
        """Returns task overview"""
        return f"""Task Id:     {self.task_id}
Task Title:  {self.title}
Task Owner:  {self.owner}
Created by:  {self.created_by}
Date Raised: {self.date_raised}
Date Due:    {self.date_due}
Complete:    {self.is_complete}
Task Description:
    {self.description}"""

    # Determine if a task is overdue
    def is_task_overdue(self):
        due_date_time = datetime.strptime(self.date_due, DATETIME_STRING_FORMAT)
        current_date_time = datetime.today()
        if self.is_complete == "Yes":
            return
        if current_date_time > due_date_time:
            self.is_overdue = True        
            return
    
    # Mark a task complete
    def mark_task_complete(self):
        if self.is_complete == "No":
            self.is_complete = "Yes"
            print(f"\n-> Task {self.task_id} has been marked complete.\n")
            return
        else:
            print("\nError marking task complete, task is already complete.\n")
            return

    # Reassign a task    
    def reassign_task(self, new_owner):
        self.owner = new_owner
        print(f"\n-> Task {self.task_id} has been reassigned to {new_owner}.")
        return

    # Create a string to write to a file
    def string_to_file(self):
        return f"{self.task_id};{self.owner};{self.created_by};{self.title};{self.description};{self.date_raised};{self.date_due};{self.is_complete}\n"  
    
    # Update a task due date
    def update_due_date(self, new_due_date):
        self.date_due = new_due_date
        print(f"\n-> Due date updated to {new_due_date}.")
        return

    