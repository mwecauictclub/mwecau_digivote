from django.urls import path
from .views import VoteView, ResultsView
from .views_ui import elections_list, election_vote, election_results, submit_vote

app_name = 'election'

urlpatterns = [
    # UI views for voting
    path('', elections_list, name='elections_list'),
    path('<int:election_id>/vote/', election_vote, name='vote'),
    path('<int:election_id>/vote/submit/', submit_vote, name='submit_vote'),
    path('<int:election_id>/results/', election_results, name='results'),
    
    # Minimal API endpoints for voting submission and results (JSON)
    path('api/<int:election_id>/submit/', VoteView.as_view(), name='api_vote_submit'),
    path('api/<int:election_id>/results/', ResultsView.as_view(), name='api_results'),
]
