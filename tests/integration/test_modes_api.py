import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport
from api.app import app


def _ctx(session):
    ctx = MagicMock()
    ctx.__aenter__ = AsyncMock(return_value=session)
    ctx.__aexit__ = AsyncMock(return_value=False)
    return ctx


@pytest.mark.asyncio
async def test_get_modes_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/v1/modes")

    assert res.status_code == 200
    data = res.json()
    assert "modes" in data
    modes = {m["mode"]: m for m in data["modes"]}
    assert "research" in modes
    assert "study" in modes
    assert "brief" in modes
    assert "deep" in modes
    assert modes["study"]["include_study_guide"] is True
    assert modes["study"]["display_name"] == "Study & Learn"


@pytest.mark.asyncio
async def test_submit_research_with_mode():
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    mock_redis = AsyncMock()
    mock_redis.enqueue_job = AsyncMock()
    mock_redis.aclose = AsyncMock()

    with patch("api.routes.research.get_db_session", side_effect=lambda: _ctx(mock_session)), \
         patch("api.routes.research.create_pool", AsyncMock(return_value=mock_redis)):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.post(
                "/v1/research",
                headers={"Authorization": "Bearer sk-testkey123456"},
                json={"query": "Explain quantum computing", "mode": "study"},
            )

    assert res.status_code == 202
    data = res.json()
    assert data["status"] == "queued"
    assert data["mode"] == "study"
    assert data["query"] == "Explain quantum computing"

    # Check job added to db session had mode="study"
    added_job = mock_session.add.call_args[0][0]
    assert added_job.mode == "study"
