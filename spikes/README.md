# WebKitGTK compatibility spike

This spike exists to reduce technical risk before FocusShell's real UI and architecture are built.

## Question

Can the current Brain.fm web application reliably run inside WebKitGTK 6 on Linux with working authentication, persistent session state, and audio playback?

## Fedora 44 setup

Install the native runtime dependencies:

```bash
sudo dnf install python3-gobject gtk4 webkitgtk6.0
```

Then run the spike directly from the repository root:

```bash
python3 spikes/webkit_brainfm.py
```

WebKitGTK 6 is the GTK 4 API and Fedora ships it as `webkitgtk6.0`.

## Test protocol

Do these in order and record what happens rather than fixing unrelated UI details.

1. Launch the spike and confirm Brain.fm reaches a usable page.
2. Log in normally with your own Brain.fm account.
3. Start a Focus session and confirm audible playback.
4. Change to another available Brain.fm mode/session and confirm playback follows.
5. Minimize the FocusShell window for at least one minute and confirm audio continues.
6. Close FocusShell completely.
7. Launch the same command again and check whether you are still authenticated.
8. Start playback again after relaunch.

## Acceptance criteria

- [ ] Brain.fm loads without a fatal WebKit error
- [ ] Login succeeds
- [ ] Authentication survives a full app restart
- [ ] Audio playback starts from a normal user interaction
- [ ] Audio remains stable while the window is minimized
- [ ] Brain.fm navigation/session switching works
- [ ] Relaunching the app does not corrupt the saved web session
- [ ] Terminal logging is sufficient to identify failed loads/redirects

## Where profile data lives

The spike deliberately uses persistent WebKit data directories:

```text
~/.local/share/focusshell/webkit-spike
~/.cache/focusshell/webkit-spike
```

To repeat the test with a completely fresh Brain.fm session:

```bash
rm -rf ~/.local/share/focusshell/webkit-spike ~/.cache/focusshell/webkit-spike
```

Do not delete those directories between the login and persistence tests.

## What we are *not* testing yet

- FocusShell visual design
- Libadwaita
- MPRIS / media keys
- tray/background behavior
- direct or undocumented Brain.fm APIs
- packaging
- custom player controls

If the spike passes, the next step is to turn the result into a provider-backed application shell rather than continuing to grow this file.
