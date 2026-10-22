# Module 11 — Solutions

အောက်ပါ output များသည် `python3 modules/11_upgrade/lab.py` ၏ တကယ့် output
ဖြစ်သည်။

## Exercise 1 — Outdated vs upgradable

`0.12.0` မဟုတ်သော agent သုံးခုသည် upgradable ဖြစ်သည်။ Fleet အတွင်း
အမြင့်ဆုံး version သည် `0.12.0` ဖြစ်သဖြင့် ထို version မဟုတ်သော agent
သုံးခုသည် outdated လည်း ဖြစ်သည်။

```text
[OK] exercise_1 — latest=0.12.0; can-be-upgraded=3; fleet-outdated=3
```

## Exercise 2 — Upgrade လမ်းကြောင်း

Native server တွင် console ၏ Update Servers ကို သုံးနိုင်သည်။
Docker တွင် ထို လုပ်ဆောင်ချက် အလုပ်မလုပ်သဖြင့် compose command နှစ်ခု
လိုအပ်သည်။ Agent များကို console မှ အစုလိုက် update လုပ်သည်။

```text
[OK] exercise_2 — native='console Update Servers, or apt/dnf upgrade'; docker=compose pull + force-recreate; agent=console driven
```

## Exercise 3 — Maintenance window

Pilot နှင့် wave-1 သည် ယခု လုပ်နိုင်သည်။ wave-2 ၏ window မဖွင့်သေးသဖြင့်
ပိတ်ထားသည်။

```text
[OK] exercise_3 — allowed=pilot,wave-1; blocked=wave-2
```

## Exercise 4 — Task state transitions

`Success` သည် အဆုံးသတ် အခြေအနေ ဖြစ်သဖြင့် ပြန်၍ `Pending` သို့
မကူးနိုင်ပါ။ ထပ် update လုပ်လိုပါက task အသစ် တစ်ခု ဖန်တီးရသည်။

```text
[OK] exercise_4 — task states: 3/4 valid; rejected=Success->Pending
```

## Exercise 5 — Rollback target

`0.12.0` ထက် နိမ့်သော version သုံးခု ရှိသည်။ အနီးဆုံး (အမြင့်ဆုံး) ဖြစ်သော
`0.11.2` သို့ ပြန်လျှော့သည်။

```text
[OK] exercise_5 — rollback target: 0.12.0 -> 0.11.2 (candidates=3)
```

## Exercise 6 — Post-upgrade checklist

Upgrade task များ မအောင်မြင်သေးသဖြင့် ထို အချက်ကို ဦးစွာ စစ်ရသည်။
ကျန် စစ်ဆေးချက် လေးခု အောင်မြင်သည်။

```text
[OK] exercise_6 — post-upgrade checks: 4/5 passed; failed=upgrade-task-success
```
