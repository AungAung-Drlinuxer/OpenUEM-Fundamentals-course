# Module 12 — Exercises

Six exercises on RustDesk deployment and connectivity.

```bash
python3 modules/12_rustdesk/lab.py
```

## Exercise 1 — Port check

Mandatory RustDesk server ports are 21115/TCP, 21116/TCP, 21116/UDP and
21117/TCP. The ports currently open are 21115/TCP, 21116/TCP, 21116/UDP and
21117/TCP. Are all mandatory ports open, and are the web client ports open?

## Exercise 2 — Public key validation

Validate three keys. A valid key is base64 that decodes to exactly 32 bytes.

```text
key A: base64 of 32 bytes  (length 44)
key B: base64 of "too-short"
key C: this-is-not-base64!!
```

## Exercise 3 — Client config completeness

A client config requires `id_server` and `key`; `relay_server` and `api_server`
are optional. Which of the three configs is incomplete?

```text
good:        id_server=hbbs.example.com, key=valid, relay=, api=
missing-key: id_server=hbbs.example.com, key=,      relay=, api=
pro:         id_server=hbbs.example.com, key=valid, relay=hbbr.example.com, api=https://api.example.com
```

## Exercise 4 — Connection path

Decide the route for each endpoint: direct, relay or blocked.

```text
ws-001  same_subnet=true   relay_available=false
ws-020  same_subnet=false  relay_available=true
ws-030  same_subnet=false  relay_available=false
```

## Exercise 5 — OpenUEM org settings

The organization's RustDesk settings contain `id_server`, `relay_server` and
`key`, and permanent password is enabled. Is the setting complete, and what is
the password mode?

## Exercise 6 — OS permissions

Required permissions per platform are:

```text
Windows: rustdesk-service
Linux:   x11-session-or-wayland-portal
macOS:   screen-recording, accessibility
```

The host has every Windows and Linux permission but none for macOS. Which
permissions are missing?
