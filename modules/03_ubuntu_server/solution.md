# Module 03 — အဖြေများ

ဤ အဖြေများသည် `lab.py` ၏ တကယ့် output နှင့် တိုက်ရိုက် ကိုက်ညီသည်။ Output
တစ်ခုချင်းကို ထို exercise အတွက် ထုတ်ပေးသည့် စာကြောင်းများ အတိုင်း ကူးထားသည်။
မိမိ run သည့် ရလဒ်နှင့် မကိုက်ညီပါက sort မလုပ်ရသေးသည့် dict သို့မဟုတ် set
တစ်ခု ကျန်နေနိုင်သည်။

## Exercise 1 — Package မှ Component Role သို့ ပုံဖော်ခြင်း

အဓိက အယူအဆမှာ package အမည်တစ်ခုက ထို package ၏ တာဝန် နှင့် inbound port ကို
တိုက်ရိုက် ဆုံးဖြတ်ပေးခြင်း ဖြစ်သည်။ ထို ကွာခြားချက်ကို ဇယားတစ်ခုအဖြစ် ဖော်ပြရသည်။

ဖြေဆိုပုံ —

1. `REQUESTED_PACKAGES` ကို `sorted()` ဖြင့် စီသည်။
2. အမည် တစ်ခုချင်းကို `PACKAGE_ROLES` တွင် ရှာသည်။ တွေ့ပါက တာဝန်နှင့် port
   စာရင်းကို ယူသည်။ မတွေ့ပါက `UNKNOWN PACKAGE` ဟု မှတ်သည်။
3. Port မရှိသည့် component အတွက် `-` ကို ပြသည်။
4. Inbound port အားလုံးကို စုပြီး `sorted()` ဖြင့် စီသည်။

စစ်ဆေးချက် — `openuem-console` သည် 1323 နှင့် 1324 ကို ပိုင်သည်။ NATS သည်
4433၊ OCSP သည် 8000 ဖြစ်သည်။ Worker လေးခုနှင့် cert-manager CLI တွင် inbound
port မရှိ။ `openuem-telemetry-sidecar` သည် OpenUEM package မဟုတ်သဖြင့်
မလုပ်နိုင်သည့် စာရင်းသို့ ရောက်သည်။

```text
== Exercise 1 — package to role mapping ==
  openuem-agent-worker          agent-report-worker       -
  openuem-cert-manager-worker   certificate-issuer-worker -
  openuem-console               console+auth-server       1323,1324
  openuem-nats-service          nats-broker               4433
  openuem-notification-worker   notification-worker       -
  openuem-ocsp-responder        ocsp-responder            8000
  openuem-server-updater        ini-generator-service     -
  openuem-telemetry-sidecar     UNKNOWN PACKAGE           -
  mapped=7 unmapped=1
  listener ports: 1323,1324,4433,8000
[OK] exercise_1 — resolved 7 packages to roles and flagged 1 unknown package
```

## Exercise 2 — Service စတင်သည့် အစီအစဉ် စစ်ဆေးခြင်း

အဓိက အယူအဆမှာ အစီအစဉ် တစ်ခုကို အတွဲများဖြင့် စစ်ဆေးခြင်း ဖြစ်သည်။
position map တစ်ခု တည်ဆောက်ပြီး အတွဲတစ်ခုချင်းအတွက် "မတိုင်မီ" service ၏
index သည် "ပြီးနောက်" service ၏ index ထက် ကြီးနေပါက ချိုးဖောက်မှု ဖြစ်သည်။

ဖြေဆိုပုံ —

1. `{name: index}` ဖြင့် position map ကို တည်ဆောက်သည်။
2. `(before, after)` အတွဲတစ်ခုချင်းအတွက် `position[before] > position[after]`
   ဖြစ်ပါက `"<after> starts before <before>"` ကို စာရင်းသို့ ထည့်သည်။
3. ရလဒ်ကို `sorted()` ဖြင့် စီသည်။

ဤ နည်းလမ်းဖြင့် documentation အစီအစဉ်တွင် ချိုးဖောက်မှု မရှိကြောင်း ပြသည်။
`PROPOSED_ORDER` တွင် console ကို ရှေ့ဆုံးသို့ ရွှေ့ထားသဖြင့် ချိုးဖောက်မှု
နှစ်ခု ထွက်သည် — console သည် updater ၏ ရှေ့တွင်လည်း ကောင်း၊ OCSP ၏
ရှေ့တွင်လည်းကောင်း ရောက်နေသည်။

```text
== Exercise 2 — service start-order validation ==
  documented order: ocsp-responder -> nats-service -> server-updater -> agent-worker -> notification-worker -> cert-manager-worker -> console
  documented order violations: 0
  proposed order: console, nats-service, ocsp-responder, server-updater, agent-worker, notification-worker, cert-manager-worker
  proposed order violations: 2
    - openuem-console starts before openuem-ocsp-responder
    - openuem-console starts before openuem-server-updater
[OK] exercise_2 — documented order is valid and the proposed order breaks 2 dependencies
```

## Exercise 3 — `openuem.ini` ကို Section အလိုက် ခွဲခြမ်းခြင်း

`configparser` သည် section မတိုင်မီ key များကို လက်မခံသဖြင့် လက်ဖြင့် parser
တစ်ခု ရေးခြင်းသည် ဤ ဖိုင်၏ တကယ့် ပုံစံနှင့် ပိုကိုက်ညီသည်။

ဖြေဆိုပုံ —

1. `sections` ကို `{"(global)": {}}` ဖြင့် စတင်သည်။
2. `[` ဖြင့် စပြီး `]` ဖြင့် ဆုံးသည့် စာကြောင်းကို section header အဖြစ် ယူသည်။
3. `#` သို့မဟုတ် `;` ဖြင့် စသည့် စာကြောင်းနှင့် အလွတ်လိုင်းကို ကျော်သည်။
4. `=` ပါသည့် စာကြောင်းကို ပထမ `=` တစ်ခုတည်းတွင် ခွဲသည်။
5. Port key သုံးခုကို `int()` ဖြင့် ပြောင်းသည်။
6. `REQUIRED_INI` ကို လိုက်ပြီး မရှိသည့် entry များကို စာရင်းပြသည်။

Broken မိတ္တူကို `authport` စာကြောင်းနှင့် `[JWT] Key` စာကြောင်းကို ဖျက်ခြင်းဖြင့်
ဖန်တီးသည်။ ထို မိတ္တူတွင် လိုအပ်ချက် နှစ်ခု ပျောက်နေသည်ကို တွေ့ရသည်။

```text
== Exercise 3 — openuem.ini section parsing ==
  sections: (global), Console, JWT
  (global) keys: CACert, CAKey, NATSCert
  Console: hostname=console.openuem.example port=1323 authport=1324 domain=openuem.example
  Console reverse proxy: caddy.openuem.example:443
  JWT key length=32
  missing required entries: none
  broken fixture missing: Console.authport, JWT.Key
[OK] exercise_3 — parsed 3 ini sections and detected 2 missing entries in the broken copy
```

## Exercise 4 — `--years-valid` မှ သက်တမ်းကုန်ဆုံးရက် တွက်ချက်ခြင်း

အဓိက အယူအဆမှာ နှစ် ပေါင်းခြင်းကို ရက် ၃၆၅ ပေါင်းခြင်းဖြင့် အစားမထိုးသင့်ခြင်း
ဖြစ်သည်။
`date.replace(year=...)` သည် ဖေဖော်ဝါရီ 29 အတွက် `ValueError` ကို ထုတ်သည်။
ထို အခြေအနေတွင် 28 ရက်သို့ ချိန်ညှိရသည်။

ဖြေဆိုပုံ —

1. `_add_years(day, years)` တွင် `day.replace(year=day.year + years)` ကို
   ကြိုးစားသည်။ `ValueError` ဖြစ်ပါက `day=28` ဖြင့် ပြန်ကြိုးစားသည်။
2. `years < 1` ဖြစ်ပါက ငြင်းပယ်သည်။
3. `(expiry - issued).days` ဖြင့် ရက် အရေအတွက် ရှာသည်။
4. ထုတ်ပေးရက်သည် ဖေဖော်ဝါရီ 29 ဖြစ်ပါက `leap_day_clamped=yes` ကို ထည့်သည်။

တွက်ချက်မှု နှစ်ခုကို စစ်ဆေးရသည်။ 2026-03-15 မှ ၂ နှစ်သည် 2028-03-15 ဖြစ်ပြီး
ထို ကာလတွင် 2028 ၏ ဖေဖော်ဝါရီ 29 ပါဝင်သဖြင့် 731 ရက် ဖြစ်သည်။ 2024-02-29
မှ ၁ နှစ်သည် 2025-02-28 ဖြစ်ပြီး 365 ရက် ဖြစ်သည်။

```text
== Exercise 4 — certificate expiry from --years-valid ==
  issued=2026-03-15 years=2 expires=2028-03-15 term_days=731
  issued=2024-02-29 years=1 expires=2025-02-28 term_days=365 leap_day_clamped=yes
  issued=2026-03-15 years=0 rejected (window must be >= 1 year)
  accepted=2 rejected=1
[OK] exercise_4 — computed 2 expiry dates and rejected 1 invalid window
```

## Exercise 5 — Console/Auth/NATS/OCSP Port ထပ်နေမှု ရှာခြင်း

အဓိက အယူအဆမှာ port နံပါတ် တစ်ခုတည်း မဟုတ်ဘဲ `(port, protocol)` အတွဲကို
သာ ထပ်နေမှု အဖြစ် သတ်မှတ်ခြင်း ဖြစ်သည်။ TCP နှင့် UDP သည် သီးခြား
namespace ဖြစ်သည်။

ဖြေဆိုပုံ —

1. `PORT_PLAN` နှင့် `EXTRA_LISTENERS` ကို ပေါင်းသည်။
2. `{(port, proto): [owners]}` ဖြင့် အုပ်စုဖွဲ့သည်။
3. ပိုင်ရှင် နှစ်ဦး အထက် ရှိသည့် အုပ်စုကို ထပ်နေမှု အဖြစ် ယူသည်။
4. `sorted(conflicts)` ဖြင့် စီပြီး ပိုင်ရှင်များကို `sorted()` ဖြင့် စီသည်။
5. UDP အုပ်စုတစ်ခုအတွက် တူညီသည့် port ၏ TCP အုပ်စု ရှိမရှိ စစ်သည်။
6. 1024 အောက် port များကို သီးခြား စုသည်။

ရလဒ်မှာ ထပ်နေမှု တစ်ခုသာ ဖြစ်သည် — 1323/tcp ကို console နှင့် probe-agent
နှစ်ဦး သုံးနေသည်။ 4433/udp သည် TCP 4433 နှင့် မထပ်နိုင်။

```text
== Exercise 5 — port conflict detection ==
  plan entries: 5 extra listeners: 2
  conflicts (1):
    1323/tcp -> openuem-console(console), probe-agent(http)
  same number, other protocol (no conflict): 4433/udp vs 4433/tcp
  privileged ports (<1024): 443
[OK] exercise_5 — found 1 real conflict and ignored 1 same-number/different-protocol pair
```

## Exercise 6 — Port စီမံချက်မှ Firewall စည်းမျဉ်း ထုတ်ခြင်း

အဓိက အယူအဆမှာ firewall စည်းမျဉ်းကို လက်ဖြင့် ရေးခြင်း မဟုတ်ဘဲ port
စီမံချက်မှ ထုတ်ခြင်း ဖြစ်သည်။ ထို နည်းလမ်းဖြင့် စီမံချက် နှင့် firewall
မကိုက်ညီမှု မဖြစ်နိုင်။

ဖြေဆိုပုံ —

1. `PORT_PLAN` ထဲက တစ်ခုချင်းအတွက် `(port, proto, line)` tuple ဖန်တီးသည်။
2. Line ပုံစံမှာ `ufw allow <port>/<proto> comment '<component> <role>'` ဖြစ်သည်။
3. Tuple စာရင်းကို `sorted()` ဖြင့် စီသည်။ Port သည် ပထမ element ဖြစ်သဖြင့်
   port အလိုက် စီသွားသည်။
4. ရှေ့ဆုံးတွင် `ufw default deny incoming` ကို ပြသည်။
5. စည်းမျဉ်းကို ဒုတိယ အကြိမ် ထုတ်ပြီး နှစ်ကြိမ် ရလဒ် တူညီမှုကို စစ်သည်။

စည်းမျဉ်း ၅ ခု ထွက်သည် — 443၊ 1323၊ 1324၊ 4433 နှင့် 8000။ Port တစ်ခုချင်းစီ
တစ်ကြိမ်သာ ပါဝင်သည်။

```text
== Exercise 6 — firewall rules from the port plan ==
  ufw default deny incoming
  ufw allow 443/tcp comment 'caddy https'
  ufw allow 1323/tcp comment 'openuem-console console'
  ufw allow 1324/tcp comment 'openuem-console auth'
  ufw allow 4433/tcp comment 'openuem-nats-service nats'
  ufw allow 8000/tcp comment 'openuem-ocsp-responder ocsp'
  rules=5 lowest_port=443 highest_port=8000
[OK] exercise_6 — generated 5 idempotent firewall rules covering every planned port
```

## နောက်ဆုံး စစ်ဆေးချက်

`lab.py` ကို run ပါက လေ့ကျင့်ခန်း ခြောက်ခုလုံး၏ `[OK]` စာကြောင်းများ နှင့်
အတူ အောက်ပါ စာကြောင်းကို မြင်ရမည်။

```text
[PASS] All 6/6 exercises passed successfully.
```
