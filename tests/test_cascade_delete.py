import pytest


@pytest.mark.asyncio
async def test_cascade_delete_question(client, user_id):
    q = await client.post("/questions/", json={"text": "Q"})
    q_id = q.json()["id"]

    a1 = await client.post(f"/questions/{q_id}/answers", json={"user_id": user_id, "text": "A1"})
    a2 = await client.post(f"/questions/{q_id}/answers", json={"user_id": user_id, "text": "A2"})

    a1_id = a1.json()["id"]
    a2_id = a2.json()["id"]

    resp = await client.delete(f"/questions/{q_id}")
    assert resp.status_code in (200, 204)

    r1 = await client.get(f"/answers/{a1_id}")
    r2 = await client.get(f"/answers/{a2_id}")

    assert r1.status_code in (404, 400)
    assert r2.status_code in (404, 400)
