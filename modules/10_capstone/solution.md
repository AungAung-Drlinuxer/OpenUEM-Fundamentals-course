# Module 10 — အဖြေများ

ဤ module ၏ အဖြေများသည် `lab.py` ၏ အမှန် output ကို အခြေခံသည်။
အောက်ပါ output တစ်ခုစီကို ထို ဖိုင်ကို run ခြင်းဖြင့် ပြန်လည် ရယူနိုင်သည်။
ကိန်းဂဏန်း အားလုံးသည် သင်ကြားရေး fixture ဖြစ်ပြီး တိုင်းတာထားသော
ရလဒ် မဟုတ်ပါ။

```bash
python3 modules/10_capstone/lab.py
```

## Exercise 1 — Readiness checklist ကို စစ်ဆေးခြင်း

စစ်ဆေးချက် ၁၂ ခုအနက် ၁၁ ခု အောင်မြင်သည်။ ကျရှုံးသည့် အချက်မှာ
`ca-cert-days-left` ဖြစ်သည်။ သတ်မှတ်ချက်မှာ ရက် ၃၆၅ နှင့် အထက်
ဖြစ်ပြီး လက်ရှိ တန်ဖိုးမှာ ရက် ၁၂၀ ဖြစ်သည်။ ထို့ကြောင့် gate က
`NOT-READY` ဖြစ်သည်။

```text
[exercise_1] Build readiness for the openuem.example deployment
  check               rule  expected      actual        verdict
  db-service          eq    active        active        PASS
  db-name             eq    openuem       openuem       PASS
  db-owner            eq    openuem_app   openuem_app   PASS
  ca-cert-days-left   ge    365           120           FAIL
  console-port-1323   eq    free          free          PASS
  auth-port-1324      eq    free          free          PASS
  nats-port-4433      eq    free          free          PASS
  ocsp-port-8000      eq    free          free          PASS
  hosts-override      eq    present       present       PASS
  console-health      eq    200           200           PASS
  nats-handshake      eq    ok            ok            PASS
  clock-skew-seconds  le    300           42            PASS
[RESULT] 11/12 checks passed
[RESULT] blocking item(s): ca-cert-days-left
[RESULT] build gate: NOT-READY
[RESULT] action: renew the CA certificate and re-run the checklist
[OK] exercise_1 — 11/12 readiness checks pass and the CA validity gap blocks the build
```

အဓိပ္ပာယ် ဖွင့်ဆိုချက်:

- `db-service`, `db-name`, `db-owner` သုံးခုက database အဆင်သင့် ဖြစ်ကြောင်း
  ပြသည်။ ဤအဆင့် မပြီးလျှင် component များ စတင်၍ မရပါ။
- port လေးခု (`1323`, `1324`, `4433`, `8000`) အလွတ် ဖြစ်ကြောင်း စစ်ဆေးခြင်းက
  ဆောက်လုပ်မှု အချိန်တွင် port ထပ်နေမှုကို ကြိုတင်ကာကွယ်သည်။
- `ca-cert-days-left` တစ်ခုတည်းက gate ကို ပိတ်ထားသည်။ ဤအချက်သည်
  နောက်ပိုင်း ဖြစ်ရပ်၏ အစ ဖြစ်သည်။
- `clock-skew-seconds` က စက္ကန့် ၄၂ သာ ဖြစ်သဖြင့် အချိန် ကွာဟမှု
  မရှိကြောင်း အတည်ပြုသည်။

readiness checklist က အတားအဆီး တစ်ခုကို ဖော်ထုတ်နိုင်ခြင်းသည်
ဆောက်လုပ်မှု အလယ်တွင် ရပ်တန့်ရမှုကို ရှောင်နိုင်သည်။ ဤဇာတ်လမ်းတွင်
အဖွဲ့သည် ထို အတားအဆီးကို မှန်ကန်စွာ တွေ့ခဲ့သည်။ သို့သော် ပြုပြင်မှုကို
change record မပါဘဲ လုပ်ဆောင်ခဲ့သဖြင့် နောက်ပိုင်း certificate ဖြစ်ရပ်
ဖြစ်ပေါ်ခဲ့သည်။

## Exercise 2 — Enrollment wave စီမံချက် ရေးဆွဲခြင်း

wave သုံးခုတွင် ၃, ၁၅, ၉ ဟု ခွဲထားသည်။ စုစုပေါင်း ၂၇ ဖြစ်သည်။
wave တစ်ခုစီတွင် platform သုံးမျိုး ပါဝင်သည်။

```text
[exercise_2] Enrollment wave plan
  wave    scope         endpoints   platforms
  wave 1  pilot         3           linux,macos,windows
  wave 2  head-office   15          linux,macos,windows
  wave 3  branch        9           linux,macos,windows
[RESULT] assigned 27/27 endpoints, duplicates 0
[RESULT] wave size cap 20 respected: yes
[RESULT] plan accepted: yes
[OK] exercise_2 — three waves of 3/15/9 cover all 27 endpoints and every wave spans three platforms
```

တွက်ချက်ပုံ:

- pilot အဖြစ် ဌာနချုပ်မှ အမည် `-01` ဖြင့် ဆုံးသော endpoint သုံးခုကို
  ရွေးသည်။ ၎င်းတို့မှာ `LNX-HO-01`, `MAC-HO-01`, `WIN-HO-01` ဖြစ်သည်။
- ကျန် ဌာနချုပ် endpoint ၁၅ ခုကို ဒုတိယ wave အဖြစ် သတ်မှတ်သည်။
- ဌာနခွဲ endpoint ၉ ခုကို တတိယ wave အဖြစ် သတ်မှတ်သည်။
- ထပ်နေမှု သုည ဖြစ်ကြောင်းကို စာရင်း အရှည်နှင့် အစုအဝေး အရှည်
  နှိုင်းယှဉ်ခြင်းဖြင့် စစ်သည်။

pilot တွင် platform သုံးမျိုး ပါဝင်ရခြင်း၏ အကြောင်းရင်းမှာ install နည်းလမ်းနှင့်
certificate နေရာချမှုသည် platform အလိုက် ကွဲပြားခြင်း ဖြစ်သည်။ Windows တွင်
silent flag များ၊ Debian တွင် package နှင့် certificate folder၊ macOS တွင်
installer နှင့် HomeBrew ကြိုတင်ပြင်ဆင်မှု လိုအပ်သည်။ pilot တွင် သုံးမျိုးလုံး
ပါဝင်မှသာ နောက် wave နှစ်ခုတွင် ထပ်တူ ပြဿနာ မျိုး မကြုံရနိုင်ပါ။

## Exercise 3 — Rollout gate ကို အကဲဖြတ်ခြင်း

ဆုံးဖြတ်ချက် အစဉ်မှာ `HOLD -> GO -> HOLD` ဖြစ်သည်။

```text
[exercise_3] Patch wave gate for the Saturday maintenance window
  window 2026-03-14 01:00-05:00 (+06:30), 27 targets
  attempt           at      reporting  rate    validation decision
  first-attempt     01:05   24/27      0.889   1          HOLD
    reason: reporting-rate-below-0.90
    reason: validation-failures-present
  after-remediation 02:40   27/27      1.000   0          GO
  late-evaluation   06:15   27/27      1.000   0          HOLD
    reason: outside-maintenance-window
[RESULT] decision sequence: HOLD -> GO -> HOLD
[RESULT] wave executed in-window after remediation: yes
[OK] exercise_3 — the gate holds on two blockers, opens after remediation, and closes outside the window
```

အကြောင်းရင်း ခွဲခြမ်းစိတ်ဖြာမှု:

- ပထမ တိုင်းတာမှု (01:05): reporting ၂၄/၂၇ သည် ၀.၈၈၉ ဖြစ်သဖြင့် ၉၀%
  သတ်မှတ်ချက်ကို မပြည့်ပါ။ validation ကျရှုံးမှု တစ်ခု လည်း ရှိသည်။
  gate နှစ်ခု ကျရှုံးသဖြင့် `HOLD` ဖြစ်သည်။
- ဒုတိယ တိုင်းတာမှု (02:40): reporting ၂၇/၂၇ နှင့် ကျရှုံးမှု သုည။
  window အတွင်း ဖြစ်သဖြင့် gate လေးခုလုံး ပြည့်မီသည်။ `GO` ဖြစ်သည်။
- တတိယ တိုင်းတာမှု (06:15): အခြေအနေ အားလုံး ကောင်းသော်လည်း window
  ပြင်ပ ဖြစ်သဖြင့် `outside-maintenance-window` တစ်ခုတည်းက `HOLD` ဖြစ်စေသည်။

တတိယ တိုင်းတာမှုက gate သည် အခြေအနေကို သာ မဟုတ်ဘဲ အချိန်ကိုလည်း
အမြဲ ထည့်သွင်း စစ်ဆေးကြောင်း ပြသည်။ ထို အချက်ကို မစစ်လျှင်
အသုံးပြုသူ အများဆုံး အချိန်တွင် patch ဖြန့်မိမည်။

## Exercise 4 — လိုက်နာမှု သက်သေ အနှစ်ချုပ် ထုတ်ခြင်း

စုစုပေါင်း လိုက်နာမှုမှာ ၂၄/၂၇ = ၈၈.၉% ဖြစ်သည်။

```text
[exercise_4] Compliance evidence summary (software baseline + patch level)
  platform  total   compliant  rate
  linux     8       7          87.5%
  macos     4       3          75.0%
  windows   15      14         93.3%
[RESULT] overall compliance: 24/27 = 88.9%
[RESULT] gap(s), sorted:
  LNX-BR-02   software-baseline   Flatpak browser package missing
  MAC-HO-03   patch-level         one pending update above the baseline
  WIN-BR-04   software-baseline   WinGet package removed by the user
[OK] exercise_4 — 24 of 27 endpoints are compliant (88.9 percent of the fleet)
```

platform အလိုက် ရလဒ်:

| Platform | စုစုပေါင်း | လိုက်နာသူ | ရာခိုင်နှုန်း |
|---|---|---|---|
| linux | 8 | 7 | 87.5% |
| macos | 4 | 3 | 75.0% |
| windows | 15 | 14 | 93.3% |

macOS သည် အနိမ့်ဆုံး ဖြစ်သည်။ အရေအတွက် နည်းသော platform တွင် endpoint
တစ်ခု ကျရှုံးလျှင် ရာခိုင်နှုန်း ပြင်းထန်စွာ ကျသည်။ ထို့ကြောင့် စုစုပေါင်း
ကိန်းဂဏန်းတစ်ခုတည်းဖြင့် ဆုံးဖြတ်ခြင်း မပြုရ။ platform တစ်ခုစီ၏
ကိန်းဂဏန်းကို သီးခြား ကြည့်ရသည်။

## Exercise 5 — ဖြစ်ရပ်၏ အမြစ်အကြောင်းရင်း ရွေးချယ်ခြင်း

ရွေးချယ်ထားသော အကြောင်းရင်းမှာ `trust-anchor-mismatch` ဖြစ်သည်။
ထို အကြောင်းရင်းသာ မျှော်မှန်းချက် လေးခုလုံးကို ကိုက်ညီသည်။

```text
[exercise_5] Incident root cause after the certificate rotation
  rotated certificates: 23   endpoints reporting: 4/27
  signal                           observed
  agent_log_unknown_authority     True
  agents_reporting                4
  agents_total                    27
  certificates_rotated            23
  clock_skew_seconds              3
  console_https_200               True
  dns_resolution_ok               True
  nats_port_4433_open             True
  ocsp_responder_200              True
  postgres_accepting              True
  candidate               matched  required  score
  trust-anchor-mismatch   4        4         1.00
  dns-resolution-failure  0        1         0.00
  endpoint-clock-skew     0        1         0.00
  nats-service-down       0        1         0.00
  postgres-unavailable    0        1         0.00
[RESULT] selected root cause: trust-anchor-mismatch (score 1.00)
[RESULT] evidence: the agent log reports an unknown certificate authority while NATS, OCSP, DNS and PostgreSQL all answer
[RESULT] recovery plan
   1. freeze the certificate rotation batch
   2. restore the previous CA certificate in openuem.ini and in the certificate tree
   3. re-issue agent certificates from the trusted CA
   4. openuem-ocsp-responder
   5. openuem-nats-service
   6. openuem-server-updater
   7. openuem-agent-worker
   8. openuem-notification-worker
   9. openuem-cert-manager-worker
  10. openuem-console
  11. force report on the affected endpoints
  12. confirm reporting rate returns to 27/27
[OK] exercise_5 — trust-anchor mismatch is the only candidate that fits the evidence
```

ဖယ်ထုတ်ခဲ့သော အကြောင်းရင်းများ:

- `nats-service-down` — port 4433 ချိတ်ဆက်မှု အောင်မြင်သည်။ NATS service
  အသက်ရှင်နေသည်။
- `postgres-unavailable` — console က HTTP 200 ပြန်သည်။ database မှ
  ဒေတာ ဖတ်နိုင်နေသည်။
- `dns-resolution-failure` — အမည် ဖြေရှင်းမှု အောင်မြင်သည်။ ဌာနခွဲ host များ
  လည်း တူညီသော အမည်ကို ရနိုင်သည်။
- `endpoint-clock-skew` — clock skew သည် စက္ကန့် ၃ သာ ဖြစ်သည်။
  certificate သက်တမ်း စစ်ဆေးမှုကို မထိခိုက်နိုင်ပါ။

အထောက်အထား ကွင်းဆက်:

1. agent log က `x509: certificate signed by unknown authority` ဟု ဆိုသည်။
   ဆိုလိုသည်မှာ server က agent certificate ကို လက်မှတ်ထိုးသူကို
   မယုံကြည်ခြင်း ဖြစ်သည်။
2. certificate အစားထိုးမခံရသော endpoint ၄ ခု ဆက်လက် report ပို့နေသည်။
   ထို အချက်က အခြေခံအဆောက်အအုံ ပျက်မနေကြောင်း ပြသည်။
3. အစားထိုးခံရသော endpoint ၂၃ ခု အားလုံး တိတ်ဆိတ်သည်။
   ထို အချက်က ပြောင်းလဲမှုနှင့် ကျရှုံးမှုကို တိုက်ရိုက် ဆက်စပ်သည်။
4. ပြန်လည် ထူထောင်မှု အစီအစဉ်ရှိ service များ၏ အစဉ်သည် module 03 ၏
   အစဉ်နှင့် တိတိကျကျ ကိုက်ညီသည်။ OCSP အရင်၊ ထို့နောက် NATS, updater,
   worker များ, console ဖြစ်သည်။

## Exercise 6 — အဆုံးသတ် scorecard တွက်ချက်ခြင်း

အလေးချိန်ဖြင့် တွက်ထားသော စုစုပေါင်း အမှတ်မှာ ၈၅.၅ ဖြစ်သည်။
အနိမ့်ဆုံး နယ်ပယ်မှာ `incident-response` ဖြစ်ပြီး အမှတ် ၇၀ ဖြစ်သည်။

```text
[exercise_6] Capstone scorecard
  domain              weight   score   contribution
  build-readiness     15%      80      12.0
  enrollment-waves    15%      100     15.0
  software-baseline   20%      90      18.0
  patch-wave          20%      85      17.0
  incident-response   20%      70      14.0
  evidence-pack       10%      95      9.5
[RESULT] weight total: 100%
[RESULT] weighted score: 85.5 / 100
[RESULT] lowest domain: incident-response at 70
[RESULT] verdict: meets
[RESULT] capstone gate: PASS
[OK] exercise_6 — weighted 85.5 with every domain at or above the 60 floor

[PASS] All 6/6 exercises passed successfully.
```

တွက်ချက်ပုံ:

- `build-readiness`: ၁၅ × ၈၀ = ၁၂၀၀၊ ပံ့ပိုးမှု ၁၂.၀
- `enrollment-waves`: ၁၅ × ၁၀၀ = ၁၅၀၀၊ ပံ့ပိုးမှု ၁၅.၀
- `software-baseline`: ၂၀ × ၉၀ = ၁၈၀၀၊ ပံ့ပိုးမှု ၁၈.၀
- `patch-wave`: ၂၀ × ၈၅ = ၁၇၀၀၊ ပံ့ပိုးမှု ၁၇.၀
- `incident-response`: ၂၀ × ၇၀ = ၁၄၀၀၊ ပံ့ပိုးမှု ၁၄.၀
- `evidence-pack`: ၁၀ × ၉၅ = ၉၅၀၊ ပံ့ပိုးမှု ၉.၅

ပေါင်းလဒ်မှာ ၈၅၅၀ ဖြစ်ပြီး ၁၀၀ ဖြင့် စားလျှင် ၈၅.၅ ရသည်။
နှစ်ခုသော သတ်မှတ်ချက်ကို စစ်သည်။ ပထမ၊ စုစုပေါင်း ၇၅ နှင့် အထက်
ဖြစ်ရမည်။ ဒုတိယ၊ နယ်ပယ် တစ်ခုမျှ ၆၀ အောက် မဖြစ်ရ။
`incident-response` သည် ၇၀ ဖြစ်သဖြင့် အနိမ့်ဆုံး သတ်မှတ်ချက်ကို
ပြည့်မီသည်။ ထို့ကြောင့် gate က `PASS` ဖြစ်သည်။

နယ်ပယ် တစ်ခု ၆၀ အောက် ဖြစ်လျှင် စုစုပေါင်း အမှတ် မြင့်နေပါလျက်
မအောင်မြင်ဟု သတ်မှတ်ရခြင်း၏ အကြောင်းရင်းမှာ အားနည်းသော နယ်ပယ်တစ်ခုက
လုပ်ငန်း တစ်ခုလုံးကို အန္တရာယ် ဖြစ်စေနိုင်ခြင်း ဖြစ်သည်။
ဥပမာ ဖြစ်ရပ် တုံ့ပြန်မှု အားနည်းလျှင် အခြား နယ်ပယ် ငါးခု ကောင်းနေခြင်းက
endpoint များ တိတ်ဆိတ်သွားချိန်တွင် အကျိုး မရှိပါ။
