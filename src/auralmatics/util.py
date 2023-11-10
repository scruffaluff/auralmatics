"""Utility functions."""


from pathlib import Path
from typing import Tuple
import warnings

import bokeh
from bokeh.models import Plot
import numpy
from numpy.typing import NDArray
from scipy.io import wavfile
import streamlit
import streamlit.components.v1 as components


def plot_chart(plot: Plot) -> None:
    """Plot Bokeh chart with Streamlit.

    Separated into a function to support Bokeh versions 2 and 3.
    """
    if bokeh.__version__ < "3":
        streamlit.bokeh_chart(plot, use_container_width=True)
    else:
        components.html(
            bokeh.embed.file_html(plot, "cdn"),
            height=800,
        )


def read_wave(path: Path) -> Tuple[int, NDArray]:
    """Read wave file data into floating point array."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rate, samples = wavfile.read(path)

    if samples.dtype != numpy.float32:
        samples = samples.astype(numpy.float32) / numpy.iinfo(samples.dtype).max
    return rate, samples[:, 0]
