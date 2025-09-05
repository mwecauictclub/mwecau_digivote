# election/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from .models import Election, ElectionLevel, Position, Candidate, VoterToken, Vote
from .serializers import ElectionSerializer, PositionSerializer, CandidateSerializer, VoterTokenSerializer, VoteSerializer
from core.models import User

class ElectionCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ElectionSerializer(data=request.data)
        if serializer.is_valid():
            election = serializer.save()
            # Generate tokens for all eligible users per level
            users = User.objects.filter(is_verified=True)
            for user in users:
                User.objects.generate_voter_tokens(user.id, election.id)  # From core UserManager
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ElectionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        elections = Election.objects.all()
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data)

class VoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            election = serializer.validated_data['election']
            if not election.is_ongoing():
                return Response({'error': 'Election not ongoing'}, status=status.HTTP_400_BAD_REQUEST)
            # Validate token and eligibility
            token = VoterToken.objects.filter(
                user=request.user,
                election=election,
                election_level=serializer.validated_data['election_level'],
                is_used=False,
                expiry_date__gte=timezone.now()
            ).first()
            if not token:
                return Response({'error': 'Invalid or used token'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(voter=request.user, token=token)
            token.mark_as_used()
            return Response({'message': 'Vote cast'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResultsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, election_id):
        election = Election.objects.filter(id=election_id).first()
        if not election:
            return Response({'error': 'Election not found'}, status=status.HTTP_404_NOT_FOUND)
        # Aggregate votes
        votes = Vote.objects.filter(election=election).values('candidate').annotate(count=Count('candidate'))
        return Response(votes)