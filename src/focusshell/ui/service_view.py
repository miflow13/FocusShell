"""Native container for the embedded Brain.fm service."""

from __future__ import annotations

import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gtk  # noqa: E402

from focusshell.providers.base import PlaybackProvider


class ServiceView(Gtk.Box):
    """Keep service-specific web content behind native FocusShell chrome."""

    def __init__(self, provider: PlaybackProvider) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self._provider = provider

        self.set_hexpand(True)
        self.set_vexpand(True)

        toolbar = Adw.ToolbarView()
        toolbar.set_hexpand(True)
        toolbar.set_vexpand(True)

        header = Adw.HeaderBar()

        reload_button = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        reload_button.set_tooltip_text("Reload Brain.fm")
        reload_button.connect("clicked", self._on_reload_clicked)
        header.pack_end(reload_button)

        toolbar.add_top_bar(header)
        toolbar.set_content(provider.widget)
        self.append(toolbar)

    def _on_reload_clicked(self, _button: Gtk.Button) -> None:
        self._provider.reload()
