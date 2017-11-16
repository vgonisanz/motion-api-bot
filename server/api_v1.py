# -*- coding: utf-8 -*-

import linkero.core.linkero as linkero

api_base_path = "/motion/api/v1"


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


class Cmd(linkero.Resource):
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
        if self.is_cmd_in_list(self.cmd_list, cmd):
            value = list(self.cmd_list[cmd].keys())[0](self)         # Invoke callback for each command
        else:
            value = 'No valid command for v1. Use help command to check valid cmds'
        return value, 201

    def delete(self, cmd):
        #is_cmd_in_list(cmd_list, cmd)
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
    # Internal <function_call> from cmd_list, modify to add behavior.
    ###############################################################
    def f_help(self):
        message = ''
        for value in self.cmd_list:
            message = message + 'Command: <' + str(value) + '>: ' + self.cmd_list[value].values()[0] + '. \n'
        return message

    def f_info(self):
        return self.info

    def f_start(self):
        return core.start()

    def f_stop(self):
        return core.stop()

    def f_version(self):
        return self.version

    def f_test(self):
        print("f_test")
        return 'f_test'

    ###############################################################
    # Array with <cmd>:<function_call> modify to add cmds.
    ###############################################################
    cmd_list = {
        'help': {f_help: 'Show all commands available'},
        'start': {f_start: 'Start motion binary to detect events. If is already active do nothing.'},
        'stop': {f_stop: 'Stop motion binary detecting events. If no active do nothing.'},
        'info': {f_info: 'Print info about author and implementation'},
        'version': {f_version: 'Print version info'},
        'test': {f_test: 'Testing tochas stuffs'},
    }

##
## Actually setup the Api resource routing here
##
def loadAPI():
    linkero.api.add_resource(CmdList, api_base_path + '/help')  # Call CmdList resource if HTTP request to help
    linkero.api.add_resource(Cmd, api_base_path + '/cmd/<cmd>')
