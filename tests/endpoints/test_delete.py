import pytest


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_delete_success(self, client):
        """Test successful removal of a participant"""
        email = "michael@mergington.edu"
        
        response = client.delete(
            f"/activities/Chess%20Club/participants/{email}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]

    def test_delete_removes_participant(self, client):
        """Test that delete actually removes the participant"""
        email = "michael@mergington.edu"
        
        # Verify participant exists
        before = client.get("/activities").json()
        assert email in before["Chess Club"]["participants"]
        
        # Delete participant
        client.delete(f"/activities/Chess%20Club/participants/{email}")
        
        # Verify participant is removed
        after = client.get("/activities").json()
        assert email not in after["Chess Club"]["participants"]

    def test_delete_nonexistent_activity_fails(self, client):
        """Test that delete fails for a non-existent activity"""
        response = client.delete(
            "/activities/Fake%20Activity/participants/student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_delete_unregistered_participant_fails(self, client):
        """Test that delete fails for a participant not in the activity"""
        response = client.delete(
            "/activities/Chess%20Club/participants/notregistered@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "not registered" in data["detail"]

    def test_delete_preserves_other_participants(self, client):
        """Test that deleting one participant doesn't affect others"""
        email_to_delete = "michael@mergington.edu"
        email_to_preserve = "daniel@mergington.edu"
        
        # Get original participants
        before = client.get("/activities").json()
        assert email_to_preserve in before["Chess Club"]["participants"]
        
        # Delete one participant
        client.delete(f"/activities/Chess%20Club/participants/{email_to_delete}")
        
        # Verify other participant still there
        after = client.get("/activities").json()
        assert email_to_preserve in after["Chess Club"]["participants"]

    def test_delete_twice_fails_second_time(self, client):
        """Test that deleting the same participant twice fails the second time"""
        email = "michael@mergington.edu"
        
        # First delete should succeed
        response1 = client.delete(
            f"/activities/Chess%20Club/participants/{email}"
        )
        assert response1.status_code == 200
        
        # Second delete should fail
        response2 = client.delete(
            f"/activities/Chess%20Club/participants/{email}"
        )
        assert response2.status_code == 404
        data = response2.json()
        assert "not registered" in data["detail"]

    def test_signup_then_delete(self, client):
        """Test signup followed by delete for the same participant"""
        email = "signup.delete@mergington.edu"
        
        # Signup
        signup_response = client.post(
            f"/activities/Gym%20Class/signup?email={email}"
        )
        assert signup_response.status_code == 200
        
        # Verify participant was added
        after_signup = client.get("/activities").json()
        assert email in after_signup["Gym Class"]["participants"]
        
        # Delete
        delete_response = client.delete(
            f"/activities/Gym%20Class/participants/{email}"
        )
        assert delete_response.status_code == 200
        
        # Verify participant was removed
        after_delete = client.get("/activities").json()
        assert email not in after_delete["Gym Class"]["participants"]
