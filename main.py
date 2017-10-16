import sys
import os
import json

import telegram


# Configuration
setting_file_name = 'config.json'
settings = None                     # Load here configuration and use as global

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

def main():
    """
    Main: Print bot info
    """
    read_configuration_file()
    bot = telegram.Bot(token=settings["token"])
    print(bot.get_me())
    return

if __name__ == '__main__':
    # Entry point
    main()
