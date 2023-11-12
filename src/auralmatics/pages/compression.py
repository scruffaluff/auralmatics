"""Compression page."""


import inspect
from pathlib import Path
from typing import cast, Tuple

from bokeh import plotting
import numpy
from numpy.typing import NDArray
import streamlit

from auralmatics import util


def compress(
    signal: NDArray,
    knee_width: float = 0.0,
    make_gain: float = 0.0,
    ratio: float = 4.0,
    threshold: float = 0.8,
) -> NDArray:
    sign = numpy.sign(signal)
    amplitude = numpy.abs(signal)

    for index in range(len(signal)):
        value = amplitude[index] - threshold
        if value > knee_width / 2:
            amplitude[index] = value / ratio + threshold
        elif value > -knee_width / 2:
            smoothing = (value + knee_width / 2) ** 2 / (2 * knee_width)
            amplitude[index] += (1 / ratio - 1) * smoothing

    return cast(NDArray, sign * (amplitude + make_gain))


def example_guitar() -> None:
    """Compression example with a jazz guitar sample input."""
    streamlit.markdown(
        """We can take the following sample of a jazz guitar and apply
        compression."""
    )

    path = Path("data/jazz_guitar.wav")
    rate, samples = util.read_wave(path)

    knee_width, make_gain, ratio, threshold = parameters(
        key_prefix="example_guitar"
    )
    processed = compress(
        numpy.copy(samples),
        knee_width=knee_width,
        make_gain=make_gain,
        ratio=ratio,
        threshold=threshold,
    )

    times = numpy.arange(len(samples), dtype=numpy.uint64) / rate
    plot = plotting.figure(
        title="Jazz Guitar",
        x_axis_label="Time (s)",
        x_range=(times[0], times[-1]),
        y_axis_label="Amplitude",
        y_range=(-1, 1),
        output_backend="webgl",
    )
    plot.toolbar.logo = None
    plot.line(
        times,
        samples,
        color="#60e1e0",
        legend_label="original",
        line_width=2,
    )
    plot.line(
        times,
        processed,
        color="#fdc182",
        legend_label="compressed",
        line_width=2,
    )
    util.plot_chart(plot)

    streamlit.audio(processed, format="audio/wav", sample_rate=rate)


def example_linear() -> None:
    """Compression example with a linear input."""
    streamlit.markdown(
        """
            Let's test out the compression algorithm on linear input.
            """
    )

    knee_width, make_gain, ratio, threshold = parameters(
        key_prefix="example_linear"
    )
    input = numpy.linspace(0, 1, 1_000)
    output = compress(
        numpy.copy(input),
        knee_width=knee_width,
        make_gain=make_gain,
        ratio=ratio,
        threshold=threshold,
    )

    plot = plotting.figure(
        output_backend="webgl",
        title="Compressor",
        x_axis_label="Input",
        x_range=(0, 1),
        y_axis_label="Output",
        y_range=(0, 1),
    )
    plot.toolbar.logo = None
    plot.line(
        input,
        input,
        color="#60e1e0",
        legend_label="original",
        line_width=2,
    )
    plot.line(
        input,
        output,
        legend_label="compressed",
        color="#fdc182",
        line_width=2,
    )
    util.plot_chart(plot)


def loudness(signal: NDArray) -> NDArray:
    """Based on https://en.wikipedia.org/wiki/Decibel#Acoustics."""
    return cast(NDArray, 20 * numpy.log10(signal))


def parameters(key_prefix: str) -> Tuple[float, float, float, float]:
    """Create parameters."""
    parameters = streamlit.columns(4)
    knee_width = parameters[0].number_input(
        "Knee Width",
        key=f"{key_prefix}_knee_width",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
    )
    make_gain = parameters[1].number_input(
        "Make Gain",
        key=f"{key_prefix}_make_gain",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
    )
    ratio = parameters[2].number_input(
        "Ratio",
        key=f"{key_prefix}_ratio",
        min_value=1.0,
        max_value=100.0,
        value=4.0,
    )
    threshold = parameters[3].number_input(
        "Threshold",
        key=f"{key_prefix}_threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
    )
    return knee_width, make_gain, ratio, threshold


class Page:
    """Page application."""

    def run(self) -> None:
        """Begin main application loop."""
        streamlit.set_page_config(
            page_title="Auralmatics",
            page_icon=":musical_note:",
        )
        streamlit.title("Compression")

        streamlit.markdown(
            """
            Dynamic range compressors decrease an audio signal's dynamic range
            by attenuating loud samples and amplifying quiet samples.

            Compressor paramaters:

            - _Threshold_ is the minimum amplitude for compression to be
              applied.
            - _Ratio_ is the amount of compression to be applied.
            - _Attack_ is how quickly compression is applied.
            - _Release_ is how quickly compression falls off.
            - _Make gain_ is additional gain applied to the entire signal.
            - _Knee width_ smooths the compression to ensure differentiability
              at the threshold.

            The compression algorithm for this tutorial is implemented with the
            following code.
            """
        )
        streamlit.code(inspect.getsource(compress))

        example_linear()
        example_guitar()


if __name__ == "__main__":
    page = Page()
    page.run()
