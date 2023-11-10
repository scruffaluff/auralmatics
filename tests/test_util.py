"""Tests for utility functions."""


from pathlib import Path

from auralmatics import util


def test_read_wave_range() -> None:
    """Samples read from wave file are between -1 and 1."""
    _, samples = util.read_wave(Path("data/school_bell.wav"))

    assert samples.max() <= 1
    assert samples.min() >= -1
