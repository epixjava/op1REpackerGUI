import click
import os
import sys
import importlib.util


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

class OpieCLI(click.MultiCommand):
    opie_logo = r"""
  ___    ____    _   _______
 / _ \  |  _ \  (_) | |_____| 
| | | | | | | | | | | |__
| | | | | |_| | | | | |__|
| |_| | |  __/  | | | |_____  
 \___/  |_|     |_| |_|_____| 

*================================*
   | Your OP-1 's best frand! |
*================================*
"""
    
    def __init__(self, **attrs):
        click.MultiCommand.__init__(self, invoke_without_command=True, no_args_is_help=False, chain=False, **attrs)
    
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
     ns = {}
     fn = os.path.join(plugin_folder, name + '.py')
     with open(fn) as f:
         code = compile(f.read(), fn, 'exec')
         eval(code, ns, ns)
     return click.Command(name, callback=ns['cli'].callback)

    def get_command_description(self, name):
        spec = importlib.util.spec_from_file_location(name, os.path.join(plugin_folder, name + '.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, 'description', 'No description available.')

    def print_help(self):
        commands = self.list_commands(None)
        print("Available commands: \n")
        for cmd in commands:
            description = self.get_command_description(cmd)
            print(f"  {cmd}: {description}")

    def invoke(self, ctx,):
        print(self.opie_logo)
        self.print_help()
        while True:
            choice = input("\nEnter a command or type exit: ").strip().lower()
            
            if choice in ['quit', 'exit']:
                print("Exiting...\nPlease return to OP-1RepackerGUI")
                return
            elif choice in self.list_commands(ctx):
                command = self.get_command(ctx, choice)
                return command.invoke(ctx)
            else:
                print(f"Invalid command: {choice}. Please select from the list of available commands")

cli = OpieCLI()

if __name__ == '__main__':
    cli()
