from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import UserLoginSerializer, VerifyPhoneNumberSerializer
from register.models import User
from rest_framework.response import Response
from rest_framework import status
from auth.utils import GenerateError

@api_view(["POST"])
def loginUser(request):
    
    phone_number_header = request.headers.get("phone-number")

    if phone_number_header is None:
        serializer = VerifyPhoneNumberSerializer(data=request.data)

        if serializer.is_valid():
            
            phone_number = serializer.validated_data["phone_number"]
            phone_number = phone_number.replace("+98", "0")
            try:
                User.objects.get(phone_number=phone_number)

            except User.DoesNotExist:
                error = GenerateError("user with this phone number does not exist")
                return Response(error, status.HTTP_404_NOT_FOUND)
            

            return Response({"user exists. enter password now"},status.HTTP_200_OK)
        
        return Response(serializer.errors , status.HTTP_400_BAD_REQUEST)
    
    else:
        
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            phone_number_header = phone_number_header.replace("+98", "0")
            user = User.objects.get(phone_number=phone_number_header)
            
            if user.check_password(serializer.validated_data["password"]):
                return Response({"detail": "you logged in successfully"} , status.HTTP_200_OK)
            else:
                error = GenerateError("wrong phone number or password")
                return Response(error , status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.errors , status.HTTP_400_BAD_REQUEST)