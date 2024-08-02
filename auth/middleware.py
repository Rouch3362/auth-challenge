from functools import wraps
from .utils import checkIsBlocked, getUserIp
from rest_framework.response import Response
from .utils import validatePhoneNumber, formatPhoneNumber
from rest_framework.validators import ValidationError
from rest_framework import status

def checkIfUserIsBlocked(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        
        userIp = getUserIp(request)
        phone_number = request.data.get("phone_number")

        if phone_number is None:
            raise ValidationError({"detail": "phone number is required"} , status.HTTP_400_BAD_REQUEST)

        phone_number = formatPhoneNumber(phone_number)

        validatePhoneNumber(phone_number)

        if checkIsBlocked(phone_number, userIp):
            return Response({"detail": "you've been blocked for 1 hour"})

        return view_function(request, *args, **kwargs)
    return wrap