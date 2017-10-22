class Core(object):
    """
    This python 3 class will manager the logic of motion behavior.

    To generate HTML documentation for this module issue the command: pydoc -w Core
    """

    is_working = False

    """ ********************************************************************** """
    """ ******                   Internal functions                *********** """
    """ ********************************************************************** """

    """
    Initialize class: Initialize CursesManager
    """
    def __init__(self):
        """
        Initialize
        """
        self.is_working = False
        return

    def __enter__(self):
        return

    def __del__(self):
        # Catch any weird termination situations
        return

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def start(self):
        started = False
        if not self.is_working:
            # Call motion to start

            # Update variables
            self.is_working = True
            started = True
        return started

    def stop(self):
        stopped = False
        if self.is_working:
            # Call motion to stop

            # Update variables
            self.is_working = False
            stopped = True
        return stopped