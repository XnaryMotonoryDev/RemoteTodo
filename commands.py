class Command():
    def __init__(self, description: str = None):
        self.description = description
        self.__show_description()

        self.system_commands = {
            'help': {
                'help': "Output hint",
                'action': self.show_commands
            },
            'info': {
                'help': 'Shows detailed information about commands',
                'action': self.show_info
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

    def add_command(self, command: str,
                    keys: dict[str, str] = None,
                    args: str | list[str] = '',
                    _help: str = '',
                    description: str = '',
                    action = None):
        keys = keys or {}

        self.commands[command] = {
            'keys': keys,
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

    def show_info(self):
        for cmd, info in self.commands.items():
            args_str = ' '.join([arg.upper() for arg in info['args']]) if info['args'] else ''

            print(f"{cmd} {args_str}".strip())
            if isinstance(info.get('keys'), dict):
                for key in info['keys']:
                    print(f"{cmd} {key} {args_str}".strip())

                print('\tOptions:')
                for key, desc in info['keys'].items():
                    print(f"\t{key}: {desc}")

            print()

    def execute(self, command: str, *args):
        command = command.strip()

        if command in self.system_commands:
            self.system_commands[command]['action']()
        elif command in self.commands:
            action = self.commands[command]['action']
            if action:
                return action(*args)