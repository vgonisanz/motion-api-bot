import sys
import os
import json
import argparse
import shutil

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater

# Configuration
setting_file_name = 'config.json'
settings = None                     # Load here configuration and use as global

# Variables
bot = None
dispatcher = None
updater = None

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", default=None, required=False, help="Create config from default", action="store_true")
    parser.add_argument('-q', '--query', default=None, required=False, help="query string", action="store", dest="query")
    args = parser.parse_args()
    if args.create is True:
        create_default_config()
        sys.exit(0)
    if args.query is not None:
        print("Create query; %s" % args.query)
    return

def create_default_config():
    if not os.path.isfile(setting_file_name):
        print("Creating default configuration...")
        shutil.copyfile("templates/config_default.json", setting_file_name)
    else:
        print("You cannot create config file if exist, remove it before.")
    return

def read_configuration_file():
    """
    Read configuration file
    """
    exist = os.path.isfile(setting_file_name)
    if not exist:
        print("Error reading config file: %s" % setting_file_name)
        sys.exit(1)
    else:
        global settings

        with open(setting_file_name) as data_file:
            settings = json.load(data_file)
    return

def initialize_bot():
    global dispatcher, bot, updater

    #bot = telegram.Bot(token=settings["token"])
    updater = Updater(token=settings["token"])
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    print("Bot is running now...")
    updater.start_polling()



    return

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    return

def print_bot_info():
    print(bot.get_me())
    return

def main():
    """
    Main: Print bot info
    """
    parse_arguments()
    read_configuration_file()
    initialize_bot()
    return

if __name__ == '__main__':
    # Entry point
    main()
