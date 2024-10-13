def login(user_list):
    """Authenticate a user. A successful login returns the logged in User instance."""
    while True:
        print("\nLOGIN")
        username_input = input("Username: ")
        password_input = input("Password: ")
        user_check = does_user_exist(username_input, 1, user_list)
        if user_check == False:
            print("\n-> User does not exist.")
            continue
        elif password_input != user_check.password:
            print("\n-> Incorrect login details, try again.")
            continue
        else:
            print(f'\n-> Successfully logged in as "{username_input}".\n')
            return user_check


def does_user_exist(user_input, check_type, user_list):
    """Checks if a user exists.\n
    Type 0, check if any variation of the name exists. Type 1, check if the exact name exits.\n
    Type 0 - Create new user (eg, so only one of Admin, admin, ADMIN can exist)\n
    Type 1 - Log in, create a new task (eg, task can only be assigned to the exact name created. Or, only admin can log in, Admin and ADMIN cannot.)
    """

    if check_type == 0:
        for user in user_list:
            if user_input.lower() == user.username.lower():
                return user
        return False

    if check_type == 1:
        for user in user_list:
            if user.username == user_input:
                return user
        return False
    else:
        print("-> Error with type declaration inside does_user_exist")
        return
