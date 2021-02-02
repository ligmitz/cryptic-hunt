from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils import timezone
from questions.lib.actions import is_active_period, local_publish_date, local_deactivate_date

def hunt_is_active(function):
    def wrap(request, *args, **kwargs):
        cur_user = request.user
        active = is_active_period()

        if cur_user.is_staff:
            return function(request, *args, **kwargs)
        else:
            if active:
                return function(request, *args, **kwargs)

        return render(request, 'wait.html', {"publish_time": local_publish_date, "deactivate_time": local_deactivate_date})

    wrap.__doc__ = getattr(function, "__doc__", "")
    wrap.__name__ = getattr(function, "__name__", "")

    return wrap
