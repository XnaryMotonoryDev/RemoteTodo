from todoist_api_python.models import Project, Task
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
  
    while True:
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

    cmd.add_command('list', _help="List todos", description=
                    "Print the names of all projects made. For more information use the info command", action=tracker.list_todos)
    cmd.add_command('create', keys=['-t'], args=['name', 'id'], _help="Create todo", action=tracker.create_todos)
    cmd.add_command('info',  _help="Check your tasks", action=tracker.show_propertiese)
    cmd.add_command('delete', args=['id'], _help="Delete todo", action=tracker.delete_todo)


    while True:
        user_commands = input('> ').strip().split()
        if not user_commands:
            continue

        command = user_commands[0]
        args = user_commands[1:]

        result = cmd.execute(command, *args)

        match command.lower():
            case 'create':
                if isinstance(result, Project):
                    print(f"Project created: {result.name}. (ID: {result.id})")
                elif isinstance(result, Task):
                    print(f"Task created {result.content}")
            case 'list':
                print(f"All available todos\n{result}" if result else "No project found.")
