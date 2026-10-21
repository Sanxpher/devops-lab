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

def test_completed_task(client):
    response_post = client.post('tasks', json={"title": "Test PATCH route"})
    task_id = response_post.json['id']
    response_patch = client.patch(f'/tasks/{task_id}/complete')
    assert response_patch.status_code == 200
    response_get = client.get(f'/tasks')
    assert response_get.json[0]['done'] is True
    completed_task = next((task for task in response_get.json if task['id'] == task_id), None)

    assert completed_task is not None
    assert completed_task['done'] is True