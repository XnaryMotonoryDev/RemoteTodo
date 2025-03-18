from todoist_api_python.api import TodoistAPI
from todo_tracker import TodoTracker
from commands import Command

import re

def is_valid(api_token: str) -> bool:
    if len(api_token) < 40:
        return False
    
    if not re.match(r"^[a-zA-Z0-9]+$", api_token):
        return False
    
    return True

def init_todo():
    print("Before you start, please enter your Todoist IP")
  
    user_api = input("> ")

    if is_valid(user_api):
        todo = TodoistAPI(user_api)
        print("Initialization was successful")
        return todo
    else:
        print("Your IP is invalid")

if __name__ == "__main__":
    todo = init_todo()
    tracker = TodoTracker(todo)

    cmd = Command("Welcome to remote Todoist program. Enter the help for hint")

    cmd.add_command('list', "List todos", tracker.list_todos)
    cmd.add_command('create', "Create todo", tracker.create_todo)
    cmd.add_command('delete', "Delete todo", tracker.delete_todo)


    while True:
        user_commands = input('> ').strip().split()
        if not user_commands:
            continue

        command = user_commands[0]
        args = user_commands[1:]

        result = cmd.execute(command, *args)

        match command.lower():
            case 'create':
                print(f"Проект: {result.name} создан. (ID: {result.id})")
            case 'list':
                print(f"All available todos\n{result}")
