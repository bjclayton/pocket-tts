from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class TextSegment:
    text: str
    is_pause: bool
    duration_seconds: float = 0.0


_PAUSE_RE = re.compile(r"\[pause(?::(\d+(?:\.\d+)?)(ms|s)?)?\]", re.IGNORECASE)


def parse_pause_tags(text: str) -> list[TextSegment]:
    """Split text on pause tags into alternating text/pause segments.

    Supported formats:
        [pause]          -> 500ms default
        [pause:1.5s]     -> 1500ms
        [pause:500ms]    -> 500ms
        [pause:1]        -> 1000ms (bare number = seconds)

    Examples:
        >>> parse_pause_tags("Hello [pause:1s] world")
        [TextSegment("Hello", False), TextSegment("", True, 1.0),
         TextSegment("world", False)]
    """
    segments: list[TextSegment] = []
    last_end = 0

    for match in _PAUSE_RE.finditer(text):
        before = text[last_end : match.start()].strip()
        if before:
            segments.append(TextSegment(text=before, is_pause=False))

        value = match.group(1)
        unit = (match.group(2) or "s").lower()

        if value is None:
            duration = 0.5
        elif unit == "ms":
            duration = float(value) / 1000.0
        else:
            duration = float(value)

        segments.append(TextSegment(text="", is_pause=True, duration_seconds=duration))
        last_end = match.end()

    remaining = text[last_end:].strip()
    if remaining:
        segments.append(TextSegment(text=remaining, is_pause=False))

    return segments
