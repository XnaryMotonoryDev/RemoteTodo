from todoist_api_python.api import TodoistAPI

from typing import List, Optional



class TodoTracker:
    def __init__(self, todo: TodoistAPI):
        self.todo = todo

    def create_todo(self, name: str, tasks: List[str] = None):
        project = self.todo.add_project(name)

        if tasks is not None:
            for task in tasks:
                self.todo.add_comment(task)
        return project

    def create_todos(self, names: List[str]):
        projects = []
        for name in names:
            project = self.todo.add_project(name)
            projects.append(project)

        return projects
    
    # def check_properties(self, name: str):
    #     project = self.todo.get_project(name)

    def list_todos(self):
        projects = self.todo.get_projects()

        if projects:
            project_info = [f"NAME: {project.name}\t{project.id}" for project in projects]
            return '\n'.join(project_info)
    def delete_todo(self, _id: str):
        self.todo.delete_project(_id)