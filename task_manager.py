# T17 Capstone Project submission for Duncan Painter

### Research and References ###

# Using case rather than if/elif/else: https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/
# Terminating a script: https://stackoverflow.com/questions/73663/how-do-i-terminate-a-script, https://www.askpython.com/python/examples/exit-a-python-program
# Comparing dates: https://www.geeksforgeeks.org/comparing-dates-python/
# Classes and modules: https://stackabuse.com/creating-and-importing-modules-in-python/
# Spread iterables: https://how.wtf/spread-operator-in-python.html
# One line if statements: https://www.golinuxcloud.com/python-for-loop-in-one-line/


### Program Code ###

#=====importing libraries===========#
import os
import sys

from Task import Task
from User import User
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# Create a new task
def add_task():
    # Assign task
    while True:
        owner = input("\nName of person assigned to task: ")
        if owner == str(-1):
            return
        elif does_user_exist(owner, 1)[0] == False:
            print("\n-> User does not exist.\n")
            print("Please enter a valid username or '-1' to return to the menu.\n")
            continue
        else:
            break

    # Get task title, description and due date
    title = input("Title of Task: ")
    description = input("Description of Task: ")
    due_date =  get_date_input("Due date of task")

    # Get new task id. Try statement loop in case no tasks currently exist.
    try:
        new_task_id = int(task_list[-1].task_id) + 1
    except IndexError:
        new_task_id = 0

    # Append new task to task list and update the task file.
    task_list.append(Task(new_task_id, owner, program_user, title, description, date.today(), due_date, "No"))
    update_task_file()
    print("\n-> Task added successfully.")
    return

# Creates upper and lower "===" boundry for reporting based on user name length.
def boundary(username):
    # This function is not critical, it is used to calculate output formatting based on username length for 'View Mine' boundaries.

    #--- test case
    test_inner_lower = f"End of tasks for {username}"
    upper = ""
    lower = ""

    if len(username) >= 14:
        width = 36
        for i in range(width+1):
            upper += "="
            lower += "="
        inner_upper = f"============= User Tasks ============"
        inner_lower = f"========= End of User Tasks ========="
    
    else:
        # boundary length defined by the max length that looked acceptable on the screen.
        boundary_length = 37    
        for i in range(boundary_length):
            upper += "="
            lower += "="

        basic_inner_upper = f" {username} Tasks "      
        outside_upper_len = int((boundary_length - len(basic_inner_upper))/2)
        outside_lower_len = int((boundary_length - len(test_inner_lower))/2)
        outside_upper = ""
        outside_lower = ""

        for i in range(outside_upper_len):
            outside_upper += "="
        for i in range(outside_lower_len-1):
            outside_lower += "="

        inner_upper = f"{outside_upper}{basic_inner_upper}{outside_upper}"
        inner_lower = f"{outside_lower} {test_inner_lower} {outside_lower}"

        if len(inner_upper) < len(upper):
            inner_upper += "="
        if len(inner_lower) < len(lower):
            inner_lower += "="

    return [f"\n{upper}", inner_upper, inner_lower, f"{lower}\n"]

# Check if a file exists
def check_if_file_exists(file):
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

# Check if a user exists
def does_user_exist(user_input, check_type):

    # Type 0, check if any variation of the name exists. Type 1, check if the exact name exits.
    # Type 0 - Create new user (eg, so only one of Admin, admin, ADMIN can exist)
    # Type 1 - Log in, create a new task (eg, task can only be assigned to the exact name created. Or, only admin can log in, Admin and ADMIN cannot.)

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

# Exit function to close program
def exit_program():
    while True:
        user_input = input("""\nSelect an option:
    c - Close program
    r - Return to menu
    :""")
        if user_input.lower() != "c" and user_input.lower() != "r":
            print("\n-> Invalid selection.")
            continue
        elif user_input.lower() == "r":
            return
        else:
            sys.exit("\n-> Program closed.\n")

# Generate a list of tasks
def generate_task_list():
    with open("tasks.txt", 'r') as file:
        for i, task in enumerate(file):
            task_list.append(Task(*task.split(";")))
    return

# Generate a list of users
def generate_user_list():
    with open("users.txt", 'r') as user_file:
        for i, user in enumerate(user_file):
            user_list.append(User(*user.split(";")))
    return

# Get date input and validate the response
def get_date_input(message):
    while True:
        try:
            task_due_date = input(f'{message} (YYYY-MM-DD): ')
            # due-date_time is only used to trigger the try loop, datetime is not used or returned in this instance.
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("\n-> Invalid datetime format. Please use the format specified.\n")
    return task_due_date


# Handle login process.
def login():
    check_if_file_exists("users.txt")
    generate_user_list()
    while True:
        print("\nLOGIN")
        username_input = input("Username: ")
        password_input = input("Password: ")
        user_check = does_user_exist(username_input, 1)
        if user_check[0] == False:
            print("\n-> User does not exist.")
            continue
        elif password_input != user_check[1]:
            print("\n-> Incorrect login details, try again.")
            continue
        else:
            print(f'\n-> Successfully logged in as "{username_input}".\n')
            break            

    check_if_file_exists("tasks.txt")
    try: # an empty task file will return an empty list which causes an error with the spread operator
        task_list.append(*Task.generate_task_list())
    except:
        pass
    return username_input

# Create a new user
def reg_user():

    # Request input of a new username
    while True:
        new_username = input("\nNew Username: ")
        
        if does_user_exist(new_username, 0) == True:
            print("\n-> User already exists, please enter a different username.\n")
            continue
        else:
            break

    # Request input of a new password
    while True:
        new_password = input("\nNew Password: ")
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # write new user to user list and update user file    
            user_list.append(User(new_username,new_password,0,0))
            update_user_file()
            break
        else:
            print("\n-> Entered passwords do not match, please try again.")
            continue    
    print(f'\n\n-> {new_username} added sucessfully.') 
    return

# Print results to console and create task_overview.txt
def task_overview_creation():
    # Get total tasks
    try:
        total_tasks = int(task_list[-1].task_id) + 1
    except IndexError:
        total_tasks = 0

    # Get completed task qty, calculate incomplete tasks and overdue percentage
    completed_tasks = 0
    overdue_task_qty = 0
    for task in task_list:
        if task.is_complete == "Yes":
            completed_tasks += 1
            continue
        if task.is_overdue == True:
            overdue_task_qty +=1    
    incomplete_tasks = total_tasks - completed_tasks

    # Calculate incomplete percentages
    incomplete_percentage = 0
    try:
        incomplete_percentage = int((incomplete_tasks/total_tasks)*100)
    except ZeroDivisionError:
        incomplete_percentage = 0

    # Calculate overdue percentage
    try:
        overdue_percentage = int((overdue_task_qty/(total_tasks-completed_tasks))*100)
    except ZeroDivisionError:
        overdue_percentage = 0

    # Print results to the console.
    if len(task_list) == 0:
        print(f"\n=========== TASK OVERVIEW ===========\n\n")
        print("No tasks registered.")
        print("\n\n============= TASK  END =============")
        with open("task_overview.txt", "w") as task_overview_file:
            task_overview_file.write(f"No registered tasks.")
        return
    else:
        print(f"\n=========== TASK OVERVIEW ===========\n\n")
        print(f"Task List Overview:")
        print(f"    Total Tasks:            {total_tasks}")
        print(f"    Completed tasks:        {completed_tasks}")
        print(f"    Incomplete Tasks:       {incomplete_tasks}")
        print(f"    Overdue tasks:          {overdue_task_qty}")
        print(f"    Percentage:")
        print(f"        Incomplete:         {incomplete_percentage}%")
        print(f"        Remaining, overdue: {overdue_percentage}%")
        print("\n\n============= TASK  END =============")

        # Create reference file
        with open("task_overview.txt", "w") as task_overview_file:
            task_overview_file.write(f"Task List Overview:\n")
            task_overview_file.write(f"    Total Tasks:            {total_tasks}\n")
            task_overview_file.write(f"    Completed tasks:        {completed_tasks}\n")
            task_overview_file.write(f"    Incomplete Tasks:       {incomplete_tasks}\n")
            task_overview_file.write(f"    Overdue tasks:          {overdue_task_qty}\n")
            task_overview_file.write(f"    Percentage:\n")
            task_overview_file.write(f"        Incomplete:         {incomplete_percentage}%\n")
            task_overview_file.write(f"        Remaining, overdue: {overdue_percentage}%\n")
        return

# Decide what the user wants to do.
def task_select(program_user):
    while True:
        task_selected = False
        while task_selected == False:
            # if statement to control the acceptable options based on user type.
            # admin includes display statistic option
            if program_user == "admin":
                acceptable_selection = {
                    "r": "  -  Register a user",
                    "a": "  -  Add a task",
                    "va": " -  View all tasks",
                    "vm": " -  View my tasks",
                    "ds": " -  Display statistics",
                    "e": "  -  Exit"}
                
                print("\nSelect an option:")
                for option in acceptable_selection:
                    print(f"    {option}{acceptable_selection[option]}")
                selection = input("    : ")
            
            # options for users other than admin
            else:
                acceptable_selection = {
                    "r": "  -  Register a user",
                    "a": "  -  Add a task",
                    "va": " -  View all tasks",
                    "vm": " -  View my tasks",
                    "e": "  -  Exit"}
                print("\nSelect an option:")
                for option in acceptable_selection:
                    print(f"    {option}{acceptable_selection[option]}")
                selection = input("    : ")

            # check if input is acceptable           
            if selection not in acceptable_selection:
                print("\n-> Invalid selection.")
                continue
            else:
                task_selected = True

        # Match correct input to required function
        match selection:
            case "r":
                reg_user()
            case "a":
                add_task()
            case "va":
                view_all()
            case "vm":
                view_mine(program_user)
            case "ds":
                print("\n\n=====================================")
                user_overview_creation()
                task_overview_creation()
                print("=====================================\n")
            case "e":
                exit_program()
        
        continue

# Update the user file
def update_user_file():
    for user in user_list:
        user.task_reset()
        for task in task_list:
            if task.owner != user.username:
                continue
            if task.owner == user.username:
                user.add_to_task_count()
            if task.is_overdue == True:
                user.has_overdue_task()
            if task.is_complete == "Yes":
                user.add_to_complete_count()
    
    with open("users.txt", "w") as user_file:
        for user in user_list:
            user_file.write(user.string_to_file())
    return

# Update the task file
def update_task_file():
    with open("tasks.txt", "w") as task_file:
        for task in task_list:
            task.is_task_overdue()
            task_file.write(task.string_to_file())
    return

# Print results to console and create user_overview.txt
def user_overview_creation():
    # Update the task list and file with the latest updates, checking for overdue tasks
    # Update the user list and file, populating user task qty and overdue task qty 
    update_task_file()
    update_user_file()

    # Get number of users
    registered_user_qty = 0
    for user in user_list : registered_user_qty += 1

    # Get list of users with 0 tasks
    no_task_list = [user.username for user in user_list if user.tasks_assigned == 0]
    
    # Get number of tasks registered
    try:
        number_of_tasks_created = int(task_list[-1].task_id) + 1
    except IndexError:
        number_of_tasks_created = 0

    # Print results to Console
    print("=========== USER OVERVIEW ===========\n\n")
    print("General Overview")
    print(f"    Registered Users:       {registered_user_qty}")
    print(f"    Tasks Created:          {number_of_tasks_created}")
    for user in user_list:
        if user.tasks_assigned > 0:
            print(user)
    for user in no_task_list:
        print(f"\n  There are no tasks allocated to {user}.")
    print("\n\n============= USER  END =============")

    # Create reference file
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("General Overview\n")
        user_overview_file.write(f"    Registered Users:       {registered_user_qty}\n")
        user_overview_file.write(f"    Tasks Created:          {registered_user_qty}\n")
        for user in user_list:
                if user.tasks_assigned > 0:
                    user_overview_file.write(f"{user}\n")
        for user in no_task_list:
            user_overview_file.write(f"\n   There are no tasks allocated to {user}.")
    return

# Start of edit process selection.
def user_task_options():
    # Present the user the option edit a task or return to the main menu
    # Checks - make sure id exists
    #        - user owns task
    #        - task is not complete
    while True:
        try:
            id_selection = int(input("""Enter the Task ID to make an update.
Enter '-1' to return the main menu.\n:"""))
            if id_selection == -1:
                # User has selected to return to the main menu.
                return
        except ValueError:
            print("\n-> Incorrect Task ID selection, please try again.\n")
            continue

        # Check if the task exists
        task_exists = False
        for task in task_list:
            if task.task_id == id_selection:
                task_exists = True
                break

        # Check the user is the task owner, and if the task is complete
        if task_exists == False:
            print("\n-> Task ID does not exist, please try again.\n")
            continue
        elif task.owner != program_user:
            print("\n-> Task not owned by user, please select another option.\n")
            continue
        elif task.is_complete == "Yes":
            print("\n-> Task is already complete and cannot be edited.\n")
            continue
        else:
            break
    
    #===== User entered a valid ID to make a task update =====
    # 1 - Mark as complete
    # 5 - Edit and re assign
    # 9 - Edit and change due date

    # Get update type
    allowable_update_selection = ["1", "5", "9"]
    while True:
        selection = input("""\n1 - Mark task complete
5 - Re assign the task
9 - Update task due date
:""")
        if selection in allowable_update_selection:
            break
        else:
            print("\n-> Incorrect selection, please try again.")

    #--- 1 - Mark as complete
    if selection == "1":
        task.mark_task_complete()
        update_task_file()
        return

    #--- 5 - Re assign the task  
    if selection == "5":
        while True:
            # Get new user name
            # Check user exists
            new_owner = input("\nEnter the new task owners username: ")
            is_user_valid = does_user_exist(new_owner, 1)[0]
            if is_user_valid == True:
                task.reassign_task(new_owner)
                update_task_file()
                return
            else:
                print("\n-> Invalid user, please try again.")
                continue  
    
    #--- 9 - Update task due date
    if selection == "9":
        new_date = get_date_input("\nEnter the updated date")
        task.update_due_date(new_date)
        update_task_file()
        return

# View all of the tasks
def view_all():
    if task_list == []:
        print('\n==================================\n')
        print("There are no tasks logged.")
        print('\n==================================\n')
        return

    else:
        # Loops though task list to print all tasks.
        print('\n======================================')
        print("========= Start of Task List =========\n")
        
        for task in task_list:
            print(f"\n{task}\n")
        print("\n========== End of Task List ==========")
        print('======================================\n')  
        return

# Show user tasks
def view_mine(user):
    
    # Boundary function generates custom length headers and footers based on username length.
    boundaries = boundary(user)
    print(f"\n{boundaries[0]}")
    print(f"{boundaries[1]}\n")

    # Loop through task list and print any tasks owned by the logged in user
    user_has_tasks = False
    for task in task_list:
        if task.owner == user:
            user_has_tasks = True
            print(f"\n{task}\n")
    if user_has_tasks == False:
        print("You have no outstanding tasks.")
        print(f"\n{boundaries[2]}")
        print(f"{boundaries[3]}\n")
        return

    # Print lower boundaries
    print(f"\n{boundaries[2]}")
    print(f"{boundaries[3]}\n")

    # Present user with options to edit or update tasks
    user_task_options()
    return 


#------- Create a global list placeholders
user_list = []
task_list = []

#------- Run Program

program_user = login()
#program_user = "admin"

task_select(program_user)

