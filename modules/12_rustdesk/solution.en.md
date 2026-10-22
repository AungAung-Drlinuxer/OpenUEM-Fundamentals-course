# Module 12 — Solutions

Every output below is the real stdout of `python3 modules/12_rustdesk/lab.py`.

## Exercise 1 — Port check

All four mandatory ports are open. The web client ports 21118 and 21119 are
closed, so the browser client cannot be used.

```text
[OK] exercise_1 — required ports open: 4/4; web ports open: 0
```

## Exercise 2 — Public key validation

Key A decodes to 32 bytes and is valid. Key B decodes but has the wrong length.
Key C is not base64 at all.

```text
[OK] exercise_2 — key checks: ok,wrong-length,not-base64; key_length=44
```

## Exercise 3 — Client config completeness

`missing-key` has no key, so the connection cannot be encrypted. A missing
relay or API server is not an error.

```text
[OK] exercise_3 — config: good=complete, pro=complete, missing-key=key; relay_server=optional
```

## Exercise 4 — Connection path

ws-001 is on the same subnet and connects directly. ws-020 cannot connect
directly but a relay exists. ws-030 has no relay, so the session is blocked.

```text
[OK] exercise_4 — routes: ws-001=direct, ws-020=relay, ws-030=blocked
```

## Exercise 5 — OpenUEM org settings

All three fields are present. With permanent password enabled, a fresh random
password is generated for each connection.

```text
[OK] exercise_5 — org settings complete: 3/3; password_mode=random-password-per-session
```

## Exercise 6 — OS permissions

macOS needs both Screen Recording and Accessibility; without them the session
shows no screen.

```text
[OK] exercise_6 — permissions: Windows=ok, Linux=ok, macOS=accessibility,screen-recording
```
