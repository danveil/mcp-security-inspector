from mcpsec.detectors.base import bounded_context, safe_transformed_text


def test_bounded_context_stays_in_sentence() -> None:
    text = "First sentence is safe. Second sentence contains a signal. Third is separate."
    start = text.index("signal")
    context, offset = bounded_context(text, start, start + len("signal"))
    assert context.strip() == "Second sentence contains a signal"
    assert text[offset : offset + len(context)] == context


def test_transformed_text_escapes_terminal_and_invisible_controls() -> None:
    rendered = safe_transformed_text("visible\x1b\u200b\ntext")
    assert "U+001B" in rendered
    assert "U+200B" in rendered
    assert "\\n" in rendered
    assert "\x1b" not in rendered
