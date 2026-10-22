# Module 12 — Solutions

အောက်ပါ output များသည် `python3 modules/12_rustdesk/lab.py` ၏ တကယ့် output
ဖြစ်သည်။

## Exercise 1 — Port စစ်ဆေးမှု

မဖြစ်မနေ port လေးခုလုံး ဖွင့်ပြီး ဖြစ်သည်။ Web client အတွက် 21118 နှင့်
21119 မဖွင့်ထားသဖြင့် ထို port များမှ တစ်ဆင့် ဝင်နိုင်မည် မဟုတ်ပါ။

```text
[OK] exercise_1 — required ports open: 4/4; web ports open: 0
```

## Exercise 2 — Public key စစ်ဆေးမှု

Key A သည် byte ၃၂ လုံး ဖြစ်သဖြင့် မှန်သည်။ Key B သည် decode လုပ်နိုင်သော်လည်း
အရှည် မမှန်ပါ။ Key C သည် base64 မဟုတ်ပါ။

```text
[OK] exercise_2 — key checks: ok,wrong-length,not-base64; key_length=44
```

## Exercise 3 — Client config ပြည့်စုံမှု

`missing-key` တွင် key မပါသဖြင့် encrypt လုပ်နိုင်မည် မဟုတ်ပါ။
`relay_server` နှင့် `api_server` မပါခြင်းသည် အမှား မဟုတ်ပါ။

```text
[OK] exercise_3 — config: good=complete, pro=complete, missing-key=key; relay_server=optional
```

## Exercise 4 — ချိတ်ဆက်မှု လမ်းကြောင်း

ws-001 သည် တူညီသော subnet တွင် ရှိသဖြင့် တိုက်ရိုက် ချိတ်ဆက်နိုင်သည်။
ws-020 သည် တိုက်ရိုက် မရသော်လည်း relay ရှိသဖြင့် ချိတ်ဆက်နိုင်သည်။
ws-030 တွင် relay မရှိသဖြင့် မချိတ်ဆက်နိုင်ပါ။

```text
[OK] exercise_4 — routes: ws-001=direct, ws-020=relay, ws-030=blocked
```

## Exercise 5 — OpenUEM org settings

Setting သုံးခုလုံး ပြည့်စုံသည်။ Permanent password ဖွင့်ထားသဖြင့်
ချိတ်ဆက်မှုတိုင်း ကျပန်း password အသစ် ဖြစ်သည်။

```text
[OK] exercise_5 — org settings complete: 3/3; password_mode=random-password-per-session
```

## Exercise 6 — OS permission

macOS တွင် Screen Recording နှင့် Accessibility နှစ်ခုလုံး လိုနေသည်။
ထို permission များ မရှိပါက မျက်နှာပြင် မမြင်ရပါ။

```text
[OK] exercise_6 — permissions: Windows=ok, Linux=ok, macOS=accessibility,screen-recording
```
