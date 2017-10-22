# -*- coding: utf-8 -*-
import sys
import os
import json
import argparse
import shutil

from api import Api

# Configuration
template_file_path = "templates/config_default.json"
setting_file_name = 'config.json'
settings = None                     # Load here configuration and use as global

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", default=None, required=False, help="Create config from default", action="store_true")
    #parser.add_argument('-q', '--query', default=None, required=False, help="query string", action="store", dest="query")
    args = parser.parse_args()
    if args.create is True:
        create_default_config()
        sys.exit(0)
    #if args.query is not None:
    #    print("Create query; %s" % args.query)
    return

def create_default_config():
    if not os.path.isfile(setting_file_name):
        print("Creating default configuration...")
        shutil.copyfile(template_file_path, setting_file_name)
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


def launch_bot():
    global bot

    bot = Api(settings, True, True)
    bot.run()
    return

def main():
    """
    Main: Print bot info
    """
    parse_arguments()
    read_configuration_file()
    launch_bot()
    return

if __name__ == '__main__':
    # Entry point
    main()
