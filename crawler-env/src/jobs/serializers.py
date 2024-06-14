from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserJobs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobs
        fields = [ 'id_user', 'job_title', 'description', 'link']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False}
        }
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
       
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
       
        instance.save()
        return instance
