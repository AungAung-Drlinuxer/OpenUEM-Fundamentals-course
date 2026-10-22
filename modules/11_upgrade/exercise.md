# Module 11 — Exercises

Server နှင့် agent upgrade ဆိုင်ရာ လေ့ကျင့်ခန်း ခြောက်ခု။

```bash
python3 modules/11_upgrade/lab.py
```

## Exercise 1 — Outdated vs upgradable

Latest stable release သည် `0.12.0` ဖြစ်သည်။ အောက်ပါ agent များထဲမှ
latest မဟုတ်သော (upgradable) agent များကို ရှာပါ။ Fleet အတွင်း
အနိမ့်ဆုံး version မဟုတ်သော (outdated) agent များကိုလည်း ရှာပါ။

```text
ws-001   0.12.0
ws-002   0.11.2
srv-010  0.10.0
mac-004  0.12.0
ws-003   0.11.2
```

## Exercise 2 — Upgrade လမ်းကြောင်း

Deployment အမျိုးအစားအလိုက် မည်သည့် နည်းလမ်းကို သုံးရမည်ကို ဖြေပါ —
native server၊ Docker server နှင့် agent (platform မည်သို့ဖြစ်စေ)။
Docker အတွက် command နှစ်ခုကို အတိအကျ ရေးပါ။

## Exercise 3 — Maintenance window

Policy အရ pilot အုပ်စုကို ချက်ချင်း upgrade လုပ်နိုင်သည်။ wave အုပ်စုများကို
window ဖွင့်မှသာ လုပ်နိုင်သည်။ ယခု window သည် pilot နှင့် wave-1 အတွက်
ဖွင့်ထားပြီး wave-2 အတွက် ပိတ်ထားသည်။ မည်သည့် အုပ်စု လုပ်နိုင်သနည်း။

## Exercise 4 — Task state transitions

Update task ၏ အခြေအနေများမှာ `Pending`၊ `In Progress`၊ `Success`၊ `Error`၊
`Cancelled` ဖြစ်သည်။ အောက်ပါ အပြောင်းအလဲ လေးခုကို စစ်ပါ။

```text
Pending -> In Progress
In Progress -> Success
Success -> Pending
Error -> Pending
```

## Exercise 5 — Rollback target

`0.12.0` upgrade မအောင်မြင်ပါ။ Release history မှာ
`0.9.4`၊ `0.10.0`၊ `0.11.2`၊ `0.12.0` ဖြစ်သည်။ မည်သည့် version သို့
ပြန်လျှော့ရမည်နည်း။ ရွေးချယ်နိုင်သော version အရေအတွက်ကိုလည်း ဖော်ပြပါ။

## Exercise 6 — Post-upgrade checklist

အောက်ပါ စစ်ဆေးချက်များထဲမှ မည်သည့်အချက် မအောင်မြင်သနည်း။

```text
services-active       true
console-login         true
agents-reporting      true
upgrade-task-success  false
ocsp-healthy          true
```
