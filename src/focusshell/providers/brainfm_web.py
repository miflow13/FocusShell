"""Brain.fm web playback provider."""

from __future__ import annotations

import logging
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("WebKit", "6.0")

from gi.repository import GLib, Gtk, WebKit  # noqa: E402

from focusshell.config import BRAINFM_URL, WEB_PROFILE_NAME
from focusshell.providers.base import PlaybackProvider

logger = logging.getLogger(__name__)


class BrainFmWebProvider(PlaybackProvider):
    """Host Brain.fm in a persistent WebKitGTK profile."""

    def __init__(self) -> None:
        data_dir = Path(GLib.get_user_data_dir()) / "focusshell" / WEB_PROFILE_NAME
        cache_dir = Path(GLib.get_user_cache_dir()) / "focusshell" / WEB_PROFILE_NAME
        data_dir.mkdir(parents=True, exist_ok=True)
        cache_dir.mkdir(parents=True, exist_ok=True)

        self._network_session = WebKit.NetworkSession.new(
            str(data_dir),
            str(cache_dir),
        )
        self._web_view = WebKit.WebView(network_session=self._network_session)
        self._web_view.set_hexpand(True)
        self._web_view.set_vexpand(True)

        self._web_view.connect("load-changed", self._on_load_changed)
        self._web_view.connect("load-failed", self._on_load_failed)

        logger.info("Using persistent WebKit profile at %s", data_dir)

    @property
    def widget(self) -> Gtk.Widget:
        return self._web_view

    def start(self) -> None:
        if self._web_view.get_uri() is None:
            self._web_view.load_uri(BRAINFM_URL)

    def reload(self) -> None:
        self._web_view.reload()

    def _on_load_changed(
        self,
        _view: WebKit.WebView,
        event: WebKit.LoadEvent,
    ) -> None:
        logger.debug("Brain.fm load %s: %s", event.value_nick, self._web_view.get_uri())

    def _on_load_failed(
        self,
        _view: WebKit.WebView,
        event: WebKit.LoadEvent,
        failing_uri: str,
        error: GLib.Error,
    ) -> bool:
        logger.error(
            "Brain.fm load failed during %s: %s — %s",
            event.value_nick,
            failing_uri,
            error.message,
        )
        return False
