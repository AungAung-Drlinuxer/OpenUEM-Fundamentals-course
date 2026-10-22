# Module 09 — Reporting နှင့် Troubleshooting

ဤ module သည် OpenUEM console မှ အထောက်အထား ထုတ်ယူခြင်း (report) နှင့်
ချို့ယွင်းမှု ဖြေရှင်းခြင်း (troubleshooting) ကို တွဲဖက် သင်ကြားသည်။
ရည်ရွယ်ချက်မှာ တစ်ခုတည်း ဖြစ်သည် — ပြင်ဆင်မှု တစ်ခု မလုပ်မီ အထောက်အထား
ရယူနိုင်ခြင်း၊ ထို အထောက်အထားကို အလွှာလိုက် ခွဲခြမ်းနိုင်ခြင်း ဖြစ်သည်။

## သင်ယူရမည့် အချက်များ

- agents, computers, security နှင့် software view လေးခုမှ PDF/CSV report
  ထုတ်ယူခြင်း၊ filter နှင့် sort ကို report တွင် ထိန်းသိမ်းခြင်း
- dashboard ၏ ကဏ္ဍသုံးခု (red, green, blue) နှင့် ငါးမိနစ် refresh စည်းချက်
- component ကျန်းမာရေး စစ်ဆေးခြင်း — console, NATS, worker များ, PostgreSQL, OCSP
- အလွှာလိုက် ဆက်သွယ်မှု စစ်ဆေးခြင်း — endpoint → NATS (4433) → worker →
  PostgreSQL → console (1323/1324) → OCSP (8000)
- မကြာခဏ တွေ့ရသော ချို့ယွင်းမှု ရှစ်မျိုး၏ လက္ခဏာ နှင့် ပထမဆုံး စစ်ဆေးရမည့် အချက်
- log ရင်းမြစ်များ — agent ၏ `openuem-log.txt` (SFTP မှတစ်ဆင့်) နှင့် server
  ပေါ်ရှိ component log များ
- user invitation နှင့် registration mail အတွက် SMTP လိုအပ်ချက်
- ပြင်ပ monitoring နှင့် ချိတ်ဆက်ခြင်းကို operational pattern အဖြစ် တည်ဆောက်ခြင်း

## ကြိုတင် လိုအပ်ချက်

Module 01 မှ 07 အထိ ပြီးစီးထားရသည်။ အထူးသဖြင့် port များ (4433, 1323,
1324, 8000, 2022, 1443) နှင့် certificate တည်နေရာများကို ရင်းနှီးထားရသည်။

## ဖိုင်များ

| ဖိုင် | အကြောင်းအရာ |
|---|---|
| `README.md` | ဤ မိတ်ဆက် နှင့် လမ်းညွှန် |
| `explanation.md` | အယူအဆ ရှင်းလင်းချက်၊ ပုံလေးခု၊ ကုဒ်နမူနာများ |
| `exercise.md` | လေ့ကျင့်ခန်း ခြောက်ခု၏ တာဝန်များ |
| `solution.md` | ဖြေရှင်းချက် နှင့် `lab.py` ၏ တကယ့် output |
| `lab.py` | Python standard library သီးသန့်၊ offline lab |

## Lab ကို လုပ်ဆောင်ခြင်း

```bash
cd /path/to/OpenUEM-Fundamentals-course
python3 modules/09_reporting_troubleshooting/lab.py
```

Lab သည် ကွန်ရက် မ လိုအပ်။ fixture ဒေတာဖြင့် report filter, dashboard
ဦးစားပေး, အလွှာလိုက် စစ်ဆေးမှု, log ခွဲခြားမှု, MTTR တွက်ချက်မှု နှင့်
alert rule တိုက်ဆိုင်မှုကို လေ့ကျင့်သည်။ အောင်မြင်ပါက နောက်ဆုံး လိုင်းတွင်

```text
[PASS] All 6/6 exercises passed successfully.
```

ပေါ်လာမည်။ အသုံးပြုချိန် ခန့်မှန်းချက် — ဖတ်ရှုခြင်း ၄၅ မိနစ်၊
လေ့ကျင့်ခန်း ၉၀ မိနစ်။

## မှတ်ချက်

ဤ module ၏ command များသည် တကယ့် OpenUEM command များ ဖြစ်သည်။
သို့သော် output အားလုံးသည် သရုပ်ပြ fixture ဖြစ်ပြီး
`# simulated output — illustrative` ဟု အမှတ်အသား တပ်ထားသည်။
သင်တန်း ကွန်ပျူတာများတွင် OpenUEM မ တပ်ဆင်ထားပါ။
