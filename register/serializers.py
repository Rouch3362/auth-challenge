from .models import User, OTP
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UpdateUserSerializer(serializers.Serializer):
    first_name   = serializers.CharField()
    last_name    = serializers.CharField()
    email        = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password     = serializers.CharField()


class OTPSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OTP
        fields = ["code" , "phone_number"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "first_name", "last_name", "email"]