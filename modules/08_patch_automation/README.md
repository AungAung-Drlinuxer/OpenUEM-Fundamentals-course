# Module 08 — Patch management and automation

ဤ module သည် OpenUEM ဖြင့် endpoint များ၏ update အခြေအနေကို မြင်နိုင်ခြင်း၊ patch လုပ်ငန်းစဉ်ကို အဆင့်လိုက် စီစဉ်ခြင်း၊ maintenance window နှင့် change control ကို ချိတ်ဆက်ခြင်း၊ deployment ပြီးနောက် စစ်ဆေးခြင်းနှင့် compliance ကို တိုင်းတာခြင်းတို့ကို သင်ပေးသည်။

## ကြိုတင်လိုအပ်ချက်

- Module 05 (agent deployment) နှင့် Module 06 (enrollment) ပြီးစီးထားရန်။
- Module 07 (device management basics) ၏ profile နှင့် task အခြေခံသဘောတရား ရှိထားရန်။
- Enabled state ရှိသော agent အနည်းဆုံး တစ်ခု (သို့မဟုတ်) `lab.py` run ရန် Python 3 သာ။

## သင်ယူပြီးနောက် ရရှိမည့် စွမ်းရည်

1. Windows security view ရှိ update အချက်လေးရပ်ကို ဖတ်ပြီး မည်သည့် အချက်က မူဝါဒဆိုင်ရာ၊ မည်သည့် အချက်က အခြေအနေဆိုင်ရာ ဖြစ်သည်ကို ခွဲခြားနိုင်ခြင်း။
2. Linux pending security updates ကို Windows ၏ KB အခြေအနေနှင့် နှိုင်းယှဉ်နိုင်ခြင်း။
3. Detect → stage → deploy → verify လုပ်ငန်းစဉ်ကို wave အလိုက် စီစဉ်နိုင်ခြင်း။
4. Maintenance window တစ်ခုကို timezone offset အလိုက် အကဲဖြတ်နိုင်ခြင်း။
5. Validation matrix ဆွဲပြီး deployment ရလဒ်ကို တိုင်းတာနိုင်ခြင်း။
6. Rollback မရှိသော အခြေအနေတွင် snapshot၊ wave နှင့် package ဖျက်ခြင်းဖြင့် ပြန်လည်ထူထောင်ရေး စီစဉ်နိုင်ခြင်း။
7. Compliance ရာခိုင်နှုန်းနှင့် exception စာရင်းကို တွဲဖတ်နိုင်ခြင်း။

## ဖိုင်များ

| ဖိုင် | အကြောင်းအရာ |
|---|---|
| `README.md` | ဤ လမ်းညွှန် |
| `explanation.md` | အခြေခံသဘောတရား၊ ပုံနှစ်ခု၊ လုပ်ငန်းစဉ် အဆင့်များ၊ ကိုယ်တိုင် စစ်ဆေးမေးခွန်း |
| `exercise.md` | လေ့ကျင့်ခန်း ခြောက်ခု၏ လုပ်ဆောင်ရန် စာရင်း |
| `solution.md` | အဖြေများနှင့် `lab.py` ၏ အမှန်တကယ် output |
| `lab.py` | Standard library သာ အသုံးပြုသော တွက်ချက်မှု lab |

## Lab run ခြင်း

```bash
# module ဖိုင် run သည် — fixture များသာ အသုံးပြုပြီး ကွန်ရက် မလိုအပ်ပါ
python3 modules/08_patch_automation/lab.py
```

Lab သည် အပြင်အပြင် အခြေအနေ မလိုအပ်ပါ။ ကွန်ရက် မသုံးပါ။ အချိန်ကို ဖတ်ခြင်း မရှိပါ။ ထို့ကြောင့် run တစ်ကြိမ်နှင့် တစ်ကြိမ် output သည် တူညီသည်။

## လေ့ကျင့်ခန်း မြေပုံ

| လေ့ကျင့်ခန်း | ခေါင်းစဉ် | ကျင့်သုံးသော သဘောတရား |
|---|---|---|
| 1 | Pending update စာရင်း ခွဲခြမ်းစိတ်ဖြာခြင်း | Security view မှ အရေအတွက် စုစည်းခြင်း |
| 2 | Maintenance window ရရှိနိုင်မှု တွက်ချက်ခြင်း | Timezone offset နှင့် သန်းခေါင်ကျော် window |
| 3 | Criticality အလိုက် patch wave စီစဉ်ခြင်း | Wave စည်းမျဉ်းနှင့် window ကြာချိန် |
| 4 | Validation matrix အကဲဖြတ်ခြင်း | Deployment ပြီးနောက် စစ်ဆေးချက် ငါးခု |
| 5 | Compliance ရာခိုင်နှုန်း တွက်ချက်ခြင်း | Fleet rate နှင့် endpoint rate ကွာခြားချက် |
| 6 | Automation trigger ရွေးချယ်ခြင်း | Profile၊ deployment နှင့် report ရွေးချယ်မှု |

## အချိန် ခန့်မှန်းချက်

| အပိုင်း | အချိန် |
|---|---|
| `explanation.md` ဖတ်ခြင်း | မိနစ် 40 |
| လေ့ကျင့်ခန်း ခြောက်ခု | မိနစ် 70 |
| ပြန်လည်သုံးသပ်ခြင်း | မိနစ် 20 |

## သတိပြုရန်

- ဤ module ၏ ကိန်းဂဏန်း အားလုံးသည် သရုပ်ပြ fixture ဖြစ်သည်။ OpenUEM console ၏ တိုင်းတာချက် မဟုတ်ပါ။
- Study ကွန်ပျူတာများတွင် OpenUEM မတပ်ဆင်ထားပါ။ Command များသည် documentation မှ ရယူထားသော စစ်မှန်သည့် command များ ဖြစ်ပြီး output များသည် သရုပ်ပြ ဖြစ်သည်။
- OpenUEM သည် OS update အတွက် အပြည့်အဝ patch orchestrator မဟုတ်ပါ။ Update အခြေအနေကိုြသခြင်းနှင့် တပ်ဆင်မှု ဆုံးဖြတ်ချက်ကို လူက ချခြင်း ဖြစ်သည်။ ဤ အချက်ကို `explanation.md` ၏ နောက်ဆုံးပိုင်းတွင် အသေးစိတ် ရှင်းပြထားသည်။

## နောက်ဆက်တွဲ module

Module 08 တွင် ဤ module ၏ compliance အချက်အလက်များကို အစီရင်ခံစာအဖြစ် မည်သို့ တင်ပြမည်၊ ပြဿနာများကို မည်သို့ ရှာဖွေမည်ကို ဆက်လက် လေ့လာမည်။
