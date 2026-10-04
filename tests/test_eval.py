from fastapi.testclient import TestClient
from llmeval.main import app

client = TestClient(app)


def test_pass_and_fail():
    good = client.post("/evaluate", json={"answer": 'The monthly error budget is 43 minutes.', "gold": 'The monthly error budget is 43 minutes.', "context": 'The monthly error budget is 43 minutes of downtime.'}).json()
    assert good["passed"] is True
    bad = client.post("/evaluate", json={"answer": "The cafeteria serves soup.", "gold": 'The monthly error budget is 43 minutes.', "context": 'The monthly error budget is 43 minutes of downtime.'}).json()
    assert bad["passed"] is False
