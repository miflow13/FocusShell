"""Main FocusShell application window."""

from __future__ import annotations

import gi

gi.require_version("Adw", "1")

gif = gi.require_version
# Keep GTK version declaration explicit for PyGObject before importing widgets.
gif("Gtk", "4.0")

from gi.repository import Adw  # noqa: E402

from focusshell.config import APP_NAME
from focusshell.providers.base import PlaybackProvider
from focusshell.ui.home_view import HomeView
from focusshell.ui.service_view import ServiceView


class FocusShellWindow(Adw.ApplicationWindow):
    """Compose FocusShell-owned navigation around a playback provider."""

    def __init__(
        self,
        application: Adw.Application,
        provider: PlaybackProvider,
    ) -> None:
        super().__init__(application=application)
        self._provider = provider

        self.set_title(APP_NAME)
        self.set_default_size(1180, 780)

        self._navigation = Adw.NavigationView()

        home_view = HomeView(on_open_brainfm=self._open_brainfm)
        self._home_page = Adw.NavigationPage.new(home_view, APP_NAME)
        self._home_page.set_tag("home")

        service_view = ServiceView(provider)
        self._service_page = Adw.NavigationPage.new(service_view, "Brain.fm")
        self._service_page.set_tag("brainfm")

        # The first statically added page becomes the root page automatically.
        self._navigation.add(self._home_page)
        self._navigation.add(self._service_page)

        self.set_content(self._navigation)

    def _open_brainfm(self) -> None:
        self._provider.start()
        self._navigation.push(self._service_page)
