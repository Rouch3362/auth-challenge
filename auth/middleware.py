from functools import wraps
from .utils import checkIsBlocked, getUserIp, generateMessage
from rest_framework.response import Response
from .utils import validatePhoneNumber, formatPhoneNumber
from rest_framework.validators import ValidationError
from rest_framework import status

def checkIfUserIsBlocked(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        
        userIp = getUserIp(request)
        phone_number = request.data.get("phone_number")

        # if the request does not conatin phone number fetches it from sesssion
        if phone_number is None and 'phone-number' in request.session:
            phone_number = request.session["phone-number"]
            
        # if both of them does not contain phone number we return and error
        elif phone_number is None and 'phone-number' not in request.session:
            message = generateMessage("verify your phone number or enter phone number")
            raise ValidationError(message, status.HTTP_400_BAD_REQUEST)

        phone_number = formatPhoneNumber(phone_number)

        validatePhoneNumber(phone_number)

        if checkIsBlocked(phone_number, userIp):
            return Response({"detail": "you've been blocked for 1 hour"})

        return view_function(request, *args, **kwargs)
    return wrap