"""Tests for home page."""


from streamlit.testing.v1 import AppTest

from tests import util


def test_home_text() -> None:
    """Home page renders welcome text."""
    app_path = util.repo_path() / "src/auralmatics/app.py"
    app = AppTest.from_file(str(app_path))
    app.run()
    text = app.markdown[0].value
    assert "Auralmatics is a personal workspace" in text
