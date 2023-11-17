"""Modulation page."""


from bokeh import plotting
import numpy
import streamlit

from auralmatics import util


def ring_modulation() -> None:
    """Compression example with a jazz guitar sample input."""
    streamlit.markdown(
        """
        ## Ring Modulation

        Amplitude modulation is a special case of ring modulation.
        """
    )

    rate = 44_100
    length = 4 * rate
    times = numpy.arange(length, dtype=numpy.uint64) / rate

    parameters = streamlit.columns(4)
    amplitude = parameters[0].number_input(
        "Amplitude",
        key="ring_modulation_amplitude",
        min_value=0.0,
        value=0.5,
    )
    frequency = parameters[1].number_input(
        "Frequency",
        key="ring_modulation_frequency",
        min_value=0.0,
        max_value=100.0,
        value=1.0,
    )

    modulator = amplitude * numpy.sin(2 * frequency * numpy.pi * times) + 1
    samples = modulator * 0.5 * numpy.sin(2 * 220 * numpy.pi * times)

    plot = plotting.figure(
        title="Amplitude Modulation",
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
        color="#fdc182",
        line_width=2,
    )
    util.plot_chart(plot)

    streamlit.audio(samples, format="audio/wav", sample_rate=rate)


def frequency_modulation() -> None:
    """Compression example with a linear input."""
    streamlit.markdown(
        """
        ## Frequency Modulation
        """
    )

    rate = 44_100
    length = 4 * rate
    times = numpy.arange(length, dtype=numpy.uint64) / rate

    parameters = streamlit.columns(4)
    amplitude = parameters[0].number_input(
        "Amplitude",
        key="frequency_modulation_amplitude",
        min_value=0.0,
        value=10.0,
    )
    frequency = parameters[1].number_input(
        "Frequency",
        key="frequency_modulation_frequency",
        min_value=0.0,
        value=1.0,
    )

    modulator = amplitude * numpy.sin(2 * frequency * numpy.pi * times) + 221
    samples = numpy.sin(2 * modulator * numpy.pi * times)

    plot = plotting.figure(
        title="Frequency Modulation",
        x_axis_label="Time (s)",
        x_range=(times[0], times[10_000]),
        y_axis_label="Amplitude",
        y_range=(samples.min(), samples.max()),
        output_backend="webgl",
    )
    plot.toolbar.logo = None
    plot.line(
        times,
        samples,
        color="#fdc182",
        line_width=2,
    )
    util.plot_chart(plot)

    streamlit.audio(samples, format="audio/wav", sample_rate=rate)


class Page:
    """Page application."""

    def run(self) -> None:
        """Begin main application loop."""
        streamlit.set_page_config(
            page_title="Auralmatics",
            page_icon=":musical_note:",
        )
        streamlit.title("Modulation")

        ring_modulation()
        frequency_modulation()


if __name__ == "__main__":
    page = Page()
    page.run()
