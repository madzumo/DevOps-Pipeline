import pytz
import datetime
from colorama import Fore, Back, Style
from enum import Enum
import os


class ConsoleColors(Enum):
    title = Back.BLUE + Fore.WHITE
    menu = Back.LIGHTGREEN_EX + Fore.BLACK
    info = Back.LIGHTYELLOW_EX + Fore.BLACK
    info_bright = Back.LIGHTYELLOW_EX + Fore.BLACK + Style.BRIGHT
    error = Back.LIGHTRED_EX + Fore.WHITE + Style.BRIGHT
    basic = Back.BLACK + Fore.WHITE
    commands = Back.BLACK + Fore.LIGHTBLUE_EX
    warning = Back.MAGENTA + Fore.WHITE


welcome_message = ["This utility will deploy an e-commerce website using a full CI/CD pipeline in your AWS "
                   "infrastructure",
                   "Tools used: Git, Jenkins, Docker, Kubernetes, EKS, Prometheus Terraform, Ansible & Python",
                   "All you need is an AWS account Access Key ID and Secret Key ID. Select option below to get started"]

menu_options = ["Menu Options:", "1 - Test AWS Connection", "2 - Set AWS Credentials",
                "3 - Install Full Pipeline",
                "4 - Remove Existing Pipeline & all resources",
                "5 - View Pipeline Status", "6 - Quit"]

total_line_chars = 101

header_art_devops_demo = r"""
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

header_art_clean = r"""
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

header_art_status = r"""
.----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |    _______   | || |  _________   | || |      __      | || |  _________   | || | _____  _____ | || |    _______   | |
| |   /  ___  |  | || | |  _   _  |  | || |     /  \     | || | |  _   _  |  | || ||_   _||_   _|| || |   /  ___  |  | |
| |  |  (__ \_|  | || | |_/ | | \_|  | || |    / /\ \    | || | |_/ | | \_|  | || |  | |    | |  | || |  |  (__ \_|  | |
| |   '.___`-.   | || |     | |      | || |   / ____ \   | || |     | |      | || |  | '    ' |  | || |   '.___`-.   | |
| |  |`\____) |  | || |    _| |_     | || | _/ /    \ \_ | || |    _| |_     | || |   \ `--' /   | || |  |`\____) |  | |
| |  |_______.'  | || |   |_____|    | || ||____|  |____|| || |   |_____|    | || |    `.__.'    | || |  |_______.'  | |
| |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
"""


def get_current_time():
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(eastern)
    military_time = current_time.strftime('%H:%M:%S')
    return military_time


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
    print(Back.LIGHTBLUE_EX + Fore.BLACK + header_art_clean + Style.RESET_ALL + "\n")
    console_message(['Pipeline removed. Thank you for trying this demo',
                     'View my other projects at: https://github.com/madzumo'],
                    ConsoleColors.commands)


def display_header():
    print(Back.LIGHTYELLOW_EX + Fore.BLACK + header_art_devops_demo)
