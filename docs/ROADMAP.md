# FocusShell roadmap

## 0.1 — Core shell

Goal: turn the validated WebKit spike into a maintainable Linux application.

- [x] Validate Brain.fm in WebKitGTK 6
- [x] Define a playback-provider boundary
- [x] Create the GTK4/Libadwaita application shell
- [x] Use a persistent WebKit profile
- [ ] Verify login survives relaunch in production profile
- [ ] Add safe external-link handling
- [ ] Add load/error UI states
- [ ] Persist window size/state
- [ ] Add desktop launcher metadata and icon
- [ ] Package a first developer build

## 0.2 — Linux media integration

- [ ] MPRIS service
- [ ] play/pause media-key integration where feasible
- [ ] GNOME media controls
- [ ] background/minimize behavior preference
- [ ] compact player mode

## 0.3 — FocusShell experience

- [ ] original FocusShell session-start UI
- [ ] quick session presets
- [ ] recent-session shortcuts
- [ ] keyboard-first navigation
- [ ] global shortcut exploration

## Non-goals for early releases

- Reimplementing Brain.fm audio generation
- Redistributing Brain.fm audio or branded assets
- Depending on undocumented private endpoints as the primary architecture
- Pixel-copying the official Brain.fm desktop application
