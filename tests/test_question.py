import pytest


@pytest.mark.asyncio
async def test_list_questions(client):
    await client.post("/questions/", json={"text": "Первый"})
    await client.post("/questions/", json={"text": "Второй"})

    resp = await client.get("/questions/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    texts = [q["text"] for q in data]
    assert "Первый" in texts
    assert "Второй" in texts
