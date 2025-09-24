
---
### API testing guide for your MWECAU Digital Voting System, covering the flow from Login/Registration through to completing an election, using **Postman** as the API client.

---

### **Prerequisites**

1.  **Backend Running:** Ensure your Django development server is running (`python manage.py runserver`).
2.  **Postman:** Have Postman installed and open.
3.  **User Data:** Know the `registration_number` and password for at least one user (voter) you've registered or plan to register. Also, know the credentials for an admin user.
4.  **Election Data:** Know the IDs of `Election`, `ElectionLevel`, `Position`, and `Candidate` objects you will create or test against. You can find these in the Django Admin interface after creation.
5.  **Media Handling:** Be aware that uploading images (for candidates) requires specific handling in Postman (using `form-data`).

---

### **Postman Setup**

1.  **Create a New Collection:**
    *   Click the "New" button > "Collection".
    *   Name it something like "MWECAU Voting System".
    *   This helps organize your requests.
2.  **Set Base URL Variable (Optional but Helpful):**
    *   Select your new collection.
    *   Go to the "Variables" tab.
    *   Add a variable:
        *   **Variable:** `base_url`
        *   **Initial Value:** `http://localhost:8000`
        *   **Current Value:** `http://localhost:8000`
    *   Click "Save".
    *   Now you can use `{{base_url}}` in your request URLs (e.g., `{{base_url}}/api/auth/login/`).

---

### **Testing Flow**

We'll break this down into logical sections:

#### **1. Authentication & User Management (Core App)**

**A. User Registration Check (`/api/auth/register/`)**

*   **Method:** `POST`
*   **URL:** `{{base_url}}/api/auth/register/`
*   **Headers:**
    *   `Content-Type: application/json`
*   **Body (raw, JSON):**
    ```json
    {
      "registration_number": "T/DEG/2020/0003" // Replace with a valid one
    }
    ```
*   **Expected Response (200 OK):**
    ```json
    {
      "registration_number": "T/DEG/2020/0003",
      "first_name": "Neema",
      "last_name": "John",
      "course": {
        "id": 2,
        "name": "Applied Biology"
      }
    }
    ```
*   **Action:** Note the `course.id` from the response.

**B. Complete User Registration (`/api/auth/complete-registration/`)**

*   **Method:** `POST`
*   **URL:** `{{base_url}}/api/auth/complete-registration/`
*   **Headers:**
    *   `Content-Type: application/json`
*   **Body (raw, JSON):**
    ```json
    {
      "registration_number": "T/DEG/2020/0003", // From step A
      "state": 1,                            // Replace with a valid State ID
      "email": "neema.john@mwecau.ac.tz",    // User's email
      "password": "her_secure_password123",  // User's chosen password
      "course": 2,                          // Course ID from step A's response
      "gender": "female"                    // Optional, if applicable
    }
    ```
*   **Expected Response (201 Created):**
    ```json
    {
      "message": "Registration successful, welcome email sent",
      "user": {
        "registration_number": "T/DEG/2020/0003",
        "full_name": "Neema John",
        "email": "neema.john@mwecau.ac.tz",
        "course": "Applied Biology",
        "state": "Change State",
        "voter_id": "some-uuid-string",
        "gender": "female"
      }
    }
    ```

**C. User Login (`/api/auth/login/`)**

*   **Method:** `POST`
*   **URL:** `{{base_url}}/api/auth/login/` (**Note the trailing slash!**)
*   **Headers:**
    *   `Content-Type: application/json`
*   **Body (raw, JSON):**
    ```json
    {
      "registration_number": "T/DEG/2020/0003", // Registered user's reg number
      "password": "her_secure_password123"      // Registered user's password
    }
    ```
*   **Expected Response (200 OK):**
    ```json
    {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.x.x.x...", // Long string
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.y.y.y..."  // Long string
    }
    ```
*   **Action:** **Crucial!** Copy the `access` token value. You'll need this for all subsequent authenticated requests.

**D. Set Access Token for Future Requests (Using Auth Tab)**

*   To avoid manually adding the token each time:
    *   In any subsequent request, go to the **"Authorization"** tab.
    *   Select **"Type"** as **"Bearer Token"**.
    *   Paste the `access` token you copied into the **"Token"** field.
    *   This will automatically add the `Authorization: Bearer <your_token>` header to the request.

---

#### **2. Election Management (Election App - Admin Actions)**

These actions require an **admin user's access token**. Perform steps C (Login) and D (Set Token) above using admin credentials first.

**A. Create Election Levels (via Django Admin - Recommended)**

*   It's often easier to create `ElectionLevel` objects (President, Course Leader for Bio, State Leader for Change State) via the Django Admin interface first. Note down their IDs.

**B. Create Election (`/api/election/create/`)**

*   **Method:** `POST`
*   **URL:** `{{base_url}}/api/election/create/`
*   **Authorization:** Bearer Token (Admin's access token)
*   **Headers:**
    *   `Content-Type: application/json`
*   **Body (raw, JSON):**
    ```json
    {
      "title": "General Elections 2025",
      "description": "Annual student elections",
      "start_date": "2025-09-10T08:00:00Z", // ISO 8601 format, UTC
      "end_date": "2025-09-20T17:00:00Z",
      "is_active": false, // Can be activated later
      "has_ended": false,
      "levels": [1, 2, 3] // List of ElectionLevel IDs created earlier
    }
    ```
*   **Expected Response (201 Created):** The created election data, including the new `id`.
*   **Action:** Note the `id` of the created election from the response.

**C. Create Positions (`/api/election/position/create/`)**

*   **Method:** `POST`
*   **URL:** `{{base_url}}/api/election/position/create/`
*   **Authorization:** Bearer Token (Admin's access token)
*   **Headers:**
    *   `Content-Type: application/json`
*   **Body (raw, JSON):**
    ```json
    {
      "title": "President",
      "election_level": 1, // ID of the President ElectionLevel
      "description": "University President",
      "gender_restriction": "any"
    }
    ```
    (Repeat for other positions like Course Leader, State Leader, using their respective `election_level` IDs).
*   **Expected Response (201 Created):** Details of the created position.

**D. Create Candidates (`/api/election/candidate/create/`)**

*   **Method:** `POST`
*   **URL:** `{{base_url}}/api/election/candidate/create/`
*   **Authorization:** Bearer Token (Admin's access token)
*   **Headers:**
    *   `Content-Type: multipart/form-data` (**Important for file uploads**)
*   **Body (form-data):**
    *   **Key:** `user` **Value:** `<user_id>` (ID of the User who is the candidate)
    *   **Key:** `election` **Value:** `<election_id>` (ID from step B)
    *   **Key:** `position` **Value:** `<position_id>` (ID from step C)
    *   **Key:** `bio` **Value:** "Candidate's biography..."
    *   **Key:** `platform` **Value:** "Key campaign points..."
    *   **Key:** `image` **Value:** *(Select "File" type from dropdown, then choose an image file from your computer)*
*   **Expected Response (201 Created):** Details of the created candidate, including the image URL.

**E. Activate Election (via Django Admin or API Update)**

*   Use the Django Admin panel to find the created election and check the `is_active` box, or use the `PATCH` endpoint `/api/election/update/<election_id>/` with admin token:
    *   **Method:** `PATCH`
    *   **URL:** `{{base_url}}/api/election/update/<election_id>/`
    *   **Authorization:** Bearer Token (Admin's access token)
    *   **Headers:**
        *   `Content-Type: application/json`
    *   **Body (raw, JSON):**
        ```json
        {
          "is_active": true
        }
        ```
    *   **Expected Response (200 OK):** Updated election data.

---

#### **3. Voting Process (Election App - Voter Actions)**

Switch back to using the **voter's access token** set in Postman's Authorization tab.

**A. View Available Elections (`/api/election/list/`)**

*   **Method:** `GET`
*   **URL:** `{{base_url}}/api/election/list/`
*   **Authorization:** Bearer Token (Voter's access token)
*   **Expected Response (200 OK):** A list of active elections.

**B. View Election Details & Positions (`/api/election/detail/<election_id>/`)**

*   **Method:** `GET`
*   **URL:** `{{base_url}}/api/election/detail/<election_id>/` (Replace `<election_id>` with the ID from election creation)
*   **Authorization:** Bearer Token (Voter's access token)
*   **Expected Response (200 OK):** Detailed information about the election, including the positions the user is eligible for, the candidates running for those positions, and whether the user has voted in each position.

**C. Cast Vote (`/api/election/vote/`)**

*   **Method:** `POST`
*   **URL:** `{{base_url}}/api/election/vote/`
*   **Authorization:** Bearer Token (Voter's access token)
*   **Headers:**
    *   `Content-Type: application/json`
*   **Body (raw, JSON):**
    ```json
    {
      "token": "uuid-string-of-the-voter-token", // Get this from the user's email or potentially from a future endpoint that lists their tokens
      "candidate_id": 5 // ID of the candidate the user wants to vote for
    }
    ```
    *   **Finding the Token:** The `VoterToken` UUID is sent to the user via email after registration or election activation. You would typically get this from the user's email client. For testing, you can find it in the Django Admin under the `VoterToken` model, filtering by `user` and `election`.
    *   **Finding the Candidate ID:** Get this from the response of step B (`/api/election/detail/<election_id>/`) or from the Django Admin.
*   **Expected Response (201 Created):**
    ```json
    {
      "message": "Vote successfully cast."
    }
    ```

---

#### **4. Viewing Results (Election App)**

This action typically requires an **admin/commissioner access token** or might be public *after* the election ends (`has_ended=True`). Use the appropriate token.

**A. View Election Results (`/api/election/results/<election_id>/`)**

*   **Method:** `GET`
*   **URL:** `{{base_url}}/api/election/results/<election_id>/` (Replace `<election_id>` with the ID from election creation)
*   **Authorization:** Bearer Token (Admin/Commissioner's access token, or potentially no auth if election ended)
*   **Expected Response (200 OK):** Aggregated results, showing vote counts and percentages for candidates in each position/level.
    ```json
    [
      {
        "position_id": 1,
        "position_title": "President",
        "total_votes_cast": 1,
        "candidates": [
          {
            "candidate_id": 5,
            "candidate_name": "John Doe",
            "candidate_image_url": "http://localhost:8000/media/candidate_images/...",
            "vote_count": 1,
            "vote_percentage": 100.0
          }
        ]
      }
      // ... results for other positions/levels
    ]
    ```

---

### **Techniques Involved in Using Postman**

1.  **Collections:** Group related requests for better organization.
2.  **Environment Variables:** Store base URLs, tokens, or IDs to avoid hardcoding and make requests reusable. (We used Collection Variables, Environment Variables are similar but global).
3.  **Authorization Tab:** Easily manage authentication (Bearer Tokens, API Keys) without manually adding headers.
4.  **Different Body Types:**
    *   `raw` + `JSON`: For standard API data payloads.
    *   `form-data`: Essential for file uploads (like candidate images) or when the API expects non-JSON encoded data.
5.  **Inspecting Responses:** View status codes (200, 201, 400, 401, 403, 404, 500), response headers, and the JSON body to understand success or failure.
6.  **Capturing Data:** While Postman doesn't automatically chain requests like code, you manually copy IDs or tokens from one response to use in another request's URL, body, or headers.
7.  **Testing Different Scenarios:** Easily test with valid data, invalid data (wrong password, expired token, non-existent IDs), and edge cases (voting twice, voting outside election dates - if logic is implemented) by changing the request body or parameters.

This guide provides a structured approach to testing your backend API endpoints using Postman, covering the main user journeys from registration to voting and results.




import unittest
import requests
from datetime import datetime, timedelta
import uuid
from django.test import TestCase
from core.models import User, State, Course
from election.models import Election, ElectionLevel, Position, Candidate, VoterToken
from django.utils import timezone

class MWECAUTestCase(TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000/api/"
        self.state = State.objects.create(name="Kilimanjaro")
        self.course = Course.objects.create(name="Computer Science", code="CS100")
        self.user = User.objects.create(
            registration_number="T/DEG/2020/0003",
            email="neema@mail.com",
            is_verified=True,
            voter_id=str(uuid.uuid4()),
            course=self.course,
            state=self.state
        )
        self.user.set_password("user123")
        self.user.save()
        self.admin = User.objects.create(
            registration_number="T/DEG/2020/0001",
            email="admin@mail.com",
            is_verified=True,
            is_staff=True,
            is_superuser=True,
            voter_id=str(uuid.uuid4())
        )
        self.admin.set_password("admin123")
        self.admin.save()
        self.level_president = ElectionLevel.objects.create(code="president", name="President")
        self.level_course = ElectionLevel.objects.create(code="course", name="Course Leader")
        self.level_state = ElectionLevel.objects.create(code="state", name="State Leader")
        self.election = Election.objects.create(
            title="2025 General Election",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            is_active=True
        )
        self.election.levels.add(self.level_president, self.level_course, self.level_state)
        self.position = Position.objects.create(
            title="President",
            election_level=self.level_president
        )
        self.candidate = Candidate.objects.create(
            user=self.user,
            election=self.election,
            position=self.position
        )
        self.voter_token = VoterToken.objects.create(
            user=self.user,
            election=self.election,
            election_level=self.level_president,
            token=uuid.uuid4(),
            expiry_date=self.election.end_date
        )
        self.user_token = self.get_jwt(self.user.registration_number, "user123")
        self.admin_token = self.get_jwt(self.admin.registration_number, "admin123")

    def get_jwt(self, reg_number, password):
        response = requests.post(f"{self.base_url}core/auth/login/", json={
            "registration_number": reg_number,
            "password": password
        })
        return response.json().get("access") if response.ok else None

    def test_register(self):
        response = requests.post(f"{self.base_url}core/auth/register/", json={
            "registration_number": "T/DEG/2020/0004",
            "email": "test@mail.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = requests.post(f"{self.base_url}core/auth/login/", json={
            "registration_number": self.user.registration_number,
            "password": "user123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())

    def test_create_election(self):
        data = {
            "title": "2026 General Election",
            "description": "Next election",
            "start_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "end_date": (datetime.now() + timedelta(days=2)).isoformat(),
            "levels": [self.level_president.id, self.level_course.id, self.level_state.id]
        }
        response = requests.post(f"{self.base_url}election/create/", json=data, headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 201)

    def test_list_elections(self):
        response = requests.get(f"{self.base_url}election/list/", headers={"Authorization": f"Bearer {self.user_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_vote(self):
        data = {
            "election_id": self.election.id,
            "level_id": self.level_president.id,
            "candidate_id": self.candidate.id,
            "token": str(self.voter_token.token)
        }
        response = requests.post(f"{self.base_url}election/vote/", json=data, headers={"Authorization": f"Bearer {self.user_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "Vote recorded")

    def test_results(self):
        self.election.has_ended = True
        self.election.save()
        response = requests.get(f"{self.base_url}election/results/{self.election.id}/", headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_unauthorized_access(self):
        response = requests.post(f"{self.base_url}election/create/", json={}, headers={"Authorization": f"Bearer {self.user_token}"})
        self.assertEqual(response.status_code, 403)

if __name__ == "__main__":
    unittest.main()