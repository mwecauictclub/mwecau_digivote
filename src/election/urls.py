from django.urls import path
from .views import VoteView, ResultsView

urlpatterns = [
    # Minimal API endpoints for voting submission and results
    path('<int:election_id>/submit/', VoteView.as_view(), name='api_vote_submit'),
    path('<int:election_id>/results/', ResultsView.as_view(), name='api_results'),
]
