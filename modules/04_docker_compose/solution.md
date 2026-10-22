# Module 04 — Solutions

အောက်ပါ output များသည် `python3 modules/04_docker_compose/lab.py` ၏
တကယ့် output ဖြစ်သည်။

## Exercise 1 — `.env` လိုအပ်ချက်

`CONSOLE_JWT_KEY` သည် အလွတ် ဖြစ်နေသည်။ Key မရှိပါက console က JWT ကို
လက်မှတ်မထိုးနိုင်သဖြင့် login မလုပ်နိုင်ပါ။ ကျန် key ၁၇ ခု ပြည့်စုံသည်။

```text
[OK] exercise_1 — env: 17/18 required keys set; missing=CONSOLE_JWT_KEY
```

## Exercise 2 — JWT key မူဝါဒ

မူလတန်ဖိုး `averylongsecret` သည် ၁၅ လုံးသာ ဖြစ်ပြီး အများသိထားသော
တန်ဖိုးဖြစ်သဖြင့် ငြင်းပယ်သည်။ အလွတ်ကို ငြင်းပယ်သည်။
ကျပန်း hex ၃၂ လုံးကို လက်ခံသည်။

```text
[OK] exercise_2 — jwt key policy: default,empty,ok; accepted_length=32
```

## Exercise 3 — Hosts entry

အမည်သုံးခုကို စာလုံးအစဉ်ဖြင့် စီပြီး တစ်ကြောင်းတည်း ရေးသည်။
NATS host ကို နှစ်ကြိမ် ထည့်ထားသော်လည်း ထပ်နေမှုကို ဖယ်ရှားသည်။

```text
[OK] exercise_3 — hosts entry: 192.168.1.43  console.openuem.example  nats.openuem.example  ocsp.openuem.example
```

## Exercise 4 — Reverse proxy တန်ဖိုးများ

ပထမ — proxy မသုံးသဖြင့် port များ အလွတ်ဖြစ်သည်၊ မှန်သည်။
ဒုတိယ — host နှင့် port နှစ်ခုလုံး ရှိသည်၊ မှန်သည်။
တတိယ — host ရှိသော်လည်း auth port မရှိ၊ မှားသည်။

```text
[OK] exercise_4 — reverse proxy: no-proxy=ok, full=ok, host-without-auth-port=invalid
```

## Exercise 5 — Startup order

မှီခိုမှု မရှိသော service ကို ဦးစွာ စတင်သည်။ Database ပြီးနောက်
တစ်ဆင့်ချင်း မှီခိုသူများ စတင်နိုင်သည်။ တူညီသော အဆင့်တွင် ရှိသော
service များကို အမည်အစဉ်ဖြင့် စီသည်။

```text
[OK] exercise_5 — startup order: openuem-db -> cert-manager -> nats -> ocsp -> agent-worker -> console
```

## Exercise 6 — Teardown အန္တရာယ်

`stop` နှင့် `down` သည် volume ကို မဖျက်သဖြင့် ဒေတာ ကျန်သည်။
`down -v` သည် volume ကိုပါ ဖျက်သဖြင့် ဒေတာ ပျက်သည်။

```text
[OK] exercise_6 — teardown: data-safe=docker compose down | docker compose stop; data-loss=docker compose down -v
```
