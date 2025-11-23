import pytest


@pytest.mark.asyncio
async def test_delete_nonexistent_answer(client):
    resp = await client.delete("/answers/999999")
    assert resp.status_code in (404, 400)
