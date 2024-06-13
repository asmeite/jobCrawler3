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
        fields = ['id', 'id_user', 'job_title', 'description', 'location', 'link']