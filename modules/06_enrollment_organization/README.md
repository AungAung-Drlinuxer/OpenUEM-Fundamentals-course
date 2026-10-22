# Module 06 — Enrollment and Organization

အခန်းဤတွင် agent တစ်ခုကို စီမံခန့်ခွဲမှု အတွင်း တရားဝင် လက်ခံပုံ၊ ထို လက်ခံမှုနှင့် တွဲဖက်
ထုတ်ပေးသော certificate၊ report ကြိမ်နှုန်း၊ organization နှင့် site ဖွဲ့စည်းပုံ၊ tag နှင့် note၊
user အကောင့် လုပ်ငန်းစဉ်၊ CSV bulk import နှင့် အုပ်ချုပ်သူ အခန်းကဏ္ဍ ခွဲခြားမှု တို့ကို
လေ့လာရသည်။

## ရည်မှန်းချက်

အခန်းဤကို ပြီးဆုံးပါက အောက်ပါ အရည်အချင်းများ ရရှိမည် —

- Agent ၏ အခြေအနေ သုံးမျိုး (Waiting for admission၊ Enabled၊ Disabled) နှင့် တစ်မျိုးစီတွင်
  ခွင့်ပြုထားသော လုပ်ဆောင်ချက်များကို ရှင်းပြနိုင်ခြင်း။
- Admission လုပ်ငန်းစဉ် နှင့် automatic admission ရွေးချယ်မှု၏ အန္တရာယ် ကို သိရှိခြင်း။
- Admission အချိန်တွင် ထုတ်ပေးသော `server.cer`/`server.key` အတွဲ၏ တာဝန် ကို ဖော်ပြနိုင်ခြင်း။
- Report ကြိမ်နှုန်း 60 မိနစ် နှင့် force report ၏ ကွာခြားချက် ကို နားလည်ခြင်း။
- Organization နှင့် site တည်ဆောက်ပုံ၊ default organization ဖျက်၍ မရခြင်း တို့ကို ရှင်းပြနိုင်ခြင်း။
- User အကောင့်၏ အဆင့် လေးဆင့် နှင့် CSV import ၏ အန္တရာယ် ကို သိရှိခြင်း။
- Least privilege သဘောတရား အရ role ခွဲဝေမှု ကို အကဲဖြတ်နိုင်ခြင်း။

## ဖိုင် ဖွဲ့စည်းပုံ

| ဖိုင် | အကြောင်းအရာ |
|---|---|
| `README.md` | အခန်း အကျဉ်းချုပ် နှင့် ရည်မှန်းချက် |
| `explanation.md` | အဓိက သင်ခန်းစာ (Figure ၂ ခု အပါအဝင်) |
| `exercise.md` | လေ့ကျင့်ခန်း ၆ ခု |
| `solution.md` | အဖြေများ နှင့် lab output |
| `lab.py` | Python standard library သာ အသုံးပြုသော lab |

## Lab အကြောင်း

Lab သည် ကွန်ရက် သို့မဟုတ် OpenUEM server ကို မလိုအပ်ပါ။ Fixture ဒေတာဖြင့် console ၏
စာရင်း စီမံမှု ကို ပုံဖော်သည်။ Exercise တစ်ခုစီသည် မိမိ သင်ပေးသော စည်းမျဉ်း ကို assert
ဖြင့် စစ်ဆေးပြီးမှ `[OK]` လိုင်း ကို ထုတ်သည်။

```bash
python3 modules/06_enrollment_organization/lab.py
```

မျှော်လင့်သော အဆုံးသတ် လိုင်း —

```text
[PASS] All 6/6 exercises passed successfully.
```

Lab သည် အချိန်၊ လမ်းကြောင်း သို့မဟုတ် ကျပန်း တန်ဖိုး များကို မထုတ်သဖြင့် run တစ်ခုနှင့်
တစ်ခု၏ output သည် တူညီသည်။

## လေ့ကျင့်ခန်း ခြုံငုံသုံးသပ်ချက်

| # | ခေါင်းစဉ် | အဓိက ကျွမ်းကျင်မှု |
|---|---|---|
| 1 | State transition validation | အခြေအနေ ပြောင်းလဲမှု စည်းမျဉ်း စစ်ဆေးခြင်း |
| 2 | Admission queue summary | စောင့်ဆိုင်းနေသော agent စာရင်း အနှစ်ချုပ် |
| 3 | Organization and site resolution | Default နှင့် site သတ်မှတ်မှု ဖြေရှင်းခြင်း |
| 4 | CSV import validation | ထပ်နေမှု နှင့် site ပျောက်ဆုံးမှု စစ်ဆေးခြင်း |
| 5 | Capability matrix | Least privilege အရ role ရွေးချယ်ခြင်း |
| 6 | Certificate lifecycle | Certificate အခြေအနေ လမ်းကြောင်း စစ်ဆေးခြင်း |

## ကြိုတင် လိုအပ်ချက်

- Module 05 ကို ပြီးစီးထားခြင်း (agent install နှင့် certificate နေရာချထားမှု)
- Python 3.10 သို့မဟုတ် အထက်
- Console သို့ ဝင်ရောက်နိုင်သော စမ်းသပ်ခန်း တစ်ခု (လေ့လာရန် အတွက်သာ၊ lab အတွက် မလိုအပ်)

## သတိပြုရန်

- Console menu အမည်များ၊ role အမည်များ နှင့် identity provider စာရင်းသည် version အလိုက်
  ပြောင်းလဲနိုင်သည်။ `explanation.md` ၏ Technical review notes တွင် မှတ်သားထားသည်။
- စာတမ်းထဲ ပါသော command output များသည် `# simulated output — illustrative` ဟု
  အမှတ်အသား ပြုထားသော fixture များ ဖြစ်သည်။
