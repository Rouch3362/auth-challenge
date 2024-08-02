import re
from rest_framework import status, serializers
from register.models import OTP,User, UserLockout
import random
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone

def validatePhoneNumber(phoneNumber: str):
    # created a regex for detecting invalid or valid phone numbers
    phone_regex = re.compile(r"^((\+98|0)9\d{9})$")

   
    # check if phone number is not valid
    if not phone_regex.match(phoneNumber):
        # the proper error
        error = {
            "phone_number": "phone number is not a valid phone number"
        }
        raise serializers.ValidationError(error, status.HTTP_400_BAD_REQUEST)
    


def generateMessage(msg):
    message = {
        "message": msg,
    }

    return message


def generateOTP(phone_number):
    # generate a fake OTP code
    code = random.randint(100000,999999)
    otpCode = OTP.objects.create(phone_number=phone_number,code=str(code))

    return otpCode.code


def formatPhoneNumber(phone_number):
    # changes phone numbers from +989123456789 to 09123456789
    formatedPhoneNumber = phone_number.replace("+98", "0")

    return formatedPhoneNumber


def checkUserExistance(phone_number):
    # check for user existance and if it exist returns user and if not returns proper error
    try:
        user = User.objects.get(phone_number=phone_number)

    except User.DoesNotExist:
        error = generateMessage(f"User with this phone number does not exist: {phone_number}")

        return None,Response(error, status.HTTP_404_NOT_FOUND)
    
    return user, None


def checkIfOtpIsValid(phone_number , code):
    try:
        otp = OTP.objects.get(phone_number=phone_number, code=code)

    except OTP.DoesNotExist:
        message = generateMessage("the OTP code is invalid")
        return Response(message , status.HTTP_400_BAD_REQUEST)
    
    if timezone.now() > otp.valid_until:
        # removes expired OPT's
        otp.delete()
        message = generateMessage("the OTP code is expired")
        return Response(message, status.HTTP_400_BAD_REQUEST)
    
    # delete opt codes after usage
    otp.delete()
    
    return None

def getUserIp(request):
    # get the HTTP_X_FORWARDED_FOR header
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    # if that exist extract the ip from it
    if x_forwarded:
        ip = x_forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


# a function to create or get a lockout record based on two fields phone number and ip address
def getOrCreateLockout(phone_number, userIp):

    try:
        lockout = UserLockout.objects.get(Q(phone_number=phone_number) | Q(ip_address=userIp))

    except UserLockout.DoesNotExist:
        lockout = UserLockout.objects.create(phone_number=phone_number, ip_address=userIp)

    return lockout


def lockoutAccount(phone_number, userIp, message):
    
    lockout = getOrCreateLockout(phone_number, userIp)
    # check if account is already locked out 
    if lockout.isLockedOut():
        return Response(
            {"details": message},
            status.HTTP_403_FORBIDDEN
        )
    # if not locked out increases the attempts field
    lockout.increaseAttempts()


    if lockout.failed_attempts >= 3:
        # make the user locked out 
        lockout.lockOut()
        return Response(
            {"details": message},
            status.HTTP_403_FORBIDDEN
        )
    
    return None


# resets the lockout
def restLockout(phone_number,userIp):
    lockout = getOrCreateLockout(phone_number, userIp)

    lockout.resetLockOut()


# check user is blocked and if not resets the lockout
def checkIsBlocked(phone_number, userIp):
    lockout = getOrCreateLockout(phone_number, userIp)

    if lockout.isLockedOut():
        return True
    
    return False
