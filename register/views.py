from rest_framework.response import Response
from .serializers import UpdateUserSerializer, OTPSerializer, UserSerializer
from rest_framework.decorators import api_view
from .models import User
from rest_framework import status
from auth.middleware import checkIfUserIsBlocked
from auth.utils import (
        formatPhoneNumber,
        checkUserExistance,
        getUserIp,
        lockoutAccount,
        checkIsBlocked,
        restLockout,
        checkIfOtpIsValid,
        generateMessage
    )

# block message for showing to users
BLOCK_MESSAGE = "you've been blocked for 1 hour, because you've entered OTP code wrong 3 times"


@api_view(["POST"])
@checkIfUserIsBlocked
def register(request):
    otpSerializer = OTPSerializer(data=request.data)
    

    if otpSerializer.is_valid():
        # getting phone number and format it for database
        phone_number  = otpSerializer.validated_data["phone_number"]
        phone_number  = formatPhoneNumber(phone_number)
        # getting otp code
        code          = otpSerializer.validated_data["code"]    
        # getting user ip
        userIp = getUserIp(request)
        # if user already registered
        user, _ = checkUserExistance(phone_number)

        # check if user blocked
        if checkIsBlocked(phone_number , userIp):
            error = lockoutAccount(phone_number, userIp, BLOCK_MESSAGE)
            return error

        # if user already registered
        if user:
            message = generateMessage("user already registered")
            return Response(message , status.HTTP_409_CONFLICT)
        
        # check if OTP is valid and not expired
        error = checkIfOtpIsValid(phone_number, code)

        # if opt is wrong or expired
        if error:
            lockoutErr = lockoutAccount(phone_number , userIp , BLOCK_MESSAGE)

            if lockoutErr:
                return lockoutErr
            
            return error
        
        # create user with just phone number
        user = User.objects.create(phone_number=phone_number)

        # reset the lockout if they are not blocked and entered valid OTP
        restLockout(phone_number , userIp)
        message = generateMessage("user created successfully now update user information.")
        # serialize user for response
        userSerializer = UserSerializer(user)
        # adding it to response message
        message["user"] = userSerializer.data
        # save user phone number to session so identify it later with updating it
        request.session["phone-number"] = user.phone_number
        return Response(message, status.HTTP_201_CREATED)
        
    # if request is not valid and user forgot some fields
    return Response(otpSerializer.errors , status.HTTP_400_BAD_REQUEST)

@api_view(["PUT", "PATCH"])
@checkIfUserIsBlocked
def updateInfo(request):
    # fetch the phone number from session so users can only update their account
    if 'phone-number' not in request.session:
        message = generateMessage("phone number not provided. first you need to verify your phone number and get an OTP code")
        return Response(message , status.HTTP_400_BAD_REQUEST)

    serializer = UpdateUserSerializer(data=request.data)


    if serializer.is_valid():
        # getting phone number and format it for database
        phone_number = request.session["phone-number"]

        # check if user exists 
        user , error = checkUserExistance(phone_number)



        if error:
            return error
        
        # update user inforamtions
        user.first_name = serializer.validated_data["first_name"]
        user.last_name  = serializer.validated_data["last_name"]
        user.email      = serializer.validated_data["email"]
        user.set_password(serializer.validated_data["password"])

        user.save()
        
        message = generateMessage("user updated successfully")
        
        # serialize user for response
        userSerializer = UserSerializer(user)
        # adding it to response message
        message["user"] = userSerializer.data

        return Response(message, status.HTTP_200_OK)

    # if request is not valid
    return Response(serializer.errors , status.HTTP_400_BAD_REQUEST)