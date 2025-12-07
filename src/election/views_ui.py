from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import Election, ElectionLevel, Position, Candidate, VoterToken, Vote
from core.models import User


def _check_election_eligibility(user, election):
    """Check if user is eligible to vote in this election.
    Returns tuple: (is_eligible, reason)
    """
    if not user.is_verified:
        return False, "not_verified"
    
    # Get user's tokens for this election
    has_token = VoterToken.objects.filter(user=user, election=election).exists()
    if not has_token:
        return False, "no_token"
    
    return True, "eligible"


def _get_election_status(election):
    """Get election status badge info.
    Returns dict with status, label, and color.
    """
    now = timezone.now()
    
    if election.has_ended:
        return {'status': 'ended', 'label': 'Ended', 'color': 'danger'}
    elif election.is_active:
        return {'status': 'active', 'label': 'Active', 'color': 'success'}
    elif election.start_date > now:
        return {'status': 'upcoming', 'label': 'Upcoming', 'color': 'info'}
    else:
        return {'status': 'pending', 'label': 'Pending', 'color': 'warning'}


@login_required
def elections_list(request):
    """List all elections filtered by user eligibility and status."""
    now = timezone.now()
    user = request.user
    
    # Get all elections for display
    all_elections = Election.objects.all().prefetch_related('levels').order_by('-start_date')
    
    elections_data = []
    for election in all_elections:
        is_eligible, eligibility_reason = _check_election_eligibility(user, election)
        status_info = _get_election_status(election)
        
        # Get user's voting tokens for this election
        user_tokens = VoterToken.objects.filter(user=user, election=election)
        has_voted = user_tokens.filter(is_used=True).exists()
        
        election_data = {
            'election': election,
            'status_info': status_info,
            'is_eligible': is_eligible,
            'eligibility_reason': eligibility_reason,
            'has_voted': has_voted,
            'can_vote': is_eligible and election.is_active and not has_voted,
            'can_view_results': user.is_commissioner() or user.is_observer() or election.has_ended,
            'token_count': user_tokens.count(),
        }
        elections_data.append(election_data)
    
    # Categorize elections
    active_elections = [e for e in elections_data if e['status_info']['status'] == 'active']
    upcoming_elections = [e for e in elections_data if e['status_info']['status'] == 'upcoming']
    ended_elections = [e for e in elections_data if e['status_info']['status'] == 'ended']
    
    context = {
        'active_elections': active_elections,
        'upcoming_elections': upcoming_elections,
        'ended_elections': ended_elections,
        'all_elections_count': len(elections_data),
        'user': user,
    }
    return render(request, 'election/elections_list.html', context)


@login_required
def election_vote(request, election_id):
    """Voting page for a specific election with eligibility checks."""
    election = get_object_or_404(Election, id=election_id)
    user = request.user
    now = timezone.now()
    
    # Check if election is active for voting
    if not election.is_ongoing():
        status_info = _get_election_status(election)
        messages.error(request, f"This election is {status_info['label'].lower()} and voting is not available.")
        return redirect('election:elections_list')
    
    # Check user eligibility
    is_eligible, eligibility_reason = _check_election_eligibility(user, election)
    if not is_eligible:
        if eligibility_reason == "not_verified":
            messages.error(request, "Your account is not verified. Please verify your account first.")
        elif eligibility_reason == "no_token":
            messages.error(request, "You are not eligible to vote in this election.")
        return redirect('election:elections_list')
    
    # Get user's voting tokens for this election
    user_tokens = VoterToken.objects.filter(
        user=user,
        election=election
    ).select_related('election_level')
    
    if not user_tokens.exists():
        messages.error(request, "No voting tokens available for this election.")
        return redirect('election:elections_list')
    
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
            'has_voted': has_voted,
            'can_vote': not has_voted and election.is_ongoing(),
        })
    
    # Check if all tokens have been used
    all_voted = all(t['has_voted'] for t in voting_levels)
    
    context = {
        'election': election,
        'voting_levels': voting_levels,
        'all_voted': all_voted,
        'status_info': _get_election_status(election),
        'election_time_remaining': election.end_date - now if election.is_active else None,
    }
    return render(request, 'election/vote.html', context)


@login_required
def election_results(request, election_id):
    """Results page for election - access controlled by status and role."""
    election = get_object_or_404(Election, id=election_id)
    user = request.user
    
    # Determine if user can view results
    can_view_results = (
        user.is_commissioner() or 
        user.is_observer() or 
        user.is_staff or 
        election.has_ended
    )
    
    if not can_view_results:
        messages.error(request, "Results are not available yet. Please check back after the election ends.")
        return redirect('election:elections_list')
    
    # Check result publication status
    status_info = _get_election_status(election)
    is_results_final = election.has_ended
    
    results = []
    election_levels = election.levels.all()
    
    for level in election_levels:
        positions = Position.objects.filter(election_level=level)
        level_results = []
        level_total_votes = 0
        
        for position in positions:
            candidates = Candidate.objects.filter(position=position).annotate(
                vote_total=Count('votes')
            ).order_by('-vote_total')
            
            total_votes = sum(c.vote_total for c in candidates)
            level_total_votes += total_votes
            
            candidate_results = []
            for candidate in candidates:
                percentage = (candidate.vote_total / total_votes * 100) if total_votes > 0 else 0
                candidate_results.append({
                    'candidate': candidate,
                    'vote_count': candidate.vote_total,
                    'percentage': round(percentage, 2)
                })
            
            level_results.append({
                'position': position,
                'candidates': candidate_results,
                'total_votes': total_votes
            })
        
        results.append({
            'level': level,
            'positions': level_results,
            'total_votes': level_total_votes
        })
    
    context = {
        'election': election,
        'results': results,
        'status_info': status_info,
        'is_results_final': is_results_final,
        'can_view_results': can_view_results,
        'view_permission_reason': 'admin' if user.is_staff else ('commissioner' if user.is_commissioner() else ('observer' if user.is_observer() else 'election_ended')),
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
