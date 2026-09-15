"""Native container for the embedded Brain.fm service."""

from __future__ import annotations

import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gtk  # noqa: E402

from focusshell.providers.base import PlaybackProvider


class ServiceView(Adw.ToolbarView):
    """Keep service-specific web content behind native FocusShell chrome."""

    def __init__(self, provider: PlaybackProvider) -> None:
        super().__init__()
        self._provider = provider

        header = Adw.HeaderBar()

        reload_button = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        reload_button.set_tooltip_text("Reload Brain.fm")
        reload_button.connect("clicked", self._on_reload_clicked)
        header.pack_end(reload_button)

        self.add_top_bar(header)
        self.set_content(provider.widget)

    def _on_reload_clicked(self, _button: Gtk.Button) -> None:
        self._provider.reload()
