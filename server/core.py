import os.path
import requests
import subprocess

class Core(object):
    """
    This python 3 class will manager the logic of motion behavior.

    To generate HTML documentation for this module issue the command: pydoc -w Core
    """

    version_major = '0'
    version_minor = '1'
    version_subminor = '0'

    is_working = False

    # Process variables
    camera_configuration_path = 'config/camera0.conf'
    p_open = None
    motion_args = None

    """ ********************************************************************** """
    """ ******                   Internal functions                *********** """
    """ ********************************************************************** """

    """
    Initialize class: Initialize CursesManager
    """
    def __init__(self, camera_configuration_path):
        """
        Initialize
        """
        self.is_working = False
        self.camera_configuration_path = camera_configuration_path
        self.motion_args = ("motion", "-c", camera_configuration_path)      # Set default call to motion
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
        message = ''
        if not self.is_working:
            # Call motion to start
            self.p_open = subprocess.Popen(self.motion_args, stdout=subprocess.PIPE)
            message = ("motion started with %d process id" % self.p_open.pid)

            # Update variables
            self.is_working = True
            started = True
        else:
            message = ("motion is already working with %d process id" % self.p_open.pid)
        return started, message

    def stop(self):
        stopped = False
        if self.is_working:
            # Call motion to stop
            self.p_open.terminate()

            # Update variables
            self.is_working = False
            stopped = True
        else:
            print("motion is not working!")
        return stopped

    def info(self):
        response_info = 'Camera configuration path: %s\n' % self.camera_configuration_path

        if os.path.isfile(self.camera_configuration_path):
            file = open(self.camera_configuration_path, "r")
            response_info += '+----------------------------------------+' + '\n'
            response_info += file.read()
            response_info += '+----------------------------------------+'
        else:
            response_info += "File not exist! configurate with a existing file dude!"
        return response_info

    def version(self):
        return 'v' + self.version_major + '.' + self.version_minor + '.' + self.version_subminor

    def test(self, data):
        print("test data: %s" % data)
        r = requests.get(data)
        return r.content