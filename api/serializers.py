from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

UserModel = get_user_model()


class UserInfoSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'email', 'user_type')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_visible:
            raise ValidationError("No active account found with the given credentials")

        user_info = UserInfoSerialzer(self.user).data
        
        data['user_info'] = user_info
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "email", "first_name", "last_name", "password", "user_type"]

    def validate_password(self, value):
        """
        Validate the password field according to Django's password requirements.
        """
        validate_password(value)
        return value
    
    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user_type = validated_data.get('user_type')
        password = validated_data.get('password')

        user = UserModel.objects.create(
            email=email, first_name=first_name,
            last_name=last_name, user_type=user_type
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update an existing user.
        """
        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)
        user_type = validated_data.get('user_type', instance.user_type)
        password = validated_data.get('password', instance.password)

        instance.first_name = first_name
        instance.last_name = last_name
        instance.user_type = user_type
        if 'password' in validated_data:
            instance.set_password(password)
        instance.is_visible = True
        instance.save()
        return instance

