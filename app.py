from colorama import Fore
from bot import Bot

# Run the application
if __name__ == "__main__":
    try:
        Bot("Welcome to the KeeperBot!").run()
    except EOFError:
        print(f"\n{Fore.RED}Input ended unexpectedly. Exiting the application.")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Operation cancelled (Ctrl+C). Exiting the application.")
