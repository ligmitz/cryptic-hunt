from datetime import datetime
import pytz

PUBLISH_DATE = datetime(year=2021, month=12, day=27, hour=21, minute=17, second=00)
DEACTIVATE_DATE = datetime(year=2022, month=1, day=1, hour=00, minute=00, second=00)
tz = pytz.timezone('Asia/Kolkata')
local_publish_date = tz.localize(PUBLISH_DATE)
local_deactivate_date = tz.localize(DEACTIVATE_DATE)
local_current_date = tz.localize(datetime.now())

def is_active_period():

    if ((local_current_date >= local_publish_date) and (local_current_date <= local_deactivate_date)):
        return True

    return False

def show_leaderboard():

    if local_current_date >= local_publish_date:
        return True

    return False
