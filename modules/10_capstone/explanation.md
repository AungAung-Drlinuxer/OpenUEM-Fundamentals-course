# Module 10 — ဇာတ်လမ်းတစ်ခုလုံး: အဖွဲ့အစည်းတစ်ခုအတွက် OpenUEM ဖြန့်ကျက်ခြင်း

## ၁၀.၁ ဇာတ်လမ်း အခြေအနေ

ဤ module တွင် ခေါင်းစဉ်အသစ် မရှိပါ။ ယခင် module ရှစ်ခုတွင် သီးခြားစီ သင်ယူခဲ့သော
ကျွမ်းကျင်မှုများကို အဖွဲ့အစည်းတစ်ခု၏ လုပ်ငန်းအစီအစဉ်တစ်ခုအဖြစ် ပေါင်းစပ်
အသုံးပြုခြင်း ဖြစ်သည်။ သင်ယူသူသည် ဤ module ကို ပြီးဆုံးသောအခါ console ခလုတ်
တစ်ခုချင်းစီကို မှတ်မိရန် မလိုအပ်ပါ။ လိုအပ်သည်မှာ အစီအစဉ်တစ်ခုကို အဆင့်လိုက်
ခွဲခြားနိုင်ခြင်း၊ အဆင့်တစ်ခုစီတွင် မည်သည့် အထောက်အထား လိုအပ်သည်ကို သိရှိခြင်း
နှင့် ပြဿနာတစ်ခု ဖြစ်ပေါ်သောအခါ ရရှိထားသော အချက်အလက်များမှ ကောက်ချက်ချ
နိုင်ခြင်း ဖြစ်သည်။

ဇာတ်လမ်းတွင် ပါဝင်သော အဖွဲ့အစည်းမှာ `openuem.example` ဖြစ်သည်။ ဌာနချုပ်
(head office) သည် ရန်ကုန်တွင် တည်ရှိပြီး ဌာနခွဲ (branch) သည် မန္တလေးတွင်
တည်ရှိသည်။ နှစ်ခုလုံးကို OpenUEM instance တစ်ခုတည်းက စီမံသည်။ ဌာနခွဲတွင်
သီးခြား server မရှိပါ။ ဌာနခွဲ endpoint များသည် WAN မှတစ်ဆင့် ဌာနချုပ် server
သို့ ချိတ်ဆက်သည်။

| အချက် | တန်ဖိုး |
|---|---|
| Default organization | `openuem.example` |
| Head office | ရန်ကုန် — 18 endpoints (Windows 10, Linux 5, macOS 3) |
| Branch | မန္တလေး — 9 endpoints (Windows 5, Linux 3, macOS 1) |
| စုစုပေါင်း | 27 endpoints, platform သုံးမျိုး |
| Server | Linux host တစ်ခု, PostgreSQL နှင့် compose stack |
| Console URL | `console.openuem.example` (Caddy reverse proxy မှတစ်ဆင့်) |
| ဝန်ထမ်း အခန်းကဏ္ဍ | server administrator ၂ ဦး, helpdesk operator ၁ ဦး, change approver ၁ ဦး |
| Maintenance window | စနေနေ့ 01:00–05:00 (UTC+06:30) |

အခန်းကဏ္ဍ ခွဲခြားမှုသည် module 06 ၏ least privilege မူကို လိုက်နာသည်။
server administrator နှစ်ဦးသာ certificate နှင့် component setting များကို
ပြောင်းလဲနိုင်သည်။ helpdesk operator သည် endpoint တစ်ခုချင်းစီအပေါ် force
report နှင့် package deployment ကို လုပ်ဆောင်နိုင်သော်လည်း profile ဖန်တီးခြင်း
ကို မလုပ်ဆောင်နိုင်ပါ။ change approver သည် ဖြန့်ကျက်မှု အစီအစဉ်ကို အတည်ပြု
သည့်အဆင့်တွင်သာ ပါဝင်သည်။

ကန့်သတ်ချက် သုံးခုကို ဇာတ်လမ်းအစတွင် သတ်မှတ်ထားသည်။ ပထမအချက်မှာ ဌာနခွဲ
တွင် DNS server မရှိခြင်း ဖြစ်သည်။ ထို့ကြောင့် ဌာနခွဲ host များတွင် hosts
override ကို အသုံးပြုသည်။ ဒုတိယအချက်မှာ maintenance window တစ်လလျှင်
တစ်ကြိမ်သာ ရှိခြင်း ဖြစ်သည်။ တတိယအချက်မှာ ဌာနခွဲ endpoint များသည်
DNS နှင့် ကိုယ်ပိုင် IP ဖြင့် မှတ်ပုံတင်ထားသဖြင့် remote assistance, file
browsing နှင့် WOL ကို အသုံးမပြုနိုင်ခြင်း ဖြစ်သည်။ ဤကန့်သတ်ချက်သည်
module 07 တွင် ဖော်ပြထားသော remote endpoint ကန့်သတ်ချက်နှင့် တူညီသည်။

## ၁၀.၂ ယခင် module များမှ ယူလာသော အစိတ်အပိုင်းများ

Capstone တွင် အဆင့်တစ်ခုစီသည် ယခင် module တစ်ခု၏ output ကို နောက်တစ်ခု၏
input အဖြစ် အသုံးပြုသည်။ မည်သည့်အဆင့်က မည်သည့် module မှ ဆင်းသက်လာသည်ကို
အောက်ပါဇယားတွင် ဖော်ပြထားသည်။

| Module | ယူလာသော အရာ | Capstone တွင် ပေါ်လာပုံ |
|---|---|---|
| 01 | component မြေပုံ, lifecycle, port စီမံချက် | မည်သည့် service က မည်သည့် port ကို ပိုင်ဆိုင်သည်ကို ဆုံးဖြတ်ခြင်း |
| 02 | PostgreSQL, database role, compose, `.env` | ဆောက်လုပ်မှု အဆင့် P0 နှင့် P1 |
| 03 | certificate, `openuem.ini`, service အစဉ် | ဆောက်လုပ်မှု အဆင့် P2 နှင့် ဖြစ်ရပ် ပြန်လည်ထူထောင်မှု |
| 04 | platform အလိုက် agent install, log တည်နေရာ | enrollment wave တစ်ခုစီ၏ လုပ်ဆောင်ချက် |
| 05 | agent state, admission, org/site/tag | wave စီမံချက်နှင့် tag အခြေခံ စစ်ထုတ်မှု |
| 06 | inventory, package deployment, profile | software baseline ပေးပို့ခြင်း |
| 07 | patch pipeline, maintenance window, လိုက်နာမှု မက်ထရစ် | patch wave တစ်ခုတည်း၏ gate နှင့် တိုင်းတာမှု |
| 08 | report, dashboard, အလွှာလိုက် စစ်ဆေးမှု, log | ဖြစ်ရပ် ရှာဖွေမှုနှင့် သက်သေ အစုအဝေး |

ဤဇယားက ပြသည့် အဓိပ္ပာယ်မှာ ရှင်းလင်းသည်။ ယခင် module တစ်ခုကို မကျွမ်းကျင်လျှင်
capstone ၏ သက်ဆိုင်ရာ အဆင့်တွင် ရပ်တန့်မည် ဖြစ်သည်။ ဥပမာ certificate
သက်တမ်း တွက်ချက်မှုကို မသိလျှင် readiness checklist တွင် မည်သည့် အချက်က
အတားအဆီး ဖြစ်သည်ကို မဖော်ထုတ်နိုင်ပါ။ ထို အချက်သည် နောက်ပိုင်း ဖြစ်ရပ်၏
အမြစ်သို့ တိုက်ရိုက် ဆက်စပ်နေသည်။

## ၁၀.၃ ဆောက်လုပ်မှု အစီအစဉ် (build plan)

ဆောက်လုပ်မှုကို အဆင့် ခြောက်ဆင့်အဖြစ် ခွဲထားသည်။ အဆင့်တစ်ခုစီသည် ပြီးဆုံးမှ
သာ နောက်အဆင့်သို့ ကူးသည်။

| အဆင့် | ရည်မှန်းချက် | ပြီးဆုံးကြောင်း သိနည်း |
|---|---|---|
| P0 | PostgreSQL နှင့် database role အဆင်သင့် | `psql` မှ ချိတ်ဆက်၍ စစ်ဆေးနိုင်ခြင်း |
| P1 | compose stack လည်ပတ်ခြင်း | component အားလုံး healthy ဖြစ်ခြင်း |
| P2 | CA နှင့် component certificate များ | certificate tree တွင် ဖိုင် အားလုံး ရှိနေခြင်း |
| P3 | console နှင့် authentication | `console.openuem.example:1323` သို့ ဝင်ရောက်နိုင်ခြင်း |
| P4 | enrollment wave သုံးခု | endpoint 27 ခုလုံး Enabled ဖြစ်ခြင်း |
| P5 | baseline နှင့် patch wave | profile အခြေအနေ နှင့် patch တိုးတက်မှု တိုင်းတာနိုင်ခြင်း |

ပထမ အဆင့်တွင် database ကို server host ပေါ်တွင် တိုက်ရိုက် တည်ဆောက်သည်။
container များ စတင်မီ database ရှိနေရန် လိုအပ်သည်။

```bash
sudo apt install -y postgresql
sudo systemctl enable --now postgresql
sudo -u postgres psql
```

ပထမညွှန်ကြားချက်က PostgreSQL package ကို ထည့်သွင်းသည်။ ဒုတိယညွှန်ကြားချက်က
service ကို ယခုအချိန်တွင် စတင်ပြီး boot အချိန်တွင်လည်း အလိုအလျောက် စတင်ရန်
သတ်မှတ်သည်။ တတိယညွှန်ကြားချက်က `postgres` user အနေဖြင့် SQL shell သို့
ဝင်ရောက်သည်။

```sql
CREATE DATABASE openuem;
CREATE USER openuem_app WITH ENCRYPTED PASSWORD 'change-me';
GRANT ALL PRIVILEGES ON DATABASE openuem TO openuem_app;
ALTER DATABASE openuem OWNER TO openuem_app;
```

ပထမညွှန်ကြားချက်က OpenUEM ၏ အခြေခံ database ကို ဖန်တီးသည်။ ဒုတိယညွှန်ကြားချက်က
application အတွက် သီးခြား role တစ်ခု ဖန်တီးသည်။ `postgres` superuser ကို
application မှ တိုက်ရိုက် အသုံးပြုခြင်း မပြုရ။ တတိယနှင့် စတုတ္ထညွှန်ကြားချက်က
ထို role အား database ၏ ပိုင်ရှင် ဖြစ်စေသည်။ ပိုင်ရှင် မဖြစ်လျှင် ဇယား ဖန်တီးခြင်း
အဆင့်တွင် ခွင့်ပြုချက် error ဖြစ်ပေါ်နိုင်သည်။

Connection URI ကို `.env` ဖိုင်တွင် ထည့်သည်။ စကားဝှက်တွင် `=` ကဲ့သို့
အထူက္ခရာ ပါလျှင် percent-encoding လုပ်ရသည်။ ဥပမာ `te=st` ကို `te%3Dst`
အဖြစ် ရေးရသည်။ ဤစည်းမျဉ်းကို မလိုက်နာလျှင် component များ စတင်စဉ်
authentication failure ဖြစ်ပေါ်မည်။

ဒုတိယ အဆင့်တွင် compose deployment ကို အသုံးပြုသည်။

```bash
git clone https://github.com/open-uem/openuem-docker
cd openuem-docker
cp .env-example .env
docker compose up -d
```

ပထမညွှန်ကြားချက်က တရားဝင် compose repository ကို ရယူသည်။ ဒုတိယညွှန်ကြားချက်က
ထို folder သို့ ဝင်သည်။ တတိယညွှန်ကြားချက်က နမူနာ ဖိုင်ကို `.env` အဖြစ်
ကူးသည်။ ဖိုင်အမည်တွင် အစက်ရှေ့ဆုံး ရှိရမည်။ စတုတ္ထညွှန်ကြားချက်က
container များကို background တွင် စတင်သည်။ Podman အသုံးပြုသူများအတွက်
`podman compose` ကို အစားထိုး အသုံးပြုနိုင်သည်။

`.env` တွင် မဖြစ်မနေ ဖြည့်ရသော key များမှာ အောက်ပါအတိုင်း ဖြစ်သည်။

| Key | တန်ဖိုး ဥပမာ | ရည်ရွယ်ချက် |
|---|---|---|
| `OPENUEM_ORGNAME` | `openuem.example` | default organization အမည် |
| `OPENUEM_COUNTRY` | `MM` | CA certificate တွင် ပါဝင်သော နိုင်ငံ |
| `OPENUEM_DOMAIN` | `openuem.example` | component များ၏ အခြေခံ domain |
| `OPENUEM_DATABASE_URL` | `postgres://openuem_app:***@192.168.1.43:5432/openuem` | component များ အသုံးပြုသော URI |
| `CONSOLE_HOST` | `console.openuem.example` | console ၏ host အမည် |
| `CONSOLE_PORT` | `1323` | console port |
| `CONSOLE_AUTH_PORT` | `1324` | authentication port |
| `CONSOLE_JWT_KEY` | အက္ခရာ ၃၂ လုံး ကျပန်း စာသား | session token လက်မှတ် |
| `NATS_HOST`, `NATS_PORT` | `nats.openuem.example`, `4433` | agent ချိတ်ဆက်ရာ broker |
| `OCSP_URL`, `OCSP_PORT` | `http://ocsp.openuem.example:8000`, `8000` | certificate ပြန်လည်ရုပ်သိမ်းမှု စစ်ဆေးရာ |
| `REVERSE_PROXY_*` | Caddy host နှင့် port | reverse proxy မသုံးလျှင် အလွတ် ထားရသည် |

Hosts override ကို ဌာနခွဲ host များတွင် ထည့်သည်။

```text
192.168.1.43  nats.openuem.example  ocsp.openuem.example  console.openuem.example
```

ဤနေရာတွင် LAN IP ကို အသုံးပြုရသည်။ `localhost` သို့မဟုတ် `127.0.0.1` ကို
မသုံးရ။ container တစ်ခုစီသည် ထို အမည်ကို မိမိကိုယ်တိုင် အဖြစ် ဖြေရှင်းမည်
ဖြစ်သောကြောင့် ချိတ်ဆက်မှု ကျရှုံးမည်။

တတိယ အဆင့်တွင် CA နှင့် component certificate များကို ဖန်တီးသည်။
`openuem-cert-manager` သည် CA နှင့် certificate များကို တစ်နေရာတည်းမှ
ထုတ်ပေးသော command line tool ဖြစ်သည်။

```bash
sudo openuem-cert-manager client-cert --name "OpenUEM Agent" --dst ./agents \
  --type="agent" --org "$ORGNAME" --country "$COUNTRY" --province "$ORGPROVINCE" \
  --locality "$ORGLOCALITY" --address "$ORGADDRESS" --years-valid 2 \
  --filename "agent" --ocsp "http://$OCSP_SERVER:$OCSP_PORT" \
  --description "Agent certificate" --cacert ./ca/ca.cer --cakey ./ca/ca.key \
  --dburl "$DATABASE_URL"
```

ဤညွှန်ကြားချက်က agent အမျိုးအစား certificate တစ်ခုကို `agents` folder သို့
ထုတ်ပေးသည်။ `--years-valid 2` က သက်တမ်း နှစ်နှစ် သတ်မှတ်သည်။
`--ocsp` က certificate အတွင်း ထည့်သွင်းမည့် OCSP URL ဖြစ်သည်။
`--cacert` နှင့် `--cakey` က လက်မှတ်ထိုးရန် အသုံးပြုမည့် CA ဖြစ်သည်။
ဤနေရာတွင် မှားယွင်းသော CA ကို ညွှန်ပြခြင်းသည် နောက်ပိုင်း ဖြစ်ရပ်၏
အကြောင်းရင်း ဖြစ်လာသည်။

**Figure 1 — ဆောက်လုပ်မှု အဆင့်များ: host အလွတ်မှ စီမံနိုင်သော endpoint အထိ**

```mermaid
flowchart LR
    P0["P0 PostgreSQL နှင့် role"] --> P1["P1 compose stack"]
    P1 --> P2["P2 CA နှင့် certificate"]
    P2 --> P3["P3 console ဝင်ရောက်မှု"]
    P3 --> P4["P4 agent wave ၃ ခု"]
    P4 --> P5["P5 baseline နှင့် patch"]
    P5 --> P6["P6 သက်သေ အစုအဝေး"]
```

ပုံရှင်းလင်းချက် — ဤပုံသည် အဆင့် ခြောက်ဆင့်ကို ဘယ်မှ ညာ စီစဉ်ထားသည်။
P0 တွင် database နှင့် application role ကို အရင် တည်ဆောက်သည်။ database
မရှိဘဲ component များ စတင်လျှင် ချက်ချင်း ရပ်တန့်မည်။ P1 တွင် container
အားလုံး လည်ပတ်စေသည်။ P2 တွင် CA နှင့် component certificate များ ထုတ်ပေးသည်။
ဤအဆင့် မပြီးမချင်း agent များကို မဖြန့်ရ။ P3 တွင် ဘရောက်ဇာမှ console သို့
ဝင်ရောက်၍ login စမ်းသပ်သည်။ P4 တွင် agent များကို wave သုံးခုဖြင့် အဆင့်လိုက်
ဖြန့်သည်။ P5 တွင် software baseline နှင့် patch wave ကို လုပ်ဆောင်သည်။
P6 တွင် ရလဒ်များကို သက်သေအဖြစ် ထုတ်ယူ သိမ်းဆည်းသည်။ မြှားတစ်ခုစီသည်
"ပြီးဆုံးမှ ဆက်လုပ်ရန်" ဟု ဆိုလိုသည်။

## ၁၀.၄ လက်ခံနိုင်မှု စံနှုန်းများ (acceptance criteria)

ဖြန့်ကျက်မှုကို "ပြီးပြီ" ဟု ဆုံးဖြတ်ရန် တိုင်းတာနိုင်သော စံနှုန်း ရှစ်ခု
သတ်မှတ်ထားသည်။ စံနှုန်းတစ်ခုစီတွင် တိုင်းတာနည်း ပါဝင်သည်။

| အမှတ် | စံနှုန်း | တိုင်းတာပုံ |
|---|---|---|
| AC-1 | database နှင့် stack အဆင်သင့် | `psql` မှ ချိတ်ဆက်နိုင်ခြင်း, container အားလုံး healthy |
| AC-2 | CA သက်တမ်း go-live တွင် ရက် ၃၆၅ ကျော် | certificate ဖိုင် သက်တမ်း တွက်ချက်မှု |
| AC-3 | endpoint ၂၇ ခုလုံး Enabled | console ၏ agent စာရင်း |
| AC-4 | ရက် ၇ ဆက်တိုက် reporting ၉၀% ကျော် | dashboard ၏ ၂၄ နာရီ ကွက်လပ် |
| AC-5 | baseline လွှမ်းခြုံမှု ၈၅% ကျော် | software view CSV |
| AC-6 | patch wave ပြီးနောက် လိုက်နာမှု ၉၅% ကျော် | security view CSV |
| AC-7 | သက်သေ အစုအဝေး သိမ်းဆည်းပြီး | archive တွင် ဖိုင် အားလုံး ရှိခြင်း |
| AC-8 | ဖြစ်ရပ် မှတ်တမ်း ပိတ်ပြီး runbook ပြင်ပြီး | review မှတ်တမ်း |

စံနှုန်းများသည် အလှဆင်ရန် မဟုတ်ပါ။ ဖြန့်ကျက်မှု တိုးတက်မှုကို တိုင်းတာရန်
အသုံးပြုသည်။ ဥပမာ AC-2 ကို readiness checklist တွင် ကြိုတင် စစ်ဆေးလျှင်
CA သက်တမ်း ရက် ၁၂၀ သာ ကျန်နေသည်ကို တွေ့ရသည်။ ထို အချက်တစ်ခုတည်းက
ဆောက်လုပ်မှုကို ရပ်တန့်စေသည်။ ဤဇာတ်လမ်းတွင် အဖွဲ့သည် ထို အတားအဆီးကို
မှန်ကန်စွာ ဖော်ထုတ်နိုင်ခဲ့သော်လည်း ပြုပြင်မှုကို change record မပါဘဲ
အလျင်အမြန် လုပ်ဆောင်ခဲ့သည်။ ထို ဆုံးဖြတ်ချက်သည် နောက်ပိုင်း ဖြစ်ရပ်နှင့်
တိုက်ရိုက် ဆက်စပ်နေသည်။

## ၁၀.၅ Enrollment wave စီမံချက်

Endpoint ၂၇ ခုကို တစ်ပြိုင်နက် မဖြန့်ပါ။ wave သုံးခုဖြင့် ခွဲသည်။
ပထမ wave သည် pilot ဖြစ်ပြီး platform တစ်မျိုးလျှင် တစ်ခု ပါဝင်သည်။

| Wave | အတိုင်းအတာ | အရေအတွက် | ရည်ရွယ်ချက် |
|---|---|---|---|
| 1 | ဌာနချုပ် pilot (platform တစ်မျိုးလျှင် တစ်ခု) | 3 | install နည်းလမ်းနှင့် certificate ကို စမ်းသပ်ခြင်း |
| 2 | ဌာနချုပ် ကျန် endpoint များ | 15 | LAN အတွင်း အစုလိုက် ဖြန့်ခြင်း |
| 3 | ဌာနခွဲ endpoint များ | 9 | WAN ကန့်သတ်ချက်အောက်တွင် ဖြန့်ခြင်း |

wave တစ်ခုနှင့် တစ်ခုအကြား ရက် ၃ ရက် ခွဲထားသည်။ ပထမ wave ပြီးနောက်
force report ဖြင့် inventory အပြည့်အစုံ ရောက်ကြောင်း စစ်သည်။
ဒုတိယ wave ပြီးနောက် ဌာနချုပ် endpoint များ၏ ကွန်ရက် အသုံးပြုမှုကို
တစ်ရက်ကြာ ကြည့်သည်။ တတိယ wave ကို WAN အသုံးပြုမှု အများဆုံး အချိန်နှင့်
မတိုက်မိစေရန် ညနေပိုင်းတွင် စတင်သည်။

Windows agent ကို silent install ဖြင့် ဖြန့်သည်။

```text
openuem-agent-setup.exe /VERYSILENT /cacert=ca.cer /cert=agent.cer /key=agent.key \
  /server=nats.openuem.example:4433 /sftp=2022 /vnc=1443 /tenantid=1 /siteid=2
```

ဤညွှန်ကြားချက်တွင် `/VERYSILENT` က အပြ မပြဘဲ ထည့်သွင်းစေသည်။
`/cacert`, `/cert`, `/key` က certificate သုံးခု၏ တည်နေရာကို ပြသည်။
`/server` က NATS host နှင့် port ဖြစ်သည်။ `/sftp` နှင့် `/vnc` က
agent-side service နှစ်ခု၏ port ဖြစ်သည်။ `/tenantid` နှင့် `/siteid` ကို
တွဲဖက် ပေးရသည်။ တစ်ခုတည်း ပေးလျှင် install က လက်မခံပါ။

Debian-based host များတွင် package ဖြင့် ထည့်သည်။

```bash
sudo apt install openuem-agent
sudo systemctl restart openuem-agent
sudo systemctl restart openuem-agent-updater
```

ပထမညွှန်ကြားချက်က agent package ကို ထည့်သွင်းပြီး NATS server, SFTP port
နှင့် VNC proxy port အတွက် မေးခွန်းများ မေးသည်။ ဒုတိယနှင့် တတိယ
ညွှန်ကြားချက်က certificate များ နေရာချပြီးနောက် service နှစ်ခုကို
ပြန်လည် စတင်သည်။ certificate များကို `/etc/openuem-agent/certificates`
အောက်တွင် `ca.cer`, `sftp.cer`, `agent.cer`, `agent.key` အမည်များဖြင့်
ထားရသည်။

RPM-based host များတွင် `dnf install -y openuem-agent` ကို အသုံးပြုပြီး
`/etc/openuem-agent/openuem.ini` ကို တိုက်ရိုက် တည်းဖြတ်ရသည်။ ထို ဖိုင်တွင်
`[NATS] NATSServers=` နှင့် port များ ပါဝင်သည်။ ပြီးနောက် folder ပိုင်ဆိုင်မှုကို
`openuem-agent` user သို့ ပြောင်းရသည်။ macOS agent အတွက် တရားဝင် installer
ကို အသုံးပြုသည်။ installer ၏ အမည်နှင့် flag များသည် version အလိုက်
ပြောင်းလဲနိုင်သဖြင့် လက်ရှိ documentation နှင့် ပြန်စစ်ရန် လိုသည်။

**Figure 2 — wave တစ်ခုစီ၏ အစဉ်လိုက် လုပ်ဆောင်မှု**

```mermaid
sequenceDiagram
    participant ADMIN as Administrator
    participant CONSOLE as OpenUEM console
    participant W1 as Wave 1 pilot
    participant W2 as Wave 2 head office
    participant W3 as Wave 3 branch
    ADMIN->>CONSOLE: wave 1 ကို အတည်ပြု
    CONSOLE->>W1: agent install နှင့် admission
    W1-->>CONSOLE: မိနစ် ၆၀ အတွင်း report
    ADMIN->>CONSOLE: ရက် ၃ ကြာ ရလဒ် စစ်ဆေး
    ADMIN->>CONSOLE: wave 2 ကို အတည်ပြု
    CONSOLE->>W2: agent install နှင့် admission
    W2-->>CONSOLE: report နှင့် inventory
    ADMIN->>CONSOLE: wave 3 ကို အတည်ပြု
    CONSOLE->>W3: WAN မှတစ်ဆင့် install
    W3-->>CONSOLE: report နှင့် inventory
```

ပုံရှင်းလင်းချက် — ဤပုံတွင် ပါဝင်သူ ငါးဦး ရှိသည်။ ဘယ်ဘက်ဆုံးမှာ စီမံခန့်ခွဲသူ
ဖြစ်သည်။ သူက console သို့ wave တစ်ခုကို အတည်ပြုကြောင်း အချက်ပြသည်။
console က သက်ဆိုင်ရာ wave အုပ်စုသို့ agent install နှင့် admission ကို
ပို့သည်။ wave အုပ်စုက report ပြန်ပို့သည်။ မြှားတစ်ခုစီ၏ အစီအစဉ်က
အရေးကြီးသည်။ pilot ပြီးဆုံးပြီး ရက် ၃ ကြာ ရလဒ် မစစ်ရသေးဘဲ wave 2 ကို
မစရ။ wave 2 ပြီးဆုံးမှ wave 3 ကို စသည်။ ဤအစီအစဉ်က ပြဿနာတစ်ခု
ဖြစ်ပေါ်လျှင် ထိခိုက်မှု အတိုင်းအတာကို wave တစ်ခုအတွင်းသာ ကန့်သတ်ထားသည်။
ဌာနခွဲ wave တွင် WAN ကြန့်ကြာမှု ပါဝင်သဖြင့် report ရောက်ချိန် ပိုကြာနိုင်သည်။

wave တစ်ခုစီအတွင်း endpoint များကို tag ဖြင့် စုသည်။
`site=head-office`, `site=branch`, `platform=windows` ကဲ့သို့ tag များက
စစ်ထုတ်မှုနှင့် report ထုတ်ယူမှုကို ရိုးရှင်းစေသည်။ tag အမည်များကို
ဇာတ်လမ်းတစ်လျှောက် မပြောင်းရ။ ပြောင်းလျှင် ယခင် report များနှင့်
နှိုင်းယှဉ်မှု ပျက်သွားမည်။

## ၁၀.၆ Software baseline နှင့် profile

baseline သည် "endpoint တိုင်းတွင် ရှိရမည့် package စာရင်း" ဖြစ်သည်။
platform အလိုက် package manager မတူသဖြင့် စာရင်းကို သုံးခု ခွဲထားသည်။

| Platform | Package manager | baseline ပစ္စည်း | profile task အမျိုးအစား |
|---|---|---|---|
| Windows | WinGet | browser, archive tool, media player | WinGet configuration (DSC) |
| Linux | Flatpak | browser, media player | Ansible |
| macOS | HomeBrew | browser, media player | Ansible |

profile သည် desired state တစ်ခုဖြစ်သည်။ task တစ်ခုစီက "ဤအခြေအနေသို့ ရောက်စေရန်"
ဟု ဖော်ပြသည်။ agent သည် profile အသစ်ကို မိနစ် ၃၀ တစ်ကြိမ် စစ်ဆေးသည်။
ထို့ကြောင့် profile တစ်ခု ထုတ်လိုက်ပြီးနောက် ရလဒ်ကို ချက်ချင်း မမျှော်ရ။
endpoint တစ်ခု offline ဖြစ်နေလျှင် ၎င်း ပြန်လာချိန်တွင် task ကို လက်ခံမည်။
package request များသည် NATS တွင် တန်းစီသည်။

နှစ်ခုသော ကြိုတင်ပြင်ဆင်မှု လိုအပ်သည်။ Windows တွင် WinGet အသုံးပြုရန်
Microsoft Store နှင့် App Installer ကို မွမ်းမံထားရသည်။ macOS တွင်
HomeBrew ကို ကိုယ်တိုင် ထည့်သွင်းထားရသည်။ ထို နှစ်ခုကို မပြင်ဆင်ဘဲ
profile ကို ဖြန့်လျှင် task များ ကျရှုံးမည်။ ထို ကျရှုံးမှုကို agent log
တွင် တွေ့ရမည်။

baseline ဖြန့်ပြီးနောက် software view မှ CSV ကို ထုတ်ယူသည်။ ထို ဖိုင်သည်
package အမည်, publisher နှင့် install အရေအတွက်ကို စုစည်း ပြသည်။
ဤဇာတ်လမ်းတွင် endpoint ၂၇ ခုအနက် ၂၄ ခု လိုက်နာမှု ရှိသည်။
ကျန်သော သုံးခုမှာ `LNX-BR-02` (Flatpak package မရှိ), `MAC-HO-03`
(update တစ်ခု ကျန်) နှင့် `WIN-BR-04` (အသုံးပြုသူက package ကို ဖြုတ်ပစ်)
ဖြစ်သည်။ ရာခိုင်နှုန်းအားဖြင့် ၈၈.၉ ရာခိုင်နှုန်း ဖြစ်သည်။

## ၁၀.၇ Patch wave နှင့် maintenance window

patch wave ကို စနေနေ့ 01:00 မှ 05:00 အတွင်း သာ လုပ်ဆောင်သည်။
ဤအချိန်ကွက်သည် ဌာနချုပ်နှင့် ဌာနခွဲ နှစ်ခုလုံးအတွက် တူညီသည်။
wave စတင်ရန် gate လေးခုကို ဖြတ်ရသည်။

| Gate | သတ်မှတ်ချက် | မပြည့်လျှင် လုပ်ဆောင်ချက် |
|---|---|---|
| G1 | လက်ရှိအချိန် window အတွင်း | နောက် window သို့ ရွှေ့ |
| G2 | reporting ၉၀% ကျော် | တိတ်ဆိတ်နေသော endpoint များကို ရှာဖွေ |
| G3 | validation ကျရှုံးမှု သုည | ကျရှုံးသော host ကို ဖယ်ပြီး ပြန်စစ် |
| G4 | ဖွင့်ထားသော P1 ဖြစ်ရပ် မရှိ | ဖြစ်ရပ်ကို အရင် ပိတ် |

**Figure 3 — patch wave အတွက် gate ဆုံးဖြတ်ချက်**

```mermaid
flowchart TD
    S["Wave စတင် 01:00"] --> W{"Window အတွင်း လား"}
    W -- "မဟုတ်" --> H1["HOLD: နောက် window သို့ ရွှေ့"]
    W -- "ဟုတ်" --> R{"Reporting ၉၀% ကျော်လား"}
    R -- "မဟုတ်" --> H2["HOLD: တိတ်ဆိတ် endpoint ရှာ"]
    R -- "ဟုတ်" --> V{"Validation ကျရှုံးမှု သုညလား"}
    V -- "မဟုတ်" --> H3["HOLD: host ဖယ်ပြီး ပြန်စစ်"]
    V -- "ဟုတ်" --> P{"P1 ဖြစ်ရပ် ဖွင့်ထားလား"}
    P -- "ဟုတ်" --> H4["HOLD: ဖြစ်ရပ်ကို အရင်ပိတ်"]
    P -- "မဟုတ်" --> G["GO: ဖြန့်ပြီး စစ်ဆေး"]
```

ပုံရှင်းလင်းချက် — ဤပုံသည် အပေါ်မှ အောက်သို့ စီးဆင်းသည်။ ပထမဆုံး စစ်ဆေးချက်မှာ
အချိန် ဖြစ်သည်။ window မဟုတ်လျှင် ဘယ်ဘက်လမ်းသို့ သွား၍ ရပ်သည်။
window အတွင်း ဖြစ်လျှင် reporting ရာခိုင်နှုန်းကို စစ်သည်။
၉၀% မပြည့်လျှင် တိတ်ဆိတ်နေသော endpoint များကို အရင် ရှာရသည်။
ပြည့်လျှင် validation ရလဒ်ကို စစ်သည်။ ကျရှုံးမှု တစ်ခု ရှိလျှင်
ထို host ကို wave မှ ဖယ်ပြီး ပြန်စစ်ရသည်။ ပြီးမှ ဖွင့်ထားသော P1
ဖြစ်ရပ် ရှိ မရှိ စစ်သည်။ လေးခုလုံး အောင်မှ ညာဘက်ဆုံး အစိမ်းရောင်
လမ်းသို့ ရောက်သည်။ ဤအစီအစဉ်က "တစ်ခု ကျရှုံးလျှင် အားလုံး ရပ်" ဟု
ဆိုလိုသည်။ အလယ်တွင် တစ်ပိုင်း ဖြန့်ပြီး ထားခြင်း မရှိပါ။

ပထမ အကြိမ် တိုင်းတာမှုတွင် reporting ၂၄/၂၇ ဖြစ်ပြီး validation ကျရှုံးမှု
တစ်ခု ရှိသည်။ gate က HOLD ဟု ဆုံးဖြတ်သည်။ အကြောင်းရင်း နှစ်ခု ဖြစ်သည်။
အဖွဲ့သည် `LNX-HO-04` ကို wave မှ ဖယ်ပြီး၊ ကျန် endpoint သုံးခုကို
force report ဖြင့် ပြန်လည် စစ်ဆေးသည်။ 02:40 တွင် ဒုတိယ အကြိမ်
တိုင်းတာရာ ၂၇/၂၇ နှင့် ကျရှုံးမှု သုည ဖြစ်သဖြင့် GO ရသည်။
ထို wave ကို 03:10 တွင် စတင်၍ 04:35 တွင် ပြီးဆုံးသည်။ 06:15 တွင်
ထပ်၍ တိုင်းတာလျှင် window ပြင်ပ ဖြစ်သဖြင့် HOLD ဖြစ်သည်။
ဤအချက်က gate သည် အချိန်ကို အမြဲ ထည့်သွင်း စစ်ဆေးကြောင်း ပြသည်။

## ၁၀.၈ ဖြစ်ရပ်: certificate ပြောင်းလဲမှုနောက် agent များ ရပ်ဆိုင်းခြင်း

patch wave ပြီးဆုံးပြီး လေးနာရီအကြာ 09:05 တွင် agent certificate အုပ်စုတစ်ခုကို
အစားထိုးသည်။ 09:20 တွင် dashboard ၏ အနီရောင် အပိုင်းက သတိပေးသည်။
endpoint ၂၇ ခုအနက် ၄ ခုသာ report ပို့နေသည်။

| အချိန် | ဖြစ်ရပ် |
|---|---|
| 09:05 | agent certificate ၂၃ ခုကို အစားထိုး |
| 09:20 | reporting ၄/၂၇ သို့ ကျဆင်း, dashboard သတိပေး |
| 09:35 | အလွှာလိုက် စစ်ဆေးမှု စတင် |
| 09:50 | agent log တွင် unknown authority ကို တွေ့ |
| 10:15 | အမြစ်အကြောင်းရင်း အတည်ပြု |
| 10:40 | ပြန်လည် ထူထောင်မှု စတင် |
| 11:40 | reporting ၂၇/၂၇ သို့ ပြန်ရောက် |

အလွှာလိုက် စစ်ဆေးမှုသည် module 09 ၏ နည်းလမ်းကို လိုက်နာသည်။
အောက်ခြေ အလွှာမှ အပေါ်သို့ တက်သည်။

| အချက်အလက် | တွေ့ရှိမှု | ဖယ်ထုတ်နိုင်သော အကြောင်းရင်း |
|---|---|---|
| `console.openuem.example:1323` | HTTP 200 | console နှင့် database အလုပ်လုပ်နေသည် |
| port 4433 | TCP ချိတ်ဆက်မှု အောင်မြင် | NATS service ရပ်မနေပါ |
| OCSP responder 8000 | HTTP 200 | OCSP service ရပ်မနေပါ |
| PostgreSQL | ချိတ်ဆက်မှု လက်ခံ | database ပျက်မနေပါ |
| DNS ဖြေရှင်းမှု | အောင်မြင် | အမည် ဖြေရှင်းမှု မဟုတ်ပါ |
| clock skew | ၃ စက္ကန့် | အချိန် ကွာဟမှု မဟုတ်ပါ |
| agent log | `x509: certificate signed by unknown authority` | လက်မှတ် ကွင်းဆက် မကိုက်ညီ |

agent log သည် အဓိက အထောက်အထား ဖြစ်သည်။ ထို စာသားက "server သည် agent ၏
certificate ကို လက်မှတ်ထိုးသူကို မသိ" ဟု ဆိုသည်။ ဆက်စပ် အချက်နှစ်ခုက
ဤ ကောက်ချက်ကို ခိုင်မာစေသည်။ ပထမ၊ certificate အစားထိုးမခံရသော endpoint
၄ ခု (pilot သုံးခုနှင့် အပိုတစ်ခု) သည် ပုံမှန် report ပို့နေသည်။
ဒုတိယ၊ အစားထိုးခံရသော ၂၃ ခု အားလုံး တိတ်ဆိတ်သည်။ ဤပုံစံက
အခြေခံအဆောက်အအုံ ပြဿနာကို မဟုတ်ဘဲ လက်မှတ် ပြဿနာကို ညွှန်သည်။

အမြစ်အကြောင်းရင်း မှာ ထို ဖြစ်သည်။ အစားထိုးမှု လုပ်ဆောင်စဉ်
`openuem-cert-manager` ကို အသစ် ဖန်တီးထားသော CA တစ်ခုဖြင့် ခေါ်ခဲ့သည်။
သို့သော် `openuem.ini` ၏ `CACert` နှင့် OCSP responder က အဟောင်း CA ကို
ယုံကြည်နေဆဲ ဖြစ်သည်။ ထို့ကြောင့် agent ၏ အသစ်သော certificate ကို
NATS က လက်မခံပါ။ agent က report ပို့သည့်အခါ TLS handshake ကျရှုံးသည်။

ပြန်လည် ထူထောင်မှုကို အစဉ်လိုက် လုပ်ဆောင်သည်။

1. certificate အစားထိုးမှု အစုကို ရပ်ဆိုင်းသည်။
2. `openuem.ini` နှင့် certificate tree တွင် ယခင် CA ကို ပြန်ထည့်သည်။
3. ယုံကြည်ရသော CA မှ agent certificate များကို ပြန်ထုတ်သည်။
4. `openuem-ocsp-responder` ကို စတင်သည်။
5. `openuem-nats-service` ကို စတင်သည်။
6. `openuem-server-updater` ကို စတင်သည်။
7. `openuem-agent-worker` ကို စတင်သည်။
8. `openuem-notification-worker` ကို စတင်သည်။
9. `openuem-cert-manager-worker` ကို စတင်သည်။
10. `openuem-console` ကို စတင်သည်။
11. သက်ဆိုင်ရာ endpoint များတွင် force report ကို လုပ်ဆောင်သည်။
12. reporting ၂၇/၂၇ ပြန်ရောက်ကြောင်း အတည်ပြုသည်။

service အစဉ်သည် module 03 တွင် သတ်မှတ်ထားသော အစဉ်အတိုင်း ဖြစ်သည်။
OCSP ကို အရင် စတင်ရသည်။ ထို့နောက် NATS, updater, worker များ, နောက်ဆုံး
console ဖြစ်သည်။ အစဉ် မှားလျှင် worker များက certificate ကို မရနိုင်ဘဲ
ထပ်၍ ကျရှုံးမည်။

ဤဖြစ်ရပ်မှ သင်ခန်းစာ နှစ်ခု ရသည်။ ပထမ၊ readiness checklist တွင် CA သက်တမ်း
အတားအဆီး တွေ့ခဲ့သည်မှာ မှန်သည်။ သို့သော် ပြုပြင်မှုကို change record မပါဘဲ
လုပ်ခဲ့သည်။ ဒုတိယ၊ certificate အစားထိုးမှုကို endpoint တစ်ခုတွင် အရင်
စမပ်ပြီး ရလဒ် ကောင်းမှ ကျန် အစုကို လုပ်ရသည်။ တစ်ပြိုင်နက်
အစားထိုးလျှင် ပြန်လည် ထူထောင်ရန် အချိန်များစွာ ကုန်မည်။

## ၁၀.၉ သက်သေ အစုအဝေး (evidence pack)

review တွင် "လုပ်ခဲ့သည်" ဟု ပြောခြင်းက မလုံလောက်ပါ။ ဖြန့်ကျက်မှု
အခြေအနေကို ပြသနိုင်သော ဖိုင်များ လိုအပ်သည်။ အောက်ပါ ဖိုင်များကို
တစ်နေရာတည်းတွင် စုစည်း သိမ်းဆည်းသည်။

| အမှတ် | သက်သေ | ရင်းမြစ် | သက်သေပြသည့် အချက် |
|---|---|---|---|
| E1 | dashboard မြင်ကွင်း ဓာတ်ပုံ | console dashboard | reporting, platform အချိုးအစား |
| E2 | agent စာရင်း CSV | console agent view | state နှင့် နောက်ဆုံး report အချိန် |
| E3 | inventory overview PDF | endpoint တစ်ခုချင်း | hardware နှင့် OS အချက်အလက် |
| E4 | software CSV | software view | baseline လွှမ်းခြုံမှု |
| E5 | security CSV | security view | patch အခြေအနေ |
| E6 | profile စာရင်း | console profile view | desired state သတ်မှတ်ချက် |
| E7 | wave မှတ်တမ်း | ပြင်ပ စာရွက်စာတမ်း | မည်သည့် endpoint က မည်သည့် အချိန် |
| E8 | ဖြစ်ရပ် အချိန်လိုင်း | ဖြစ်ရပ် မှတ်တမ်း | ရှာဖွေမှု နှင့် ပြန်လည် ထူထောင်မှု |
| E9 | `lab.py` output | lab run | တွက်ချက်မှု အားလုံး၏ ရလဒ် |
| E10 | verifier output | repo verifier | module ၏ ဖွဲ့စည်းမှု မှန်ကန်မှု |

E1 နှင့် E2 ကို ဖြန့်ကျက်မှု ပြီးဆုံးသည့် နေ့တွင် ထုတ်ယူသည်။
E4 နှင့် E5 ကို patch wave မတိုင်မီနှင့် ပြီးနောက် နှစ်ကြိမ် ထုတ်ယူပြီး
နှိုင်းယှဉ်သည်။ CSV ထုတ်ယူသောအခါ စစ်ထုတ်မှု (filter) နှင့် စီစဉ်မှု
(sort) ကို မဖျက်ရ။ report သည် လက်ရှိ စစ်ထုတ်မှုအတိုင်း ထွက်လာသည်။
ထို အချက်က နှိုင်းယှဉ်မှုကို တိကျစေသည်။

သက်သေ ဖိုင်များကို ရက်စွဲ ပါသော folder တစ်ခုတွင် သိမ်းသည်။
ဖိုင်အမည်တွင် ရက်စွဲ နှင့် အဆင့် ပါဝင်ရသည်။ ဥပမာ 2026-03-14_wave1_agents.csv
ဖြစ်သည်။ ဖိုင်အမည် မပါဘဲ သိမ်းလျှင် review တွင် မည်သည့် ဖိုင် မည်သည့်
အဆင့် ဖြစ်သည်ကို မခွဲခြားနိုင်ပါ။

## ၁၀.၁၀ ပြန်လည် သုံးသပ်မှု ဆွေးနွေးပွဲ

review ကို မိနစ် ၄၅ ကြာ သတ်မှတ်သည်။ အစီအစဉ် ငါးပိုင်း ရှိသည်။
၁၀ မိနစ်က ရလဒ် တင်ပြမှု၊ ၁၅ မိနစ်က ဖြစ်ရပ် ဆန်းစစ်မှု၊ ၁၀ မိနစ်က
သက်သေ စစ်ဆေးမှု၊ ၅ မိနစ်က လိုအပ်ချက် ဖော်ထုတ်မှု၊ ၅ မိနစ်က
နောက်အဆင့် သတ်မှတ်မှု ဖြစ်သည်။

ဆွေးနွေးရန် မေးခွန်းများ:

- endpoint ၂၇ ခုအနက် မည်သည့် အရေအတွက်က reporting ရှိသည်ကို
  သက်သေ ဖိုင်တွင် ရှာနိုင်သလား။
- baseline မပြည့်သော endpoint သုံးခုကို မည်သည့် အစီအစဉ်ဖြင့် ပြင်မည်နည်း။
- patch wave ၏ ပထမ gate က HOLD ဖြစ်ခဲ့သည်မှာ မှန်သလား။
  ထို ဆုံးဖြတ်ချက်က အချိန်ကို မည်မျှ ကုန်စေခဲ့သလဲ။
- certificate အစားထိုးမှုကို endpoint တစ်ခုတွင် အရင် စမ်းသပ်ခဲ့လျှင်
  ဖြစ်ရပ် ဖြစ်ပေါ်နိုင်သလား။
- ဖြစ်ရပ် တစ်ခု ထပ်ဖြစ်လျှင် မည်သည့် အချက်အလက်ကို ပထမ ကြည့်မည်နည်း။
- ဤ ဖြန့်ကျက်မှုကို နောက် site တစ်ခုသို့ တိုးချဲ့လျှင် မည်သည့် အဆင့်ကို
  ပြန်လုပ်ရမည်နည်း။

ကောင်းသော အဖြေတစ်ခုသည် ကိန်းဂဏန်း တစ်ခုနှင့် ဖိုင် တစ်ခုကို အမြဲ
တွဲဖက် ပြသည်။ "အားလုံး အဆင်ပြေသည်" ကဲ့သို့ ယေဘုယျ စကားသည်
သက်သေ မဟုတ်ပါ။

## ၁၀.၁၁ မိမိကိုယ်ကို စစ်ဆေးခြင်း

**၁။ readiness checklist တွင် CA သက်တမ်း ကျရှုံးလျှင် ဘာလုပ်ရမည်နည်း။**
ဆောက်လုပ်မှုကို မစတင်ရ။ CA ကို အသစ်ထုတ်ပြီး component certificate အားလုံးကို
ပြန်ထုတ်ကာ change record တွင် မှတ်တမ်းတင်ရသည်။

**၂။ wave သုံးခု၏ အရေအတွက်က ဘာကို ပြသနည်း။**
pilot သုံးခုက install နည်းလမ်းကို စမ်းသပ်သည်။ ဌာနချုပ် ၁၅ ခုက LAN အတွင်း
အစုလိုက် ဖြန့်မှုကို ပြသည်။ ဌာနခွဲ ၉ ခုက WAN ကန့်သတ်ချက်အောက်တွင်
ဖြန့်မှုကို ပြသည်။ ထိခိုက်မှု အတိုင်းအတာကို wave တစ်ခုအတွင်း ကန့်သတ်ထားသည်။

**၃။ gate က HOLD ပြလျှင် wave ကို လုံးဝ မလုပ်တော့သလား။**
မဟုတ်ပါ။ HOLD သည် "ယခု မလုပ်ရ" ဟု ဆိုသည်။ အကြောင်းရင်းကို ဖယ်ရှားပြီး
window အတွင်း ထပ်မံ တိုင်းတာနိုင်သည်။ window ပြင်ပ ရောက်လျှင် နောက်
window သို့ ရွှေ့ရသည်။

**၄။ certificate ဖြစ်ရပ်တွင် OCSP ကို ဘာကြောင့် အရင် စစ်သနည်း။**
OCSP responder ရပ်နေလျှင် agent ၏ certificate စစ်ဆေးမှု ကျရှုံးမည်။
service တစ်ခုတည်း၏ အခြေအနေကို ကျန်အလွှာများ မှန်ကန်နေစဉ် ခွဲထုတ်
စစ်ဆေးခြင်းက အကြောင်းရင်း အရေအတွက်ကို လျှော့ချသည်။

**၅။ သက်သေ အစုအဝေးတွင် ဖိုင် မည်မျှ လိုသနည်း။**
အရေအတွက် မဟုတ်ပါ။ လက်ခံနိုင်မှု စံနှုန်း တစ်ခုစီအတွက် အနည်းဆုံး
သက်သေ တစ်ခု ရှိရသည်။ ဤဇာတ်လမ်းတွင် ဖိုင် ဆယ်ခု သတ်မှတ်ထားသည်။

## ၁၀.၁၂ လုပ်ငန်းသုံး သတိပြုချက်များ

- `.env` တွင် `localhost` ကို မသုံးရ။ container တစ်ခုစီသည် ထို အမည်ကို
  မိမိကိုယ်တိုင် အဖြစ် ဖြေရှင်းမည်။
- agent မှ NATS host နှင့် port သို့ outbound ချိတ်ဆက်မှု ရှိရသည်။
  firewall က ထို လမ်းကြောင်းကို ပိတ်ထားလျှင် agent သည် Waiting for
  admission အခြေအနေတွင် ရပ်နေမည်။
- dashboard ၏ "၂၄ နာရီ" ကွက်လပ်သည် ကြားဖြတ်ကာလကို ပြသည်။ report
  အချိန်ကွာဟမှုကို ခွဲခြားရန် agent စာရင်းတွင် နောက်ဆုံး report အချိန်ကို
  တိုက်ရိုက် ကြည့်ရသည်။
- `CONSOLE_JWT_KEY` ကို ပြောင်းလျှင် လက်ရှိ session အားလုံး ပျက်မည်။
  maintenance window အတွင်းသာ ပြောင်းရသည်။
- certificate နှင့် CA ကို ပြောင်းခြင်းသည် change တစ်ခု ဖြစ်သည်။
  endpoint တစ်ခုတွင် အရင် စမပ်ပြီး မှ ကျန် အစုကို လုပ်ရသည်။
- သက်သေ ဖိုင်များကို teardown မလုပ်မီ ထုတ်ယူရသည်။ stack ကို ဖျက်ပြီးမှ
  report ထုတ်ရန် ကြိုးစားလျှင် ဒေတာ မရှိတော့ပါ။
- ဌာနခွဲကဲ့သို့ remote endpoint များတွင် remote assistance, file browsing
  နှင့် WOL ကို အသုံးမပြုနိုင်ပါ။ ထို လုပ်ငန်းများအတွက် အခြားနည်းလမ်း
  သတ်မှတ်ထားရသည်။
- console menu အမည်များနှင့် dashboard ကတ်အမည်များသည် version အလိုက်
  ပြောင်းလဲနိုင်သည်။ runbook တွင် version ကို မှတ်ထားရသည်။

## Technical review notes

- ပြင်ဆင်ချက်: ပထမ မူကြမ်းတွင် wave အရေအတွက်ကို ၄/၁၄/၉ ဟု ရေးထားခဲ့သည်။
  pilot ကို platform တစ်မျိုးလျှင် တစ်ခု ဟု သတ်မှတ်ထားသဖြင့် ၃ ဖြစ်ရမည်။
  လက်ရှိ စာသားနှင့် `lab.py` နှစ်ခုလုံးတွင် ၃/၁၅/၉ ဟု ညှိထားသည်။
- ပြင်ဆင်ချက်: patch gate တွင် reporting သတ်မှတ်ချက်ကို ၈၅% မှ ၉၀% သို့
  ပြောင်းခဲ့သည်။ ပထမ အကြိမ် တိုင်းတာမှု ၂၄/၂၇ သည် ၈၈.၉% ဖြစ်သဖြင့်
  ထို သတ်မှတ်ချက်အောက်တွင် ကျရှုံးမှု နှစ်ခု ပေါ်လာသည်။
- ပြင်ဆင်ချက်: သက်သေ ဖိုင် စာရင်းတွင် ပထမ ကိုးခု သာ ရှိခဲ့သည်။
  verifier output ကို ဆယ်ခုမြောက်အဖြစ် ထည့်သည်။
- အတည်ပြုရန် လိုသည်: macOS agent installer ၏ တိကျသော flag များ။
  ဤစာတမ်းတွင် command ကို မပေးထားပါ။ version အလိုက် ပြန်စစ်ရန် လိုသည်။
- အတည်ပြုရန် လိုသည်: `openuem-cert-manager` ၏ flag အစုံသည် version အလိုက်
  ပြောင်းလဲနိုင်သည်။ ဤစာတမ်းတွင် documentation မှ နမူနာကို အတိုင်း
  ကူးထားသည်။
- အတည်ပြုရန် လိုသည်: console ၏ menu အမည်များ (dashboard ကတ်, profile view)
  သည် version အလိုက် ကွဲပြားနိုင်သည်။ ဤစာတမ်းတွင် ယေဘုယျ အမည်များ သုံးထားသည်။
- ကိန်းဂဏန်း အားလုံး (endpoint ၂၇, wave ၃/၁၅/၉, လိုက်နာမှု ၂၄/၂၇,
  လက်မှတ် ၂၃, scorecard ၈၅.၅) သည် သင်ကြားရေး ဥပမာ ဖြစ်သည်။
  တိုင်းတာထားသော ရလဒ် မဟုတ်ပါ။
