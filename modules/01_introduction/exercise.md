# Module 01 — Exercises

Modul 01 မှ သင်ယူခဲ့သော concept များကို စစ်ဆေးရန် လေ့ကျင့်ခန်း ခြောက်ခု။
အဖြေများကို `solution.md` တွင် ကြည့်နိုင်သည်။ လေ့ကျင့်ခန်း တစ်ခုချင်းကို
`lab.py` က အလိုအလျောက် စစ်ဆေးသည်။

```bash
python3 modules/01_introduction/lab.py
```

## Exercise 1 — Lifecycle transitions

Agent lifecycle တွင် အခြေအနေ လေးခု ရှိသည် — `Waiting for admission`,
`Enabled`, `Disabled`, `Removed`။ အောက်ပါ အပြောင်းအလဲ ငါးခုကို စစ်ဆေးပါ။

```text
Waiting for admission -> Enabled
Waiting for admission -> Disabled
Enabled -> Disabled
Disabled -> Enabled
Removed -> Enabled
```

မည်သည့် အပြောင်းအလဲ နှစ်ခုသည် ခွင့်မပြုသနည်း။ ခွင့်ပြုသော အရေအတွက်ကို
လည်း ဖော်ပြပါ။

## Exercise 2 — Component ports

OpenUEM ၏ component ခုနစ်ခုအတွက် default port များကို ရေးပါ —
`console`, `console-auth`, `nats`, `ocsp-responder`, `agent-sftp`,
`agent-vnc-proxy`, `postgresql`။ အဖြေကို port အတိုင်း စီပြီး
`name=port` ပုံစံဖြင့် ဖော်ပြပါ။

## Exercise 3 — Report freshness

အောက်ပါ agent ၏ နောက်ဆုံး report အချိန်ကို အခြေခံပြီး `fresh` (မိနစ် ၆၀ အောက်)၊
`late` (မိနစ် ၂၄၀ အောက်)၊ `stale` (မိနစ် ၂၄၀ အထက်) ဟု အမျိုးအစားခွဲပါ။

```text
ws-001   Enabled                12
ws-002   Waiting for admission  25
srv-010  Enabled                95
mac-004  Disabled               600
ws-003   Enabled                300
```

အမျိုးအစား တစ်ခုစီ၏ အရေအတွက်နှင့် `stale` ဖြစ်နေသော agent အမည်များကို
ဖော်ပြပါ။

## Exercise 4 — Capability matrix

အောက်ပါ စွမ်းရည်များထဲမှ Windows တစ်ခုတည်းအတွက်သာ ရနိုင်သော စွမ်းရည်များကို
ရှာပါ။ ထို့အပြင် `shell-script` ကို macOS တွင် ရ/မရ ဖြေပါ။

```text
package-deploy, registry-key, powershell-script, shell-script,
msi-package, bitlocker-status, remote-assistance, wol
```

## Exercise 5 — Port conflict detection

Lab port plan တွင် service ရှစ်ခု ရှိသည်။

```text
console 1323
console-auth 1324
nats 4433
ocsp-responder 8000
agent-sftp 2022
agent-vnc-proxy 1443
postgresql 5432
console-old 1323
```

ထပ်နေသော port ကို ရှာပြီး မည်သည့် service နှစ်ခု အသုံးပြုနေသည်ကို ဖော်ပြပါ။
ထူးခြားသော (unique) port အရေအတွက်ကိုလည်း ရေးပါ။

## Exercise 6 — Incident triage order

အောက်ပါ incident လေးခုကို severity အလိုက်၊ ထို့နောက် အသက်ကြီးသော
(age များသော) အလိုက် စီပါ။

```text
INC-104  low       400
INC-101  critical   15
INC-103  high       30
INC-102  critical    5
```
