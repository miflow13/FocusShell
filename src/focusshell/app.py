"""FocusShell application lifecycle."""

from __future__ import annotations

import logging
import sys

import gi

gi.require_version("Adw", "1")

from gi.repository import Adw, Gio  # noqa: E402

from focusshell.config import APP_ID
from focusshell.providers.brainfm_web import BrainFmWebProvider
from focusshell.window import FocusShellWindow


class FocusShellApplication(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self._window: FocusShellWindow | None = None

    def do_activate(self) -> None:
        if self._window is None:
            provider = BrainFmWebProvider()
            self._window = FocusShellWindow(self, provider)
        self._window.present()


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    app = FocusShellApplication()
    return app.run(argv if argv is not None else sys.argv)
