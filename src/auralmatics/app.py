"""Home page."""


import streamlit


class App:
    """Home page application."""

    def run(self) -> None:
        """Begin main application loop."""
        streamlit.set_page_config(
            initial_sidebar_state="expanded",
            page_title="Auralmatics",
            page_icon=":musical_note:",
        )
        streamlit.title("Auralmatics")

        streamlit.markdown(
            """
            Auralmatics is a personal workspace for exploring audio processing
            mathematics.

            Use the left sidebar to visit pages for each audio processing
            concept.
            """
        )


if __name__ == "__main__":
    app = App()
    app.run()
