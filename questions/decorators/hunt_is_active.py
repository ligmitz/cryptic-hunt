from django.core.exceptions import PermissionDenied
from datetime import datetime
from django.shortcuts import render
from django.utils import timezone
import pytz

PUBLISH_DATE = datetime(year=2021, month=2, day=11, hour=0, minute=0, second=0)
DEACTIVATE_DATE = datetime(year=2021, month=2, day=11, hour=23, minute=59, second=59)

def hunt_is_active(function):
    def wrap(request, *args, **kwargs):

        tz = pytz.timezone('Asia/Kolkata')
        local_publish_date = tz.localize(PUBLISH_DATE)
        local_deactivate_date = tz.localize(DEACTIVATE_DATE)
        local_current_date = tz.localize(datetime.now())
        cur_user = request.user

        if cur_user.is_staff:
            return function(request, *args, **kwargs)
        else:
            if ((local_current_date >= local_publish_date) and (local_current_date <= local_deactivate_date)):
                return function(request, *args, **kwargs)

        return render(request, 'wait.html', {"publish_time": local_publish_date, "deactivate_time": local_deactivate_date})

    wrap.__doc__ = getattr(function, "__doc__", "")
    wrap.__name__ = getattr(function, "__name__", "")

    return wrap
