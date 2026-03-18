import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant"""
        email = "test.student@mergington.edu"
        
        # Get activities before signup
        before = client.get("/activities").json()
        before_count = len(before["Chess Club"]["participants"])
        
        # Signup
        client.post(f"/activities/Chess%20Club/signup?email={email}")
        
        # Get activities after signup
        after = client.get("/activities").json()
        after_count = len(after["Chess Club"]["participants"])
        
        assert after_count == before_count + 1
        assert email in after["Chess Club"]["participants"]

    def test_signup_duplicate_email_fails(self, client):
        """Test that signing up with an already registered email fails"""
        email = "michael@mergington.edu"  # Already registered for Chess Club
        
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client):
        """Test that signup fails for a non-existent activity"""
        response = client.post(
            "/activities/Fake%20Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_missing_email_parameter(self, client):
        """Test that signup fails when email parameter is missing"""
        response = client.post("/activities/Chess%20Club/signup")
        assert response.status_code == 422  # Unprocessable Entity

    def test_signup_empty_email(self, client):
        """Test signup with empty email (email is optional parameter)"""
        response = client.post("/activities/Chess%20Club/signup?email=")
        # Empty email is accepted by the API (no validation on email format)
        # This is a limitation that could be improved with input validation
        assert response.status_code == 200

    def test_signup_to_different_activities(self, client):
        """Test that a student can signup to multiple different activities"""
        email = "versatile@mergington.edu"
        
        # Signup to Chess Club
        response1 = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Signup to Programming Class
        response2 = client.post(
            f"/activities/Programming%20Class/signup?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify both signups
        activities = client.get("/activities").json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]

    def test_signup_preserves_existing_participants(self, client):
        """Test that signup doesn't remove existing participants"""
        email = "fresh.student@mergington.edu"
        
        # Get original participants
        before = client.get("/activities").json()
        original_participants = before["Gym Class"]["participants"].copy()
        
        # Signup new participant
        client.post(
            f"/activities/Gym%20Class/signup?email={email}"
        )
        
        # Verify original participants still there
        after = client.get("/activities").json()
        for participant in original_participants:
            assert participant in after["Gym Class"]["participants"]
