from django.contrib.auth.models import User
from datetime import datetime
import pytz

utc_tz = pytz.utc
tz = pytz.timezone('Asia/Kolkata')


# These should be in IST
PUBLISH_DATE = datetime(year=2022, month=2, day=28, hour=18, minute=00, second=00)
DEACTIVATE_DATE = datetime(year=2022, month=3, day=1, hour=23, minute=59, second=59)


local_publish_date = tz.localize(PUBLISH_DATE)
local_deactivate_date = tz.localize(DEACTIVATE_DATE)
local_current_date = tz.localize(datetime.now())
# local_current_date = tz.localize(utc_tz.localize(datetime.utcnow()))

def is_active_period():

    find_key = User.objects.get(username='chabhi_for_abhedya')    
    view_question = True if find_key.is_staff else False
    
    if (view_question):
        return True

    return False

def show_leaderboard():
            
    find_key = User.objects.get(username='chabhi_for_abhedya')    
    view_question = True if find_key.is_staff else False
    
    if view_question:
        return True

    return False
