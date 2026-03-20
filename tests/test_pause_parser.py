"""Tests for pause tag parsing utilities."""

from pocket_tts.utils.pause_parser import parse_pause_tags


def test_no_pauses():
    segs = parse_pause_tags("Hello world")
    assert len(segs) == 1
    assert segs[0].text == "Hello world"
    assert not segs[0].is_pause


def test_default_pause():
    segs = parse_pause_tags("Hello [pause] world")
    assert len(segs) == 3
    assert segs[1].is_pause
    assert segs[1].duration_seconds == 0.5


def test_seconds():
    segs = parse_pause_tags("Hello [pause:1.5s] world")
    assert segs[1].duration_seconds == 1.5


def test_milliseconds():
    segs = parse_pause_tags("Hello [pause:300ms] world")
    assert abs(segs[1].duration_seconds - 0.3) < 1e-9


def test_bare_number():
    segs = parse_pause_tags("Hello [pause:2] world")
    assert segs[1].duration_seconds == 2.0


def test_multiple_pauses():
    segs = parse_pause_tags("One [pause:1s] two [pause:500ms] three")
    pauses = [s for s in segs if s.is_pause]
    assert len(pauses) == 2
    assert pauses[0].duration_seconds == 1.0
    assert pauses[1].duration_seconds == 0.5


def test_pause_at_start():
    segs = parse_pause_tags("[pause:1s] Hello")
    assert segs[0].is_pause
    assert segs[1].text == "Hello"


def test_pause_at_end():
    segs = parse_pause_tags("Hello [pause:1s]")
    assert segs[0].text == "Hello"
    assert segs[1].is_pause


def test_case_insensitive():
    segs = parse_pause_tags("Hello [PAUSE:1s] world")
    assert segs[1].is_pause
    assert segs[1].duration_seconds == 1.0


def test_empty_string():
    segs = parse_pause_tags("")
    assert segs == []


def test_only_pause():
    segs = parse_pause_tags("[pause:1s]")
    assert len(segs) == 1
    assert segs[0].is_pause
    assert segs[0].duration_seconds == 1.0


def test_consecutive_pauses():
    segs = parse_pause_tags("[pause:1s][pause:2s]")
    assert len(segs) == 2
    assert all(s.is_pause for s in segs)
    assert segs[0].duration_seconds == 1.0
    assert segs[1].duration_seconds == 2.0
