from .models import User, OTP
from rest_framework import serializers
from rest_framework import status
from auth import utils

class UpdateUserSerializer(serializers.Serializer):

    def validate(self, data):
        utils.ValidatePhoneNumber(data["phone_number"])
        
        return data

    phone_number = serializers.CharField()
    first_name   = serializers.CharField()
    last_name    = serializers.CharField()
    email        = serializers.EmailField()
    password     = serializers.CharField()


class OTPSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OTP
        fields = ["code" , "phone_number"]