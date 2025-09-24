import unittest
import requests
from datetime import datetime, timedelta
import uuid
from django.test import TestCase
from core.models import User, State, Course
from election.models import Election, ElectionLevel, Position, Candidate, VoterToken

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
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
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