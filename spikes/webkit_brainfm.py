#!/usr/bin/env python3
"""FocusShell WebKitGTK compatibility spike.

Purpose: answer one question before we build the real app:
Can Brain.fm reliably load, authenticate, persist its session, and play audio
inside WebKitGTK 6 on Linux?

This file is intentionally standalone and disposable.
"""

from __future__ import annotations

import sys
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("WebKit", "6.0")

from gi.repository import GLib, Gtk, WebKit  # noqa: E402

APP_ID = "io.github.miflow13.FocusShell.WebKitSpike"
BRAINFM_URL = "https://www.brain.fm/"


class SpikeWindow(Gtk.ApplicationWindow):
    def __init__(self, application: Gtk.Application) -> None:
        super().__init__(application=application)
        self.set_title("FocusShell — WebKit spike")
        self.set_default_size(1180, 780)

        data_dir = Path(GLib.get_user_data_dir()) / "focusshell" / "webkit-spike"
        cache_dir = Path(GLib.get_user_cache_dir()) / "focusshell" / "webkit-spike"
        data_dir.mkdir(parents=True, exist_ok=True)
        cache_dir.mkdir(parents=True, exist_ok=True)

        print(f"[spike] data directory:  {data_dir}")
        print(f"[spike] cache directory: {cache_dir}")
        print(
            "[spike] WebKitGTK: "
            f"{WebKit.get_major_version()}."
            f"{WebKit.get_minor_version()}."
            f"{WebKit.get_micro_version()}"
        )

        # WebKitGTK 6 moved persistent networking state to NetworkSession.
        # Reusing these directories between launches lets us test whether
        # Brain.fm authentication/session state survives an app restart.
        self.network_session = WebKit.NetworkSession.new(
            str(data_dir),
            str(cache_dir),
        )
        print(f"[spike] ephemeral session: {self.network_session.is_ephemeral()}")

        self.web_view = WebKit.WebView(network_session=self.network_session)
        self.web_view.set_hexpand(True)
        self.web_view.set_vexpand(True)

        self.web_view.connect("load-changed", self._on_load_changed)
        self.web_view.connect("load-failed", self._on_load_failed)
        self.web_view.connect("notify::uri", self._on_uri_changed)
        self.web_view.connect("notify::title", self._on_title_changed)

        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label="FocusShell WebKit Spike"))

        reload_button = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        reload_button.set_tooltip_text("Reload")
        reload_button.connect("clicked", lambda _button: self.web_view.reload())
        header.pack_end(reload_button)
        self.set_titlebar(header)

        self.set_child(self.web_view)
        self.web_view.load_uri(BRAINFM_URL)

    def _on_load_changed(self, _view: WebKit.WebView, event: WebKit.LoadEvent) -> None:
        print(f"[load] {event.value_nick}: {self.web_view.get_uri()}")

    def _on_load_failed(
        self,
        _view: WebKit.WebView,
        event: WebKit.LoadEvent,
        failing_uri: str,
        error: GLib.Error,
    ) -> bool:
        print(
            f"[error] load failed during {event.value_nick}: "
            f"{failing_uri} — {error.message}",
            file=sys.stderr,
        )
        return False

    def _on_uri_changed(self, _view: WebKit.WebView, _param: object) -> None:
        print(f"[uri] {self.web_view.get_uri()}")

    def _on_title_changed(self, _view: WebKit.WebView, _param: object) -> None:
        title = self.web_view.get_title()
        if title:
            self.set_title(f"{title} — FocusShell spike")


class SpikeApplication(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id=APP_ID)
        self.window: SpikeWindow | None = None

    def do_activate(self) -> None:
        if self.window is None:
            self.window = SpikeWindow(self)
        self.window.present()


def main() -> int:
    app = SpikeApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
