from django.test import TestCase
from rest_framework.test import APITestCase
from core.models import Subject,StudySession
from django.urls import reverse
from unittest.mock import patch, Mock

# Create your tests here.

class SubjectTests(APITestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(
            name="Test Name",
            description="Test Description"
        )
        self.subject2 = Subject.objects.create(
            name="Test 2",
            description="Test 2"
        )

    def test_all_subjects(self):
        url = reverse("all-subjects")
        response = self.client.get(url)

        self.assertEqual(response.data[0]["id"], self.subject1.id)
        self.assertEqual(response.data[0]["description"], self.subject1.description)

    def test_all_subjects_post(self):
        payload = {"name":"Success", "description": "Success"}

        url = reverse("all-subjects")
        response = self.client.post(url, payload)

        new_subject = Subject.objects.get(name="Success")
        self.assertIsNotNone(new_subject)
        self.assertEqual(new_subject.description, payload["description"])
    
    def test_third_party_api(self):
        payload = {"name": "matt"}

        url = reverse("third-party-api")
        response = self.client.post(url, payload)

        self.assertEqual(response.data["name"], "matt")

    @patch("drf.views.requests.get")  # IMPORTANT: patch where it's USED
    def test_third_party_api_creates_subject(self, mock_get):
        # Mock third-party API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "count": 22,
            "name": "matt",
            "age": 22,
        }
        mock_get.return_value = mock_response

        url = reverse("third-party-api")  # make sure your URL has this name
        response = self.client.post(url, {"name": "matt"}, format="json")

        assert response.status_code == 200
        assert response.data["name"] == "matt"
        assert response.data["description"] == "count: 22, age: 22"

        # DB assertion
        subject = Subject.objects.get(name="matt")
        assert subject.description == "count: 22, age: 22"

        # Ensure third-party API was called correctly
        mock_get.assert_called_once_with(
            "https://api.agify.io/",
            params={"name": "matt"},
            timeout=10,
        )




class StudySessionTests(APITestCase):
    def setUp(self):
        self.subject=Subject.objects.create(name="Test1",description="Test test")
        self.study_session1 = StudySession.objects.create(
            subject = self.subject,
            datetime = "2026-01-22",
            duration_minutes = 60,
            notes="test test"
        )

    def test_get_session(self):
        ss_id = self.study_session1.id
        url = reverse(f"study-session",kwargs={"numri":ss_id})
        response = self.client.get(url)

        self.assertEqual(response.data["id"],self.study_session1.id)
        #self.assertEqual(response.data["datetime"],self.study_session1.datetime)
        self.assertEqual(response.data["duration_minutes"],self.study_session1.duration_minutes)


    def test_total_time_all_subjects(self):
        # Create second session for the same subject
        StudySession.objects.create(
            subject=self.subject,
            datetime="2026-01-23",
            duration_minutes=45,
            notes="bonus test"
        )
        
        url = reverse("total-time-all-subjects")
        response = self.client.get(url)
<<<<<<< HEAD
        self.assertEqual(response.data[0]["Total Time"],self.study_session1.duration_minutes)
    
    def test_total_time_async(self):
            """StudySession.objects.create(
                subject=self.subject1,
                datetime="2026-01-29",
                duration_minutes=60,
                notes="Whatever"
            )"""
            url = reverse("total-time-all-subjects-async")
            response = self.client.get(url)
            self.assertEqual(response.data["id"],self.study_session1.id)
=======
        
        # Total should be 60 (from setUp) + 45 = 105
        expected_total = 105
        
        # Find the dictionary for our subject
        subject_data = next(item for item in response.data if item["id"] == self.subject.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(subject_data["Total Time"], expected_total)
>>>>>>> bfbf54085d23588c77527eb347b4d9ece4ecbdb5
