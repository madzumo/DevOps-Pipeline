import pytz
import datetime
from colorama import Fore, Back, Style
from enum import Enum
import os


class ConsoleColors(Enum):
    welcome = Back.BLUE + Fore.WHITE
    menu = Back.LIGHTGREEN_EX + Fore.BLACK
    info = Fore.BLACK + Back.LIGHTYELLOW_EX
    error = Fore.WHITE + Back.LIGHTRED_EX + Style.BRIGHT
    basic = Fore.WHITE + Back.BLACK
    commands = Fore.LIGHTBLUE_EX + Back.BLACK


welcome_message = ["This utility will deploy an e-commerce website using a full DevOps pipeline in your AWS"
                   "infrastructure",
                   "Tools used: Git, Jenkins, Docker, Kubernetes, EKS, ECR, Terraform, Ansible & Python",
                   "All you need is an AWS account Access Key ID and Secret Key ID. Select option below to get started"]

menu_options = ["Menu Options:", "1 - Test AWS Connection", "2 - Install Full Pipeline",
                "3 - Remove Existing Pipeline & all resources",
                "4 - View Pipeline Status", "5 - Quit"]

total_line_chars = 103


def get_current_time():
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(eastern)
    military_time = current_time.strftime('%H:%M:%S')
    return military_time


def display_header():
    intro_message = Fore.BLACK + Back.LIGHTYELLOW_EX + r"""
    ___________________  
    |# :           : #|  
    |  :  DevOps   :  |  
    |  :   demo    :  |  
    |  :___________:  |  
    |     _________   |  
    |    | __      |  |  
    |    ||  |     |  |       by Jonathan M. 
    \____||__|_____|__|   github.com/madzumo """
    print(intro_message)


def display_filler_line():
    print(Back.BLACK + ' ' * total_line_chars)


def console_message(message_words, message_color, total_chars=total_line_chars, pause_message=False,
                    no_formatting=False):
    """Display console messages in color scheme. message_words must be a list. Each item in it's own line.
    message_color must be the value of the ConsoleColors enum"""
    paragraph = ''
    multi_word = False
    for word in message_words:
        if multi_word:
            paragraph += '\n'
        if len(word) > total_chars:
            remaining_word = word
            paragraph += remaining_word[:total_chars]
            paragraph += remaining_word[total_chars:]
        else:
            remaining_spaces = total_chars - len(word)
            paragraph += word
            paragraph += ' ' * remaining_spaces
        multi_word = True

    if pause_message:
        input(message_color + paragraph + Style.RESET_ALL)
    elif no_formatting:
        print(paragraph + Style.RESET_ALL)
    else:
        print(message_color + paragraph + Style.RESET_ALL)


def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Linux/Unix/MacOS
    else:
        os.system('clear')

    print(Style.RESET_ALL + ' ')
