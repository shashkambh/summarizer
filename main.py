#! ./bin/python3
import apis
import helpers
import sys

class InvalidTaskException(Exception):
    """raised when command or dispatcher is invalid"""

command_dispatcher = {
    'task': apis.Todoist,
    'time': apis.Timer,
    'cal': apis.Calendar,
    'help': helpers.print_help,
    None: helpers.print_summary
}

commands = {
    'task': {
        'add': 'quick_add',
        'finish': 'complete_task',
        'list': 'print_all_tasks'
    },
    'time': {
        'start': 'start',
        'stop': 'stop'
    },
    'cal': {
        'list': 'print_all_events',
        'add': 'add'
    }
}

def dispatch(exeName, dispatcher=None, command=None, *args):
    if command is None:
        to_run = command_dispatcher[dispatcher]
    else:
        to_run = getattr(command_dispatcher[dispatcher](), commands[dispatcher][command])
    if to_run is None:
        raise InvalidTaskException('Failed to find task')
    return to_run(*args)

def main():
    print(dispatch(*sys.argv))

if __name__ == '__main__':
    main()
