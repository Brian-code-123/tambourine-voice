import re


def _strip_leading_checklist_like_lines(text: str) -> str:
    """Naive post-processing helper used for mock-based test.

    This function mimics conservative post-processing: remove an initial
    block of checklist-like lines (bullets, numbered steps, or short labeled
    lines) until we reach what looks like the transcription body.
    """
    lines = text.splitlines()
    i = 0
    # skip leading blank lines
    while i < len(lines) and lines[i].strip() == "":
        i += 1

    # Remove leading checklist-like lines
    while i < len(lines):
        line = lines[i].strip()
        if line == "":
            i += 1
            continue
        # bullets or numbered list
        if re.match(r"^(-|\*|\d+\.|\[[ xX]\])\s+", line):
            i += 1
            continue
        # very short label-like lines (e.g., "Checklist:")
        if len(line.split()) <= 4 and line.endswith(":"):
            i += 1
            continue
        # short single-phrase checklist items
        if len(line.split()) <= 6 and any(
            word in line.lower() for word in ("check", "verify", "confirm", "ensure")
        ):
            i += 1
            continue
        break

    return "\n".join(lines[i:]).strip()


def test_mock_llm_output_with_checklist_is_stripped() -> None:
    # Simulated LLM assistant response that incorrectly includes an internal checklist
    llm_output = """
    Checklist:
    - Verify speaker identity
    - Confirm capitalization and punctuation

    Final transcription: This is the cleaned and formatted sentence.
    """

    formatted = _strip_leading_checklist_like_lines(llm_output)

    # The checklist lines should be removed
    assert "Verify speaker identity" not in formatted
    assert "Confirm capitalization" not in formatted

    # The transcription body remains and is preserved
    assert formatted.startswith("Final transcription:"), (
        "Transcription body should remain after stripping checklist"
    )
