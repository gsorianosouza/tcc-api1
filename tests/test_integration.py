from faker import Faker

fake = Faker()

def test_predict_endpoint(client):
    payload = {"url": fake.url()}
    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data