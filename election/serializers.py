from rest_framework import serializers
from .models import Election, ElectionLevel, Position, Candidate, VoterToken, Vote
from core.models import User, Course, State

class ElectionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionLevel
        fields = ['id', 'name', 'code', 'description']

class ElectionSerializer(serializers.ModelSerializer):
    levels = ElectionLevelSerializer(many=True)
    class Meta:
        model = Election
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'is_active', 'has_ended', 'levels', 'created_at', 'updated_at']

class PositionSerializer(serializers.ModelSerializer):
    election_level = ElectionLevelSerializer()
    state = serializers.SlugRelatedField(slug_field='name', queryset=State.objects.all(), allow_null=True)
    course = serializers.SlugRelatedField(slug_field='code', queryset=Course.objects.all(), allow_null=True)
    class Meta:
        model = Position
        fields = ['id', 'title', 'election_level', 'description', 'gender_restriction', 'state', 'course']

class CandidateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    image_url = serializers.SerializerMethodField()
    position = PositionSerializer(read_only=True)
    class Meta:
        model = Candidate
        fields = ['id', 'user', 'user_name', 'election', 'position', 'bio', 'platform', 'image_url', 'vote_count']
    
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

class VoterTokenSerializer(serializers.ModelSerializer):
    election_level = ElectionLevelSerializer()
    class Meta:
        model = VoterToken
        fields = ['token', 'election_level', 'expiry_date', 'is_used']

class VoteSerializer(serializers.Serializer):
    election_id = serializers.IntegerField()
    level_id = serializers.IntegerField()
    candidate_id = serializers.IntegerField()
    token = serializers.UUIDField()

class ResultSerializer(serializers.Serializer):
    position_id = serializers.IntegerField()
    position_title = serializers.CharField()
    candidates = serializers.SerializerMethodField()
    total_votes = serializers.IntegerField()
    
    def get_candidates(self, obj):
        candidates = Candidate.objects.filter(position_id=obj['position_id'])
        total_votes = obj['total_votes']
        return [{
            'candidate_id': c.id,
            'name': c.user.get_full_name(),
            'image_url': c.image.url if c.image else None,
            'vote_count': c.vote_count,
            'vote_percentage': 0 if total_votes == 0 else (c.vote_count / total_votes) * 100
        } for c in candidates]