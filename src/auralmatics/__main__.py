"""Command line interface for Auralmatics."""


from pathlib import Path
import sys

from streamlit.web import cli


def main() -> None:
    """Pass command line arguments to Streamlit."""
    script = str(Path(__file__).parent / "app.py")
    sys.argv.insert(1, "run")
    sys.argv.append(script)
    cli.main(prog_name="streamlit")


if __name__ == "__main__":
    main()
