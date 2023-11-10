"""Compression page."""


from pathlib import Path

from bokeh import plotting
import numpy
import streamlit

from auralmatics import util


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
            Dynamic range compressors decrease the dynamic range of an audio
            signal.

            Compressor paramaters:

            - _Threshold_ is the minimum amplitude for compression to be
              applied.
            - _Ratio_ is the amount of compression to be applied.
            - _Attack_ is how quickly compression is applied.
            - _Release_ is how quickly compression falls off.
            - _Make gain_ is additional gain applied to the entire signal.
            - _Knee width_ smooths the compression to ensure differentiability
              at the threshold.
            """
        )

        path = Path("data/school_bell.wav")
        rate, samples = util.read_wave(path)
        times = numpy.arange(len(samples), dtype=numpy.uint64) / len(samples)

        plot = plotting.figure(
            title="School Bell",
            x_axis_label="Time (s)",
            y_axis_label="Amplitude",
            output_backend="webgl",
        )
        plot.toolbar.logo = None
        plot.line(
            times,
            samples,
            legend_label="Trend",
            line_width=2,
        )
        util.plot_chart(plot)

        streamlit.audio(samples, format="audio/wav", sample_rate=rate)


if __name__ == "__main__":
    page = Page()
    page.run()
