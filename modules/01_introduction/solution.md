# Module 01 — Solutions

အောက်ပါ output များသည် `python3 modules/01_introduction/lab.py` ၏
တကယ့် output ဖြစ်သည်။

## Exercise 1 — Lifecycle transitions

`Waiting for admission` မှ `Disabled` သို့ တိုက်ရိုက် မကူးနိုင်ပါ။ ထို agent ကို
ဦးစွာ Admit လုပ်ပြီး `Enabled` ဖြစ်မှသာ Disable လုပ်နိုင်သည်။ `Removed`
အခြေအနေသည် အဆုံးသတ် အခြေအနေ ဖြစ်ပြီး မည်သည့်နေရာသို့ မျှ ပြန်မကူးနိုင်ပါ။

ခွင့်ပြုသော အပြောင်းအလဲ သုံးခု၊ ငြင်းပယ်သော အပြောင်းအလဲ နှစ်ခု ဖြစ်သည်။

```text
[OK] exercise_1 — lifecycle: 3/5 transitions valid; rejected=Waiting for admission->Disabled,Removed->Enabled
```

## Exercise 2 — Component ports

Console သည် web UI အတွက် 1323၊ authentication အတွက် 1324 ကို သုံးသည်။
Agent များ ချိတ်ဆက်သော NATS သည် 4433 ဖြစ်သည်။ OCSP responder သည် 8000။
Agent ၏ SFTP သည် 2022 နှင့် VNC proxy သည် 1443။ PostgreSQL သည် 5432။

```text
[OK] exercise_2 — component ports: agent-sftp=2022, agent-vnc-proxy=1443, console=1323, console-auth=1324, nats=4433, ocsp-responder=8000, postgresql=5432
```

## Exercise 3 — Report freshness

`ws-001` (12) နှင့် `ws-002` (25) သည် fresh။ `srv-010` (95) သည် late။
`ws-003` (300) နှင့် `mac-004` (600) သည် stale ဖြစ်သည်။
`mac-004` သည် Disabled ဖြစ်နေသဖြင့် report မပို့ခြင်းသည် ပုံမှန် ဖြစ်သည်။

```text
[OK] exercise_3 — freshness: fresh=2 late=1 stale=2; stale=mac-004,ws-003
```

## Exercise 4 — Capability matrix

Windows တစ်ခုတည်းအတွက်သာ ရနိုင်သော စွမ်းရည်များမှာ `bitlocker-status`,
`msi-package`, `powershell-script` နှင့် `registry-key` ဖြစ်သည်။
`shell-script` ကို macOS တွင် အသုံးပြုနိုင်သည်။

```text
[OK] exercise_4 — capability matrix: windows-only=bitlocker-status,msi-package,powershell-script,registry-key; shell-script on macOS=True
```

## Exercise 5 — Port conflict detection

`console` နှင့် `console-old` နှစ်ခုလုံး 1323 ကို သုံးနေသည်။
ထို့ကြောင့် service ရှစ်ခုအတွက် ထူးခြားသော port ခုနစ်ခုသာ ရှိသည်။
ဤအခြေအနေတွင် ဒုတိယ service ကို မဖွင့်နိုင်ပါ။

```text
[OK] exercise_5 — port conflict: 1323 used by console and console-old; unique_ports=7
```

## Exercise 6 — Incident triage order

Severity အလိုက် ဦးစားပေးပြီး တူညီသော severity အတွင်း အသက်ကြီးသော
incident ကို ဦးစွာ ကိုင်တွယ်သည်။ `INC-101` သည် `INC-102` ထက် အသက် ၁၀ မိနစ်
ပိုကြီးသဖြင့် ဦးစွာ ရသည်။

```text
[OK] exercise_6 — triage order: INC-101 > INC-102 > INC-103 > INC-104
```
