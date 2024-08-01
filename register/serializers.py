from .models import User
from rest_framework import serializers
from rest_framework import status
import re

class CreateUserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        # created a regex for detecting invalid or valid phone numbers
        phone_regex = re.compile(r"(?:(?:\+98|0098|0)9\d{9})|(?:\+98|0098|0\d{2}\d{7,8})")
        # check if phone number is not valid
        if not phone_regex.match(data['phone_number']):
            # return the proper error
            error = {
                "phone_number": "phone number is not a valid phone number"
            }

            raise serializers.ValidationError(error, status.HTTP_400_BAD_REQUEST)
        
        return data

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name', 'email', 'password']