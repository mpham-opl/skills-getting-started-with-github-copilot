"""
Tests for the GET /activities endpoint.

Tests verify that the activities list endpoint returns all activities
with the correct structure, including descriptions, schedules, and participants.
"""

import pytest


class TestActivitiesList:
    """Test suite for GET /activities endpoint"""

    def test_get_all_activities(self, client, fresh_data):
        """
        Arrange: Create TestClient
        Act: Send GET request to /activities
        Assert: Verify 9 activities returned with correct structure
        """
        # Arrange
        expected_activity_count = 9

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert isinstance(activities, dict)

    def test_activities_contain_required_fields(self, client, fresh_data):
        """
        Arrange: Create TestClient
        Act: Fetch activities from endpoint
        Assert: Verify each activity has required fields (description, schedule, max_participants, participants)
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing required field '{field}'"

    def test_activities_have_participants_lists(self, client, fresh_data):
        """
        Arrange: Create TestClient
        Act: Fetch activities from endpoint
        Assert: Verify each activity has a participants list (can be empty or populated)
        """
        # Arrange
        # (no explicit setup needed, fresh_data fixture handles initialization)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert all(isinstance(email, str) for email in activity_data["participants"])

    def test_activities_have_valid_max_participants(self, client, fresh_data):
        """
        Arrange: Create TestClient
        Act: Fetch activities from endpoint
        Assert: Verify each activity has max_participants as a positive integer
        """
        # Arrange
        # (fresh_data fixture provides initialized activities)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert "max_participants" in activity_data
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_specific_activities_exist(self, client, fresh_data):
        """
        Arrange: Create TestClient and list of expected activities
        Act: Fetch activities from endpoint
        Assert: Verify that specific known activities are returned
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Swimming Club",
            "Art Club",
            "Drama Society",
            "Math Olympiad",
            "Science Club"
        ]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name in expected_activities:
            assert activity_name in activities, f"Expected activity '{activity_name}' not found"

    def test_activity_descriptions_not_empty(self, client, fresh_data):
        """
        Arrange: Create TestClient
        Act: Fetch activities from endpoint
        Assert: Verify all activities have non-empty description strings
        """
        # Arrange
        # (fresh_data fixture initializes activities)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0
