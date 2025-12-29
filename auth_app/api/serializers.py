from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
            raise serializers.ValidationError('Username email is already registered.')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':'Email is already registered.'})
        
        

        return attrs
    
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
            print(user.email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Wrong username or password 1')
        
        if not user.check_password(password):
            raise serializers.ValidationError('Wrong username or password 2')

        data = super().validate({"username": user.username, "password": password})
        data['user'] = user
        return data
        