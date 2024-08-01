from rest_framework import serializers
from auth import utils
from register.models import User

class UserLoginSerializer(serializers.Serializer):

    def validate(self, data):
        utils.ValidatePhoneNumber(data["phone_number"])
        return data

    phone_number = serializers.CharField()
    password     = serializers.CharField()



class VerifyPhoneNumberSerializer(serializers.Serializer):


    def validate(self, data):
        utils.ValidatePhoneNumber(data["phone_number"])
        return data

    phone_number = serializers.CharField()