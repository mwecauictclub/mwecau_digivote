from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, CollegeData, Course, State
from .serializers import UserSerializer, RegisterSerializer, CompleteRegistrationSerializer
from election.models import Election
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import uuid

@shared_task(queue='email_queue')
def send_verification_email(user_id, token):
    user = User.objects.get(id=user_id)
    subject = "MWECAU Election Platform - Verify Your Email"
    message = (
        f"Dear {user.get_full_name()},\n\n"
        f"Please complete your registration by setting your password:\n"
        f"http://localhost:8000/api/core/auth/complete-registration/?token={token}\n"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True
    )

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            college_data = CollegeData.objects.filter(
                registration_number=serializer.validated_data['registration_number']
            ).first()
            if not college_data:
                return Response({'error': 'Invalid registration number'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_from_college_data(college_data)
            token = str(uuid.uuid4())
            user.verification_token = token
            user.save()
            send_verification_email.delay(user.id, token)
            return Response({'message': 'User registered, check email for verification'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompleteRegistrationView(APIView):
    def post(self, request):
        serializer = CompleteRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(
                verification_token=serializer.validated_data['token'],
                is_verified=False
            ).first()
            if not user:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['password'])
            user.state = serializer.validated_data['state']
            user.course = serializer.validated_data['course']
            user.is_verified = True
            user.verification_token = None
            user.save()
            for election in Election.objects.filter(is_active=True, has_ended=False):
                User.objects.generate_voter_tokens(user.id, election.id)
            return Response({'message': 'Registration completed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        registration_number = request.data.get('registration_number')
        password = request.data.get('password')
        user = authenticate(request, registration_number=registration_number, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)