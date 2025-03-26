from todoist_api_python.models import Project
from todoist_api_python.api import TodoistAPI


class TodoTracker:
    def __init__(self, todo: TodoistAPI):
        self.todo = todo

    def create_todos(self, *args):
        if args[0] == '-t':
            content = args[1]

            if '--project' in args:
                project_name = args[3]
                project_id = self.__get_project_id(project_name)

                task = self.todo.add_task(content, project_id=project_id)
            else:
                task = self.todo.add_task(content)
            return task
        else:
            name = args[0]
            project = self.todo.add_project(name)
            return project

    def list_todos(self):
        projects = self.todo.get_projects()

        if projects:
            project_info = [f"NAME: {project.name}\t{project.id}" for project in projects if project.name.lower() != 'inbox']

            if project_info:
                return '\n'.join(project_info)
        
    def show_propertiese(self):
        projects = self.todo.get_projects()

        if projects:
            for project in projects:
                if project.name.lower() == 'inbox':
                    continue

                project_name = project.name
                project_id = project.id
                
                tasks = self.todo.get_tasks(project_id=project.id)

                print('project:')
                print(f"\tNAME: {project_name}")
                print(f"\tID: {project_id}")
                print("\tTasks:")

                if tasks:
                    for task in tasks:
                        print(f"\t\t{task.content}")
                else:
                    print("\t\tNo tasks found.")
        else:
            print("No project found.")

    def delete_todo(self, *args: str):
        if args[0] == '-a':
            projects = self.todo.get_projects()

            for project in projects:
                    self.todo.delete_project(project.id)
                    print(f"project {project.name} was successfully deleted.")
        elif args[0].isdigit():
            _id = args[0]
            self.todo.delete_project(_id)
        else:
            name = args[0]
            project_id = self.__get_project_id(name)
            self.todo.delete_project(project_id)
            print(f"project {name} was successfully deleted.")

    def __get_project_id(self, name: str) -> int:
        projects = self.todo.get_projects()

        for project in projects:
            if project.name == name:
                return project.id