from fastapi.testclient import TestClient
from pid_intel.api import app
client = TestClient(app)

def test_health():
    assert client.get('/health').json()['status'] == 'ok'

def test_compare_contract():
    response = client.get('/documents/compare?base=rev-a&candidate=rev-b')
    assert response.status_code == 200
    assert response.json()['entity_changes']['removed'] == ['PT-101']
