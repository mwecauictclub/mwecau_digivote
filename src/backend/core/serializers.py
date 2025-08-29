from rest_framework import serializers
from core.models import User, State, Course
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    # Override course field to return name instead of ID
    course = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = User
        fields = ['registration_number', 'first_name', 'last_name', 'email', 'is_verified', 'role', 'course']

class ForgotPasswordSerializer(serializers.Serializer):
    registration_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        registration_number = attrs.get('registration_number')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            registration_number=registration_number,
            password=password
        )
        if user is None:
            raise serializers.ValidationError('Invalid registration number or password')
        refresh = RefreshToken.for_user(user) # type: ignore
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }