from todoist_api_python.api import TodoistAPI


class Command():
    def __init__(self, description: str = None):
        self.description = description
        self.__show_description()

        self.system_commands = {
            'help': {
                'help': "Output hint",
                'action': self.show_commands
            },
            'exit': {
                'help': "Exit the program",
                'action': self.__exit
            }
        }
        self.commands = {}

    def __exit(self):
        quit()

    def __show_description(self):
        print(self.description)

    def add_command(self, command: str, _help: str, action = None):
        self.commands[command] = {
            'help': _help,
            'action': action
        }

    def show_commands(self):
        print("Available commands:")

        for cmd, info in self.commands.items():
            print(f"\t{cmd}:\t{info['help']}")

        for cmd, info in self.system_commands.items():
            print(f"\t{cmd}:\t{info['help']}")

    def execute(self, command: str, *args):
        if command in self.system_commands:
            self.system_commands[command]['action']()
        elif command in self.commands:
            action = self.commands[command]['action']
            if action:
                return action(*args)