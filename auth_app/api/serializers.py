from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re


class RegisterSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)


    def validate(self, attrs):
        password = attrs['password']
        repeated_password = attrs.pop('confirmed_password')
        username = attrs['username']
        email = attrs['email']

        if password !=repeated_password:
            raise serializers.ValidationError('Password and confirmation password do not match.')
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error':'Username or email is already registered.'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Username or email is already registered.'})
        
        return attrs
    
    def validate_password(self, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{6,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Password must be at least 6 characters and include an uppercase letter, a lowercase letter, and a number.'
            )
        return value

    
    def create(self, validated_data):
        password = validated_data.pop('password')


        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirmed_password', 'email']


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Wrong username or password')
        
        if not user.check_password(password):
            raise serializers.ValidationError('Wrong username or password')

        data = super().validate({"username": user.username, "password": password})
        data['user'] = user
        return data
        