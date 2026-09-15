# FocusShell architecture

FocusShell is organized around a small provider boundary so the native Linux UI is not coupled to Brain.fm implementation details.

## Layers

```text
FocusShellApplication
        |
        v
FocusShellWindow  ----->  PlaybackProvider
                              |
                              v
                       BrainFmWebProvider
                              |
                              v
                  WebKitGTK + Brain.fm web app
```

### Application lifecycle

`app.py` owns process/application lifecycle and composes the concrete provider with the main window.

### Window/UI

`window.py` owns native GTK/Libadwaita presentation. It may call methods defined by `PlaybackProvider`, but it must not reach into WebKit objects directly.

### Playback provider

`providers/base.py` defines the minimum behavior the UI requires. The first implementation, `BrainFmWebProvider`, owns WebKitGTK, persistent browser state, Brain.fm navigation, and provider-specific logging.

## Design rules

1. UI code does not know Brain.fm private endpoints, cookies, or WebKit internals.
2. Provider code does not decide how FocusShell's native window is laid out.
3. New Linux integrations such as MPRIS live outside the provider unless they are inherently backend-specific.
4. The WebKit compatibility spike remains reference material; production features are implemented in `src/` rather than added to the spike.
5. Prefer small interfaces introduced by actual needs rather than speculative abstractions.

## Why this boundary exists

Brain.fm is an external service whose web application can change independently of FocusShell. Keeping that integration behind a provider gives us one place to adapt while preserving the rest of the application. It also leaves room for another supported playback implementation later without rewriting the UI.
