import time
import ast
import os
from functools import wraps
from colorama import Fore, Style, init

HEADER_LENGTH = 90
# Initialize colorama
init(autoreset=True)


def print_header(_text):
    """
    Function to print a greeting message to the user.
    Args:
        _text: String with the greeting message.
    Return:
        ================================
        --------------- _text ---------------
    """
    print("=" * HEADER_LENGTH)
    message_text = f" {_text} "
    print(f"{Fore.BLUE}{message_text:-^{HEADER_LENGTH}}", end="\n\n")


def print_footer(_text):
    """
    Function to print a completion message to the user.
    Args:
        _text: String with the completion message.
    Return:
        --------------- _text ---------------
        ================================
    """
    message_text = f" {_text} "
    print(f"\n{Fore.BLUE}{message_text:-^{HEADER_LENGTH}}" + Style.RESET_ALL)
    print("=" * HEADER_LENGTH, end="\n\n")


def print_execution_time(func):
    """
    Decorator that measures and prints the execution time of the decorated function.
    Args:
        func (callable): The function to be decorated.
    Returns:
        callable: The decorated function that measures and prints the execution time.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, "start_time"):
            wrapper.start_time = time.time()
            wrapper.call_depth = 0

        wrapper.call_depth += 1
        result = func(*args, **kwargs)
        wrapper.call_depth -= 1

        if wrapper.call_depth == 0:
            end_time = time.time()
            print(
                f"{Fore.MAGENTA}{func.__name__} executed in {end_time - wrapper.start_time:.6f} seconds"
            )
            del wrapper.start_time

        return result

    return wrapper


def list_functions_in_file(file_path):
    """
    Prints all functions in a Python file along with their docstrings.

    Args:
        file_path (str): The path to the Python file.
    """
    try:
        with open(file_path, "r") as file:
            # Read the file content
            file_content = file.read()

        # Parse the file content into AST
        tree = ast.parse(file_content)

        # Traverse all nodes in the AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                # Get the docstring of the function
                docstring = ast.get_docstring(node)

                # Print the function name and its description with colors
                print(Fore.CYAN + f"Function: {Fore.WHITE}{func_name}")
                if docstring:
                    print(Fore.GREEN + "Description:")
                    print(Fore.YELLOW + f"{docstring}")
                else:
                    print(Fore.RED + "Description: No docstring")
                print(Style.RESET_ALL)  # Reset the style

    except FileNotFoundError:
        print(Fore.RED + f"File not found: {file_path}")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")


def main():
    """Main function for performing calculations"""

    print_header("Module with helper functions")

    # Print information about the module and the list of functions
    current_file = os.path.abspath(__file__)
    list_functions_in_file(current_file)

    print_footer("Work completed.")


# Call the main function
if __name__ == "__main__":
    main()
