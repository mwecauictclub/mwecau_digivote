from rest_framework import serializers
from .models import User, State, Course

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'registration_number', 'email', 'course', 'state', 'is_verified']

class RegisterSerializer(serializers.Serializer):
    registration_number = serializers.CharField(max_length=50)
    email = serializers.EmailField()

class CompleteRegistrationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=36)
    password = serializers.CharField(write_only=True)
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), allow_null=True)