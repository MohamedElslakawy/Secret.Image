# Version 1.0
# This class is responsible for making the connection between all classes
# and managing the flow of the program.

# Import the Interface class from the ui folder.
from ui.interface import Interface


# This condition means:
# Run the following code only when this file is executed directly.
if __name__ == "__main__":

    # Create an object from the Interface class.
    app = Interface()

    # Start the GUI application.
    app.run()
