from colorama import Fore
from bot import Bot
from bot_cmd import BotCmd


def completer(text, state):
    """
    This function provides autocompletion for the user input.
    Args:
        text: the current input text.
        state: the current state.
    """
    options = [cmd for cmd in BotCmd.get_all_commands() if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


# Run the application
if __name__ == "__main__":
    try:
        Bot("Welcome to the KeeperBot!").run()
    except EOFError:
        print(f"\n{Fore.RED}Input ended unexpectedly. Exiting the application.")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Operation cancelled (Ctrl+C). Exiting the application.")
