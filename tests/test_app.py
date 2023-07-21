from fastapi.testclient import TestClient

from app.main import app

test_file = 'tests/test.jpg'

client = TestClient(app)

def test_upload_file():
    with open(test_file, 'rb') as f:
        files = {"file": ('test.jpeg', f, 'multipart/form-data')}
        response = client.post('http://127.0.0.1:8000/images', files=files)
    assert response.status_code == 201


def test_upload_no_file():
    response = client.post('/images/', files=None)
    assert response.status_code == 422

def test_delete_file():
    response = client.delete(f"/frames/qwerty_lol_no_such_file")
    assert response.status_code == 404
