# -*- coding: utf-8 -*-
import sys
import os
import logging

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

from core import Core

class Api(object):
    """
    This python 3 class will manager the api of the motion bot calling the core to work.
        * Complete api array with commands wanted. Create a function into the class with same name.
        * In example: 'my_command' in api array need def my_command(self, bot, update): with its behavior.

    To generate HTML documentation for this module issue the command: pydoc -w Api
    """

    logger = None
    _log_folder = "log"
    updater = None
    settings = None

    api_commands = [
        'start',
        'stop'
    ]

    _core = None

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
            * Bot api commands: Create bot actions

        Usage: To launch updater and dispatcher, please use run function.
        """
        self.settings = settings

        self.__create_log(use_stdout, use_file_log)
        self._core = Core()
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

    def __create_log(self, use_stdout, use_file_log):
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

    def __create_api_commands(self):
        """
        Create and add all handlers using api array. Require define a function with the same name has the command to be called when received.
        Also add a special handler to manage unknown commands.
        """
        # Add handler for api commands
        for command in self.api_commands:
            print("Creating command: %s" % command)
            cmd_handler = CommandHandler(command, getattr(self, command))
            self._updater.dispatcher.add_handler(cmd_handler)

        # Add a handler for unknown commands
        unknown_handler = MessageHandler(Filters.command, getattr(self, 'unknown'))
        self._updater.dispatcher.add_handler(unknown_handler)

        # Add a handler to manage exceptions
        self._updater.dispatcher.add_error_handler(self.__error_callback)
        return

    def __error_callback(self, bot, update, error):
        try:
            raise error
        except Unauthorized:
            # remove update.message.chat_id from conversation list
            self.logger.info("Error Unauthorized found!")
        except BadRequest:
            # handle malformed requests - read more below!
            self.logger.info("Error BadRequest found!")
        except TimedOut:
            # handle slow connection problems
            self.logger.info("Error TimedOut found!")
        except NetworkError:
            # handle other connection problems
            self.logger.info("Error NetworkError found!")
        except ChatMigrated as e:
            # the chat_id of a group has changed, use e.new_chat_id instead
            self.logger.info("Error ChatMigrated found!")
        except TelegramError:
            # handle all other telegram related errors
            self.logger.info("Error TelegramError found!")

    def run(self):
        """
        Run the bot:
            * Initialize online the bot using user token
            * Create all handlers linked to its functions using create_api
            * Start polling to work
        """
        self._updater = Updater(token=self.settings["token"])
        self.__create_api_commands()
        self.logger.info("The bot is now waiting for orders!")
        self._updater.start_polling()
        return

    """ ********************************************************************** """
    """ ******                        API functions                *********** """
    """ ********************************************************************** """
    def start(self, bot, update):
        self.logger.info("Received start command")
        response_text = ''
        self.logger.info("start")
        success = self._core.start()
        self.logger.info("started")
        if success:
            response_text = 'Motion start to detect events'
        else:
            response_text = 'Error: Motion is already working!'
        bot.send_message(chat_id=update.message.chat_id, text=response_text)
        return

    def stop(self, bot, update):
        self.logger.info("Received stop command")
        response_text = ''
        success = self._core.stop()
        if success:
            response_text = 'Motion stop to detect events'
        else:
            response_text = 'Error: Motion is not working!'
        bot.send_message(chat_id=update.message.chat_id, text=response_text)
        return

    def unknown(self, bot, update):
        self.logger.info("Received unknown command")
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, unknown command")
