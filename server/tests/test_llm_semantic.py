import re

from processors.llm import ADVANCED_PROMPT_DEFAULT, DICTIONARY_PROMPT_DEFAULT


def _assert_no_visible_checklist(prompt: str) -> None:
    """Semantic check: assert prompt does not request a visible checklist.

    We avoid exact-string matching and instead look for patterns that imply
    the prompt is asking the model to 'begin' or 'output' a checklist.
    """
    s = prompt.lower()
    patterns = [
        r"\bbegin\b.*\bchecklist\b",
        r"\boutput\b.*\bchecklist\b",
        r"\bchecklist\b.*\boutput\b",
    ]
    for p in patterns:
        assert not re.search(p, s), (
            f"Prompt appears to ask for visible checklist (matched pattern: {p})"
        )


def test_advanced_prompt_does_not_request_visible_checklist_semantic() -> None:
    _assert_no_visible_checklist(ADVANCED_PROMPT_DEFAULT)


def test_dictionary_prompt_does_not_request_visible_checklist_semantic() -> None:
    _assert_no_visible_checklist(DICTIONARY_PROMPT_DEFAULT)
