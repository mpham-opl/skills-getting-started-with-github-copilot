"""
Pytest configuration and fixtures for FastAPI tests.

This module provides fixtures for:
- TestClient initialization
- Fresh in-memory database reset between tests
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient for making requests to the FastAPI app.
    
    Returns:
        TestClient: FastAPI test client for making HTTP requests
    """
    return TestClient(app)


@pytest.fixture
def fresh_data():
    """
    Reset in-memory activities database to initial state before each test.
    
    This ensures test isolation by providing a fresh copy of activities
    for each test function. The original activities are restored after
    the test completes.
    
    Yields:
        None - modifies the global activities dict in-place
    """
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team-based soccer practice and competitive matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training, laps, and water safety",
            "schedule": "Mondays, Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and creative art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["sophia@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Society": {
            "description": "Acting, stagecraft, and theater production",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Advanced math problem solving and competition preparation",
            "schedule": "Tuesdays, 4:30 PM - 6:00 PM",
            "max_participants": 14,
            "participants": ["oliver@mergington.edu", "emma@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and science exploration",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "benjamin@mergington.edu"]
        }
    }
    
    # Clear current activities and repopulate with fresh data
    activities.clear()
    activities.update(original_activities)
    
    # Yield control to test
    yield
    
    # Restore original activities after test completes
    activities.clear()
    activities.update(original_activities)
