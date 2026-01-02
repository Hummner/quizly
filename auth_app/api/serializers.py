from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles validation of user input, password confirmation,
    password strength, and user creation.
    """

    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validates cross-field data.

        - Checks if password and confirmation match
        - Ensures username and email are unique
        """

        password = attrs['password']
        repeated_password = attrs.pop('confirmed_password')
        username = attrs['username']
        email = attrs['email']

        if password != repeated_password:
            raise serializers.ValidationError(
                'Password and confirmation password do not match.'
            )

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'error': 'Username or email is already registered.'}
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'error': 'Username or email is already registered.'}
            )

        return attrs

    def validate_password(self, value):
        """
        Validates password strength.

        Requires at least 6 characters, one uppercase letter,
        one lowercase letter, and one number.
        """

        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{6,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Password must be at least 6 characters and include an uppercase letter, a lowercase letter, and a number.'
            )
        return value

    def create(self, validated_data):
        """
        Creates a new user instance.

        Hashes the password before saving the user.
        """

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        """
        Serializer configuration.
        """

        model = User
        fields = ['id', 'username', 'password', 'confirmed_password', 'email']


class CustomTokenSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer for user login.

    Authenticates the user manually and
    attaches the user object to the token response.
    """

    def validate(self, attrs):
        """
        Validates login credentials.

        - Checks if user exists
        - Verifies the password
        """

        username = attrs['username']
        password = attrs['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Wrong username or password')

        if not user.check_password(password):
            raise serializers.ValidationError('Wrong username or password')

        data = super().validate(
            {"username": user.username, "password": password}
        )
        data['user'] = user
        return data
