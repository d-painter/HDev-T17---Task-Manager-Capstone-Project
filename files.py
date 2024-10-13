# Imports
from User import User
from Task import Task


def check_if_file_exists(file):
    """Checks whether a file exists"""
    try:
        with open(file, "r") as file_to_check:
            return
    except FileNotFoundError:
        if file == "users.txt":
            with open(file, "w") as user_file:
                user_file.write("admin;password;0;0")
        else:
            with open(file, "w") as new_file:
                return


def generate_user_list():
    """Generates a list of user objects."""
    check_if_file_exists("users.txt")

    user_list = []
    with open("users.txt", 'r') as user_file:
        for i, user in enumerate(user_file):
            user_list.append(User(*user.split(";")))
    return user_list


def generate_task_list():
    """Returns an list of tasks read from tasks.txt.
    An empty task file returns an empty list.
    """
    check_if_file_exists("tasks.txt")

    task_list = []
    with open("tasks.txt", 'r') as file:
        for i, task in enumerate(file):
            task_list.append(Task(*task.split(";")))
    return task_list
