#!/usr/bin/env python3
"""Module 12 lab — RustDesk server/client configuration checks, offline."""

import base64

REQUIRED_PORTS = {
    21115: ("tcp",),
    21116: ("tcp", "udp"),
    21117: ("tcp",),
}
WEB_PORTS = {21118: ("tcp",), 21119: ("tcp",)}

OPEN_PORTS = {(21115, "tcp"), (21116, "tcp"), (21116, "udp"), (21117, "tcp")}

VALID_KEY = base64.b64encode(bytes(range(32))).decode()
SHORT_KEY = base64.b64encode(b"too-short").decode()
NOT_B64 = "this-is-not-base64!!"

CONFIGS = {
    "good": {"id_server": "hbbs.example.com", "key": VALID_KEY,
             "relay_server": "", "api_server": ""},
    "missing-key": {"id_server": "hbbs.example.com", "key": "",
                    "relay_server": "", "api_server": ""},
    "pro": {"id_server": "hbbs.example.com", "key": VALID_KEY,
            "relay_server": "hbbr.example.com", "api_server": "https://api.example.com"},
}

SESSIONS = [
    {"name": "ws-001", "same_subnet": True, "relay_available": False},
    {"name": "ws-020", "same_subnet": False, "relay_available": True},
    {"name": "ws-030", "same_subnet": False, "relay_available": False},
]

ORG_SETTINGS = {"id_server": "hbbs.example.com", "relay_server": "hbbr.example.com",
                "key": VALID_KEY, "permanent_password": True}

PLATFORM_PERMISSIONS = {
    "Windows": ["rustdesk-service"],
    "Linux": ["x11-session-or-wayland-portal"],
    "macOS": ["screen-recording", "accessibility"],
}
HOST_PERMISSIONS = {"Windows": ["rustdesk-service"],
                    "Linux": ["x11-session-or-wayland-portal"],
                    "macOS": []}


def exercise_1():
    """Check that every mandatory RustDesk port is open with the right protocol."""
    required = {(port, proto) for port, protos in REQUIRED_PORTS.items() for proto in protos}
    missing = sorted(required - OPEN_PORTS)
    assert missing == [], missing
    optional_open = sorted(p for p in WEB_PORTS if (p, "tcp") in OPEN_PORTS)
    assert optional_open == [], optional_open
    print(f"[OK] exercise_1 — required ports open: {len(required)}/{len(required)}; "
          f"web ports open: {len(optional_open)}")


def exercise_2():
    """Validate a RustDesk public key: base64 that decodes to 32 bytes."""
    def check(key):
        try:
            raw = base64.b64decode(key, validate=True)
        except Exception:
            return "not-base64"
        if len(raw) != 32:
            return "wrong-length"
        return "ok"

    verdicts = [check(VALID_KEY), check(SHORT_KEY), check(NOT_B64)]
    assert verdicts == ["ok", "wrong-length", "not-base64"], verdicts
    print("[OK] exercise_2 — key checks: " + ",".join(verdicts)
          + f"; key_length={len(VALID_KEY)}")


def exercise_3():
    """Report missing mandatory client settings."""
    def missing(config):
        gaps = []
        if not config.get("id_server"):
            gaps.append("id_server")
        if not config.get("key"):
            gaps.append("key")
        return sorted(gaps)

    results = {name: missing(cfg) for name, cfg in CONFIGS.items()}
    assert results["good"] == [] and results["pro"] == [], results
    assert results["missing-key"] == ["key"], results
    print("[OK] exercise_3 — config: good=complete, pro=complete, "
          "missing-key=key; relay_server=optional")


def exercise_4():
    """Decide whether a session connects directly, via relay, or not at all."""
    def route(session):
        if session["same_subnet"]:
            return "direct"
        if session["relay_available"]:
            return "relay"
        return "blocked"

    routes = {s["name"]: route(s) for s in SESSIONS}
    assert routes == {"ws-001": "direct", "ws-020": "relay", "ws-030": "blocked"}, routes
    print("[OK] exercise_4 — routes: " + ", ".join(f"{k}={v}" for k, v in sorted(routes.items())))


def exercise_5():
    """Check that OpenUEM's organization RustDesk settings are complete."""
    required = ("id_server", "relay_server", "key")
    missing = [k for k in required if not ORG_SETTINGS.get(k)]
    assert missing == [], missing
    mode = "random-password-per-session" if ORG_SETTINGS["permanent_password"] else "permanent-password"
    print(f"[OK] exercise_5 — org settings complete: {len(required)}/{len(required)}; "
          f"password_mode={mode}")


def exercise_6():
    """List the OS permissions still missing on the target endpoint."""
    missing = {platform: sorted(set(required) - set(HOST_PERMISSIONS[platform]))
               for platform, required in PLATFORM_PERMISSIONS.items()}
    assert missing["Windows"] == [] and missing["Linux"] == [], missing
    assert missing["macOS"] == ["accessibility", "screen-recording"], missing
    print("[OK] exercise_6 — permissions: Windows=ok, Linux=ok, "
          "macOS=accessibility,screen-recording")


def main():
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    print("[PASS] All 6/6 exercises passed successfully.")


if __name__ == "__main__":
    main()
