import linkero.core.linkero as linkero
import linkero.core.gateway.gevent_service as gevent
import linkero.core.gateway.waitress_service as waitress

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

    """ ********************************************************************** """
    """ ******                   HTTP    functions                 *********** """
    """ ********************************************************************** """

    def get(self, cmd):
        value = ''
        if self.is_cmd_in_list(self.v1_cmd_list, cmd):
            value = self.v1_cmd_list[cmd]()         # Invoke callback for each command
        else:
            value = 'No valid command for v1'
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
    def f_help():
        print("f_help")
        return 'f_help'

    def f_info():
        print("f_info")
        return 'f_info'

    def f_start():
        print("f_start")
        return 'f_start'

    def f_stop():
        print("f_stop")
        return 'f_stop'

    def f_version():
        print("f_version")
        return 'f_f_versionf_infoinfo'

    def f_info():
        print("f_info")
        return 'f_info'

    def f_test():
        print("f_test")
        return 'f_test'

    ###############################################################
    # Array with <cmd>:<function_call> modify to add cmds.
    ###############################################################
    v1_cmd_list = {
        'help': f_help,
        'info': f_info,
        'start': f_start,
        'stop': f_stop,
        'info': f_info,
        'version': f_version,
        'test': f_test
    }

class Server(object):
    """
    This python 3 class manage server with user's motion execution.

    To generate HTML documentation for this module issue the command: pydoc -w Core
    """

    """ ********************************************************************** """
    """ ******                   Internal functions                *********** """
    """ ********************************************************************** """

    """
    Initialize class: Initialize CursesManager
    """
    def __init__(self):
        """
        load: Api load add all server resources to get them ready to be used with HTTP requests.
                - help: This resource return all versions valid.
        """
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

    def run(self):
        linkero.run()  # Run with Werkzeug (not recommended for production environments)
        # gevent.run(linkero.app)    # Run with Gevent
        # waitress.run(linkero.app)   # Run with Waitress
        return

if __name__ == '__main__':
    # Entry point
    server = Server()
    server.run()
