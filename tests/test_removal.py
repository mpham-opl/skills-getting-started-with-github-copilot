"""
Tests for the DELETE /activities/{activity_name}/participants endpoint.

Tests verify that participant removal functionality works correctly, including:
- Successfully removing an existing participant
- Handling non-existent activities
- Handling non-existent participants
- Verifying participant is removed from the list
"""

import pytest


class TestRemoval:
    """Test suite for DELETE /activities/{activity_name}/participants endpoint"""

    def test_removal_success(self, client, fresh_data):
        """
        Arrange: Create TestClient and identify existing participant
        Act: DELETE participant from activity
        Assert: Verify 200 status and participant removed from list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Exists in initial data

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_removal_activity_not_found(self, client, fresh_data):
        """
        Arrange: Create TestClient with non-existent activity name
        Act: DELETE from activity that doesn't exist
        Assert: Verify 404 status
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_removal_participant_not_found(self, client, fresh_data):
        """
        Arrange: Create TestClient with valid activity but non-existent participant
        Act: DELETE non-existent participant from activity
        Assert: Verify 404 status with appropriate message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_removal_from_activity_with_multiple_participants(self, client, fresh_data):
        """
        Arrange: Create TestClient and identify activity with multiple participants
        Act: DELETE one participant from activity
        Assert: Verify participant removed but others remain
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        
        # Get initial participants
        activities_response = client.get("/activities")
        activities = activities_response.json()
        initial_participants = activities[activity_name]["participants"].copy()
        other_participants = [e for e in initial_participants if e != email_to_remove]

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200
        
        # Verify the removed participant is gone and others remain
        activities_response = client.get("/activities")
        activities = activities_response.json()
        final_participants = activities[activity_name]["participants"]
        
        assert email_to_remove not in final_participants
        assert all(email in final_participants for email in other_participants)

    def test_removal_reduces_participant_count(self, client, fresh_data):
        """
        Arrange: Create TestClient and get initial participant count
        Act: DELETE a participant
        Assert: Verify participant count decreased by 1
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        # Get initial count
        activities_response = client.get("/activities")
        activities = activities_response.json()
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        
        # Verify count decreased
        activities_response = client.get("/activities")
        activities = activities_response.json()
        final_count = len(activities[activity_name]["participants"])
        
        assert final_count == initial_count - 1

    def test_removal_allows_same_participant_to_rejoin(self, client, fresh_data):
        """
        Arrange: Create TestClient and identify a participant
        Act: Remove participant, then signup again
        Assert: Verify participant can rejoin after removal
        """
        # Arrange
        activity_name = "Soccer Team"
        email = "liam@mergington.edu"

        # Act - remove participant
        removal_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        assert removal_response.status_code == 200

        # Act - signup same participant again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert signup_response.status_code == 200
        
        # Verify participant is back in list
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_removal_idempotent_returns_different_status(self, client, fresh_data):
        """
        Arrange: Create TestClient and remove a participant once
        Act: Attempt to remove same participant again
        Assert: Verify second removal returns 404 (not idempotent)
        """
        # Arrange
        activity_name = "Swimming Club"
        email = "noah@mergington.edu"

        # Act - remove participant first time
        response_first = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Act - attempt to remove same participant again
        response_second = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response_first.status_code == 200
        assert response_second.status_code == 404  # Should fail on second attempt
