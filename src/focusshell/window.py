"""Main FocusShell application window."""

from __future__ import annotations

import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gtk  # noqa: E402

from focusshell.config import APP_NAME
from focusshell.providers.base import PlaybackProvider


class FocusShellWindow(Adw.ApplicationWindow):
    """Compose native window chrome around a playback provider."""

    def __init__(
        self,
        application: Adw.Application,
        provider: PlaybackProvider,
    ) -> None:
        super().__init__(application=application)
        self._provider = provider

        self.set_title(APP_NAME)
        self.set_default_size(1180, 780)

        toolbar = Adw.ToolbarView()
        header = Adw.HeaderBar()

        reload_button = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        reload_button.set_tooltip_text("Reload Brain.fm")
        reload_button.connect("clicked", self._on_reload_clicked)
        header.pack_end(reload_button)

        toolbar.add_top_bar(header)
        toolbar.set_content(provider.widget)
        self.set_content(toolbar)

        self._provider.start()

    def _on_reload_clicked(self, _button: Gtk.Button) -> None:
        self._provider.reload()
