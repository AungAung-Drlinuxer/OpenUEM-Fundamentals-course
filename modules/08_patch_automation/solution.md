# Module 08 — အဖြေများ

ဤ အဖြေများတွင် ပြထားသော output သည် `lab.py` ၏ အမှန်တကယ် stdout ဖြစ်သည်။ Fixture များသည် သရုပ်ပြ ဒေတာဖြစ်ပြီး console ၏ တိုင်းတာချက် မဟုတ်ပါ။

## Solution 1 — Pending update စာရင်း ခွဲခြမ်းစိတ်ဖြာခြင်း

Endpoint တစ်ခုစီ၏ စုစုပေါင်းကို severity လေးမျိုး ပေါင်းခြင်းဖြင့် ရသည်။ Fleet စုစုပေါင်းကို ထို ကိန်းများ ပေါင်းခြင်းဖြင့် ရသည်။ အရေးကြီးသည့် အချက်မှာ စာရင်းကိုပြမီ စီရခြင်း ဖြစ်သည်။ `sorted()` ကို tuple အပေါ် သုံးပါက အမည်အလိုက် တည်ငြိမ်စွာ စီသည်။

```python
total = row["critical"] + row["important"] + row["moderate"] + row["low"]
per_endpoint.append((row["endpoint"], total))
per_endpoint.sort()
```

Critical အရေအတွက် အများဆုံး endpoint ကို ရွေးသည့်အခါ အမည်ကို ဒုတိယ key အဖြစ် ထည့်ရသည်။ မဟုတ်ပါက အရေအတွက် တူညီသော endpoint နှစ်ခု၏ အစဉ်သည် ပြောင်းလဲနိုင်သည်။

```python
ranked = sorted(PENDING_UPDATES, key=lambda r: (-r["critical"], r["endpoint"]))
```

ရလဒ် —

```text
  endpoint    pending  critical
  MB-CEO-01         1         0
  SRV-APP-01        8         1
  SRV-DB-01         7         5
  WS-ACC-01        10         2
  WS-ACC-02         5         0
  fleet total pending updates: 31
  by severity: critical=8 important=9 moderate=7 low=7
[OK] exercise_1 — pending-update counts and severity split from the security-view fixture
```

ဖတ်ပုံ — `SRV-DB-01` တွင် pending 7 ခုသာ ရှိသော်လည်း ၎င်းတို့အနက် 5 ခုသည် critical ဖြစ်သည်။ ထို့ကြောင့် ဦးစားပေး စာရင်းတွင် ပထမဆုံး ဖြစ်သည်။ `WS-ACC-01` တွင် pending 10 ခု ရှိသော်လည်း critical 2 ခုသာ ဖြစ်သည်။ ဤ ကွာခြားချက်က "အရေအတွက် အများဆုံး" နှင့် "အန္တရာယ် အများဆုံး" မတူသည်ကို ပြသည်။

## Solution 2 — Maintenance window ရရှိနိုင်မှု တွက်ချက်ခြင်း

Window ကို မိနစ်အဖြစ် ပြောင်းပြီး နှိုင်းယှဉ်ခြင်းသည် အလွယ်ဆုံး နည်းဖြစ်သည်။ သန်းခေါင်ကျော် window တွင် အစနှင့် အဆုံး အစဉ်ပြောင်းသွားသည်။ ထို့ကြောင့် အခြေအနေ နှစ်ခု ခွဲရသည်။

```python
def _in_window(reference, window, offset_minutes):
    local = reference + timedelta(minutes=offset_minutes)
    start, end = _minutes(window["start"]), _minutes(window["end"])
    now_minutes = local.hour * 60 + local.minute
    if start <= end:
        return local.weekday() == window["weekday"] and start <= now_minutes < end
    if local.weekday() == window["weekday"] and now_minutes >= start:
        return True
    next_day = (window["weekday"] + 1) % 7
    return local.weekday() == next_day and now_minutes < end
```

အဓိက အချက်သုံးခု ရှိသည်။ ပထမ၊ local time ကို offset ဖြင့် တွက်သည်။ ဒုတိယ၊ သန်းခေါင်ကျော် window တွင် နောက်တစ်နေ့ကို ဆက်စပ်စစ်သည်။ တတိယ၊ စတင်ချိန်ကို အတွင်းဟု သတ်မှတ်သည်။

ရလဒ် —

```text
  endpoint    local-time    eligible-windows
  MB-CEO-01   Mon 18:30     windows-ring-1
  SRV-DB-01   Tue 00:30     linux-ring-1
  WS-ACC-01   Tue 07:30     (none)
  reference instant: Mon 2026-06-01 23:30 UTC
[OK] exercise_2 — maintenance-window eligibility resolved through UTC offsets
```

ဖတ်ပုံ — `MB-CEO-01` သည် −05:00 offset ရှိသည်။ UTC 23:30 သည် ထို endpoint တွင် 18:30 ဖြစ်သည်။ `windows-ring-1` သည် 18:00 မှ 21:00 အထိ ဖြစ်သောကြောင့် အတွင်းကျသည်။ `SRV-DB-01` သည် +01:00 ဖြစ်ပြီး local time သည် အင်္ဂါနေ့ 00:30 ဖြစ်သည်။ `linux-ring-1` သည် တနင်္လာနေ့ 22:00 မှ အင်္ဂါနေ့ 01:00 အထိ ဆက်သောကြောင့် အတွင်းကျသည်။ `WS-ACC-01` သည် +08:00 ဖြစ်ပြီး 07:30 ဖြစ်သည်။ မည်သည့် window မျှ မကိုက်ညီပါ။

ဤ ရလဒ်က patch wave တစ်ခုကို တစ်ချိန်တည်း မလုပ်နိုင်သည်ကို ပြသည်။ ဌာန တစ်ခုစီ၏ local time ကို ကြည့်ရသည်။

## Solution 3 — Criticality အလိုက် patch wave စီစဉ်ခြင်း

Wave ကို severity မှ တိုက်ရိုက် ဆင်းသက်စေသည်။ Window ကြာချိန်ကို reboot လိုအပ်မှုက ဆုံးဖြတ်သည်။ စီစဉ်မှုတွင် `not p["reboot"]` ကို ဒုတိယ key အဖြစ် ထည့်ခြင်းဖြင့် reboot လိုအပ်သော patch ကို အရင်ရောက်စေသည်။

```python
plan.sort(key=lambda p: (p["wave"], not p["reboot"],
                         _severity_rank(p["severity"]), p["id"]))
```

Wave တစ်ခုအတွက် လိုအပ်သော window သည် ထို wave ရှိ patch များ၏ အကြီးဆုံး ကြာချိန်ဖြစ်သည်။ Patch တစ်ခုချင်းစီအတွက် window မလိုပါ။ Wave တစ်ခုလုံးကို တစ်ကြိမ်တည်း လုပ်ဆောင်သည်။

```python
wave_minutes[item["wave"]] = max(wave_minutes.get(item["wave"], 0),
                                 item["window_minutes"])
```

ရလဒ် —

```text
  wave  patch        severity   reboot  window(min)
  1     KB5034441    critical   yes      90
  1     libssl3      critical   no       30
  2     openssl      important  yes      90
  2     KB5034123    important  no       30
  3     KB5031539    moderate   no       30
  3     firefox-esr  moderate   no       30
  3     curl         low        no       30
  3     tzdata       low        no       30
  wave sizes: wave1=2, wave2=2, wave3=4
[OK] exercise_3 — criticality-driven patch wave plan with reboot-aware windows
```

ဖတ်ပုံ — Wave 1 တွင် `KB5034441` သည် reboot လိုအပ်သောကြောင့် `libssl3` အရင်ရောက်သည်။ Wave 1 ၏ window သည် မိနစ် 90 ဖြစ်သည်။ Wave 3 တွင် patch လေးခု ရှိပြီး reboot မလိုအပ်သောကြောင့် မိနစ် 30 ဖြင့် လုံလောက်သည်။ Wave 3 ကို နောက်ဆုံးထားခြင်းသည် အန္တရာယ် နည်းသော patch များကို စောင့်ဆိုင်းစေသည်။

## Solution 4 — Validation matrix အကဲဖြတ်ခြင်း

စစ်ဆေးချက် တစ်ခုစီကို function အဖြစ် သိမ်းထားခြင်းဖြင့် matrix ကို ဒေတာအဖြစ် ကိုင်တွယ်နိုင်သည်။ ကျရှုံးသော စစ်ဆေးချက် အမည်များကို သိမ်းထားပါက အစီရင်ခံစာ ရေးရန် လွယ်သည်။

```python
VALIDATION_RULES = [
    ("report_fresh", lambda row: row["last_report_minutes"] <= 90, "report within 90 min"),
    ("patch_applied", lambda row: row["pending_after"] == 0, "no pending update left"),
    ("service_healthy", lambda row: row["service"] == "running", "service running"),
    ("disk_headroom", lambda row: row["free_disk_gb"] >= 10, "at least 10 GB free"),
    ("reboot_settled", lambda row: row["uptime_hours"] <= 24, "uptime under 24 h"),
]

failed = [name for name, rule, _ in VALIDATION_RULES if not rule(row)]
```

Rollback အခြေအနေကို စစ်ဆေးချက် တစ်ခုတည်းနှင့် ချိတ်ထားသည်။ Service မတက်ခြင်းသည် အသုံးပြုသူ ခံစားရသော ပျက်စီးမှု ဖြစ်သည်။ Disk နေရာ နည်းခြင်းသည် နောက်မှ ပြင်နိုင်သည်။ ထို့ကြောင့် အတိုင်းအတာ နှစ်မျိုးကို မတူညီစွာ ကိုင်တွယ်သည်။

ရလဒ် —

```text
  endpoint     passed/total  failed-checks
  SRV-APP-01    2/5          disk_headroom,patch_applied,service_healthy
  WS-ACC-01     5/5          (none)
  WS-ACC-02     4/5          report_fresh
  checks passed overall: 11/15
  rollback required: SRV-APP-01
[OK] exercise_4 — validation matrix scored per endpoint with rollback flag
```

ဖတ်ပုံ — `WS-ACC-01` သည် စစ်ဆေးချက် ငါးခုလုံး အောင်မြင်သည်။ `WS-ACC-02` တွင် report သည် မိနစ် 120 ဖြစ်သောကြောင့် `report_fresh` ကျရှုံးသည်။ သို့သော် patch တပ်ဆင်မှု အောင်မြင်သည်။ `SRV-APP-01` တွင် စစ်ဆေးချက် သုံးခု ကျရှုံးသည်။ Service မတက်ခြင်းက rollback အလံကို မြှင့်သည်။

## Solution 5 — Compliance ရာခိုင်နှုန်း တွက်ချက်ခြင်း

အတိုင်းအတာ နှစ်ခုကို ခွဲတွက်ရသည်။ Fleet patch rate သည် patch အရေအတွက် အချိုးဖြစ်သည်။ Endpoint compliance သည် endpoint အရေအတွက် အချိုးဖြစ်သည်။

```python
pct = round(row["installed"] * 100.0 / row["required"], 1)
compliant = pct >= COMPLIANCE_THRESHOLD_PCT and row["critical_pending"] == 0
fleet_pct = round(total_installed * 100.0 / total_required, 1)
endpoint_pct = round(compliant_count * 100.0 / len(rows), 1)
```

`round()` ကို ဆယ်ပုံတစ်ပုံ တိကျမှုဖြင့် သုံးခြင်းသည် အစီရင်ခံစာ တစ်လျှောက် ကိန်းဂဏန်း တူညီစေသည်။ `round()` မပါဘဲ ပြပါက 94.44444 ကဲ့သို့ ကိန်းများ ထွက်လာမည်။

ရလဒ် —

```text
  endpoint     patch-rate  critical-pending  compliant
  SRV-APP-01        83.3%                 2  no
  WS-ACC-02         90.0%                 1  no
  MB-CEO-01        100.0%                 0  yes
  SRV-DB-01        100.0%                 0  yes
  WS-ACC-01        100.0%                 0  yes
  fleet patch rate: 94.4% (68/72)
  endpoint compliance: 60.0% (3/5)
  exceptions: SRV-APP-01,WS-ACC-02
[OK] exercise_5 — compliance percentage with a separate exception list
```

ဖတ်ပုံ — Fleet patch rate သည် 94.4 ရာခိုင်နှုန်း ဖြစ်သော်လည်း endpoint compliance သည် 60.0 ရာခိုင်နှုန်းသာ ဖြစ်သည်။ အဘယ်ကြောင့်ဆိုပါက endpoint ငါးခုအနက် နှစ်ခုတွင် သတ်မှတ်ချက် မပြည့်ပါ။ ဤ ကွာခြားချက်သည် အစီရင်ခံစာ နှစ်မျိုးလုံး လိုအပ်သည်ကို ပြသည်။

## Solution 6 — Automation trigger ရွေးချယ်ခြင်း

Trigger ရွေးချယ်မှုကို စည်းမျဉ်း သုံးခုဖြင့် ရေးသည်။ အစဉ်သည် အရေးကြီးသည်။ တစ်ခုတည်းသော endpoint အတွက် တစ်ကြိမ်တည်း အလုပ်ကို အရင်စစ်ရသည်။ မဟုတ်ပါက desired state ရှိသော အလုပ်များ အားလုံး profile သို့ ရောက်သွားမည်။

```python
def _select_trigger(job):
    if job["scope"] == "single" and job["repeat"] == "one-off":
        return "deployment"
    if job["desired_state"]:
        return "profile"
    return "report"
```

တစ်ရက်လျှင် အကြိမ်ရေကို မိနစ်ဖြင့် စားခြင်းဖြင့် ရသည်။ Profile စစ်ဆေးမှုသည် မိနစ် 30 ဖြစ်သောကြောင့် 48 ကြိမ်၊ report သည် မိနစ် 60 ဖြစ်သောကြောင့် 24 ကြိမ် ဖြစ်သည်။

```python
per_day_profile = 24 * 60 // PROFILE_CHECK_MINUTES
per_day_report = 24 * 60 // REPORT_INTERVAL_MINUTES
```

ရလဒ် —

```text
  trigger     jobs
  deployment  fix-one-endpoint-service,remove-legacy-package
  profile     enforce-baseline-registry,install-critical-updates
  report      collect-patch-state,daily-inventory-sweep
  profile checks per day: 48 (every 30 min)
  agent reports per day: 24 (every 60 min)
[OK] exercise_6 — automation trigger selected per job shape

==============================================================
[PASS] All 6/6 exercises passed successfully.
```

ဖတ်ပုံ — `install-critical-updates` သည် desired state အလုပ်ဖြစ်သောကြောင့် profile သို့ ရောက်သည်။ `fix-one-endpoint-service` သည် endpoint တစ်ခုတည်းအတွက် တစ်ကြိမ်တည်း ဖြစ်သောကြောင့် deployment သို့ ရောက်သည်။ `collect-patch-state` သည် အခြေအနေ စုဆောင်းခြင်းသာ ဖြစ်သောကြောင့် report ကို အားကိုးသည်။ Profile စစ်ဆေးမှုသည် တစ်ရက်လျှင် 48 ကြိမ် ဖြစ်သောကြောင့် ထပ်ခါတလဲလဲ အလုပ်အတွက် ပိုမြန်သော လီဗာ ဖြစ်သည်။
