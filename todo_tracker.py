from todoist_api_python.models import Task, Project, Section
from todoist_api_python.api import TodoistAPI

from typing import Union


class TodoTracker:
    def __init__(self, todo: TodoistAPI):
        self.todo = todo

    def create_todo(self, *args: str) -> Union[Task, Project, Section]:
        if args[0] == '-t':
            return self.create_task(*args)
        elif args[0] == '-s':
            return self.create_section(*args)
        else:
            return self.create_project(args[0])

    def create_project(self, name: str) -> Project:
        return self.todo.add_project(name)

    def create_task(self, *args: str) -> Task:
        content = args[1]

        if '--project' in args:
            project_name = args[3]
            project_id = self.__get_project_id(project_name)

            if '--section' in args:
                section_name = args[5]
                section_id = self.__get_section_id(section_name)

                self.todo.add_task(content, project_id=project_id, section_id=section_id)

            task = self.todo.add_task(content, project_id=project_id)
        else:
            task = self.todo.add_task(content)
        return task
    
    def create_section(self, *args: str) -> Section:
        section_name = args[1]
        name = args[2]

        _id = self.__get_project_id(name)
        self.todo.add_section(section_name, _id)

    def list_todos(self, *args):
        projects = self.todo.get_projects()

        full = len(args) > 0 and args[0] == '-f'
        if full:
            if projects:
                for project in projects:
                    if project.name.lower() == 'inbox':
                        continue
    
                    project_name = project.name
                    project_id = project.id
                    
                    tasks = self.todo.get_tasks(project_id=project.id)
                    sections = self.todo.get_sections(project_id=project.id)
    
                    print('Project:')
                    print(f"\tNAME: {project_name}")
                    print(f"\tID: {project_id}")
                    print("\tTasks:")
    
                    self.__check_tasks(tasks)

                    print("\tSections:")

                    self.__check_sections(sections)

        else:
            if projects:
                project_info = [f"NAME: {project.name}\t{project.id}" for project in projects if project.name.lower() != 'inbox']

                if project_info:
                    return '\n'.join(project_info)


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
            
    def __check_sections(self, sections):
        if sections:
            for section in sections:
                print(f"\t\t{section.name}")
        else:
            print("\t\tNo sections found.")

    def __check_tasks(self, tasks):
        if tasks:
            for task in tasks:
                print(f"\t\t{task.content}")
        else:
            print("\t\tNo tasks found.")

    def __get_project_id(self, name: str) -> int:
        projects = self.todo.get_projects()

        for project in projects:
            if project.name == name:
                return project.id
            
    def __get_section_id(self, name: str) -> int:
        sections = self.todo.get_sections()

        for section in sections:
            if section.name == name:
                return section.id