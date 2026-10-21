# Import the app and db objects from our main file
from app import app, db
import pytest

# This fixture sets up a clean testing environment for each test
@pytest.fixture
def client():
    # Configure the app for testing with an in-memory SQLite database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    # Create a test client that can send requests to our Flask app
    with app.test_client() as client:
        with app.app_context():
            db.create_all() # Create tables in the in-memory database
            yield client
            db.drop_all()   # Clean up after the test

def test_health_check(client):
    """Test if the /health endpoint returns a 200 OK status."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_create_and_list_task(client):
    """Test if we can create a task and then list it."""
    # 1. Create a task via POST request
    new_task = {"title": "Learn CI/CD"}
    post_response = client.post('/tasks', json=new_task)
    assert post_response.status_code == 201
    assert post_response.json['title'] == "Learn CI/CD"

    # 2. List tasks via GET request to ensure it was saved
    get_response = client.get('/tasks')
    assert get_response.status_code == 200
    assert len(get_response.json) == 1
    assert get_response.json[0]['title'] == "Learn CI/CD"