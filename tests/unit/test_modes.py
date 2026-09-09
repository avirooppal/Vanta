import pytest
from unittest.mock import AsyncMock
from core.research.modes import (
     ResearchMode,
    ResearchMode,
    get_mode_config,
    list_available_modes,
    RESEARCH_MODE_CONFIG,
    STUDY_MODE_CONFIG,
    BRIEF_MODE_CONFIG,
    DEEP_MODE_CONFIG,
)
from core.research.state import ResearchState, ValidatedSource
from core.research.agents.search import SearchAgent
from core.research.agents.extractor import ExtractorAgent
from core.research.agents.synthesizer import SynthesizerAgent
from core.research.agents.coordinator import CoordinatorAgent
from core.llm.types import LLMResponse


def test_get_mode_config_defaults_and_resolution():
    # Valid lookups
    assert get_mode_config("research") == RESEARCH_MODE_CONFIG
    assert get_mode_config("study") == STUDY_MODE_CONFIG
    assert get_mode_config("brief") == BRIEF_MODE_CONFIG
    assert get_mode_config("deep") == DEEP_MODE_CONFIG

    # Case insensitivity and whitespace stripping
    assert get_mode_config("  STUDY  ") == STUDY_MODE_CONFIG
    assert get_mode_config("DEEP") == DEEP_MODE_CONFIG

    # None and unknown fallback to standard research
    assert get_mode_config(None) == RESEARCH_MODE_CONFIG
    assert get_mode_config("invalid_mode") == RESEARCH_MODE_CONFIG


def test_list_available_modes():
    modes = list_available_modes()
    assert len(modes) == 4
    mode_names = [m["mode"] for m in modes]
    assert "research" in mode_names
    assert "study" in mode_names
    assert "brief" in mode_names
    assert "deep" in mode_names

    study = next(m for m in modes if m["mode"] == "study")
    assert study["include_study_guide"] is True
    assert "Study Guide" in study["description"] or "Educational" in study["description"]


@pytest.mark.asyncio
async def test_search_agent_mode_guidance():
    mock_llm = AsyncMock()
    mock_llm.complete.return_value = LLMResponse(
        content='["quantum tutorial for beginners", "qubits explained simply"]',
        model="gpt-4o",
        tokens_in=10,
        tokens_out=10,
    )

    agent = SearchAgent(mock_llm)
    state = ResearchState(
        question="How do quantum computers work?",
        max_rounds=2,
        mode="study",
        mode_config=STUDY_MODE_CONFIG,
    )

    queries = await agent.run(state)
    assert len(queries) == 2

    # Verify mode guidance was sent to LLM
    call_args = mock_llm.complete.call_args[0][0]
    user_content = call_args[1].content
    assert "Study & Learn" in user_content
    assert "educational guides" in user_content.lower() or "pedagogical" in user_content.lower()


@pytest.mark.asyncio
async def test_extractor_agent_mode_guidance():
    mock_llm = AsyncMock()
    mock_llm.complete.return_value = LLMResponse(
        content='[{"facts": "Superposition allows qubit to be 0 and 1 simultaneously", "trust_score": 95}]',
        model="gpt-4o",
        tokens_in=10,
        tokens_out=10,
    )

    agent = ExtractorAgent(mock_llm)
    source = ValidatedSource(
        url="https://example.edu/quantum",
        title="Intro to Quantum",
        text="A qubit can exist in superposition of state 0 and 1.",
        trust_score=90,
        flags="None",
    )

    findings = await agent.run(
        source,
        "What is superposition?",
        round_n=1,
        mode_config=STUDY_MODE_CONFIG,
    )
    assert len(findings) == 1
    assert "superposition" in findings[0].facts.lower()

    # Verify extraction focus was passed in prompt
    call_args = mock_llm.complete.call_args[0][0]
    user_content = call_args[1].content
    assert "Mode Extraction Focus:" in user_content
    assert "core definitions" in user_content.lower() or "analogies" in user_content.lower()


@pytest.mark.asyncio
async def test_synthesizer_agent_uses_mode_prompt():
    mock_llm = AsyncMock()
    mock_llm.complete.return_value = LLMResponse(
        content="# Quantum Study Guide\n\n## 1. Overview\nLearning quantum concepts.",
        model="gpt-4o",
        tokens_in=10,
        tokens_out=10,
    )

    agent = SynthesizerAgent(mock_llm)
    state = ResearchState(
        question="What is quantum computing?",
        max_rounds=2,
        mode="study",
        mode_config=STUDY_MODE_CONFIG,
    )

    report = await agent.run(state)
    assert report.query == "What is quantum computing?"

    # Check system prompt used in synthesis
    call_args = mock_llm.complete.call_args[0][0]
    system_content = call_args[0].content
    assert "Master Tutor" in system_content or "Study Guide" in system_content


@pytest.mark.asyncio
async def test_coordinator_agent_includes_mode():
    mock_llm = AsyncMock()
    mock_llm.complete.return_value = LLMResponse(
        content="SYNTHESIZE",
        model="gpt-4o",
        tokens_in=10,
        tokens_out=1,
    )

    agent = CoordinatorAgent(mock_llm)
    state = ResearchState(
        question="Brief on solid state batteries",
        max_rounds=3,
        current_round=1,
        mode="brief",
        mode_config=BRIEF_MODE_CONFIG,
    )
    # Add a mock finding
    from core.research.state import Finding
    state.findings.append(Finding(url="https://b.com", title="B", facts="New battery tech", round_number=1))

    decision = await agent.run(state)
    assert decision == "SYNTHESIZE"

    call_args = mock_llm.complete.call_args[0][0]
    user_content = call_args[1].content
    assert "Executive Brief" in user_content
