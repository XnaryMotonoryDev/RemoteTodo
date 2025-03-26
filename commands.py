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

    def add_command(self, command: str, keys: str | list[str] = '', args: str | list[str] = '', _help: str = '', description: str = '', action = None):
        self.commands[command] = {
            'keys': [key for key in keys],
            'args': [arg.upper() for arg in args],
            'help': _help,
            'desc': description,
            'action': action
        }

    def show_commands(self):
        print("Available commands:")

        for cmd, info in self.system_commands.items():
            print(f"\t{cmd}:\t{info['help']}")

        print()

        for cmd, info in self.commands.items():
            print(f"\t{cmd} {info['args']}:\t{info['help']}")

    def show_help_commands(self):
        for command_name in self.commands:
            command_info = self.commands[command_name]

            print(command_info['desc'])
            print('Keys:')
            print(f"\t{command_info.get('keys', '')}")

    def execute(self, command: str, *args):
        command = command.strip()

        if command.endswith('/help'):
            help_command = command[:-5]
            if help_command in self.commands:
                self.show_help_commands()

        if command in self.system_commands:
            self.system_commands[command]['action']()
        elif command in self.commands:
            action = self.commands[command]['action']
            if action:
                return action(*args)