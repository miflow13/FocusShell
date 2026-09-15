"""Native FocusShell home screen."""

from __future__ import annotations

from collections.abc import Callable

import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gtk  # noqa: E402


class HomeView(Gtk.ScrolledWindow):
    """FocusShell-owned landing page shown before the Brain.fm service view."""

    def __init__(self, on_open_brainfm: Callable[[], None]) -> None:
        super().__init__()
        self._on_open_brainfm = on_open_brainfm

        self.set_hscrollbar_policy(Gtk.PolicyType.NEVER)
        self.set_vexpand(True)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(760)
        clamp.set_margin_top(48)
        clamp.set_margin_bottom(48)
        clamp.set_margin_start(24)
        clamp.set_margin_end(24)

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=28,
        )
        clamp.set_child(content)
        self.set_child(clamp)

        title = Gtk.Label(label="Ready to focus?")
        title.set_halign(Gtk.Align.START)
        title.add_css_class("title-1")
        content.append(title)

        subtitle = Gtk.Label(
            label="Choose what you need, then let FocusShell get out of your way."
        )
        subtitle.set_halign(Gtk.Align.START)
        subtitle.set_wrap(True)
        subtitle.add_css_class("dim-label")
        content.append(subtitle)

        modes_label = Gtk.Label(label="What do you need right now?")
        modes_label.set_halign(Gtk.Align.START)
        modes_label.add_css_class("title-3")
        content.append(modes_label)

        modes = Gtk.ListBox()
        modes.set_selection_mode(Gtk.SelectionMode.NONE)
        modes.add_css_class("boxed-list")
        content.append(modes)

        modes.append(
            self._activity_row(
                "Focus",
                "Open Brain.fm and choose a session for concentration or deep work.",
            )
        )
        modes.append(
            self._activity_row(
                "Relax",
                "Open Brain.fm when you want to slow things down and unwind.",
            )
        )
        modes.append(
            self._activity_row(
                "Sleep",
                "Open Brain.fm when it is time to wind down for the night.",
            )
        )

        service_label = Gtk.Label(label="Brain.fm")
        service_label.set_halign(Gtk.Align.START)
        service_label.add_css_class("title-3")
        content.append(service_label)

        service_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )
        content.append(service_box)

        service_copy = Gtk.Label(
            label=(
                "Playback currently uses Brain.fm's official web experience inside "
                "FocusShell's persistent Linux session."
            )
        )
        service_copy.set_halign(Gtk.Align.START)
        service_copy.set_wrap(True)
        service_copy.add_css_class("dim-label")
        service_box.append(service_copy)

        open_button = Gtk.Button(label="Open Brain.fm")
        open_button.set_halign(Gtk.Align.START)
        open_button.add_css_class("suggested-action")
        open_button.add_css_class("pill")
        open_button.connect("clicked", lambda _button: self._on_open_brainfm())
        service_box.append(open_button)

    def _activity_row(self, title: str, subtitle: str) -> Adw.ActionRow:
        row = Adw.ActionRow(title=title, subtitle=subtitle)
        row.set_activatable(True)

        arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
        row.add_suffix(arrow)
        row.set_activatable_widget(arrow)
        row.connect("activated", lambda _row: self._on_open_brainfm())

        return row
