from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import UserLoginSerializer, VerifyPhoneNumberSerializer
from register.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from auth.middleware import checkIfUserIsBlocked
from auth.utils import (
    generateOTP, 
    formatPhoneNumber, 
    checkUserExistance, 
    getUserIp, 
    lockoutAccount, 
    restLockout,
    generateMessage
)

BLOCK_MESSAGE = "you've been blocked for 1 hour"

@api_view(["POST"])
@checkIfUserIsBlocked
def verifyNumber(request):
    
    serializer = VerifyPhoneNumberSerializer(data=request.data)
    
    if serializer.is_valid():
        # get phone number from serializer and replace country code with zero
        phone_number = serializer.validated_data["phone_number"]
        phone_number = formatPhoneNumber(phone_number)

        # check if user not exists
        _, error = checkUserExistance(phone_number)

        if error:
            # generate a fake otp and pass it to user for just testing
            code = generateOTP(phone_number)
            message = generateMessage("'this is temporarily solution for otp' enter this code to continue registering")
            message["code"] = code
            return Response(message , status.HTTP_200_OK)

        # if user found
        message = generateMessage("phone number exists. now login to your account")
        return Response(message,status.HTTP_200_OK)
    
    return Response(serializer.errors , status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@checkIfUserIsBlocked
def loginUser(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        # get phone number from serializer and replace country code with zero
        phone_number = serializer.validated_data["phone_number"]
        phone_number = formatPhoneNumber(phone_number)
        userIp       = getUserIp(request)
        

        user , error = checkUserExistance(phone_number)

        if error:
            return error
        
        # extracts password from serializer
        password = serializer.validated_data["password"]

        if not user.password:
            message = generateMessage("first you should set a password for login")
            return Response(message , status.HTTP_401_UNAUTHORIZED)

        # check if password is matchs with user password
        if user.check_password(password):
            # if password is right so we reset the lockout
            restLockout(phone_number , userIp)

            message = generateMessage("you logged in successfully")

            # serialize user for response
            userSerializer = UserSerializer(user)
            # adding it to response message
            message["user"] = userSerializer.data

            return Response(message, status.HTTP_200_OK)
        # if password is wrong one failed attempt will be added to lockout
        else:
            error = lockoutAccount(
                phone_number,
                userIp, 
                f"{BLOCK_MESSAGE}, because you've entered wrong phone number or password 3 time."
            )

            if error:
                return error
            message = generateMessage("phone number or password is wrong")
            return Response(message, status.HTTP_401_UNAUTHORIZED)
    # bad request errors
    return Response(serializer.errors , status.HTTP_400_BAD_REQUEST)