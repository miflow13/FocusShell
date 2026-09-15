"""Playback provider contract.

The UI depends on this contract, not on WebKitGTK or Brain.fm implementation details.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gi.repository import Gtk


class PlaybackProvider(ABC):
    """Minimal interface the FocusShell window needs from a playback backend."""

    @property
    @abstractmethod
    def widget(self) -> "Gtk.Widget":
        """Return the widget that occupies the application's playback area."""
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        """Initialize or navigate the provider to its starting experience."""
        raise NotImplementedError

    @abstractmethod
    def reload(self) -> None:
        """Reload the provider's current content."""
        raise NotImplementedError
