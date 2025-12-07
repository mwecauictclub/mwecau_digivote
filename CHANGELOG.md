# Changelog

All notable changes to this project should be documented in this file.

Formatting: This project follows a simplified Keep a Changelog style.

Unreleased
---------

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
