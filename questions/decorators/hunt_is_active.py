from django.core.exceptions import PermissionDenied
from datetime import datetime
from django.shortcuts import render
from django.utils import timezone
import pytz

def hunt_is_active(function):
    def wrap(request, *args, **kwargs):
        tz = pytz.timezone('Asia/Kolkata')
        publish_date = tz.localize(datetime(year=2021, month=2, day=1, hour=20, minute=45, second=0))

        if tz.localize(datetime.now())>=publish_date:
            print("Early")
            return function(request, *args, **kwargs)
        else:
            return render(request, 'wait.html', {"time": publish_date})
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
