from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from .models import Election, ElectionLevel, Position, Candidate, VoterToken, Vote
from .serializers import ElectionSerializer, PositionSerializer, CandidateSerializer, VoterTokenSerializer, VoteSerializer, ResultSerializer
from .tasks import notify_voters_of_active_election, send_vote_confirmation_email
import logging

logger = logging.getLogger(__name__)

class ElectionCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = ElectionSerializer(data=request.data)
        if serializer.is_valid():
            election = serializer.save()
            if election.is_active:
                notify_voters_of_active_election.delay(election.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ElectionListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        elections = Election.objects.all()
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data)

class PositionCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            position = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CandidateCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            candidate = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, election_id):
        election = Election.objects.filter(id=election_id, is_active=True, has_ended=False).first()
        if not election or timezone.now() < election.start_date or timezone.now() > election.end_date:
            return Response({'error': 'Election not active'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        positions = []
        if ElectionLevel.objects.filter(code=ElectionLevel.LEVEL_PRESIDENT, id__in=election.levels.values('id')).exists():
            positions.extend(Position.objects.filter(election_level__code=ElectionLevel.LEVEL_PRESIDENT))
        if user.state:
            positions.extend(Position.objects.filter(election_level__code=ElectionLevel.LEVEL_STATE, state=user.state))
        if user.course:
            positions.extend(Position.objects.filter(election_level__code=ElectionLevel.LEVEL_COURSE, course=user.course))
        
        position_data = []
        for pos in positions:
            user_vote = Vote.objects.filter(voter=user, election=election, election_level=pos.election_level).first()
            candidates = Candidate.objects.filter(election=election, position=pos)
            tokens = VoterToken.objects.filter(user=user, election=election, election_level=pos.election_level, is_used=False)
            position_data.append({
                'position': PositionSerializer(pos).data,
                'candidates': CandidateSerializer(candidates, many=True).data,
                'user_vote': user_vote.candidate.id if user_vote else None,
                'token': VoterTokenSerializer(tokens.first()).data if tokens.exists() else None
            })
        return Response({'election_id': election_id, 'positions': position_data})

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        election = Election.objects.filter(id=serializer.validated_data['election_id'], is_active=True, has_ended=False).first()
        if not election or timezone.now() < election.start_date or timezone.now() > election.end_date:
            return Response({'error': 'Election not active'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        level = ElectionLevel.objects.filter(id=serializer.validated_data['level_id']).first()
        candidate = Candidate.objects.filter(id=serializer.validated_data['candidate_id'], election=election).first()
        token = VoterToken.objects.filter(
            user=user,
            election=election,
            election_level=level,
            token=serializer.validated_data['token'],
            is_used=False,
            expiry_date__gte=timezone.now()
        ).first()
        
        if not (level and candidate and token and candidate.position.election_level == level):
            return Response({'error': 'Invalid vote data'}, status=status.HTTP_400_BAD_REQUEST)
        
        if level.code == ElectionLevel.LEVEL_COURSE and user.course != candidate.position.course:
            return Response({'error': 'Not eligible for course vote'}, status=status.HTTP_403_FORBIDDEN)
        if level.code == ElectionLevel.LEVEL_STATE and user.state != candidate.position.state:
            return Response({'error': 'Not eligible for state vote'}, status=status.HTTP_403_FORBIDDEN)
        
        vote = Vote.objects.create(
            voter=user,
            election=election,
            election_level=level,
            candidate=candidate,
            token=token
        )
        token.mark_as_used()
        candidate.vote_count += 1
        candidate.save(update_fields=['vote_count'])
        send_vote_confirmation_email.delay(user.id, election.id, level.id)
        return Response({'message': 'Vote recorded'}, status=status.HTTP_200_OK)

class ResultsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, election_id):
        election = Election.objects.filter(id=election_id).first()
        if not election:
            return Response({'error': 'Election not found'}, status=status.HTTP_404_NOT_FOUND)
        if not election.has_ended and not request.user.is_commissioner():
            return Response({'error': 'Results not available'}, status=status.HTTP_403_FORBIDDEN)
        
        positions = []
        if ElectionLevel.objects.filter(code=ElectionLevel.LEVEL_PRESIDENT, id__in=election.levels.values('id')).exists():
            positions.extend(Position.objects.filter(election_level__code=ElectionLevel.LEVEL_PRESIDENT))
        if request.user.state:
            positions.extend(Position.objects.filter(election_level__code=ElectionLevel.LEVEL_STATE, state=request.user.state))
        if request.user.course:
            positions.extend(Position.objects.filter(election_level__code=ElectionLevel.LEVEL_COURSE, course=request.user.course))
        if request.user.is_commissioner():
            positions = Position.objects.filter(election=election)
        
        results = []
        for pos in positions:
            total_votes = Vote.objects.filter(election=election, election_level=pos.election_level).count()
            results.append({
                'position_id': pos.id,
                'position_title': pos.title,
                'total_votes': total_votes
            })
        return Response(ResultSerializer(results, many=True).data)
# # election/views.py

# from django.http import Http404
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from django.utils import timezone
# from django.db.models import Count
# from django.shortcuts import get_object_or_404
# from .models import Election, ElectionLevel, Position, Candidate, VoterToken, Vote
# from .serializers import (
#     ElectionListSerializer, 
#     # Add a dedicated serializer for detailed election view if needed, or reuse/extend
#     PositionDetailSerializer, 
#     CandidateListSerializer, 
#     VoterTokenSerializer, 
#     VoteCreateSerializer,
#     PositionResultSerializer # For structured results if used
# )
# from core.models import User
# # Import the Celery task
# # from .tasks import send_voter_token_email # If you create/rename this task
# from .tasks import send_vote_confirmation_email
# from election import models # Using the existing task name from your snippet

# # --- Election Views ---

# class ElectionListView(APIView):
#     """
#     API endpoint for listing elections.
#     Authenticated users see active elections.
#     Admins could potentially see all with filters.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Filter for active elections. Could add query params for admins to see more.
#         elections = Election.objects.filter(is_active=True)
#         serializer = ElectionListSerializer(elections, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class ElectionDetailView(APIView):
#     """
#     API endpoint for retrieving details of a specific election.
#     Includes positions and candidates relevant to the requesting user.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request, election_id):
#         election = get_object_or_404(Election, id=election_id)
        
#         # Optional: Check if election is active or user has special permissions
#         # if not election.is_active and not (request.user.is_staff or request.user.is_commissioner()):
#         #     return Response({'error': 'Election details not available.'}, status=status.HTTP_403_FORBIDDEN)

#         # --- Get Positions and Candidates relevant to the user ---
#         user = request.user
#         relevant_positions_data = []

#         # Iterate through levels included in this election
#         for level in election.levels.all():
#             # Check user eligibility for this level
#             is_eligible = False
#             if level.type == ElectionLevel.TYPE_PRESIDENT:
#                 is_eligible = True # All users are eligible for President
#             elif level.type == ElectionLevel.TYPE_COURSE and user.course == level.course:
#                 is_eligible = True
#             elif level.type == ElectionLevel.TYPE_STATE and user.state == level.state:
#                 is_eligible = True

#             if is_eligible:
#                 # Get positions for this eligible level within this election
#                 positions = Position.objects.filter(election_level=level)
#                 for position in positions:
#                     # Serialize position details
#                     position_serializer = PositionDetailSerializer(position)
#                     position_data = position_serializer.data
                    
#                     # Get candidates for this position
#                     candidates = Candidate.objects.filter(position=position)
#                     candidate_serializer = CandidateListSerializer(candidates, many=True, context={'request': request})
#                     position_data['candidates'] = candidate_serializer.data
                    
#                     # Check if user has already voted for this position/level in this election
#                     # Find the relevant VoterToken
#                     user_token_for_level = VoterToken.objects.filter(
#                         user=user, election=election, election_level=level
#                     ).first()
                    
#                     user_vote_for_position = None
#                     if user_token_for_level and user_token_for_level.is_used:
#                         # Find the vote associated with the used token for this position
#                         user_vote = Vote.objects.filter(
#                             token=user_token_for_level, 
#                             election=election, 
#                             election_level=level,
#                             candidate__position=position # Ensure vote is for a candidate in this specific position
#                         ).first()
#                         if user_vote:
#                             user_vote_for_position = user_vote.candidate.id
                    
#                     position_data['user_has_voted'] = user_vote_for_position is not None
#                     position_data['user_vote_candidate_id'] = user_vote_for_position
                    
#                     relevant_positions_data.append(position_data)

#         # Serialize the main election details
#         election_serializer = ElectionListSerializer(election, context={'request': request})
#         election_data = election_serializer.data
#         # Add the relevant positions data
#         election_data['positions'] = relevant_positions_data

#         return Response(election_data, status=status.HTTP_200_OK)

# # --- Voting Views ---

# class VoteView(APIView):
#     """
#     API endpoint for casting a vote.
#     Requires a valid VoterToken UUID and Candidate ID.
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = VoteCreateSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             # Get validated data and objects from serializer
#             token_obj = serializer.token_obj
#             election = serializer.election
#             election_level = serializer.election_level
#             candidate = serializer.candidate
#             user = request.user # Get the user from the request

#             # --- Double-check token ownership (belt and suspenders) ---
#             if token_obj.user != user:
#                  return Response({'error': 'You are not authorized to use this token.'}, status=status.HTTP_403_FORBIDDEN)

#             # --- Create the Vote ---
#             # The Vote model's save method handles denormalization and integrity checks
#             try:
#                 vote = Vote.objects.create(
#                     token=token_obj,
#                     candidate=candidate
#                     # election and election_level are set by Vote.save()
#                 )
#             except Exception as e: # Catch potential integrity errors from Vote.save
#                  # Log the error e
#                  return Response({'error': 'An error occurred while recording your vote. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # --- Mark Token as Used ---
#             # The model method handles setting is_used and used_at
#             token_obj.mark_as_used() 

#             # --- Trigger Confirmation Email (Celery) ---
#             # Assuming the task takes user_id, election_id, level_id
#             send_vote_confirmation_email.delay(user.id, election.id, election_level.id)
#             # Or if the task is designed for token ID: send_vote_confirmation_email.delay(token_obj.id) 

#             return Response({'message': 'Vote successfully cast.'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # --- Results Views ---

# class ResultsView(APIView):
#     """
#     API endpoint for viewing election results.
#     Access control: e.g., only after election ends, or for admins/commissioners.
#     """
#     # Start with IsAuthenticated, add more specific logic inside
#     permission_classes = [IsAuthenticated] 

#     def get(self, request, election_id):
#         election = get_object_or_404(Election, id=election_id)
#         user = request.user

#         # --- Access Control Check ---
#         # Define who can see results. Example logic:
#         can_view_results = (
#             election.has_ended or # Anyone can see results after election ends
#             user.is_staff or      # Admins
#             user.is_commissioner() # Commissioners
#             # Add other conditions if needed
#         )

#         if not can_view_results:
#             return Response({'error': 'Results are not available yet.'}, status=status.HTTP_403_FORBIDDEN)

#         # --- Aggregate Results ---
#         results_data = []
#         # Get all levels for this election
#         election_levels = election.levels.all()

#         for level in election_levels:
#             # Get all positions for this level in this election
#             positions = Position.objects.filter(election_level=level)

#             for position in positions:
#                 # Count votes for each candidate in this specific position/level
#                 # Using annotations for efficiency
#                 candidate_votes_qs = Candidate.objects.filter(
#                     position=position
#                 ).annotate(
#                     vote_count=Count('votes', filter=models.Q(votes__election=election, votes__election_level=level))
#                 ).order_by('-vote_count') # Order by votes descending

#                 total_votes_for_level_position = sum(c.vote_count for c in candidate_votes_qs)

#                 candidate_results = []
#                 for candidate_obj in candidate_votes_qs:
#                     count = candidate_obj.vote_count
#                     percentage = (count / total_votes_for_level_position * 100) if total_votes_for_level_position > 0 else 0
#                     # Use serializer for candidate details if needed, or build dict
#                     # candidate_serializer = CandidateListSerializer(candidate_obj, context={'request': request})
#                     candidate_results.append({
#                         'candidate_id': candidate_obj.id,
#                         'candidate_name': candidate_obj.user.get_full_name(),
#                         # 'candidate_details': candidate_serializer.data, # Include if more detail needed
#                         # Add image URL if needed
#                         'candidate_image_url': CandidateListSerializer().get_image_url(candidate_obj) if request else None,
#                         'vote_count': count,
#                         'vote_percentage': round(percentage, 2)
#                     })

#                 # Append results for this position
#                 results_data.append({
#                     'position_id': position.id,
#                     'position_title': position.title,
#                     'total_votes_cast': total_votes_for_level_position,
#                     'candidates': candidate_results
#                 })

#         # Optional: Serialize final results with PositionResultSerializer if defined and complex
#         # serializer = PositionResultSerializer(results_data, many=True)
#         # return Response(serializer.data, status=status.HTTP_200_OK)
        
#         return Response(results_data, status=status.HTTP_200_OK) # Return aggregated data

# # --- Admin Views ---

# class ElectionCreateView(APIView):
#     """
#     API endpoint for creating a new election (Admin only).
#     """
#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         # Use ElectionListSerializer for creation, or a dedicated one
#         serializer = ElectionListSerializer(data=request.data)
#         if serializer.is_valid():
#             # Save the main election object
#             election = serializer.save()
            
#             # --- Post-Creation Logic: Associate Levels ---
#             # Handle M2M relationship for levels after saving the main object
#             level_ids = request.data.get('levels', []) # Expect a list of ElectionLevel IDs
#             if level_ids:
#                 try:
#                     levels = ElectionLevel.objects.filter(id__in=level_ids)
#                     # Use set() for M2M
#                     election.levels.set(levels) 
#                 except Exception as e:
#                     # Log error e
#                     # Consider deleting the partially created election or handling error gracefully
#                     return Response({'error': 'Failed to associate election levels.'}, status=status.HTTP_400_BAD_REQUEST)

#             # --- Trigger Token Generation (asynchronously) ---
#             # Important: This should ideally be a Celery task itself for large user bases
#             # to avoid blocking the request.
#             # from .tasks import generate_tokens_for_election # Hypothetical task
#             # generate_tokens_for_election.delay(election.id) 
            
#             # For now, triggering inline (not ideal for large scales):
#             # Trigger token generation for all *verified* users
#             verified_users = User.objects.filter(is_verified=True)
#             # failures = []
#             for user in verified_users:
#                 # Call the method on the UserManager
#                 # Ensure the method name matches your core/models.py UserManager
#                 try:
#                     # Assuming the method is named generate_voter_tokens_for_election
#                     tokens_generated = User.objects.generate_voter_tokens_for_election(user.id, election.id)
#                     # Optional: Send email notification for tokens (another Celery task)
#                     # You might need to adapt the task signature
#                     # send_voter_token_email.delay(user.id, election.id) # If you have this task
#                     # Or re-use the confirmation email task if it's adapted:
#                     # send_vote_confirmation_email.delay(user.id, election.id) # Check task logic
#                 except Exception as e:
#                     # Log the specific error e for debugging
#                     # failures.append({'user_id': user.id, 'error': str(e)})
#                     # Depending on requirements, you might want to return partial success/failure info
#                     print(f"Error generating tokens for user {user.id} for election {election.id}: {e}")
            
#             # if failures:
#             #     # Log failures or include in response
#             #     print(f"Token generation failures: {failures}")
#             #     # Decide if this warrants an error response or just logging
#             #     # return Response({'message': 'Election created, but some tokens failed to generate.', 'failures': failures}, status=status.HTTP_201_CREATED_WITH_ISSUES) # Not a standard status

#             # Return the created election data
#             # Refresh serializer data to include M2M levels if needed
#             # serializer.refresh_from_db() # Not always necessary, depends on serializer
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CandidateCreateView(APIView):
#     """
#     API endpoint for creating a new candidate (Admin/Class Leader).
#     """
#     permission_classes = [IsAdminUser] # Or custom permission for Class Leaders

#     def post(self, request):
#         # Use CandidateListSerializer or a dedicated create serializer
#         # Ensure it handles image upload correctly (requires proper parser in settings)
#         serializer = CandidateListSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save() # This will call Candidate.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # --- Additional Views for Admin/Management ---

# # --- Position Management Views ---
# class PositionCreateView(APIView):
#     """
#     API endpoint for creating a new position (Admin only).
#     """
#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         # A dedicated serializer for Position creation might be beneficial
#         # to handle nested creation or specific validation if needed.
#         serializer = PositionDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PositionDetailView(APIView):
#     """
#     API endpoint for retrieving, updating, or deleting a specific position (Admin only).
#     """
#     permission_classes = [IsAdminUser]

#     def get_object(self, pk):
#         try:
#             return Position.objects.get(pk=pk)
#         except Position.DoesNotExist:
#             raise Http404("Position not found")

#     def get(self, request, pk):
#         position = self.get_object(pk)
#         serializer = PositionDetailSerializer(position)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         position = self.get_object(pk)
#         serializer = PositionDetailSerializer(position, data=request.data, partial=False)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         position = self.get_object(pk)
#         serializer = PositionDetailSerializer(position, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         position = self.get_object(pk)
#         position.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # --- Candidate Management Views ---
# class CandidateDetailView(APIView):
#     """
#     API endpoint for retrieving, updating, or deleting a specific candidate (Admin only).
#     """
#     permission_classes = [IsAdminUser]

#     def get_object(self, pk):
#         try:
#             return Candidate.objects.get(pk=pk)
#         except Candidate.DoesNotExist:
#             raise Http404("Candidate not found")

#     def get(self, request, pk):
#         candidate = self.get_object(pk)
#         serializer = CandidateListSerializer(candidate, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         candidate = self.get_object(pk)
#         # PUT typically requires all fields. Consider if you want to allow changing the user/election/position.
#         # If image is updated, request.FILES might be needed depending on setup.
#         serializer = CandidateListSerializer(candidate, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         candidate = self.get_object(pk)
#         # PATCH allows partial updates.
#         serializer = CandidateListSerializer(candidate, data=request.data, partial=True, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         candidate = self.get_object(pk)
#         candidate.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # --- Election Management Views ---
# class ElectionDetailView(APIView):
#     """
#     API endpoint for retrieving, updating, or deleting a specific election (Admin only).
#     Note: Updating levels or managing complex M2M relationships might require custom logic.
#     """
#     permission_classes = [IsAdminUser]

#     def get_object(self, pk):
#         try:
#             return Election.objects.get(pk=pk)
#         except Election.DoesNotExist:
#             raise Http404("Election not found")

#     def get(self, request, pk):
#         election = self.get_object(pk)
#         # Use the list serializer or a dedicated detail serializer if fields differ
#         serializer = ElectionListSerializer(election, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         election = self.get_object(pk)
#         # PUT for full update. Be cautious with M2M fields like 'levels'.
#         serializer = ElectionListSerializer(election, data=request.data, partial=False)
#         if serializer.is_valid():
#             serializer.save()
#             # Handle M2M 'levels' update if included in request.data
#             # This part can be tricky and might need custom handling
#             # similar to ElectionCreateView
#             level_ids = request.data.get('levels')
#             if level_ids is not None: # Allow clearing levels with []
#                  try:
#                      levels = ElectionLevel.objects.filter(id__in=level_ids)
#                      election.levels.set(levels)
#                  except Exception as e:
#                      # Log error e
#                      return Response({'error': 'Failed to update election levels.'}, status=status.HTTP_400_BAD_REQUEST)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         election = self.get_object(pk)
#         # PATCH for partial update.
#         serializer = ElectionListSerializer(election, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             # Handle partial M2M 'levels' update if included in request.data
#             # This is complex. Often, a specific endpoint for managing levels is better.
#             # Example: Add/Remove level endpoints.
#             # For simplicity here, we'll mimic PUT logic if 'levels' is provided.
#             level_ids = request.data.get('levels')
#             if level_ids is not None: # Checks for key existence, even if value is []
#                  try:
#                      if level_ids: # If list is not empty
#                          levels = ElectionLevel.objects.filter(id__in=level_ids)
#                          election.levels.set(levels)
#                      else: # If empty list is sent, clear levels
#                          election.levels.clear()
#                  except Exception as e:
#                      # Log error e
#                      return Response({'error': 'Failed to update election levels.'}, status=status.HTTP_400_BAD_REQUEST)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         election = self.get_object(pk)
#         # Consider implications of deleting an election with votes/candidates.
#         # Might want soft delete or cascade protection.
#         election.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # Placeholder for specific M2M management if needed (e.g., adding/removing levels from an election)
# # class ElectionLevelManagementView(APIView):
# #     permission_classes = [IsAdminUser]
# #     def post(self, request, election_pk, action): # action: 'add' or 'remove'
# #         election = get_object_or_404(Election, pk=election_pk)
# #         level_id = request.data.get('level_id')
# #         if not level_id:
# #             return Response({'error': 'level_id is required'}, status=status.HTTP_400_BAD_REQUEST)
# #         level = get_object_or_404(ElectionLevel, pk=level_id)
# #
# #         if action == 'add':
# #             election.levels.add(level)
# #         elif action == 'remove':
# #             election.levels.remove(level)
# #         else:
# #             return Response({'error': 'Invalid action. Use "add" or "remove".'}, status=status.HTTP_400_BAD_REQUEST)
# #
# #         return Response({'message': f'Level {action}ed successfully'}, status=status.HTTP_200_OK)

# # --- Token Management Views (Potentially Useful for Admin) ---
# class VoterTokenListView(APIView):
#     """
#     API endpoint for listing voter tokens (potentially for admin debugging/oversight).
#     Filtering by election, user, or used status would be beneficial.
#     """
#     permission_classes = [IsAdminUser] # Restrict access

#     def get(self, request):
#         # Get query parameters for filtering
#         election_id = request.query_params.get('election_id', None)
#         user_id = request.query_params.get('user_id', None)
#         is_used = request.query_params.get('is_used', None) # Expect 'true' or 'false' string

#         tokens = VoterToken.objects.all()

#         if election_id:
#             tokens = tokens.filter(election_id=election_id)
#         if user_id:
#             tokens = tokens.filter(user_id=user_id)
#         if is_used is not None:
#             # Convert string parameter to boolean
#             is_used_bool = is_used.lower() == 'true'
#             tokens = tokens.filter(is_used=is_used_bool)

#         # Consider pagination for large datasets
#         serializer = VoterTokenSerializer(tokens, many=True)
#         return Response(serializer.data)

# class VoterTokenDetailView(APIView):
#     """
#     API endpoint for viewing details of a specific voter token (Admin).
#     """
#     permission_classes = [IsAdminUser]

#     def get(self, request, pk):
#         token = get_object_or_404(VoterToken, pk=pk)
#         serializer = VoterTokenSerializer(token)
#         return Response(serializer.data)

# # --- Vote Management/Inspection Views (Potentially Useful for Admin) ---
# class VoteListView(APIView):
#     """
#     API endpoint for listing votes (Admin only, likely for auditing).
#     """
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         # Get query parameters for filtering votes
#         election_id = request.query_params.get('election_id', None)
#         candidate_id = request.query_params.get('candidate_id', None)

#         votes = Vote.objects.select_related('token__user', 'candidate__user', 'election', 'election_level')

#         if election_id:
#             votes = votes.filter(election_id=election_id)
#         if candidate_id:
#             votes = votes.filter(candidate_id=candidate_id)

#         # Consider pagination for large datasets
#         # A simple serializer that outputs key vote details might be needed
#         # For now, returning basic data
#         vote_data = []
#         for vote in votes:
#              vote_data.append({
#                  'id': vote.id,
#                  'voter': vote.token.user.get_full_name() if vote.token.user else 'Unknown',
#                  'voter_reg_number': vote.token.user.registration_number if vote.token.user else 'Unknown',
#                  'election': vote.election.title,
#                  'level': vote.election_level.name,
#                  'candidate': vote.candidate.user.get_full_name() if vote.candidate.user else 'Unknown',
#                  'timestamp': vote.timestamp,
#                  # 'token_id': vote.token.id, # If needed
#              })

#         return Response(vote_data) # Or use a dedicated VoteListSerializer

# # ... (Ensure all necessary imports like Http404 are at the top) ...
# # Add these new views to your election/urls.py
