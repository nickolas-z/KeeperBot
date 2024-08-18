from .helpers import print_header, print_footer, print_execution_time
from colorama import init, Fore


class Application:
    """
    A base class for creating and inheriting from other projects.
    """

    def __init__(self, app_name="Application") -> None:
        """
        Initializes the Application class.

        Args:
            app_name (str, optional): The name of the application. Defaults to "Application".
        """
        init(autoreset=True)
        self.app_name = app_name
        print_header(self.app_name)

    def __del__(self) -> None:
        """
        Cleans up resources and prints a farewell message.
        """
        print_footer("Work completed. Goodbye!")

    @print_execution_time
    def run(self) -> bool:
        """
        The main entry point for the application.

        Returns:
            bool: True if the application runs successfully, False otherwise.
        """
        # Add your custom logic here
        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the Application object.
        """
        return f"Application(app_name='{self.app_name}')"

    def print_description(self) -> None:
        """
        Prints the description of the Application class.
        """
        print(self.__doc__)

    def print_functions(self) -> None:
        """
        Prints the names and docstrings of the callable functions in the Application class.
        """
        for name, func in self.__class__.__dict__.items():
            if callable(func):
                print(name)
                print(func.__doc__)


if __name__ == "__main__":
    app = Application("Опис класу Application")
    app.print_description()
    app.print_functions()
