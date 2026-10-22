# Module 05 — အဖြေများ

ဤဖိုင်ရှိ output တိုင်းသည် `lab.py` ကို အမှန်တကယ် run ခြင်း၏ ရလဒ် ဖြစ်သည်။ Run တစ်ကြိမ်နှင့် တစ်ကြိမ် ထပ်တူညီသည်။

```bash
python3 modules/05_agent_deployment/lab.py
```

## Exercise 1 — Silent-install flag line တည်ဆောက်ခြင်း

အဖြေ၏ အဓိကအချက်မှာ flag အစီအစဉ်ကို ပုံသေ သတ်မှတ်ထားခြင်း ဖြစ်သည်။ Dictionary တွင် key အစီအစဉ် ဘယ်လို ဖြစ်နေသည်ကို မူတည်ခြင်း မရှိဘဲ ရလဒ် တူညီရသည်။

```python
def _build_silent_args(params):
    if not params.get("server"):
        raise ValueError("server=<domain:port> is required")
    tenant, site = params.get("tenantid"), params.get("siteid")
    if bool(tenant) != bool(site):
        raise ValueError("tenantid and siteid must be supplied together")
    tokens = ["/VERYSILENT"]
    for name in FLAG_ORDER:
        value = params.get(name)
        if value is not None:
            tokens.append("/%s=%s" % (name, value))
    return " ".join(tokens)
```

`bool(tenant) != bool(site)` ဆိုသည့် နှိုင်းယှဉ်မှုသည် တန်ဖိုး နှစ်ခုထဲမှ တစ်ခုသာ ရှိသည့် အခြေအနေကို ဖမ်းယူသည်။ တန်ဖိုး နှစ်ခုလုံး မရှိပါက ကွက်လပ် မဖြစ်ပါ။

```text
full     : /VERYSILENT /cacert=C:\certs\ca.cer /cert=C:\certs\agent.cer /key=C:\certs\agent.key /sftpcert=C:\certs\sftp.cer /tenantid=1 /siteid=2 /server=nats.openuem.example:4433 /sftp=2022 /vnc=1443
minimal  : /VERYSILENT /server=nats.openuem.example:4433
pairing  : tenantid and siteid must be supplied together
no-server: server=<domain:port> is required
[OK] exercise_1 — silent-install builder orders flags and enforces the tenant/site pair
```

ပထမစာကြောင်းတွင် flag ကိုးခုလုံး ပါဝင်ပြီး အစီအစဉ်မှာ `cacert` မှ `vnc` အထိ ဖြစ်သည်။ ဒုတိယစာကြောင်းတွင် `server` တစ်ခုတည်းသာ ပါဝင်သည်။ တတိယ နှင့် စတုတ္ထစာကြောင်းတို့သည် ငြင်းပယ်ခံရသည့် အခြေအနေ နှစ်ခု၏ အကြောင်းရင်း ဖြစ်သည်။

## Exercise 2 — Platform အလိုက် certificate ဖိုင်စစ်ဆေးခြင်း

`missing` စာရင်းကို `CERTS` ၏ အစီအစဉ်အတိုင်း ဆောက်ခြင်းဖြင့် output သည် တည်ငြိမ်သည်။ `extra` ကို `sorted()` ဖြင့် စီသည်။

```python
present = set(files)
return {
    "platform": platform,
    "dir": AGENT_DIRS[platform],
    "missing": [c for c in CERTS if c not in present],
    "extra": sorted(present - set(CERTS)),
}
```

```text
debian   missing=-                      extra=-            dir=/etc/openuem-agent/certificates
debian   missing=sftp.cer,agent.key     extra=-            dir=/etc/openuem-agent/certificates
rpm      missing=-                      extra=notes.txt    dir=/etc/openuem-agent
windows  missing=agent.cer,agent.key    extra=-            dir=C:\Program Files\OpenUEM Agent
[OK] exercise_2 — certificate check reports the four needed files per platform
```

ပထမတန်းတွင် ဖိုင် လေးခုလုံး ရှိသည်။ ဒုတိယတန်းတွင် `sftp.cer` နှင့် `agent.key` ပျက်ကွက်သည်။ တတိယတန်းတွင် ဖိုင် လေးခုလုံး ရှိပြီး မလိုအပ်သည့် `notes.txt` တစ်ခု ပိုနေသည်။ စတုတ္ထတန်းတွင် Windows endpoint ၏ `agent.cer` နှင့် `agent.key` ပျက်ကွက်သည်။ Debian ၏ folder သည် RPM ၏ folder အောက်တွင် တည်ရှိသည်။

## Exercise 3 — NATS endpoint နှင့် cluster စာရင်း စစ်ဆေးခြင်း

စစ်ဆေးမှုကို အဆင့်လိုက် ပြုလုပ်သည်။ ဗလာ တန်ဖိုး, scheme, comma အလွတ်, port မပါခြင်း, ကိန်းဂဏန်း မဟုတ်ခြင်း, အတိုင်းအတာ ပြင်ပ, host ထပ်ခြင်း ဟူသည့် အဆင့် ခုနစ်ဆင့် ဖြစ်သည်။

```python
host, sep, port = entry.strip().partition(":")
if not sep or not host:
    return (False, "missing port in " + entry.strip())
if not port.isdigit():
    return (False, "non numeric port in " + entry.strip())
```

```text
OK    nats.openuem.example:4433                                  1 server(s)
OK    nats1.openuem.example:4433,nats2.openuem.example:4433      2 server(s)
FAIL  https://nats.openuem.example:4433                          scheme not allowed, use host:port
FAIL  nats.openuem.example                                       missing port in nats.openuem.example
FAIL  nats.openuem.example:0                                     port out of range in nats.openuem.example:0
FAIL  nats.openuem.example:99999                                 port out of range in nats.openuem.example:99999
FAIL  nats.openuem.example:abc                                   non numeric port in nats.openuem.example:abc
FAIL  nats.openuem.example:4433,                                 empty entry in cluster list
FAIL  <empty>                                                    empty value
FAIL  nats.openuem.example:4433,nats.openuem.example:4433        duplicate host in cluster list
[OK] exercise_3 — NATS endpoint and cluster list validation rejects bad ports
```

ပထမတန်း နှစ်တန်းသာ လက်ခံခံရသည်။ ကျန် ရှစ်တန်းသည် ငြင်းပယ်ခံရပြီး တစ်တန်းချင်းစီတွင် အကြောင်းရင်း ကွဲပြားသည်။ `:0` နှင့် `:99999` နှစ်ခုလုံးသည် အတိုင်းအတာ ပြင်ပ ဖြစ်သည်။

## Exercise 4 — Report ကာလ တွက်ချက်ခြင်း

တစ်ရက်လျှင် report အရေအတွက်ကို `1440 // interval` ဖြင့် တွက်သည်။ အချိြသမှုကို မိနစ်မှ `HH:MM` သို့ ပြောင်းသည့် function တစ်ခုဖြင့် ပြုလုပ်သည်။ စက်မှ အချိန်ကို မဖတ်သဖြင့် output သည် တည်ငြိမ်သည်။

```python
def _clock(total_minutes):
    remainder = total_minutes % 1440
    return "%02d:%02d" % (remainder // 60, remainder % 60)
```

```text
interval=60 min  reports/day=24  gap=60 min
interval=30 min  reports/day=48  gap=30 min
interval=15 min  reports/day=96  gap=15 min
profile checks/day=48  per report cycle=2
last=09:10  next report=10:10  next profile check=09:40
now=11:05  lateness=55 min  state=overdue
[OK] exercise_4 — report interval arithmetic derives volume, due time and lateness
```

ပထမတန်း သုံးတန်းသည် ကာလ တစ်ခုစီအတွက် တစ်ရက်လျှင် report အရေအတွက်ကို ပြသည်။ စတုတ္ထတန်းတွင် profile စစ်ဆေးမှု တစ်ရက်လျှင် 48 ကြိမ် နှင့် report တစ်ကြိမ်လျှင် နှစ်ကြိမ် ဖြစ်သည်။ ပဉ္စမတန်းတွင် နောက်ဆုံး report 09:10 မှ မိနစ် 60 ကြာပြီးနောက် 10:10 တွင် နောက် report ရောက်မည် ဖြစ်ပြီး profile စစ်ဆေးမှုကာလ မိနစ် 30 အတွက် 09:40 တွင် ဖြစ်သည်။ ဆဋ္ဌမတန်းတွင် 10:10 မှ 11:05 အထိ 55 မိနစ် နောက်ကျသဖြင့် `overdue` ဖြစ်သည်။

## Exercise 5 — Log စာကြောင်း ခွဲခြားခြင်း

စည်းမျဉ်းစာရင်းကို အစဉ်လိုက် စစ်ပြီး ပထမဆုံး ကိုက်ညီသည့် အုပ်စုကို ယူသည်။ ထို့ကြောင့် စည်းမျဉ်း အစီအစဉ်သည် အဓိပ္ပာယ် သက်ရောက်သည်။

```python
lowered = line.lower()
for keyword, category in LOG_RULES:
    if keyword in lowered:
        return category
return "unclassified"
```

```text
unclassified agent: connecting to nats.openuem.example:4433
certificate  agent: x509: certificate signed by unknown authority
connectivity agent: dial tcp 192.168.1.43:4433: i/o timeout
enrollment   agent: report queued, waiting for admission
sftp         agent: sftp server listening on 2022
vnc          agent: vnc proxy listening on 1443
configuration agent: openuem.ini loaded from /etc/openuem-agent
unclassified agent: rotating log file
count certificate  1
count configuration 1
count connectivity 1
count enrollment   1
count sftp         1
count unclassified 2
count vnc          1
[OK] exercise_5 — log triage maps keywords to certificate, connectivity and service classes
```

ပထမတန်းတွင် NATS လိပ်စာ ပါဝင်သော်လည်း မည်သည့် keyword နှင့်မျှ မကိုက်ညီသဖြင့် `unclassified` ဖြစ်သည်။ နောက်ဆုံးတန်း `rotating log file` သည်လည်း `unclassified` ဖြစ်သည်။ ကျန် ခြောက်တန်းသည် အုပ်စု ခြောက်မျိုးသို့ ခွဲခြားခံရသည်။ အုပ်စု စာရင်းကို အက္ခရာ အစီအစဉ်ဖြင့် စီထားသဖြင့် output တည်ငြိမ်သည်။

## Exercise 6 — Upgrade အန္တရာယ် အဆင့်သတ်မှတ်ခြင်း

အလေးချိန် စာရင်းကို tuple အဖြစ် သတ်မှတ်ထားသဖြင့် အစီအစဉ် ပြောင်းလဲခြင်း မရှိပါ။ ရမှတ် ကို ပေါင်းပြီး အဆင့် သုံးဆင့်ဖြင့် ခွဲခြားသည်။

```python
score = 0
reasons = []
for name, weight in RISK_WEIGHTS:
    value = factors.get(name)
    if not value:
        continue
    score += weight
    reasons.append(...)
level = "high" if score >= 5 else "medium" if score >= 2 else "low"
```

```text
low    score=0  patch bump, clean config           no risk factor
medium score=4  minor bump with two agents offline 2 agent(s) offline; config customised
high   score=5  major bump with customised ini     config customised; major version
high   score=5  expired certificate, no rollback test cert expired; rollback untested
[OK] exercise_6 — upgrade risk classified by certificate, version and config factors
```

ပထမတန်းတွင် အကြောင်းရင်း မရှိသဖြင့် ရမှတ် သုည နှင့် `low` ဖြစ်သည်။ ဒုတိယတန်းတွင် offline agent နှစ်ခု (2) နှင့် ini ပြင်ထားခြင်း (2) ပေါင်း၍ 4 ဖြစ်ပြီး `medium` ဖြစ်သည်။ တတိယ နှင့် စတုတ္ထတန်းတို့သည် 5 ရမှတ်ဖြင့် `high` ဖြစ်သည်။ Certificate သက်တမ်း ကုန်ဆုံးခြင်း တစ်ခုတည်းကပင် အလေးချိန် 4 ရှိသဖြင့် rollback မစမ်းသပ်ထားခြင်းနှင့် တွဲပါက `high` အဆင့်သို့ ရောက်သည်။

## Lab တစ်ခုလုံး၏ output

```text
[PASS] All 6/6 exercises passed successfully.
```

Exercise ခြောက်ခုလုံး အောင်မြင်ပါက ဤစာကြောင်းကို အဆုံးတွင် ပြသည်။ မည်သည့် exercise မဆို ကျရှုံးပါက assertion error ဖြင့် run ရပ်တန့်ပြီး ဤစာကြောင်း မပေါ်ပါ။
