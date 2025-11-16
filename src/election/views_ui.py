from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Election, ElectionLevel, Position, Candidate, VoterToken, Vote
from core.models import User


@login_required
def elections_list(request):
    """List all active elections for the user."""
    active_elections = Election.objects.filter(is_active=True).prefetch_related('levels')
    
    context = {
        'elections': active_elections,
    }
    return render(request, 'election/elections_list.html', context)


@login_required
def election_vote(request, election_id):
    """Voting page for a specific election."""
    election = get_object_or_404(Election, id=election_id)
    
    if not election.is_ongoing():
        messages.error(request, "This election is not currently active.")
        return redirect('election:elections_list')
    
    user_tokens = VoterToken.objects.filter(
        user=request.user,
        election=election
    ).select_related('election_level')
    
    voting_levels = []
    for token in user_tokens:
        level = token.election_level
        positions = Position.objects.filter(election_level=level).prefetch_related(
            'candidates__user'
        )
        
        has_voted = token.is_used
        
        voting_levels.append({
            'token': token,
            'level': level,
            'positions': positions,
            'has_voted': has_voted
        })
    
    context = {
        'election': election,
        'voting_levels': voting_levels,
    }
    return render(request, 'election/vote.html', context)


@login_required
def election_results(request, election_id):
    """Results page for a specific election."""
    election = get_object_or_404(Election, id=election_id)
    
    if not (request.user.is_commissioner() or request.user.is_staff or election.has_ended):
        messages.error(request, "Results are not available yet.")
        return redirect('election:elections_list')
    
    results = []
    election_levels = election.levels.all()
    
    for level in election_levels:
        positions = Position.objects.filter(election_level=level)
        level_results = []
        
        for position in positions:
            candidates = Candidate.objects.filter(position=position).annotate(
                votes=Count('vote')
            ).order_by('-votes')
            
            total_votes = sum(c.votes for c in candidates)
            
            candidate_results = []
            for candidate in candidates:
                percentage = (candidate.votes / total_votes * 100) if total_votes > 0 else 0
                candidate_results.append({
                    'candidate': candidate,
                    'vote_count': candidate.votes,
                    'percentage': round(percentage, 2)
                })
            
            level_results.append({
                'position': position,
                'candidates': candidate_results,
                'total_votes': total_votes
            })
        
        results.append({
            'level': level,
            'positions': level_results
        })
    
    context = {
        'election': election,
        'results': results,
    }
    return render(request, 'election/results.html', context)


@login_required
def submit_vote(request, election_id):
    """Process vote submission via form POST."""
    if request.method != 'POST':
        return redirect('election:vote', election_id=election_id)
    
    election = get_object_or_404(Election, id=election_id)
    
    try:
        token_id = request.POST.get('token_id')
        candidate_id = request.POST.get('candidate_id')
        
        token = get_object_or_404(VoterToken, id=token_id, user=request.user)
        candidate = get_object_or_404(Candidate, id=candidate_id)
        
        if token.is_used:
            messages.error(request, "This token has already been used.")
            return redirect('election:vote', election_id=election_id)
        
        if not election.is_ongoing():
            messages.error(request, "Election is not active.")
            return redirect('election:vote', election_id=election_id)
        
        if candidate.position.election_level != token.election_level:
            messages.error(request, "Invalid vote selection.")
            return redirect('election:vote', election_id=election_id)
        
        Vote.objects.create(
            token=token,
            candidate=candidate,
        )
        
        token.mark_as_used()
        
        messages.success(request, f"Your vote for {candidate.position.title} has been recorded successfully!")
        
    except Exception as e:
        messages.error(request, f"Error submitting vote: {str(e)}")
    
    return redirect('election:vote', election_id=election_id)
