# Imports
from User import User


# Code
user_list = []


def generate_user_list():
    with open("users.txt", 'r') as user_file:
        for i, user in enumerate(user_file):
            user_list.append(User(*user.split(";")))
    return


def does_user_exist(user_input, check_type):
    """Checks if a user exists.
    Type 0, check if any variation of the name exists. Type 1, check if the exact name exits.
    Type 0 - Create new user (eg, so only one of Admin, admin, ADMIN can exist)
    Type 1 - Log in, create a new task (eg, task can only be assigned to the exact name created. Or, only admin can log in, Admin and ADMIN cannot.)
    """

    if check_type == 0:
        for user in user_list:
            if user_input.lower() == user.username.lower():
                return True
        return False

    if check_type == 1:
        for user in user_list:
            if user.username == user_input:
                return [True, user.password]
        return [False, ""]
    else:
        print("-> Error with type declaration inside does_user_exist")
        return


generate_user_list()
print(user_list)
