# Module 09 — ဖြေရှင်းချက်

ဤ ဖိုင်၏ output အားလုံးသည် `lab.py` ကို တကယ် မောင်းနှင်သည့် အခါ
ရရှိသည့် stdout အတိအကျ ဖြစ်သည်။ fixture ဒေတာများသည် သရုပ်ပြ အတွက်
ဖြစ်ပြီး တကယ့် fleet မှ တိုင်းတာသည့် ကိန်းဂဏန်း မ ဟုတ်ပါ။

```bash
python3 modules/09_reporting_troubleshooting/lab.py
```

## Exercise 1 — Report အတန်း စစ်ထုတ်ခြင်း

### ချဉ်းကပ်ပုံ

filter တစ်ခုစီကို dictionary အဖြစ် သတ်မှတ်ပြီး ထို dictionary ကို
view function သို့ ပေးသည်။ ထို နည်းဖြင့် filter သတ်မှတ်ချက် နှင့်
ရလဒ် အတန်းများ တွဲဖက် နေသည် — ဖိုင် အမည်တွင် filter ကို
ရေးထည့်နိုင်သည့် အခြေခံ ဖြစ်သည်။

- `agents` — site နှင့် state ကို တိုက်ဆိုင်စစ်သည်။
- `computers` — platform ကို tuple ဖြင့် စစ်ပြီး `Waiting for admission`
  state ကို ဖယ်ထုတ်သည်။ ထို agent များသည် report ပို့သော်လည်း
  စီမံခန့်ခွဲနိုင်သည့် အခြေအနေ မ ရောက်သေးသဖြင့် chart များတွင်
  မ ပါဝင်ပါ။
- `security` — antivirus တန်ဖိုးကို တိုက်ရိုက် နှိုင်းယှဉ်သည်။
- `software` — install count ကို အနည်းဆုံး တန်ဖိုးဖြင့် စစ်သည်။

အတန်း အားလုံးကို အမည် အလိုက် စီပြီးမှ print သည်။ ထို ကြောင့် output
သည် တူညီသည့် filter အတွက် တစ်သမတ်တည်း ဖြစ်သည်။

### Output

```text
[report] agents    filter=site:yangon,state:Enabled      rows=3/6 -> lnx-003, lnx-006, ws-001
[report] computers filter=platform:windows|linux,max_hours:24 rows=2/6 -> lnx-003, ws-001
[report] security  filter=antivirus:disabled             rows=1/6 -> ws-002
[report] software  filter=min_installs:3                 rows=3/4 -> 7-Zip, Firefox, VLC
```

### ရလဒ် ဖတ်ခြင်း

- `rows=3/6` — agent ခြောက်ခုအနက် သုံးခု ကျန်သည်။ `lnx-006` သည်
  နာရီ ၈၀ မ report သေးသော်လည်း state `Enabled` ဖြစ်သဖြင့်
  agents view တွင် ပါဝင်သည်။ agents view သည် လက်ရှိ state ကို
  ပြသည်၊ report လတ်ဆတ်မှုကို မ စစ်ပါ။
- `rows=2/6` — computers view တွင် `ws-005` မ ပါဝင်ခြင်းသည်
  `Waiting for admission` ဖယ်ထုတ်မှု၏ ရလဒ် ဖြစ်သည်။
- `rows=1/6` — antivirus disabled ဖြစ်သည့် စက် တစ်လုံးသာ ရှိသည်။
- `rows=3/4` — install count ၃ နှင့် အထက် software သုံးခု ကျန်သည်။

## Exercise 2 — Dashboard alert ဦးစားပေး သတ်မှတ်ခြင်း

### ချဉ်းကပ်ပုံ

စီရန် key ကို tuple သုံးခုဖြင့် တည်ဆောက်သည် — severity အလေးချိန်
(အငယ်က ရှေ့)၊ count ၏ အနုတ်လက္ခဏာ (အများက ရှေ့)၊ နှင့် အမည်
(က္ခရာ အစဉ်)။ ဤ tuple သုံးခုက ဦးစားပေး အစဉ်ကို တိတိကျကျ
သတ်မှတ်သည်။ Green နှင့် blue ကဏ္ဍများကို alert စာရင်းထဲ
မ ထည့်ပါ — ထို ကဏ္ဍများသည် ကိန်းဂဏန်း နှင့် အခြေအနေ ဖြစ်ပြီး
လုပ်ဆောင်ရမည့် အလုပ် မ ဟုတ်ပါ။

### Output

```text
[dashboard] refresh=300s max_data_age=300s
[dashboard] red  priority 1: agents_not_reporting   count=4   severity=critical
[dashboard] red  priority 2: antivirus_disabled     count=7   severity=high
[dashboard] red  priority 3: pending_updates        count=23  severity=medium
[dashboard] red  priority 4: agent_app_updates      count=11  severity=low
[dashboard] green users=42 apps=96 tags=6
[dashboard] blue  console=ok nats=ok ocsp=ok postgres=ok workers=degraded
[dashboard] blue_degraded=workers
```

### ရလဒ် ဖတ်ခြင်း

- `agents_not_reporting` သည် critical ဖြစ်သဖြင့် count အနည်းငယ်သာ
  ရှိသော်လည်း ပထမ ရောက်သည်။
- `pending_updates` ၏ count (၂၃) သည် အများဆုံး ဖြစ်သော်လည်း
  severity medium ဖြစ်သဖြင့် တတိယ သာ ရသည်။ ဤ အချက်သည်
  "အရေအတွက် များသည် အရေးကြီးသည်" ဟူသည့် အယူအဆ မ မှန်ကြောင်း
  ပြသည်။
- `max_data_age=300s` — refresh ကာလ တစ်ခုလုံး နောက်ကျနိုင်သည်။
- `blue_degraded=workers` — component ကျန်းမာရေး ချို့ယွင်းမှုကို
  သီးခြား လိုင်းဖြင့် ပြသည်။

## Exercise 3 — အလွှာလိုက် ဆက်သွယ်မှု အကဲဖြတ်ခြင်း

### ချဉ်းကပ်ပုံ

အလွှာ ငါးခုကို အစဉ်လိုက် ဖြတ်သည်။ `blocked` အလံကို သုံးပြီး
ပထမဆုံး ကျသည့် အလွှာ နောက်တွင် ကျန်သည့် အလွှာ အားလုံးကို
`not tested` ဟု သတ်မှတ်သည်။ ထို အလံ မ ပါလျှင် အောက်လွှာများကို
"ok" ဟု မှားယွင်း သတ်မှတ်မိမည်။

### Output

```text
[diag] scenario=healthy    first_failure=none                       verdict=healthy
[diag]   endpoint->nats:4433=ok nats->agent-worker=ok agent-worker->postgres:5432=ok console:1323/1324=ok console->ocsp:8000=ok
[diag] scenario=nats_down  first_failure=endpoint->nats:4433        verdict=blocked_at_layer_1
[diag]   endpoint->nats:4433=fail nats->agent-worker=not tested agent-worker->postgres:5432=not tested console:1323/1324=not tested console->ocsp:8000=not tested
[diag] scenario=db_down    first_failure=agent-worker->postgres:5432 verdict=blocked_at_layer_3
[diag]   endpoint->nats:4433=ok nats->agent-worker=ok agent-worker->postgres:5432=fail console:1323/1324=not tested console->ocsp:8000=not tested
[diag] scenario=ocsp_down  first_failure=console->ocsp:8000         verdict=blocked_at_layer_5
[diag]   endpoint->nats:4433=ok nats->agent-worker=ok agent-worker->postgres:5432=ok console:1323/1324=ok console->ocsp:8000=fail
```

### ရလဒ် ဖတ်ခြင်း

- `healthy` — အလွှာ ငါးခုလုံး `ok`၊ `first_failure=none`။
- `nats_down` — အလွှာ ၁ တွင် ရပ်ပြီး ကျန် လေးခု `not tested`။
- `db_down` — အလွှာ ၁ နှင့် ၂ ကောင်းသည်၊ အလွှာ ၃ ကျသည်။
  အလွှာ ၄ နှင့် ၅ ကို မ စမ်းသပ်ရသေး။
- `ocsp_down` — အလွှာ ၄ အထိ ကောင်းပြီး အလွှာ ၅ တွင် ကျသည်။
  ထို အခြေအနေတွင် agent report များ မ ရပ်ပါ၊ certificate စစ်ဆေးမှု
  သာ ကျသည်။
- မည်သည့် အခြေအနေတွင်မဆို ကျသည့် အလွှာ နောက်တွင် `ok` တစ်ခုမျှ
  မ ရှိကြောင်း assertion က အာမခံသည်။

## Exercise 4 — Log ခွဲခြားခြင်း

### ချဉ်းကပ်ပုံ

keyword စာရင်းကို အုပ်စု အလိုက် သတ်မှတ်ပြီး အုပ်စု အစဉ်ကို
`certificate, dns, auth, database, nats, sftp, other` ဟု သတ်မှတ်သည်။
လိုင်း တစ်လိုင်းကို စာလုံး အသေး အကြီး မ ခွဲဘဲ စစ်ပြီး ပထမဆုံး
ကိုက်ညီသည့် အုပ်စုကို ယူသည်။ ထို အစဉ်က အဓိပ္ပာယ် ရှိသည် —
DNS လိုင်းတွင် `nats` ဟူသည့် စာလုံး ပါနိုင်သဖြင့် dns ကို
nats အထက် စစ်ရသည်။

### Output

```text
[logs] classified=11
[logs] auth=2 certificate=3 database=1 dns=1 nats=1 other=2 sftp=1
[logs] triage_order=certificate,dns,auth,database,nats,sftp,other
```

### ရလဒ် ဖတ်ခြင်း

- `classified=11` — လိုင်း ဆယ်တစ်လိုင်း လုံး အုပ်စု တစ်ခုစီ ရသည်။
- `certificate=3` — `ca.cer` လိုင်း၊ `x509` လိုင်း နှင့်
  `time skew ... TLS handshake` လိုင်း။ နာရီ မ ကိုက်ညီမှုသည်
  TLS မှတစ်ဆင့် ပေါ်သဖြင့် certificate အုပ်စုသို့ ရောက်သည်။
- `dns=1` — `lookup nats.openuem.example: no such host` လိုင်းသည်
  nats စာလုံး ပါသော်လည်း dns အုပ်စုသို့ ရောက်သည်။
- `auth=2` — `jwt signature mismatch` နှင့် `token expired` လိုင်း။
- `other=2` — ကျန်းမာသည့် အခြေအနေ လိုင်း နှစ်ခု။ ထို လိုင်းများသည်
  ချို့ယွင်းမှု မ ဟုတ်သဖြင့် ချက်ချင်း လုပ်ဆောင်ရန် မ လိုပါ။
- `triage_order` သည် ဖတ်ရမည့် အစဉ်ကို သတ်မှတ်သည်။

## Exercise 5 — MTTR နှင့် ပြန်ဖြစ်နှုန်း တွက်ချက်ခြင်း

### ချဉ်းကပ်ပုံ

အချိန် တန်ဖိုး နှစ်ခုကို `datetime.strptime` ဖြင့် ဖတ်ပြီး ခြားနားချက်ကို
မိနစ်သို့ ပြောင်းသည်။ ထို နောက် အကြောင်းရင်း အလိုက် စုပြီး ပျမ်းမျှ
တွက်သည်။ လက်ရှိ အချိန်ကို လုံးဝ မ သုံးပါ — ထို ကြောင့် ရလဒ်သည်
နေ့ရက် မည်သည့် အချိန် မောင်းနှင်သည်ဖြစ်စေ တူညီသည်။

### Output

```text
[mttr] overall=95.8 min over 6 incidents
[mttr] auth=120.0 certificate=75.0 database=20.0 dns=45.0 nats=240.0
[mttr] longest=inc-03 cause=nats duration=240 min
[mttr] recurrence>=2: ws-001, ws-005
```

### ရလဒ် ဖတ်ခြင်း

- `certificate` ၏ MTTR သည် (၉၀ + ၆၀) / ၂ = ၇၅.၀ မိနစ်။
- `nats` ၏ MTTR သည် ၂၄၀.၀ မိနစ် ဖြစ်ပြီး အမြင့်ဆုံး ဖြစ်သည်။
  ထို ကြောင့် ထို အမျိုးအစားကို automation ဖြင့် လျှော့ချရန်
  ဦးစားပေး ရသည်။
- `overall=95.8` — ချို့ယွင်းမှု ခြောက်ခု၏ ပျမ်းမျှ။
- `recurrence>=2: ws-001, ws-005` — ထို endpoint နှစ်ခုတွင် ချို့ယွင်းမှု
  နှစ်ကြိမ် စီ ဖြစ်သည်။ ထပ်ခါ ဖြစ်ခြင်းသည် လက္ခဏာ မ ဟုတ်၊
  အမြစ်အကြောင်းရင်း ရှိနေကြောင်း အချက် ဖြစ်သည်။

## Exercise 6 — Alert rule တိုက်ဆိုင်မှု

### ချဉ်းကပ်ပုံ

rule တစ်ခုစီအတွက် sample စာရင်း၏ နောက်ဆုံး `for_samples` ခုကို
ယူသည်။ ထို window အတွင်း တန်ဖိုး အားလုံး ခြွင်းချက် နှင့် ကိုက်ညီမှ
alert ဖွင့်သည်။ မ ကိုက်ညီလျှင် အကြောင်းရင်း နှစ်မျိုး ခွဲသည် —
နောက်ဆုံး တန်ဖိုး ကိုယ်တိုင် မ ကိုက်ညီလျှင် `threshold`၊
နောက်ဆုံး တန်ဖိုး ကိုက်ညီသော်လည်း window မ ပြည့်လျှင် `duration`။

### Output

```text
[alert] evaluated=6 pairs, fired=3
[alert] critical agent_silent          AP-1 value=30
[alert] high     pending_updates_high  AP-3 value=12
[alert] high     disk_low              AP-4 value=6
[alert] suppressed duration=1 threshold=2
```

### ရလဒ် ဖတ်ခြင်း

- `evaluated=6 pairs` — endpoint ခြောက်ခု နှင့် rule တိုက်ဆိုင်မှု
  ခြောက်ခု။
- `AP-1` — `hours_since_report` နောက်ဆုံး နှစ်ခု (၂၆, ၃၀) လုံး
  ၂၄ ထက် ကြီးသဖြင့် critical alert ဖွင့်သည်။
- `AP-2` — sample နှစ်ခု (၁၂, ၂၆) အနက် နောက်ဆုံး တစ်ခုသာ ကိုက်ညီသည်။
  window မ ပြည့်သဖြင့် `duration` အဖြစ် ပယ်သည်။
- `AP-3` နှင့် `AP-4` — threshold နှင့် window နှစ်ခုလုံး ကိုက်ညီသည်။
- `AP-5` နှင့် `AP-6` — နောက်ဆုံး တန်ဖိုး ကိုယ်တိုင် မ ကိုက်ညီသဖြင့်
  `threshold` အဖြစ် ပယ်သည်။
- High severity နှစ်ခုကို endpoint အလိုက် စီသဖြင့် `AP-3` သည်
  `AP-4` အထက် ရောက်သည်။

## စစ်ဆေးမှု

Lab ကို သုံးကြိမ် မောင်းနှင်ပြီး stdout ကို byte အလိုက် နှိုင်းယှဉ်ရသည်။
အောင်မြင်ပါက နောက်ဆုံး လိုင်းတွင် အောက်ပါ စာသား ပေါ်လာမည်။

```text
[PASS] All 6/6 exercises passed successfully.
```
