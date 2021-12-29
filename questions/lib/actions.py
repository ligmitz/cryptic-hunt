from datetime import datetime
import pytz

utc_tz = pytz.utc
tz = pytz.timezone('Asia/Kolkata')


# These should be in IST
PUBLISH_DATE = datetime(year=2021, month=12, day=29, hour=18, minute=00, second=00)
DEACTIVATE_DATE = datetime(year=2021, month=12, day=31, hour=23, minute=59, second=59)


local_publish_date = tz.localize(PUBLISH_DATE)
local_deactivate_date = tz.localize(DEACTIVATE_DATE)
local_current_date = tz.localize(utc_tz.localize(datetime.utcnow()))

def is_active_period():

    if ((local_current_date >= local_publish_date) and (local_current_date <= local_deactivate_date)):
        return True

    return False

def show_leaderboard():

    if local_current_date >= local_publish_date:
        return True

    return False
