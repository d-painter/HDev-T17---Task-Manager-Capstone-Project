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
