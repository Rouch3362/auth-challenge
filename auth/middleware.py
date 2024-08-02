from functools import wraps
from .utils import checkIsBlocked, getUserIp
from rest_framework.response import Response


def checkIfUserIsBlocked(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        
        userIp = getUserIp(request)

        if checkIsBlocked(None, userIp):
            return Response({"detail": "you've been blocked for 1 hour"})

        return view_function(request, *args, **kwargs)
    return wrap