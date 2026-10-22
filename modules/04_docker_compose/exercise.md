# Module 04 — Exercises

Container deployment ဆိုင်ရာ လေ့ကျင့်ခန်း ခြောက်ခု။

```bash
python3 modules/04_docker_compose/lab.py
```

## Exercise 1 — `.env` လိုအပ်ချက်

အောက်ပါ `.env` တွင် လိုအပ်သော key ၁၈ ခုအနက် တစ်ခု လွတ်နေသည်။
မည်သည့် key လဲ။ ပြည့်စုံမှုအချိုးကို ဖော်ပြပါ။

```text
DATABASE_DB_NAME=openuem
DATABASE_PORT=5432
DATABASE_USER=openuem
DATABASE_PASSWORD=db-secret
OPENUEM_DATABASE_URL=postgres://openuem:db-secret@openuem-db:5432/openuem
OPENUEM_ORGNAME=Example Org
OPENUEM_COUNTRY=MM
OPENUEM_DOMAIN=openuem.example
CONSOLE_HOST=console.openuem.example
CONSOLE_PORT=1323
CONSOLE_AUTH_PORT=1324
CONSOLE_JWT_KEY=
NATS_HOST=nats.openuem.example
NATS_PORT=4433
OPENUEM_NATS_SERVERS=nats.openuem.example:4433
OCSP_URL=http://ocsp.openuem.example:8000
OCSP_HOST=ocsp.openuem.example
OCSP_PORT=8000
```

## Exercise 2 — JWT key မူဝါဒ

`.env-example` ၏ မူလ key သည် `averylongsecret` ဖြစ်သည်။
အောက်ပါ ကိုယ်စားလှယ် သုံးခုကို မူဝါဒ (အနည်းဆုံး ၃၂ လုံး၊ မူလတန်ဖိုး
မဖြစ်ရ၊ အလွတ် မဖြစ်ရ) ဖြင့် အကဲဖြတ်ပါ။

```text
averylongsecret
(empty)
9f2c41ab7d3e58c0a6b1f4d92e7c0a38
```

## Exercise 3 — Hosts entry

Lab host ၏ IP သည် `192.168.1.43` ဖြစ်သည်။ NATS host၊ OCSP host နှင့်
console host အတွက် hosts entry တစ်ကြောင်း တည်ဆောက်ပါ။ အမည်ထပ်နေပါက
တစ်ကြိမ်သာ ထည့်ပါ။ `127.0.0.1` မပါရ။

## Exercise 4 — Reverse proxy တန်ဖိုးများ

အောက်ပါ အခြေအနေ သုံးခုကို မှန်/မှား စစ်ပါ။
Proxy မသုံးပါက port နှစ်ခုလုံး အလွတ် ဖြစ်ရမည်။ Proxy သုံးပါက
host နှင့် port နှစ်ခုလုံး ဖြည့်ရမည်။

```text
host=            console_port=       auth_port=
host=console...  console_port=443     auth_port=4443
host=console...  console_port=443     auth_port=
```

## Exercise 5 — Startup order

Service များ၏ မှီခိုမှု အောက်ပါအတိုင်း ဖြစ်သည်။

```text
openuem-db      (none)
nats            openuem-db
ocsp            openuem-db
cert-manager    openuem-db
agent-worker    openuem-db, nats
console         openuem-db, nats, agent-worker
```

မှီခိုမှုအရ မှန်ကန်သော စတင်အစဉ်ကို ရေးပါ။

## Exercise 6 — Teardown အန္တရာယ်

အောက်ပါ command သုံးခုကို "ဒေတာ ကျန်" နှင့် "ဒေတာ ပျက်" ဟု ခွဲပါ။

```text
docker compose stop
docker compose down
docker compose down -v
```
