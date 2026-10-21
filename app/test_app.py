import os

os.environ["TESTING"] = "True"

import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_create_and_list_task(client):
    new_task = {"title": "Learn CI/CD"}
    post_response = client.post('/tasks', json=new_task)
    assert post_response.status_code == 201
    
    get_response = client.get('/tasks')
    assert get_response.status_code == 200
    assert len(get_response.json) >= 1