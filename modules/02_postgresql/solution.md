# Module 02 — Solutions

အောက်ပါ output များသည် `python3 modules/02_postgresql/lab.py` ၏
တကယ့် output ဖြစ်သည်။

## Exercise 1 — `.env` လိုအပ်ချက် စစ်ဆေးခြင်း

`DATABASE_PASSWORD` နှင့် `OPENUEM_DATABASE_URL` မပါဝင်ပါ။
လိုအပ်သော key ငါးခုအနက် သုံးခုသာ ပြည့်စုံသဖြင့် `.env` ကို မသုံးနိုင်ပါ။
`OPENUEM_DATABASE_URL` မရှိပါက component များ database ကို မချိတ်ဆက်နိုင်ပါ။

```text
[OK] exercise_1 — env validation: 3/5 required keys present; missing=DATABASE_PASSWORD,OPENUEM_DATABASE_URL
```

## Exercise 2 — URI percent-encoding

`=` ကို `%3D`၊ `@` ကို `%40` ဟု ကုဒ်ပြောင်းသည်။
ရလဒ်မှာ `te%3Dst%40lab` ဖြစ်ပြီး URI ကို host `localhost`၊ port `5432`၊
database `openuem` ဖြင့် တည်ဆောက်နိုင်သည်။

```text
[OK] exercise_2 — uri encoding: te=st@lab -> te%3Dst%40lab; host=localhost port=5432 db=openuem
```

## Exercise 3 — `pg_hba.conf` ဆုံးဖြတ်ချက်

`127.0.0.1/32` အတွက် ဒုတိယ rule ကိုက်ညီသဖြင့် `scram-sha-256` ဖြစ်သည်။
`10.0.0.5/32` အတွက် ကိုက်ညီသော rule မရှိသဖြင့် ချိတ်ဆက်မှုကို ငြင်းပယ်သည်။
Local socket အတွက် ပထမ rule ဖြစ်သော `peer` ကို သုံးသည်။

```text
[OK] exercise_3 — pg_hba: 127.0.0.1/32=scram-sha-256, 10.0.0.5/32=reject, local=peer
```

## Exercise 4 — Error အမျိုးအစားခွဲခြား

စာသားထဲက အဓိကစကားလုံးကို ကြည့်ပြီး အကြောင်းရင်းကို ခွဲသည်။
`password authentication failed` သည် credential၊ `no pg_hba.conf entry` သည်
rule မရှိခြင်း၊ `Connection refused` သည် service မပွင့်ခြင်း၊
`does not exist` သည် database အမည် မှားခြင်း ဖြစ်သည်။

```text
[OK] exercise_4 — error causes: credentials,hba-rule,service-or-port,wrong-database
```

## Exercise 5 — Schema ခွင့်ပြုချက်

ACL တွင် `openuem_app=UC/openuem_app` ဟု ပါဝင်သဖြင့် `U` (usage) နှင့်
`C` (create) နှစ်ခုလုံး ရှိသည်။ `readonly_user` အတွက် entry မရှိသဖြင့်
ခွင့်ပြုချက် မရှိပါ။

```text
[OK] exercise_5 — schema privileges: openuem_app=UC create=True; readonly_user=none
```

## Exercise 6 — Backup/Restore runbook အစဉ်

Service များကို ရပ်ပြီးမှ dump ယူရသည်။ Dump ပြီးနောက် restore အတွက်
database အသစ် ဖန်တီးပြီး `pg_restore` ကို run သည်။ အဆုံးတွင် service များ
ပြန်စတင်သည်။

```text
[OK] exercise_6 — runbook order: stop OpenUEM services -> pg_dump -Fc openuem -> createdb openuem_restore -> pg_restore -d openuem_restore -> start OpenUEM services
```
