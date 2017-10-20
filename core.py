import sys
import os
import logging

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater

class Core(object):
    """
    This python 3 class will manager the core of the motion bot.
        * Complete api array with commands wanted. Create a function into the class with same name.
        * In example: 'my_command' in api array need def my_command(self, bot, update): with its behavior.

    To generate HTML documentation for this module issue the command: pydoc -w Core
    """

    logger = None

    _log_folder = "log"

    updater = None

    settings = None

    api = [
        'start',
        'echo'
    ]

    """ ********************************************************************** """
    """ ******                   Internal functions                *********** """
    """ ********************************************************************** """

    """
    Initialize class: Initialize CursesManager
    """
    def __init__(self, settings, use_stdout = True, use_file_log = False):
        """
        Initialize the following elements:
            * setting: Required json with bot configuration.
            * Log: Create a log using stdout or file if required.
            * Bot api: Create bot actions

        Usage: To launch updater and dispatcher, please use run function.
        """
        self.settings = settings

        self.__createLog(use_stdout, use_file_log)
        self.logger.info("Motion api bot instance initialized!")
        return

    def __enter__(self):
        self.logger.info("Motion api bot instance enter!")
        return

    def __del__(self):
        # Catch any weird termination situations
        self.logger.info("Motion api bot instance deleted!")
        return

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info("Motion api bot instance exit!")
        return

    def __createLog(self, use_stdout, use_file_log):
        """
        Create a logger class to output messages through console at DEBUG level.
        """
        debug_level = logging.DEBUG

        self.logger = logging.getLogger(str(__name__))
        self.logger.setLevel(debug_level)
        formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s]-[%(module)s]: %(message)s', "%H:%M:%S")

        # create output folder if no exist
        if use_file_log:
            if not os.path.exists(self._log_folder):
                os.makedirs(self._log_folder)

            # create a file handler
            log_filename = self._log_folder + '/' + str(__name__) + '.log'

            # Configure file handler
            handler = logging.FileHandler(log_filename)
            handler.setLevel(debug_level)
            handler.setFormatter(formatter)

            # Add the handlers to the logger
            self.logger.addHandler(handler)

        if use_stdout:
            # Configure stdout handler
            handler_std = logging.StreamHandler()
            handler_std.setLevel(debug_level)

            # Add the handler to the stdout
            self.logger.addHandler(handler_std)
        return

    def __create_api(self):
        """
        Create and add all handlers using api array. Require define a function with the same name has the command to be called when received.
        """
        for command in self.api:
            print("Creating command: %s" % command)
            cmd_handler = CommandHandler(command, getattr(self, command))
            self._updater.dispatcher.add_handler(cmd_handler)

        return

    def run(self):
        """
        Run the bot:
            * Initialize online the bot using user token
            * Create all handlers linked to its functions using create_api
            * Start polling to work
        """
        self._updater = Updater(token=self.settings["token"])
        self.__create_api()
        self.logger.info("The bot is now waiting for orders!")
        self._updater.start_polling()
        return

    """ ********************************************************************** """
    """ ******                        API functions                *********** """
    """ ********************************************************************** """
    def start(self, bot, update):
        self.logger.info("Received start command")
        bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
        return

    def echo(self, bot, update):
        self.logger.info("Received echo command")
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
