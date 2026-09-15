from urllib.parse import urlparse

from focusshell.config import APP_ID, BRAINFM_URL


def test_application_id_is_namespaced() -> None:
    assert APP_ID.startswith("io.github.miflow13.")


def test_brainfm_url_is_https() -> None:
    parsed = urlparse(BRAINFM_URL)
    assert parsed.scheme == "https"
    assert parsed.hostname == "www.brain.fm"
