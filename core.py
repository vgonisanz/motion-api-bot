import sys
import os
import logging

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater

class Core(object):
    """
    This python 3 class will manager the core of the motion bot.

    To generate HTML documentation for this module issue the command: pydoc -w Wpm
    """

    _log_folder = "log"

    logger = None
    dispatcher = None
    updater = None

    settings = None

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

    def run(self):
        """
        Run the bot
        """

        #bot = telegram.Bot(token=settings["token"])
        self.updater = Updater(token=self.settings["token"])
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        self.logger.info("The bot is now waiting for orders!")
        self.updater.start_polling()

    """ ********************************************************************** """
    """ ******                        API functions                *********** """
    """ ********************************************************************** """
    def start(self, bot, update):
        self.logger.info("Received start command")
        bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
        return

    def print_bot_info():
        #print(bot.get_me())
        return
