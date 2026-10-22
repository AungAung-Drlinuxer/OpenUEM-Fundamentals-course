# Module 05 — Agent deployment

ဤ module သည် OpenUEM agent ကို endpoint များပေါ်တွင် ထည့်သွင်းခြင်း, certificate များ ထားရှိခြင်း, port လိုအပ်ချက် ဖြည့်ဆည်းခြင်း နှင့် ပြဿနာများကို log မှ ခွဲခြားခြင်းကို သင်ကြားသည်။ Server ဘက်သည် အသင့် ဖြစ်နေသော်လည်း agent မရှိပါက endpoint တစ်ခုကို စီမံခန့်ခွဲနိုင်ခြင်း မရှိပါ။ ထို့ကြောင့် ဤ module သည် သင်တန်း တစ်ခုလုံး၏ လက်တွေ့ အခြေခံအုတ်မြစ် ဖြစ်သည်။

## သင်ယူပြီးနောက် ရရှိမည့် စွမ်းရည်များ

- Agent ၏ အလုပ်သံသရာ (report ပေးပို့ခြင်း, မိနစ် 30 တစ်ကြိမ် profile စစ်ဆေးခြင်း) ကို ရှင်းပြနိုင်ခြင်း။
- Agent တစ်ခုစီတွင် လိုအပ်သည့် certificate ဖိုင် လေးခုကို ခွဲခြားနိုင်ခြင်း နှင့် platform အလိုက် တည်နေရာကို သိရှိခြင်း။
- Windows တွင် `/VERYSILENT` flag များဖြင့် တိတ်ဆိတ်စွာ install လုပ်နိုင်ခြင်း။
- Debian နှင့် RPM မိသားစုတွင် install လုပ်ပြီးနောက် certificate ထားရှိခြင်း နှင့် service များ ပြန်လည် စတင်ခြင်း။
- Firewall အတွက် လိုအပ်သည့် port များကို စာရင်းချနိုင်ခြင်း။
- `openuem-log.txt` မှ keyword အလိုက် ပြဿနာကို ခွဲခြားနိုင်ခြင်း။
- Upgrade တစ်ခု၏ အန္တရာယ်ကို အဆင့်သတ်မှတ်နိုင်ခြင်း။

## ကြိုတင်လိုအပ်ချက်များ

- Module 01 — OpenUEM ၏ component များ နှင့် port အခြေခံ သဘောတရား။
- Module 02 — NATS, PostgreSQL နှင့် container အခြေခံ လက်တွေ့ ပတ်ဝန်းကျင်။
- Module 03 — Server installation နှင့် certificate ဖန်တီးခြင်း။
- Python 3 standard library ဖြင့် script run နိုင်သည့် စက်တစ်လုံး။ (OpenUEM install လုပ်ထားရန် မလိုအပ်ပါ။)

## ဖိုင်များ

| ဖိုင် | အကြောင်းအရာ |
| --- | --- |
| `README.md` | Module ၏ ရည်ရွယ်ချက် နှင့် လမ်းညွှန် |
| `explanation.md` | အယူအဆ, ပုံများ, platform အလိုက် လုပ်ငန်းစဉ် နှင့် ကိုယ်တိုင်စစ်ဆေးရန် မေးခွန်းများ |
| `exercise.md` | လေ့ကျင့်ခန်း ခြောက်ခု |
| `solution.md` | လေ့ကျင့်ခန်း ခြောက်ခု၏ အဖြေ နှင့် lab output |
| `lab.py` | Standard library သာ အသုံးပြုသည့်, အော့ဖ်လိုင်း run နိုင်သည့် lab |

## Lab ကို run ခြင်း

```bash
python3 modules/05_agent_deployment/lab.py
```

Lab သည် exercise ခြောက်ခုကို အစဉ်လိုက် run ပြီး တစ်ခုချင်းစီအတွက် `[OK]` စာကြောင်း နှင့် အဆုံးတွင် `[PASS]` စာကြောင်းကို ပြသည်။ Output သည် run တစ်ကြိမ်နှင့် တစ်ကြိမ် ထပ်တူညီသည်။ မည်သည့် network ချိတ်ဆက်မှုကိုမျှ မပြုလုပ်ပါ။

Lab ကို ကိုယ်တိုင် ပြင်ဆင်ပြီး run လိုပါက တစ်ခုချင်း exercise ကို ခေါ်နိုင်သည်။

```bash
python3 -c "import importlib.util,sys; spec=importlib.util.spec_from_file_location('lab','modules/05_agent_deployment/lab.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.exercise_1()"
```

## Output နှင့် ပတ်သက်သည့် သတိပြုချက်

`explanation.md` ရှိ OpenUEM command များသည် official documentation မှ ကူးယူထားသည့် အမှန်တကယ် command များ ဖြစ်သည်။ သို့သော် ၎င်းတို့၏ output များသည် `# simulated output — illustrative` ဟု အမှတ်အသား ပါသည့် သရုပ်ပြ ဖိုင် ဖြစ်ပြီး တိုင်းတာရရှိသည့် ရလဒ် မဟုတ်ပါ။ `solution.md` ရှိ output များမှာမူ `lab.py` ကို အမှန်တကယ် run ခြင်း၏ ရလဒ် ဖြစ်သည်။

## ဤ module တွင် မပါဝင်သည့် အကြောင်းအရာများ

- Admission ပြုလုပ်ခြင်း နှင့် organization, site, tag များ စီမံခြင်း — Module 05။
- Inventory tab များ, package deployment နှင့် profile အသေးစိတ် — Module 07။
- Patch management နှင့် automation — Module 08။
- Dashboard triage နှင့် အဆင့်လိုက် ချိတ်ဆက်မှု စစ်ဆေးခြင်း — Module 09။

## အကြံပြုသည့် အစီအစဉ်

1. `explanation.md` ကို ဖတ်ပြီး Figure 1 မှ Figure 3 အထိ လုပ်ငန်းစဉ်ကို နားလည်အောင် ပြုလုပ်ပါ။
2. ကိုယ်တိုင်စစ်ဆေးရန် မေးခွန်း ငါးခုကို ဖြေကြည့်ပါ။
3. `exercise.md` ရှိ လေ့ကျင့်ခန်း ခြောက်ခုကို အစဉ်လိုက် လုပ်ပါ။
4. Lab run ပြီး `[PASS]` စာကြောင်း ရရှိကြောင်း စစ်ဆေးပါ။
5. `solution.md` နှင့် နှိုင်းယှဉ်ပါ။
