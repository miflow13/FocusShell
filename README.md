# FocusShell

FocusShell is an experimental, unofficial Linux desktop shell for Brain.fm.

The goal is not to clone Brain.fm's official desktop application. FocusShell uses the same broad
mental model—choose what you want to do, start a session, keep playback out of your way—but gives
that workflow its own Linux-native interface and integration.

> **Status:** pre-alpha / core-shell development. FocusShell is not affiliated with or endorsed by
> Brain.fm. It does not redistribute Brain.fm audio or bundled service content. A valid Brain.fm
> account/subscription may be required by the service.

## v0.1 direction

- Python 3.12+
- GTK 4 + Libadwaita
- WebKitGTK 6 for the official Brain.fm web experience
- Provider boundary between UI and service integration
- Persistent app/session data managed by the embedded web engine
- Native Linux window, launcher, shortcuts, and lifecycle

Future Linux integration may include MPRIS, media keys, mini-player mode, notifications, and session
presets.

## Why this architecture?

FocusShell owns the desktop experience. Brain.fm owns its service and content. The UI talks to a
small provider interface instead of reaching directly into Brain.fm internals. That keeps the app
maintainable and gives us room to swap implementations without rewriting the UI.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Development

Native dependencies are intentionally not hidden inside pip. On Fedora 44:

```bash
sudo dnf install python3-gobject gtk4 libadwaita webkitgtk6.0
```

Create an editable development environment using the system GI bindings:

```bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -e .
python -m focusshell
```

The production WebKit profile is stored separately from the compatibility spike under the normal
XDG data/cache directories, so validating the real application does not depend on the spike's saved
session.

## Design rule

Use Brain.fm as a product-reference point, not a pixel-reference point. Do not copy proprietary
artwork, audio, branding, icons, layouts, or source code.
