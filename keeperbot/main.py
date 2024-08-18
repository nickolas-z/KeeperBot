import sys
import os
from colorama import Fore
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from keeperbot.bot import Bot

def main():
    try:
        Bot("Welcome to the KeeperBot!").run()
    except EOFError:
        print(f"\n{Fore.RED}Input ended unexpectedly. Exiting the application.")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Operation cancelled (Ctrl+C). Exiting the application.")

# Run the application
if __name__ == "__main__":
    main()