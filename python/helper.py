import pytz
import datetime

            
def _get_current_time():
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(eastern)
    military_time = current_time.strftime('%H:%M:%S')
    return military_time

def _display_message(messagex):
    print("****************************")
    print(messagex)
    print("****************************")