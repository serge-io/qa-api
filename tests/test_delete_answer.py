import pytest


@pytest.mark.asyncio
async def test_delete_single_answer(client, user_id):
    q = await client.post("/questions/", json={"text": "Q"})
    q_id = q.json()["id"]

    a = await client.post(f"/questions/{q_id}/answers", json={"user_id": user_id, "text": "AAA"})
    a_id = a.json()["id"]

    # удаляем ответ
    resp = await client.delete(f"/answers/{a_id}")
    assert resp.status_code in (200, 204)

    # убеждаемся, что его нет
    resp = await client.get(f"/answers/{a_id}")
    assert resp.status_code in (404, 400)
