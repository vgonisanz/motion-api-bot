# -*- coding: utf-8 -*-
import sys
import os
import json
import argparse
import shutil

import linkero.core.linkero as linkero
import linkero.core.gateway.gevent_service as gevent
import linkero.core.gateway.waitress_service as waitress

from core import Core

class CmdList(linkero.Resource):
    """
    CmdList linkero resource:
        This class return a list with all commands defined for the API.
        - Type request: GET, return complete JSON object.
    """
    versions_list = {
        'v1': {'info': 'Initial version'},
    }

    def get(self):
        return self.versions_list

class CmdV1(linkero.Resource):
    """
    V1 with commands available and behavior for requests.

    To provide all bot functionality shall contain same
    commands than api_commands in Api class. This array
    have pair <cmd>:<function_call> so it is at the bottom
    of this class.
    """
    version = 'Server API V1.0'
    info = """This server run an instance to manage local motion software. 
            in order to use, send a request to help to get a list of commands. 
            This software has been develop by Victor Goni Sanz. """

    """ ********************************************************************** """
    """ ******                   HTTP    functions                 *********** """
    """ ********************************************************************** """

    def get(self, cmd):
        value = ''
        if self.is_cmd_in_list(self.v1_cmd_list, cmd):
            value = list(self.v1_cmd_list[cmd].keys())[0](self)         # Invoke callback for each command
        else:
            value = 'No valid command for v1. Use help command to check valid cmds'
        return value, 201

    def delete(self, cmd):
        #is_cmd_in_list(v1_cmd_list, cmd)
        #del versions_list[cmd]
        return '', 204

    def put(self, cmd):
        #args = parser.parse_args()
        #task = {'task': args['task']}
        #versions_list[cmd] = task
        return task, 201

    """ ********************************************************************** """
    """ ******                  Internal functions                 *********** """
    """ ********************************************************************** """

    def is_cmd_in_list(self, cmd_list, cmd):
        """
        is_cmd_in_list: Return a 404 error message if a command doesn't exist.
        """
        if cmd not in cmd_list:
            linkero.abort(404, message="Command {} doesn't exist".format(cmd))
            return False
        else:
            return True

    ###############################################################
    # Internal <function_call> from v1_cmd_list, modify to add behavior.
    ###############################################################
    def f_help(self):
        message = ''
        for value in self.v1_cmd_list:
            message = message + 'Command: <' + str(value) + '>: ' + self.v1_cmd_list[value].values()[0] + '. \n'
        return message

    def f_info(self):
        return self.info

    def f_start(self):
        print("f_start")
        return 'f_start'

    def f_stop(self):
        print("f_stop")
        return 'f_stop'

    def f_version(self):
        print("f_version")
        return self.version

    def f_test(self):
        print("f_test")
        return 'f_test'

    ###############################################################
    # Array with <cmd>:<function_call> modify to add cmds.
    ###############################################################
    v1_cmd_list = {
        'help': {f_help: 'Show all commands available'},
        'start': {f_start: 'Start motion binary to detect events. If is already active do nothing.'},
        'stop': {f_stop: 'Stop motion binary detecting events. If no active do nothing.'},
        'info': {f_info: 'Print info about author and implementation'},
        'version': {f_version: 'Print version info'},
        'test': {f_test: 'Testing tochas stuffs'},
    }

class Server(object):
    """
    This python 3 class manage server with user's motion execution.

    To generate HTML documentation for this module issue the command: pydoc -w Core
    """

    # Configuration
    template_file_path = "templates/config_server_default.json"
    config_folder = 'config'
    setting_file_name = 'config/config_server.json'

    settings = None  # Load here configuration and use as global
    _core = None

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
        self._core = Core(self.settings["camera_configuration_path"])

        linkero.api.add_resource(CmdList, '/help')  # Call CmdList resource if HTTP request to help
        linkero.api.add_resource(CmdV1, '/v1/<cmd>')
        return

    def __enter__(self):
        return

    def __del__(self):
        # Catch any weird termination situations
        return

    def __exit__(self, exc_type, exc_value, traceback):
        return

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

    def run(self):
        #self.logger.info("Motion core will use %s configuration" % self.settings["camera_configuration_path"])
        #self.logger.info("Motion api bot instance initialized!")

        linkero.run()  # Run with Werkzeug (not recommended for production environments)
        # gevent.run(linkero.app)    # Run with Gevent
        # waitress.run(linkero.app)   # Run with Waitress
        return

if __name__ == '__main__':
    # Entry point
    server = Server()
    server.run()
