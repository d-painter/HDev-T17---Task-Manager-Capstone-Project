# T17 Capstone Project submission for Duncan Painter

### Research and References ###

# Using case rather than if/elif/else: https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/
# Terminating a script: https://stackoverflow.com/questions/73663/how-do-i-terminate-a-script
# Removing duplicates fom lists using sets: https://www.programiz.com/python-programming/methods/built-in/set
# Counting lines in a file: https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
# Comparing dates: https://www.geeksforgeeks.org/comparing-dates-python/
# https://www.w3schools.com/python/ref_func_round.asp
# Sorting keys: https://learnpython.com/blog/sort-alphabetically-in-python/

### Program Code ###

#=====importing libraries===========#
import os
import sys
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# get user password
def get_user_password(input_name):
    user_password = ""
    check_if_file_exists("user.txt")
   
    with open("user.txt", "r") as file:
        for i, line in enumerate(file):
                    user_info = line.split(";")
                    if user_info[0] == input_name:
                        user_password = user_info[1].strip("\n")
                        break
    
    if user_password == "":
        return 0
    else:
        return user_password

# Function to handle login process.
def login():

    logged_in = False
    while not logged_in:

        print("\nLOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        
        # Request to get user password
        # Returns 0 for no user, [user password, user index] if they exist.
        user_pw_state = get_user_password(curr_user)

        if user_pw_state == 0:
            print("User does not exist")
            continue
        elif user_pw_state != curr_pass:
            print("Incorrect login details, try again.")
            continue
        else:
            print(f'\nSuccessfully logged in as "{curr_user}".\n')
            logged_in = True            

    return curr_user

# Check to see if a user exists
def user_exists(input_name, int):
    
    # Create a loop which checks the user input against the names to check.

    # example registered user = "Adam"
    # Int 0 - used to check all instances when creating a new user.
    # Ie, try to create "adam" - check if Adam, ADAM, adam alread registered by using .lower()
    # "Adam" exists, so return true.

    # Int 1 - used when creating a new task. Need to ensure there aren't multiple versions of the same name.
    # Ie, using Int 0 and assining a task to "adam" will return true meaning a task could be created against "Adam", "adam" or "ADAM"
    # and this would make a mess of the user log and reporting.

    # Int 0, check if any variation of the name exists. Int 1, check if the exact name exits.

    # This issue could be fixed by declaring False for the Int 0 case, but then reading the
    # logic within reg_user would be backwards and hard to read.

    user_exists = False
    while user_exists == False:
        with open("user.txt", "r") as task_file:
            if int == 0:
                for line in task_file:
                    user_info = line.split(";")
                    if user_info[0].lower() == input_name.lower():
                        user_exists = True
                        break
            if int == 1:
                for line in task_file:
                    user_info = line.split(";")
                    if user_info[0]== input_name:
                        user_exists = True
                        break
        break
    

    return user_exists

# Function to decide what task is required
def task_select():
    while True:
        task_selected = False
        while task_selected == False:
            #if statement to control the acceptable input based on user type.
            # presenting the menu to the user and 
            # making sure that the user input is converted to lower case.
            if program_user == "admin":
                acceptable_selection = ["r", "a", "va", "vm", "ds", "e"]
                selection = input('''\nSelect an option:
    r -  Registering a user
    a -  Adding a task
    va - View all tasks
    vm - View my task
    ds - Display statistics
    e -  Exit
    : ''').lower()
            else:
                acceptable_selection = ["r", "a", "va", "vm", "e"]
                selection = input('''\nSelect one of the following options below:
    r -  Registering a user
    a -  Adding a task
    va - View all tasks
    vm - View my task
    e -  Exit
    : ''').lower()
            
            if selection not in acceptable_selection:
                print("\nIncorrect selection")
                continue
            else:
                task_selected = True

        match selection:
            case "r":
                reg_user()
            case "a":
                check_if_file_exists("tasks.txt")
                add_task()
            case "va":
                check_if_file_exists("tasks.txt")
                view_all(generate_task_list())
            case "vm":
                check_if_file_exists("tasks.txt")
                view_mine(generate_task_list(), program_user)
            case "ds":
                check_if_file_exists("tasks.txt")
                user_overview_creation()
                task_overview_creation()
            case "e":
                exit_program()
        
        continue

# Check if a file exists
def check_if_file_exists(file):
    try:
        with open(file, "r") as file_to_check:
            return
    except FileNotFoundError:
        if file == "user.txt":
            with open(file, "w") as user_file:
                user_file.write("admin;password")
        else:
            with open(file, "w") as new_file:
                return

# Get amount of tasks in the task list file
def count_tasks():
    i=0
    with open("tasks.txt", "r") as task_file:
        for line in task_file:
            i +=1    
    return i

# Create task list, returns a dictonary.
def generate_task_list():

    task_list = []
    with open("tasks.txt", 'r') as file:
       
        for i, t_str in enumerate(file):
            curr_t = {}

            # Split by semicolon and manually add each component
            task_components = t_str.split(";")
            curr_t["Task ID"] = task_components[0]
            curr_t['username'] = task_components[1]
            curr_t["Created By:"] = task_components[2]
            curr_t['title'] = task_components[3]
            curr_t['description'] = task_components[4]
            curr_t['due_date'] = datetime.strptime(task_components[5], DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(task_components[6], DATETIME_STRING_FORMAT)
            curr_t['completed'] = task_components[7].strip("\n")

            task_list.append(curr_t)
    return task_list

# Create a list of users
def generate_user_list():
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    user_dict = {}
    for i, user in enumerate(user_data):
        username, password = user.split(';')
        user_dict[i] = {
            "dict id": i,
            "username": username,
            "password": password
        }

    return user_dict

# Create a new task
def add_task():
        # Allow a user to add a new task to task.txt file
        # Prompt a user for the following: 
        # A username of the person whom the task is assigned to,
        # A title of a task,
        # A description of the task and 
        # the due date of the task.

    while True:
        task_username = input("\nName of person assigned to task: ")
        if task_username == str(-1):
            return
        elif user_exists(task_username,1) == False:
            print("\nUser does not exist.")
            print("Please enter a valid username or '-1' to return to the menu.\n")
            continue
        else:
            break
    
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    
    due_date_time =  get_date_input("Due date of task")

    # Then get the current date.a
    curr_date = date.today()

    # Creates a single line string for the task and writes it to the file.
    new_task_num = str(count_tasks())
    with open("tasks.txt", "a+") as task_file:
        str_attrs = [
            new_task_num,
            task_username,
            program_user,
            task_title,
            task_description,
            due_date_time.strftime(DATETIME_STRING_FORMAT),
            curr_date.strftime(DATETIME_STRING_FORMAT),
            'No'
        ]
        task_file.write(f'{";".join(str_attrs)}\n')
    
    print("Task successfully added.")
    
    return
    
# Exit Function to close program
def exit_program():
    while True:
        user_input = input("""\nSelect an option:
    c - Close program
    r - Return to menu
    :""")
        if user_input.lower() != "c" and user_input.lower() != "r":
            print("\nInvalid selection")
            continue
        elif user_input.lower() == "r":
            return
        else:
            print("\nProgram closed\n")
            sys.exit()

# Create a new user
def reg_user():

    '''Add a new user to the user.txt file'''
    # Request input of a new username
    while True:
        new_username = input("\nNew Username: ")
        
        if user_exists(new_username, 0) == True:
            print("\nUser already exists, please enter a different username.\n")
            continue
        else:
            break

    # - Request input of a new password
    while True:
        new_password = input("\nNew Password: ")
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # write new user to file    
            with open("user.txt", "a+") as out_file:
                user_data = f"{new_username};{new_password}"
                out_file.write(f"\n{user_data}")
            break
        else:
            print("\nEntered passwords do not match, please try again.")
            continue
    print("\n\n================================")      
    print(f'{new_username} added sucessfully.')
    print("================================")      

    return
    
# Function to print all tasks
def view_all(task_list):
    if task_list == []:
        print('\n==================================\n')
        print("There are no tasks logged.")
        print('\n==================================\n')
        return

    else:
        # Takes task list from generate_task_list and loops throught to print all open tasks.
        print('\n======================================')
        print("========= Start of Task List =========\n")
        
        for t in task_list:
            disp_str = f"Task ID:\t {t['Task ID']}\n"
            disp_str += f"\nTask: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
        print("\n========== End of Task List ==========")
        print('======================================\n')  
        return

# Creates upper and lower "===" boundry for reporting based on user name length.
def boundary(username):
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

# Show user tasks
def view_mine(task_list, user):
    # Function takes the task list and signed in user as inputs
    # Looks to see if the user has tasks
    # If the user has tasks, prints them. If not, prints no tasks.
    boundaries = boundary(user)
    # Create a list of users who have tasks allocated to them.
    users_with_tasks = []
    for t in task_list:
        users_with_tasks.append(t["username"])

    # If logged in user has taks, list them. If not, state no tasks.
    user_task_ids = []
    if user in set(users_with_tasks):
        print(boundaries[0])
        print(boundaries[1])
        for t in task_list:
            if t['username'] == user:
                user_task_ids.append(t["Task ID"])
                disp_str = f"Task ID:\t {t['Task ID']}\n"
                disp_str += f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
        print(boundaries[2])
        print(boundaries[3])
    else:
        print('\n==================================\n')
        print("You have no outstanding tasks.")
        print('\n==================================\n')
    user_task_options(user_task_ids)

    return   

# Get the total registered users
def total_registered_users():
    num_lines = sum(1 for line in open('user.txt'))
    return num_lines

# Get the total amount of tasks.
# Tasks are not deleted or removed when complete
def total_tasks_created():
    i=0
    with open("tasks.txt", 'r') as file:
       for i, line in enumerate(file):
           i+=1

    return i

# Tasks assigned to a specific user
def user_task_list(task_list, user):
    user_tasks = []
    num_of_tasks = 0
    complete_tasks = 0
    late_tasks = 0
    current_date = datetime.today()
    for task in task_list:
        if task["username"] == user:
            user_tasks.append(task)
            num_of_tasks +=1
            if task["completed"].strip("\n") == "Yes":
                complete_tasks +=1
            if task["due_date"] < current_date:
                late_tasks +=1

    return [user_tasks, num_of_tasks, complete_tasks, late_tasks]

# Collate information for user_overview.txt
def user_overview_setup():

    users_registered = total_registered_users()
    total_tasks = total_tasks_created()

    general_overview_string = f'''General Overview
    Users Registered:\t    {users_registered}
    Total Tasks:\t    {total_tasks}'''
    #print(general_overview_string)

    user_list = generate_user_list()

    # sort user name so the output is alphabetical
    user_names = []
    for entry in user_list:
        user_names.append(user_list[entry]["username"])    
    sorted_user_names = sorted(user_names, key=str.lower)

    no_task_users = []
    user_strings = []
    for user in sorted_user_names:
        user_stats = user_task_list(generate_task_list(), user)
        user_tasks, num_of_tasks, completed_tasks, late_tasks = user_stats

        # if the user doesnt have
        if num_of_tasks == 0:
            no_task_users.append(user)
        else:
            if completed_tasks == 0 and num_of_tasks > 0:
                percent_to_complete = 100
            else:
                percent_to_complete = (completed_tasks/num_of_tasks)*100
        
            if late_tasks == 0:
                overdue_percentage = 0
            else:
                overdue_percentage = (late_tasks/(num_of_tasks-completed_tasks))*100
            
            user_strings.append(f'''\n{user} Overview:
    Total user tasks:\t    {num_of_tasks}
    Completed Tasks:\t    {completed_tasks}
    Percentage to complete: {round(percent_to_complete)}%
    Percentage remaining
    which are overdue:\t    {round(overdue_percentage)}%
    ''')

    return [general_overview_string, user_strings, no_task_users]

# Collate information for user_overview.txt
def task_overview_setup():

    # setup required variables 
    total_tasks = total_tasks_created()
    if total_tasks == 0:
        return
    task_list = generate_task_list()
    curr_date = datetime.today()
    completed_tasks = 0 
    not_completed_and_overdue = 0

    # loop through task list 
    for task in task_list:
        if task['completed'].strip("\n") == "Yes":
            completed_tasks +=1
        if task['due_date'] < curr_date:
            not_completed_and_overdue =+ 1

    # calculations
    percent_incomplete = round((completed_tasks/total_tasks)*100)
    uncompleted_tasks = total_tasks-completed_tasks

    # assuming the percent overdue is based on only incomplete tasks and not total
    percent_overdue = round((not_completed_and_overdue/uncompleted_tasks)*100)

    task_output = f'''Output:
    Total tasks:\t   {total_tasks}
    Completed tasks:\t   {completed_tasks}
    Uncompleted tasks:\t   {uncompleted_tasks}
    Incomplete percentage: {percent_incomplete}%
    Percent Overdue:\t   {percent_overdue}%
    '''
    return task_output

# Print results to console and create user_overview.txt
def user_overview_creation():

    #Print to Terminal
    overview_results = user_overview_setup()
    general_overview, user_overview, no_tasks = overview_results
    print("\n\n\n\n======= USER OVERVIEW =======\n")
    print(f"{general_overview}\n")
    for entry in user_overview:
        print(entry)
    for user in no_tasks:
        print(f"There are no tasks allocated to {user}.")
    print("\n========= USER  END =========")


    # Create reference file
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"{general_overview}\n")
        for entry in user_overview:
            user_overview_file.write(entry)
        for user in no_tasks:
            user_overview_file.write(f"\nThere are no tasks allocated to {user}.")
    return

# Print results to console and create task_overview.txt
def task_overview_creation():
    task_overview = task_overview_setup()

    if task_overview == None:
        print(f"\n======= TASK OVERVIEW =======\n")
        print("No tasks registered.")
        print("\n========= TASK  END =========\n\n\n\n")
        with open("task_overview.txt", "w") as task_overview_file:
            task_overview_file.write(f"No registered tasks.")
        return

    else:
        print(f"\n======= TASK OVERVIEW =======\n")
        print(f"{task_overview}")
        print("========= TASK  END =========\n\n\n\n")

        # Create reference file
        with open("task_overview.txt", "w") as task_overview_file:
            task_overview_file.write(f"{task_overview}\n")
        
        return

# Check the completed status of a task
def check_task_status(id, task_list):
    for entry in task_list:
        if entry["Task ID"] == str(id):
            if entry["completed"] == "Yes":
                return True
            else:
                return False

# Mark a task complete
def mark_complete(id, task_list):
    for entry in task_list:
        if entry["Task ID"] == str(id):
            if entry["completed"] == "Yes":
                return "Task is already complete."
            else:
                entry["completed"] = "Yes"
                return task_list
            
# Update a task date
def update_task_date(id, task_list, new_date):
    for entry in task_list:
        if entry["Task ID"] == str(id):
            entry["due_date"] = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
            break
    return task_list

# write all tasks to file
def write_task_list(new_task_list):
    with open("tasks.txt", "w") as task_file:

        for task in new_task_list:
            str_attrs =[
            task["Task ID"],
            task["username"],
            task["Created By:"],
            task["title"],
            task["description"],
            datetime.strftime(task["due_date"], DATETIME_STRING_FORMAT),
            datetime.strftime(task["assigned_date"], DATETIME_STRING_FORMAT),
            task["completed"]]
            print(f'\nstr_attrs: {";".join(str_attrs)}')
            #task_file.write(f'{";".join(str_attrs)}\n')

### Task update handler ###
def task_update(id, edit_type):
    # create a list of tasks
    task_list = generate_task_list()

    # # Check id existss ======== might not need function =========
    # if id >= len(task_list):
    #     return "That Task ID does not exist, please re enter the value."

    # See if the task is already complete.
    task_status = check_task_status(id, task_list)
    if task_status == True:
        return "\nTask is already complete, unable to make further changes."
    

    if edit_type == "complete":
        new_task_list = mark_complete(id, task_list)
        # write updates to task list
        write_task_list(new_task_list)
        return f"Task {id} has been set to 'Complete'."
    
    else:
        # date is passed through edit_type
        new_task_list = update_task_date(id, task_list, edit_type)
        # write updates to task list
        write_task_list(new_task_list)
        return f"The due date for Task {id} has been updated to {edit_type}."

# Get date input and validate the response
def get_date_input(message):
    while True:
        try:
            task_due_date = input(f'\n{message} (YYYY-MM-DD):\n')
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    return due_date_time

# Start of edit process selection.
def user_task_options(user_tasks):
    # 1 - Mark as complete
    # 2 - Edit and re assign
    # 3 - Edit and change due date

    #===== Main Menu or Edit Task Selection =====
    # Create a list of acceptable inputs, -1 to go to ma    in menu and task ids user can edit
    allowable_ids = [-1]
    for id in user_tasks:
        allowable_ids.append(id)

    # Present the user the option edit a task or return to the main menu
    while True:
        id_selection = input("""\nEnter the Task ID to make an update.
Enter '-1' to return the main menu.\n:""")
        if id_selection == str(-1) or id_selection in allowable_ids:
            break
        else:
            print("\nIncorrect input, please try again.\n")
            continue
    
    #===== User has chosen to return to the main menu =====
    if id_selection == str(-1):
        return
    
    #===== User entered a valid ID to make a task update =====
    # Get update type
    allowable_update_selection = [1, 5, 9]
    while True:
        selection = input("""\nMark task complete - 1
    Re assign the task - 5
    Update the task due date - 9""")
        if selection in allowable_update_selection:
            print("valid edit selection")
            break
        else:
            print("\nIncorrect selection, please try again.")


    #--- 1 - Mark as complete
    if selection == 1:
        update_status = task_update(int(id_selection), "complete")
        print(update_status)
        return

    #--- 5 - Re assign the task  
    if selection == 5:
        while True:
            # Get new user name
            # Check user exists
            assigned_user = input("\nEnter the updated username: ")
            is_user_valid = user_exists(assigned_user, 1)
            if is_user_valid == True:
                break
            else:
                print("\nInvalid user, please try again.")
                continue  

        # User exists, update the task.      
        update_status = task_update(int(id_selection), assigned_user)
        print(update_status)
        return
    
    #--- 9 - Update task due date
    if selection == 9:
        new_date = get_date_input("Enter the updated date")
        update_status = task_update(int(id_selection), new_date)
        print(update_status)
        return
    ### user_task_options end


#=====Run Program=====#

program_user = login()
task_select()