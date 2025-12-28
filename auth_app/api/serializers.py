from rest_framework import serializers
from django.contrib.auth.models import User


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

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirmed_password', 'email']
        