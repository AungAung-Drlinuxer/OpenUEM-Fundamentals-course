# Module 02 — Exercises

PostgreSQL ပြင်ဆင်မှုနှင့် connection ဆိုင်ရာ လေ့ကျင့်ခန်း ခြောက်ခု။
အဖြေများကို `solution.md` တွင် ကြည့်နိုင်သည်။

```bash
python3 modules/02_postgresql/lab.py
```

## Exercise 1 — `.env` လိုအပ်ချက် စစ်ဆေးခြင်း

အောက်ပါ `.env` တွင် လိုအပ်သော key ငါးခုအနက် သုံးခုသာ ပါဝင်သည်။
မည်သည့် key နှစ်ခု ပျောက်နေသနည်း။ ပြည့်စုံမှုအချိုးကိုလည်း ဖော်ပြပါ။

```text
DATABASE_DB_NAME=openuem
DATABASE_PORT=5432
DATABASE_USER=openuem_app
OPENUEM_DOMAIN=openuem.example
CONSOLE_HOST=console.openuem.example
```

လိုအပ်သော key များမှာ `DATABASE_DB_NAME`, `DATABASE_PORT`, `DATABASE_USER`,
`DATABASE_PASSWORD`, `OPENUEM_DATABASE_URL` ဖြစ်သည်။

## Exercise 2 — URI percent-encoding

Password `te=st@lab` ကို connection URI တွင် ထည့်ရန် လိုအပ်သည်။
`=` နှင့် `@` ကို မည်သို့ ကုဒ်ပြောင်းရသနည်း။ ကုဒ်ပြောင်းပြီးနောက်
host၊ port နှင့် database အမည်ကို ဖော်ပြပါ။

## Exercise 3 — `pg_hba.conf` ဆုံးဖြတ်ချက်

အောက်ပါ rule များ အစဉ်လိုက် ရှိသည်။

```text
local   all  all                  peer
host    all  all  127.0.0.1/32    scram-sha-256
host    all  all  ::1/128         scram-sha-256
```

TCP ချိတ်ဆက်မှု သုံးမျိုးအတွက် authentication method ကို ဖြေပါ —
`127.0.0.1/32`၊ `10.0.0.5/32` နှင့် local socket။

## Exercise 4 — Error အမျိုးအစားခွဲခြား

အောက်ပါ error လေးခုကို အကြောင်းရင်း အမျိုးအစားအလိုက် ခွဲပါ
(`credentials`, `hba-rule`, `service-or-port`, `wrong-database`)။

```text
FATAL:  password authentication failed for user "openuem_app"
FATAL:  no pg_hba.conf entry for host "10.0.0.5", user "openuem_app", database "openuem"
could not connect to server: Connection refused
FATAL:  database "openuem" does not exist
```

## Exercise 5 — Schema ခွင့်ပြုချက်

`public` schema ၏ ACL သည် အောက်ပါအတိုင်း ဖြစ်သည်။

```text
openuem_app=UC/openuem_app,postgres=CTc/postgres
```

`openuem_app` သည် table ဖန်တီးခွင့် (create) ရှိသလား။ `readonly_user`
အတွက် ခွင့်ပြုချက် ရှိသလား။

## Exercise 6 — Backup/Restore runbook အစဉ်

အောက်ပါ အဆင့်ငါးခုကို မှန်ကန်သော အစဉ်ဖြင့် စီပါ။

```text
pg_restore -d openuem_restore
start OpenUEM services
pg_dump -Fc openuem
stop OpenUEM services
createdb openuem_restore
```
