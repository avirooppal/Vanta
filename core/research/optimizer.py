import re
from urllib.parse import urlparse
from typing import Optional


# High-trust authoritative domains and suffixes
AUTHORITATIVE_DOMAINS = {
    "arxiv.org",
    "nature.com",
    "science.org",
    "sciencedirect.com",
    "nih.gov",
    "cdc.gov",
    "who.int",
    "wikipedia.org",
    "github.com",
    "ieee.org",
    "acm.org",
    "reuters.com",
    "apnews.com",
    "bloomberg.com",
}

AUTHORITATIVE_TLDS = {".edu", ".gov", ".mil", ".ac.uk", ".edu.au"}

# Suspicious / spam TLDs
SUSPICIOUS_TLDS = {".click", ".top", ".buzz", ".rest", ".gq", ".cf", ".tk", ".work", ".fit"}

# Boilerplate patterns to drop
BOILERPLATE_REGEX = re.compile(
    r"(accept cookies|cookie policy|privacy policy|terms of service|all rights reserved|sign up for our newsletter|subscribe now|advertisement|share on (twitter|facebook|linkedin))",
    re.IGNORECASE,
)


def heuristic_validate_domain(url: str) -> Optional[tuple[int, str]]:
    """
    Validate a URL by domain and TLD without invoking an LLM.
    Returns (trust_score, flags) or None if domain requires LLM evaluation.
    """
    if not url:
        return (20, "Empty URL")

    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        if not hostname:
            return (20, "Invalid URL hostname")

        # Check authoritative exact domains
        for domain in AUTHORITATIVE_DOMAINS:
            if hostname == domain or hostname.endswith("." + domain):
                return (90, "Authoritative Domain (heuristic)")

        # Check authoritative TLDs
        for tld in AUTHORITATIVE_TLDS:
            if hostname.endswith(tld):
                return (90, f"Authoritative TLD {tld} (heuristic)")

        # Check suspicious TLDs
        for tld in SUSPICIOUS_TLDS:
            if hostname.endswith(tld):
                return (15, f"Low-Quality / Suspicious TLD {tld} (heuristic)")

    except Exception:
        return None

    return None


def compress_source_text(text: str, query: str = "", max_chars: int = 3500) -> str:
    """
    Extract high-density, query-relevant content from scraped web text.
    Removes boilerplate, duplicate whitespace, and ranks paragraphs by relevance to query.
    """
    if not text:
        return ""

    # Normalize excessive whitespace and empty lines properly
    cleaned = re.sub(r"\r\n|\r", "\n", text)
    cleaned = re.sub(r"[ \t]*\n[ \t]*", "\n", cleaned)
    cleaned = re.sub(r"\n{2,}", "\n\n", cleaned).strip()
    cleaned = re.sub(r"[ \t]+", " ", cleaned)

    if len(cleaned) <= max_chars:
        # Check if entire text is small, but still filter out boilerplate paragraphs
        raw_paragraphs = [p.strip() for p in cleaned.split("\n\n") if len(p.strip()) > 30]
        filtered = [p for p in raw_paragraphs if not BOILERPLATE_REGEX.search(p)]
        if filtered:
            return "\n\n".join(filtered)[:max_chars]
        return cleaned

    # Split into paragraphs
    raw_paragraphs = [p.strip() for p in cleaned.split("\n\n") if len(p.strip()) > 30]

    # Filter out obvious boilerplate paragraphs
    filtered_paragraphs = [p for p in raw_paragraphs if not BOILERPLATE_REGEX.search(p)]
    if not filtered_paragraphs:
        filtered_paragraphs = raw_paragraphs

    # Tokenize query words for scoring
    query_words = set(re.findall(r"\w{3,}", query.lower())) if query else set()

    scored_paragraphs = []
    for idx, p in enumerate(filtered_paragraphs):
        p_lower = p.lower()
        # Score based on query term frequency and structural value
        score = 0
        if query_words:
            matched_words = sum(1 for w in query_words if w in p_lower)
            score += matched_words * 3

        # Prefer earlier paragraphs (lead summary paragraphs) slightly
        score += max(0, 5 - idx)

        scored_paragraphs.append((score, idx, p))

    # Sort by score descending to pick the best paragraphs
    scored_paragraphs.sort(key=lambda x: x[0], reverse=True)

    selected_indices = set()
    total_len = 0

    for _, idx, p in scored_paragraphs:
        if total_len + len(p) + 2 > max_chars:
            continue
        selected_indices.add(idx)
        total_len += len(p) + 2

    # If no paragraphs fit, fallback to direct truncated slice
    if not selected_indices:
        return cleaned[:max_chars]

    # Re-order selected paragraphs back to original flow
    ordered_paragraphs = [filtered_paragraphs[i] for i in sorted(selected_indices)]
    return "\n\n".join(ordered_paragraphs)


def _jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def deduplicate_findings(findings: list, similarity_threshold: float = 0.70) -> list:
    """
    Remove near-identical claims to eliminate context bloat in synthesizer.
    Preserves finding with higher trust score or earlier round.
    """
    if not findings or len(findings) <= 1:
        return findings

    unique_findings = []
    seen_word_sets: list[set[str]] = []

    for f in findings:
        fact_text = f.facts if isinstance(f.facts, str) else str(f.facts)
        words = set(re.findall(r"\w{3,}", fact_text.lower()))

        if not words:
            continue

        is_duplicate = False
        for existing_set in seen_word_sets:
            if _jaccard_similarity(words, existing_set) >= similarity_threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_findings.append(f)
            seen_word_sets.append(words)

    return unique_findings


def compact_system_prompt(prompt: str) -> str:
    """Compact prompt text by removing unnecessary multi-line whitespace and filler."""
    lines = [line.strip() for line in prompt.strip().splitlines() if line.strip()]
    return "\n".join(lines)
