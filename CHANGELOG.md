# Changelog

All notable changes to this project should be documented in this file.

Formatting: This project follows a simplified Keep a Changelog style.

Unreleased
---------

### Dashboard & Election Views Enhancement with Status-Based Filters (2025-12-08)

**Election Views Improvements (src/election/views_ui.py):**
- Added `_get_election_status()` helper function to determine election status (active, ended, upcoming, pending)
- Added `_check_election_eligibility()` helper to verify user voting eligibility based on verification and token status
- Enhanced `elections_list()` view:
  - Filters elections by status (active, upcoming, completed)
  - Shows eligibility info for each election (eligible, not verified, no token)
  - Displays voting status (can vote, has voted, can't vote)
  - Shows access to results based on user role or election completion
  - Orders elections by status and date
- Enhanced `election_vote()` view:
  - Validates election is active before allowing voting
  - Checks user is verified and has voting token
  - Shows eligibility reasons for rejected votes
  - Displays time remaining for election
  - Shows which voting levels user has completed
- Enhanced `election_results()` view:
  - Access control: Commissioners, Observers, Staff, or election has ended
  - Shows publication status (results final or interim)
  - Calculates vote totals per level for better analysis
  - Tracks permission reason (admin/commissioner/observer/election ended)
  - Better error messaging for access denied

**Core Dashboard Enhancements (src/core/views_ui.py):**
- Enhanced `dashboard_view()`:
  - Separates voting tokens by election status (active, completed)
  - Shows token usage status (available/used)
  - Displays active, upcoming, and completed elections separately
  - Filters elections by date for relevance
  - Shows profile edit eligibility status based on active elections
  - Displays voting statistics (total tokens, used tokens)

**Observer Dashboard Enhancements (src/core/views_commissioner.py):**
- Enhanced `observer_dashboard()`:
  - Filters elections by status (active, completed, upcoming)
  - Shows statistics separated by election status
  - Displays only votes from active/completed elections
  - Separates recent elections by status category
  - Better data organization for election observation

**Status-Based URL Control:**
- `elections_list/` - Shows all elections with status and eligibility filtering
- `elections/<id>/vote/` - Access controlled: Active election + User eligible
- `elections/<id>/results/` - Access controlled: Commissioner/Observer/Staff or election ended
- Status badges: Active (green), Ended (red), Upcoming (blue), Pending (yellow)

**Logic Filters Implemented:**
- User verification status check before voting
- Voting token eligibility verification
- Election active status validation
- Results publication status check
- Role-based access control for results viewing
- Time-based election categorization
- Vote eligibility per election level

### Election Observer Role Implementation (2025-12-07)

**New Observer Role:**
- Added new `ROLE_OBSERVER` to User model's ROLE_CHOICES
- Observer is a read-only user with comprehensive visibility into all election data
- Observers can view all votes cast, election results, token statistics, and voter participation
- Observers are eligible voters themselves (can vote if they meet election-level requirements)
- Observer role created by assigning `role='observer'` to User model

**Observer Dashboard (src/core/views_commissioner.py):**
- `observer_dashboard()` - Main HTML dashboard view for observers
  - Displays user statistics (total, verified, unverified)
  - Shows election statistics (active, completed, total)
  - Displays voting statistics (total votes, candidates, tokens, usage)
  - Shows voter participation by state and course
  - Lists recent elections with status indicators
  - Displays recent 50 votes with election, level, candidate, position, voter ID, and timestamp
  - Provides API endpoint references for JSON data access
- `observer_election_details_api()` - JSON API endpoint for election details
  - Returns complete vote data for a specific election
  - Shows votes grouped by election level and position
  - Calculates statistics per level and per position
- `observer_votes_api()` - JSON API endpoint for all system votes
  - Returns complete vote list with election, level, candidate, position, voter ID, timestamp
  - Used for comprehensive vote auditing
- `observer_tokens_api()` - JSON API endpoint for token statistics
  - Shows token usage by election
  - Displays total, used, unused tokens
  - Calculates usage percentage per election

**Observer Permissions (src/core/permissions.py):**
- `IsObserver` - Strict permission requiring user role == ROLE_OBSERVER
- `IsCommissionerOrObserver` - Allows both Commissioner and Observer roles for shared read-only endpoints

**Observer URLs (src/core/urls.py):**
- `observer/` - Observer dashboard HTML view
- `api/observer/election/<id>/` - Election details with all votes
- `api/observer/votes/` - All votes in system
- `api/observer/tokens/` - Token statistics by election

**Observer Template (src/templates/core/observer_dashboard.html):**
- Bootstrap-based responsive dashboard with statistics cards
- Color-coded status indicators for elections (Active, Ended, Pending)
- Responsive tables for states, courses, recent elections, and recent votes
- Card-based layout with hover effects
- API endpoint documentation section

**Admin Support:**
- Django admin already supports observer role selection via existing role filter
- Observers can be created/managed through admin panel

**Access Control:**
- Observer endpoints protected by login requirement and role checking
- API endpoints verify user role before returning data
- Unauthorized observers receive 403 Forbidden response

### Comprehensive Email Notification & Token Management System (2025-12-07)

**Email Notifications:**
- User verification email sent when user is verified (self-registered or admin-approved)
- Verification email includes voting tokens for all active elections user is eligible for
- Election activation emails sent to all eligible voters with their per-level tokens
- 5-minute pre-election start reminder emails to all voters with active tokens
- 30-minute pre-election end reminder emails ONLY to non-voters, showing which levels they haven't voted in
- Post-vote confirmation congratulation emails thanking voter for participation
- Custom notification emails from admin panel to election voters

**Token Management:**
- Voter ID automatically generated when user is created (applies to both self-registered and admin-created users)
- Voting tokens automatically generated when user is verified (via Django signal)
- Tokens created for all eligible election levels based on user's state/course assignment
- Tokens generated when election is activated for all verified eligible voters
- Token eligibility determined by:
  - President level: All verified voters eligible
  - Course level: Only voters assigned to that course
  - State level: Only voters assigned to that state

**Signal Improvements:**
- Refactored `src/core/signals.py`:
  - `capture_old_verification_state` - Tracks old verification status
  - `generate_voter_id_on_create` - Auto-generates voter ID for new users
  - `generate_tokens_on_verification` - Triggers token generation and email when user is verified
  - `notify_on_state_change` - Notifies users of state changes
- Refactored `src/election/signals.py`:
  - `capture_old_election_state` - Tracks old election state
  - `handle_election_activation` - Triggers voter notifications AND scheduled reminders when election is activated

**Task Improvements (src/core/tasks.py):**
- `send_verification_email()` - Enhanced to generate tokens for active elections
- `send_password_reset_email()` - Unchanged
- `send_commissioner_contact_email()` - Unchanged
- Helper `_check_eligibility()` - Determines token eligibility for users

**Task Improvements (src/election/tasks.py):**
- `send_verification_email()` - Redundant (kept in core/tasks.py as primary)
- `notify_voters_of_active_election()` - Generates and sends tokens to all eligible voters
- `schedule_election_reminders()` - NEW: Schedules 5-min and 30-min reminder tasks using Celery ETA
- `send_election_starting_reminder()` - 5-minute pre-start notification
- `send_vote_confirmation_email()` - Congratulation email after successful vote
- `send_non_voters_reminder()` - 30-minute pre-end reminder ONLY for non-voters, grouped by level
- `send_custom_election_notification()` - Custom admin notifications
- Helper `_check_eligibility()` - Consistent eligibility logic

**Error Handling:**
- All Celery tasks have try/except blocks with meaningful logging
- Fallback to synchronous execution if async queueing fails
- Missing emails handled gracefully (user.email checks)
- Non-existent objects handled properly (User, Election, ElectionLevel)

### Code Cleanup & Consolidation (2025-12-07)

**Removed Unused Files:**
- `src/core/views.py` - Deprecated old API views (replaced by `views_ui.py` with Django session auth)
- `src/core/api_views.py` - Unused API viewsets and helpers (not registered in any URL patterns)
- `src/core/api_health.py` - Unused API health check endpoint
- `src/election/views_candidate.py` - Unused candidate API views (not exposed in URLs)
- `src/election/views_voting.py` - Unused election voting API views (not exposed in URLs)
- `src/election/serializers_voting.py` - Unused voting serializers
- `src/election/serializers_candidate.py` - Unused candidate serializers

**Consolidated View Structure:**
- `src/core/` now contains only:
  - `views_ui.py` - All Django session-based UI views (home, login, register, dashboard, profile edit, commissioner dashboard)
  - `views_commissioner.py` - All commissioner-specific JSON API endpoints
  - `serializers.py` - All core serializers (user, login, verification, password reset)
  
- `src/election/` now contains only:
  - `views.py` - Minimal API endpoints for vote submission and results (VoteView, ResultsView)
  - `views_ui.py` - All election UI views (elections list, vote form, results display)
  - `serializers.py` - All election serializers (vote validation, results)

**Profile Editing Enhancement:**
- Profile editing (email/gender) now allowed when:
  - **No elections are active** (unrestricted editing window)
  - **24 hours before an election starts** (pre-election editing window)
- Editing is **blocked** during active elections
- Updated `profile_edit_view()` to detect upcoming elections and display appropriate messages
- Enhanced template with context-aware alerts for all three states

**Bug Fixes:**
- Fixed `election_results` view annotation conflict: renamed `votes=Count('vote')` to `vote_total=Count('votes')` to avoid conflict with `Candidate.votes` related manager

**Documentation Updates:**
- Updated `docs/ARCHITECTURE.md` to reflect clean codebase structure
- Removed references to deprecated files (`api_views.py`, `api_health.py`)
- Updated `TESTING_GUIDE.md` with correct minimal API endpoints


### Documentation Reconciliation (2025-12-07)
- Documentation: Reconciled docs with code

2025-11-21
-----------
- Added Celery task support and configured `django-celery-beat`/`django-celery-results`.
- Implemented JWT-based API authentication using `djangorestframework-simplejwt`.

2025-10-23
-----------
- Initial conversion and sample data seeding (historical entries may exist in repo history).

Notes
-----
- Use this file when creating releases or pull requests that change behavior, migrations, public API endpoints, or deployment requirements.
