import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status 200"""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary of activities"""
        response = client.get("/activities")
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_contains_activity_data(self, client):
        """Test that returned activities have required fields"""
        response = client.get("/activities")
        data = response.json()
        
        # Check that we have activities
        assert len(data) > 0
        
        # Check structure of an activity
        for activity_name, activity_details in data.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)

    def test_get_activities_participants_are_strings(self, client):
        """Test that participant emails are strings"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_details in data.values():
            for participant in activity_details["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_max_participants_is_positive(self, client):
        """Test that max_participants is a positive number"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_details in data.values():
            assert activity_details["max_participants"] > 0
