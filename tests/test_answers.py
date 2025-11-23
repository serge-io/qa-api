import pytest


@pytest.mark.asyncio
async def test_multiple_answers_from_same_user(client, user_id):
    q = await client.post("/questions/", json={"text": "Q"})
    q_id = q.json()["id"]

    await client.post(f"/questions/{q_id}/answers", json={"user_id": user_id, "text": "A1"})
    await client.post(f"/questions/{q_id}/answers", json={"user_id": user_id, "text": "A2"})

    resp = await client.get(f"/questions/{q_id}")
    assert resp.status_code == 200
    data = resp.json()

    texts = [a["text"] for a in data["answers"]]
    assert "A1" in texts
    assert "A2" in texts
    assert len(data["answers"]) == 2
