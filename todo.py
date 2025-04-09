from todoist_api_python.models import Project, Task, Section, Comment
from todoist_api_python.api import TodoistAPI
from todo_tracker import TodoTracker
from commands import Command

from Data.keys import *

import re

def is_valid(api_token: str) -> bool:
    if len(api_token) < 40:
        return False
    
    if not re.match(r"^[a-zA-Z0-9]+$", api_token):
        return False
    
    return True

def init_todo() -> TodoistAPI:

    while True:
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

    cmd.add_command('list', keys={
        '-f': "Shows full information"
    }, _help="List todos", action=tracker.list_todos)
    cmd.add_command('create', keys=create_keys, args=['name'], _help="Create todo", action=tracker.create_todo)
    cmd.add_command('ren', args=['old_name', 'new_name'], _help="Renamed project", action=tracker.rename_todo)
    cmd.add_command('delete', keys={
        '-a': "Delete all project"
    }, args=['name'], _help="Delete todo", action=tracker.delete_todo)


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
                elif isinstance(result, Section):
                    print(f"Section created {result.name}")
                elif isinstance(result, Comment):
                    print(f"Comment created {result.content}")
            case 'list':
                print(f"All available todos\n{result}" if result else "No project found.")
