"""Utility functions for tests."""


import logging
import socket
from typing import cast

from playwright.sync_api import Locator, Page
import requests
from requests import Session
from requests.adapters import HTTPAdapter, Retry


def find_open_port() -> int:
    """Find an available open port."""
    sock = socket.socket()
    sock.bind(("", 0))
    return cast(int, sock.getsockname()[1])


def fill_input(element: Locator, selector: str, input: str) -> None:
    """Edit a Streamlit input field."""
    selection = element.locator(selector)
    selection.click()

    field = selection.locator("input")
    field.fill(input)
    field.press("Enter")


def wait_for_run(page: Page) -> None:
    """Wait for Streamlit to finish run."""
    page.wait_for_selector("data-testid-stStatusWidget", state="detached")


def wait_for_server(url: str) -> None:
    """Retry requesting server until it is available."""
    logging.getLogger(
        requests.packages.urllib3.__package__  # type: ignore
    ).setLevel(logging.ERROR)

    with Session() as session:
        retries = Retry(total=4, backoff_factor=1)
        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.get(url)
