# Module 03 — Installing OpenUEM on Ubuntu 24.04 Server

Ubuntu 24.04 Server host တစ်ခုပေါ်တွင် OpenUEM server ကို native package ဖြင့်
အစမှ အဆုံး တည်ဆောက်သည့် module ဖြစ်သည်။ apt repository ထည့်ခြင်းမှ စ၍
certificate ဖန်တီးခြင်း၊ `/etc/openuem-server/openuem.ini` ရေးခြင်း၊ service
များကို documentation အစီအစဉ်အတိုင်း စတင်ခြင်း၊ `systemctl status` နှင့်
console URL ဖြင့် စစ်ဆေးခြင်း၊ reverse proxy အောက်သို့ ထားရှိခြင်း နှင့်
hardening အထိ အဆင့်ဆင့် လိုက်ပါသည်။

## သင်ယူပြီးပါက ရရှိမည့် စွမ်းရည်များ

| # | စွမ်းရည် |
|---|---|
| 1 | Ubuntu 24.04 တွင် OpenUEM apt repository ထည့်ပြီး component package အားလုံး install လုပ်နိုင်ခြင်း |
| 2 | Package တစ်ခုချင်းစီ၏ တာဝန်နှင့် inbound port ကို ခွဲခြားနိုင်ခြင်း |
| 3 | Certificate tree ဖန်တီးပြီး `openuem-cert-manager client-cert` ဖြင့် certificate ထုတ်နိုင်ခြင်း |
| 4 | `openuem.ini` ၏ `[Console]` နှင့် `[JWT]` section ကို ရေးနိုင်ခြင်း |
| 5 | Service ခုနစ်ခုကို အစီအစဉ်လိုက် စတင်ပြီး `systemctl status`၊ `ss`၊ console URL ဖြင့် စစ်ဆေးနိုင်ခြင်း |
| 6 | Caddy သို့မဟုတ် nginx ဖြင့် console ကို proxy အောက်တွင် ထားနိုင်ခြင်း |
| 7 | `openuem` user၊ `600` key permission နှင့် CA backup ဖြင့် hardening လုပ်နိုင်ခြင်း |

## လိုအပ်ချက်များ

- **Module 02 ပြီးစီးထားရမည်။** PostgreSQL database `openuem`၊ role နှင့်
  connection URI ကို ထို module တွင် ဖန်တီးထားသည်။ ဤ module တွင် ထို အလုပ်များကို
  ထပ်မံ မဖော်ပြပါ။
- Ubuntu 24.04 Server host တစ်ခု၊ `sudo` အာဏာ နှင့် systemd
- Console၊ NATS နှင့် OCSP အတွက် DNS အမည် (သို့မဟုတ် lab တွင် hosts file)
- Port 1323၊ 1324၊ 4433 နှင့် 8000 အလွတ် ဖြစ်မှု
- Lab များ run ရန် Python 3.10 သို့မဟုတ် အထက် (OpenUEM server မလိုအပ်)

## ဖိုင်များ

| ဖိုင် | အကြောင်းအရာ |
|---|---|
| `README.md` | module မိတ်ဆက်၊ ရည်မှန်းချက်၊ လိုအပ်ချက် |
| `explanation.md` | အဆင့်ဆင့် ရှင်းလင်းချက်၊ ပုံ ၃ ခု၊ စစ်ဆေးမေးခွန်း ၆ ခု |
| `exercise.md` | လေ့ကျင့်ခန်း ၆ ခု |
| `solution.md` | အဖြေများ နှင့် lab ၏ တကယ့် output |
| `lab.py` | Python standard library သက်သက်ဖြင့် ရေးထားသော deterministic lab |

## Lab ကို run ခြင်း

```bash
python3 modules/03_ubuntu_server/lab.py
```

Lab သည် network၊ OpenUEM server သို့မဟုတ် database ကို မချိတ်ဆက်ပါ။ Fixture
များနှင့် တွက်ချက်မှုသာ ဖြစ်သည်။ လေ့ကျင့်ခန်း ၆ ခုမှာ အောက်ပါအတိုင်း ဖြစ်သည်။

| Exercise | အဓိက ကျွမ်းကျင်မှု |
|---|---|
| 1 | Package မှ component role သို့ ပုံဖော်ခြင်း |
| 2 | Service စတင်သည့် အစီအစဉ် စစ်ဆေးခြင်း |
| 3 | `openuem.ini` ကို section အလိုက် ခွဲခြမ်းခြင်း |
| 4 | `--years-valid` မှ သက်တမ်းကုန်ဆုံးရက် တွက်ချက်ခြင်း |
| 5 | Console/Auth/NATS/OCSP port ထပ်နေမှု ရှာခြင်း |
| 6 | Port စီမံချက်မှ firewall စည်းမျဉ်း ထုတ်ခြင်း |

## မှတ်ချက်

- ဤ စာမျက်နှာများထဲက command output အားလုံးသည်
  `# simulated output — illustrative` ဟု အမှတ်အသားပြုထားသည့် ပုံစံပြ fixture
  များ ဖြစ်သည်။ သင့်စက်၏ တကယ့် output မဟုတ်။
- Package version နှင့် အတိအကျ repository line များသည် release အလိုက်
  ပြောင်းနိုင်သည်။ ထို အချက်များကို `explanation.md` ၏
  `Technical review notes` တွင် မှတ်သားထားသည်။
- Docker/Podman compose လမ်းကြောင်းကို ဤ course ၏ သီးခြား module တွင်
  ဖော်ပြထားသည်။
