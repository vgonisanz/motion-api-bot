# -*- coding: utf-8 -*-

import sys
import os
import argparse
import shutil
import json

from core import Core


class CoreConfigurator(object):
    """
    This python 3 class manage server with user's motion execution.

    To generate HTML documentation for this module issue the command: pydoc -w Core
    """

    # Configuration
    template_file_path = "templates/config_server_default.json"
    config_folder = 'config'
    setting_file_name = 'config/config_server.json'

    settings = None  # Load here configuration and use as global

    """ ********************************************************************** """
    """ ******                   Internal functions                *********** """
    """ ********************************************************************** """

    """
    Initialize class: Initialize CursesManager
    """
    def __init__(self):
        """
        load: Parse arguments and launch linkero server
        """

        self.parse_arguments()
        self.read_configuration_file()

        self.core = Core(self.settings["camera_configuration_path"])

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--create", default=None, required=False, help="Create config from default",
                            action="store_true")
        # parser.add_argument('-q', '--query', default=None, required=False, help="query string", action="store", dest="query")
        args = parser.parse_args()
        if args.create is True:
            self.create_default_config()
            sys.exit(0)
        # if args.query is not None:
        #    print("Create query; %s" % args.query)
        return

    def create_default_config(self):
        if not os.path.isdir(self.config_folder):
            print("Creating config folder...")
            os.makedirs(self.config_folder)
        if not os.path.isfile(self.setting_file_name):
            print("Creating default configuration...")
            shutil.copyfile(self.template_file_path, self.setting_file_name)
        else:
            print("You cannot create config file if exist, remove it before.")
        return

    def read_configuration_file(self):
        """
        Read configuration file
        """
        exist = os.path.isfile(self.setting_file_name)
        if not exist:
            print("Error reading config file: %s" % self.setting_file_name)
            sys.exit(1)
        else:
            with open(self.setting_file_name) as data_file:
                self.settings = json.load(data_file)
        return
