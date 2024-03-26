import pytz
import datetime
from colorama import Fore, Back, Style
from enum import Enum
import os


class ConsoleColors(Enum):
    title = Back.BLUE + Fore.WHITE
    menu = Back.LIGHTGREEN_EX + Fore.BLACK
    info = Fore.BLACK + Back.LIGHTYELLOW_EX
    info_bright = Fore.BLACK + Back.LIGHTYELLOW_EX + Style.BRIGHT
    error = Fore.WHITE + Back.LIGHTRED_EX + Style.BRIGHT
    basic = Fore.WHITE + Back.BLACK
    commands = Fore.LIGHTBLUE_EX + Back.BLACK
    warning = Back.MAGENTA + Fore.WHITE


welcome_message = ["This utility will deploy an e-commerce website using a full DevOps pipeline in your AWS"
                   "infrastructure",
                   "Tools used: Git, Jenkins, Docker, Kubernetes, EKS, ECR, Terraform, Ansible & Python",
                   "All you need is an AWS account Access Key ID and Secret Key ID. Select option below to get started"]

menu_options = ["Menu Options:", "1 - Test AWS Connection", "2 - Set AWS Credentials",
                "3 - Install Full Pipeline",
                "4 - Remove Existing Pipeline & all resources",
                "5 - View Pipeline Status", "6 - Quit"]

total_line_chars = 101


def get_current_time():
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(eastern)
    military_time = current_time.strftime('%H:%M:%S')
    return military_time


def display_header():
    intro_message = r"""
    ___________________    
    |# :           : #|    
    |  :  DevOps   :  |    
    |  :   demo    :  |    
    |  :___________:  |    
    |     _________   |    
    |    | __      |  |    
    |    ||  |     |  |       by Jonathan M. 
    \____||__|_____|__|   github.com/madzumo 
                                             """

    print(Fore.BLACK + Back.LIGHTYELLOW_EX + intro_message)


def display_filler_line():
    print(Back.BLACK + ' ' * total_line_chars)


def console_message(message_words, message_color, total_chars=total_line_chars, pause_message=False,
                    no_formatting=False):
    """Display console messages in color scheme. message_words must be a list. Each list item will be on its own line.
    Message_color is simply the selected ConsoleColors enum. To have back color end with the word (non-uniform back color)
    use total_chars = 0"""

    paragraph = ''
    multi_word = False
    for word in message_words:
        if multi_word:
            paragraph += '\n'
        if total_chars > 0:  # If 0 then do not make back color uni-form
            if len(word) > total_chars:
                remaining_word = word
                paragraph += remaining_word[:total_chars]
                paragraph += remaining_word[total_chars:]
            else:
                remaining_spaces = total_chars - len(word)
                paragraph += word
                paragraph += ' ' * remaining_spaces
        else:
            paragraph += word
        multi_word = True

    if pause_message:
        input(message_color.value + paragraph.title() + Style.RESET_ALL)
    elif no_formatting:
        print(paragraph + Style.RESET_ALL)
    else:
        print(message_color.value + paragraph + Style.RESET_ALL)


def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Linux/Unix/MacOS
    else:
        os.system('clear')

    print(Style.RESET_ALL + ' ')


def end_of_line():
    pause_console()
    clear_console()
    display_header()


def pause_console():
    console_message(['hit enter to continue'], ConsoleColors.commands, total_chars=0, pause_message=True)


def display_outro_message():
    header_text = r"""
 .----------------.  .----------------.  .----------------.  .----------------.  .-----------------.
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |     ______   | || |   _____      | || |  _________   | || |      __      | || | ____  _____  | |
| |   .' ___  |  | || |  |_   _|     | || | |_   ___  |  | || |     /  \     | || ||_   \|_   _| | |
| |  / .'   \_|  | || |    | |       | || |   | |_  \_|  | || |    / /\ \    | || |  |   \ | |   | |
| |  | |         | || |    | |   _   | || |   |  _|  _   | || |   / ____ \   | || |  | |\ \| |   | |
| |  \ `.___.'\  | || |   _| |__/ |  | || |  _| |___/ |  | || | _/ /    \ \_ | || | _| |_\   |_  | |
| |   `._____.'  | || |  |________|  | || | |_________|  | || ||____|  |____|| || ||_____|\____| | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
"""
    print(Back.BLUE + Fore.BLACK + header_text + Style.RESET_ALL + "\n")
    console_message(['Pipeline removed. Thank you for trying this demo',
                     'View my other projects at: https://github.com/madzumo'],
                    ConsoleColors.commands)
