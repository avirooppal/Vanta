import pytest
from unittest.mock import AsyncMock
from core.research.optimizer import (
    heuristic_validate_domain,
    compress_source_text,
    deduplicate_findings,
    compact_system_prompt,
)
from core.research.state import Finding
from core.llm.client import LLMClient
from core.llm.types import LLMConfig, Message, LLMResponse


def test_heuristic_validate_domain():
    # Known authoritative domains
    score, flag = heuristic_validate_domain("https://arxiv.org/abs/2301.00000")
    assert score >= 85
    assert "Authoritative" in flag

    score, flag = heuristic_validate_domain("https://www.stanford.edu/research/paper")
    assert score >= 85
    assert "Authoritative" in flag

    score, flag = heuristic_validate_domain("https://data.cdc.gov/disease/rates")
    assert score >= 85
    assert "Authoritative" in flag

    # Suspicious / spam TLDs
    score, flag = heuristic_validate_domain("https://free-crypto-rewards.click/claim")
    assert score <= 20
    assert "Suspicious" in flag or "Low-Quality" in flag

    # Unknown / neutral domains should defer to LLM (return None)
    assert heuristic_validate_domain("https://random-tech-blog-123.com/article") is None


def test_compress_source_text():
    raw = """
    Accept cookies to continue to our website. All rights reserved. Sign up for our newsletter!
    
    Quantum computing leverages superposition and entanglement to perform complex computations faster than classical computers.
    
    Share on twitter or share on facebook.
    
    Classical computers process information using binary bits representing either 0 or 1.
    """

    compressed = compress_source_text(raw, query="quantum superposition", max_chars=200)

    # Boilerplate removed
    assert "Accept cookies" not in compressed
    assert "Share on twitter" not in compressed
    # Query relevant content retained
    assert "Quantum computing leverages superposition" in compressed
    assert len(compressed) <= 200


def test_deduplicate_findings():
    f1 = Finding(url="https://a.com", title="A", facts="Qubits can exist in a superposition of states zero and one.", round_number=1, trust_score=80)
    # Near identical duplicate
    f2 = Finding(url="https://b.com", title="B", facts="A qubit can exist in a superposition of zero and one states.", round_number=1, trust_score=75)
    # Completely distinct finding
    f3 = Finding(url="https://c.com", title="C", facts="Shor's algorithm allows quantum computers to factor large integers exponentially faster.", round_number=1, trust_score=90)

    deduped = deduplicate_findings([f1, f2, f3], similarity_threshold=0.60)
    assert len(deduped) == 2
    facts_text = " ".join(f.facts for f in deduped)
    assert "Shor's algorithm" in facts_text
    assert "superposition" in facts_text


def test_compact_system_prompt():
    verbose = """
    You are a researcher.
    
    
    Do your best.
    """
    compact = compact_system_prompt(verbose)
    assert "\n\n\n" not in compact
    assert compact == "You are a researcher.\nDo your best."


@pytest.mark.asyncio
async def test_llm_client_cache_avoids_repeated_calls(monkeypatch):
    config = LLMConfig(provider="openai", base_url="https://api.openai.com/v1", api_key="test", model="gpt-4o")
    client = LLMClient(config, enable_cache=True)

    mock_openai = AsyncMock(return_value=LLMResponse(content="Cached response", model="gpt-4o", tokens_in=25, tokens_out=10))
    monkeypatch.setattr("core.llm.client.call_openai", mock_openai)

    messages = [Message(role="user", content="What is 2+2?")]

    # First call - cache miss
    res1 = await client.complete(messages)
    assert res1.content == "Cached response"
    assert mock_openai.call_count == 1
    assert client.total_tokens_in == 25
    assert client.total_tokens_out == 10
    assert client.cache_hits == 0

    # Second call with identical prompt - cache hit
    res2 = await client.complete(messages)
    assert res2.content == "Cached response"
    # Call count should still be 1!
    assert mock_openai.call_count == 1
    assert client.cache_hits == 1
    # Tokens shouldn't increase on cache hit
    assert client.total_tokens_in == 25
    assert client.total_tokens_out == 10
