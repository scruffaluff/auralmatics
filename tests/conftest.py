"""Resuable testing fixtures for Auralmatics."""


from pathlib import Path
import subprocess
from subprocess import Popen
from typing import Iterator

from playwright.sync_api import Page
import pytest

from tests import util


@pytest.fixture
def app(server: str, page: Page) -> Page:
    """Wait for first run of Streamlit app to execute."""
    page.goto(server)
    # Attached state is necessary, since Streamlit briefly shows a "Please wait"
    # message before loading the "Running" status widget.
    page.wait_for_selector("#auralmatics", state="attached")
    util.wait_for_run(page)
    return page


@pytest.fixture
def server() -> Iterator[str]:
    """Start Streamlit server as a background process."""
    script = str(Path(__file__).parent / "mock_app.py")
    port = util.find_open_port()
    url = f"http://localhost:{port}"

    process = Popen(
        [
            "streamlit",
            "run",
            "--browser.gatherUsageStats",
            "false",
            "--global.showWarningOnDirectExecution",
            "false",
            "--server.port",
            str(port),
            script,
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    util.wait_for_server(url)
    yield url
    process.terminate()
