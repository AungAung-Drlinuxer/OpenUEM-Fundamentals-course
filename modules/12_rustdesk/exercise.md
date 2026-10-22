# Module 12 — Exercises

RustDesk deployment နှင့် ချိတ်ဆက်မှု ဆိုင်ရာ လေ့ကျင့်ခန်း ခြောက်ခု။

```bash
python3 modules/12_rustdesk/lab.py
```

## Exercise 1 — Port စစ်ဆေးမှု

RustDesk server အတွက် မဖြစ်မနေ လိုအပ်သော port များမှာ 21115/TCP၊
21116/TCP၊ 21116/UDP နှင့် 21117/TCP ဖြစ်သည်။ ဖွင့်ထားသော port များမှာ
21115/TCP၊ 21116/TCP၊ 21116/UDP နှင့် 21117/TCP ဖြစ်သည်။
မဖြစ်မနေ port အားလုံး ဖွင့်ပြီးပြီလား။ Web client port များ ဖွင့်ထားသလား။

## Exercise 2 — Public key စစ်ဆေးမှု

Key သုံးခုကို စစ်ပါ။ မှန်ကန်သော key သည် base64 ဖြစ်ပြီး decode လုပ်သည့်အခါ
byte ၃၂ လုံး ရရမည်။

```text
key A: base64 of 32 bytes  (length 44)
key B: base64 of "too-short"
key C: this-is-not-base64!!
```

## Exercise 3 — Client config ပြည့်စုံမှု

Client config တွင် `id_server` နှင့် `key` မဖြစ်မနေ လိုအပ်သည်။
`relay_server` နှင့် `api_server` သည် ရွေးချယ်နိုင်သည်။ အောက်ပါ
config သုံးခုအနက် မည်သည့်အခု မပြည့်စုံသနည်း။

```text
good:        id_server=hbbs.example.com, key=valid, relay=, api=
missing-key: id_server=hbbs.example.com, key=,      relay=, api=
pro:         id_server=hbbs.example.com, key=valid, relay=hbbr.example.com, api=https://api.example.com
```

## Exercise 4 — ချိတ်ဆက်မှု လမ်းကြောင်း

Endpoint သုံးခုအတွက် လမ်းကြောင်းကို ဆုံးဖြတ်ပါ —
တိုက်ရိုက် (direct)၊ relay မှတစ်ဆင့် (relay) သို့မဟုတ် မရ (blocked)။

```text
ws-001  same_subnet=true   relay_available=false
ws-020  same_subnet=false  relay_available=true
ws-030  same_subnet=false  relay_available=false
```

## Exercise 5 — OpenUEM org settings

Organization ၏ RustDesk settings တွင် `id_server`၊ `relay_server` နှင့် `key`
ထည့်ထားပြီး permanent password ကို ဖွင့်ထားသည်။ Setting ပြည့်စုံသလား။
Password mode က ဘာဖြစ်သနည်း။

## Exercise 6 — OS permission

Target endpoint ၏ platform အလိုက် လိုအပ်သော permission များမှာ —

```text
Windows: rustdesk-service
Linux:   x11-session-or-wayland-portal
macOS:   screen-recording, accessibility
```

Host တွင် Windows နှင့် Linux အတွက် permission အားလုံး ရှိပြီး macOS တွင်
မရှိပါ။ မည်သည့် permission လိုနေသနည်း။
