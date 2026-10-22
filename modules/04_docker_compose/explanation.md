# Module 04 — Docker/Podman ဖြင့် Deployment

## Container လမ်းကြောင်း ဘယ်အခါ သင့်လျော်သနည်း

OpenUEM ကို native package ဖြင့် install လုပ်ခြင်း (Module 03) နှင့်
container ဖြင့် install လုပ်ခြင်း နှစ်မျိုးလုံး တရားဝင် ပံ့ပိုးထားသည်။
Container လမ်းကြောင်းသည် အောက်ပါ အခြေအနေများတွင် ပိုသင့်လျော်သည်။

- lab သို့မဟုတ် demo တစ်ခုကို နာရီပိုင်းအတွင်း လိုချင်သည်
- host တွင် PostgreSQL နှင့် service ခုနစ်ခုကို သီးခြား install မလုပ်လိုသည်
- ပြန်လည် ဖျက်ပစ်နိုင်သော (disposable) ပတ်ဝန်းကျင် လိုသည်
- version အလိုက် ပြောင်းလဲမှုကို image tag ဖြင့် ထိန်းချုပ်လိုသည်

ဆန့်ကျင်ဘက်အားဖြင့် production တွင် host ၏ PostgreSQL ကို သီးခြား
ထိန်းသိမ်းလိုပါက သို့မဟုတ် ကုမ္ပဏီ၏ package management စည်းမျဉ်းက
container ကို ခွင့်မပြုပါက native လမ်းကြောင်း ပိုသင့်လျော်သည်။

## လိုအပ်ချက်များ

- Docker Engine နှင့် Compose plugin (သို့မဟုတ် Podman နှင့် podman-compose)
- DNS ဖြင့် ဖြေရှင်းနိုင်သော domain တစ်ခု (သို့မဟုတ် lab အတွက် hosts override)
- Port များ လွတ်နေရမည် — 1323, 1324, 4433, 8000, 5432
- Disk နေရာ — PostgreSQL data နှင့် image များအတွက်

```bash
docker --version
docker compose version
```

ပထမ command က Docker version၊ ဒုတိယက Compose plugin ရှိ/မရှိကို ပြသည်။
Compose plugin မရှိပါက `docker-compose` (hyphen) ကို သုံးရသည်။

## Repository ကို ရယူခြင်း

```bash
git clone https://github.com/open-uem/openuem-docker
cd openuem-docker
```

`openuem-docker` repository တွင် compose ဖိုင်နှင့် `.env-example` ပါဝင်သည်။

```bash
cp .env-example .env
```

ဖိုင်အမည်သည် `.env` ဖြစ်ရမည်။ အမည်တွင် extension မပါရ။
Docker က ဤအမည်ဖြင့်သာ environment variable များကို ဖတ်သည်။

## `.env` ၏ အဓိက တန်ဖိုးများ

| Variable | အဓိပ္ပာယ် | မဖြစ်မနေ |
|---|---|---|
| `DATABASE_DB_NAME` | database အမည် (ပထမ start တွင် ဖန်တီး) | ဟုတ် |
| `DATABASE_PORT` | database ၏ public port | ဟုတ် |
| `DATABASE_USER` | database user | ဟုတ် |
| `DATABASE_PASSWORD` | database password | ဟုတ် |
| `OPENUEM_DATABASE_URL` | component များ သုံးသော URI | ဟုတ် |
| `OPENUEM_ORGNAME` | အဖွဲ့အစည်း အမည် | ဟုတ် |
| `OPENUEM_COUNTRY` | နိုင်ငံ ကုဒ် | ဟုတ် |
| `OPENUEM_DOMAIN` | DNS domain | ဟုတ် |
| `CONSOLE_HOST` | console host အမည် | ဟုတ် |
| `CONSOLE_PORT` | console port (1323) | ဟုတ် |
| `CONSOLE_AUTH_PORT` | auth port (1324) | ဟုတ် |
| `CONSOLE_JWT_KEY` | JWT လက်မှတ် key | ဟုတ် |
| `NATS_HOST` | NATS host အမည် | ဟုတ် |
| `NATS_PORT` | NATS port (4433) | ဟုတ် |
| `OPENUEM_NATS_SERVERS` | agent များ သုံးသော NATS စာရင်း | ဟုတ် |
| `OCSP_URL` | OCSP responder URL | ဟုတ် |
| `OCSP_HOST` | OCSP host အမည် | ဟုတ် |
| `OCSP_PORT` | OCSP port (8000) | ဟုတ် |
| `REVERSE_PROXY_HOST` | reverse proxy အသုံးပြုပါက host | မဟုတ် |
| `REVERSE_PROXY_CONSOLE_PORT` | proxy မှ console သို့ port | မဟုတ် |
| `REVERSE_PROXY_AUTH_PORT` | proxy မှ auth သို့ port | မဟုတ် |
| `TZ` | container time zone | မဟုတ် |

`OPENUEM_DATABASE_URL` ၏ ပုံစံမှာ —

```text
postgres://USER:PASSWORD@openuem-db:5432/DATABASE
```

ဤနေရာတွင် host သည် `localhost` မဟုတ်ဘဲ compose service အမည် (`openuem-db`)
ဖြစ်သည်။ Password တွင် အထူးစာလုံး ပါဝင်ပါက Module 02 တွင် ဖော်ပြထားသော
percent-encoding စည်းမျဉ်းကို လိုက်နာရသည်။

## JWT key ကို ပြောင်းလဲခြင်း

`.env-example` တွင် မူလတန်ဖိုး ပါဝင်သည်။ တူညီသော key ကို အသုံးပြုသူ
အားလုံး သိထားပါက token ကို ဖန်တီး၍ ရနိုင်သည်။

```bash
openssl rand -hex 16
```

ဤ command က hex စာလုံး ၃၂ လုံး ထုတ်ပေးသည်။ ရလဒ်ကို
`CONSOLE_JWT_KEY` တွင် ထည့်ရသည်။

```text
# simulated output — illustrative
9f2c41ab7d3e58c0a6b1f4d92e7c0a38
```

ထို တန်ဖိုးကို version control ထဲ မထည့်ရ။ `.env` ကို `.gitignore` တွင်
ထည့်ထားရသည်။

## Stack ကို စတင်ခြင်း

```bash
docker compose up -d
```

`-d` သည် detached mode ဖြစ်ပြီး terminal ကို ပြန်ပေးသည်။
ပထမ start တွင် image များ ဆွဲခြင်းနှင့် database ဖန်တီးခြင်း ပါဝင်သဖြင့်
မိနစ်အနည်းငယ် ကြာနိုင်သည်။

**Figure 1 — Compose service layout**

```mermaid
flowchart TD
    L["docker compose up -d"] --> D[("openuem-db<br/>PostgreSQL 5432")]
    D --> N["nats<br/>4433"]
    D --> CM["cert-manager worker"]
    N --> AW["agent worker"]
    CM --> C["console<br/>1323 / 1324"]
    AW --> C
    D --> O["ocsp responder<br/>8000"]
    C --> P["reverse proxy (optional)"]
```

ပုံရှင်းလင်းချက် — compose က service များကို တစ်ပြိုင်နက် ဖန်တီးသည်။
ပထမ၊ database container စတင်ပြီး ပထမ start တွင် database နှင့် user ကို
`.env` တန်ဖိုးများမှ ဖန်တီးသည်။ ဒုတိယ၊ NATS နှင့် worker များ database သို့
ချိတ်ဆက်သည်။ တတိယ၊ console သည် worker များနှင့် database ကို သုံးပြီး
web UI ကို ဖွင့်သည်။ စတုတ္ထ၊ reverse proxy သတ်မှတ်ထားပါက console ရှေ့တွင်
HTTPS ကို ကိုင်တွယ်သည်။ Database မရသေးဘဲ worker များ စတင်ပါက
ပထမ စက္ကန့်များတွင် ချိတ်ဆက်မှု မအောင်မြင်နိုင်သဖြင့် container log ကို
စစ်ရသည်။

## စစ်ဆေးခြင်း

```bash
docker compose ps
```

service တစ်ခုချင်း၏ အခြေအနေ (running/healthy) ကို ပြသည်။

```bash
docker compose logs --tail=50 console
```

console container ၏ နောက်ဆုံး log ငါးဆယ်လိုင်းကို ပြသည်။
စတင်မှု မအောင်မြင်ပါက ဤနေရာတွင် အကြောင်းရင်း ပေါ်လာသည်။

```bash
docker compose exec openuem-db psql -U openuem -d openuem -c "\dt"
```

database ထဲရှိ table များကို ပြသည်။ Table များ ပေါ်နေပါက schema ဖန်တီးမှု
အောင်မြင်သည်။

Console ကို browser တွင် `http://CONSOLE_HOST:1323` ဖြင့် ဖွင့်သည်။
Reverse proxy သတ်မှတ်ထားပါက `https://REVERSE_PROXY_HOST` ဖြစ်သည်။

## DNS မရှိသော lab တွင် အမည် ဖြေရှင်းခြင်း

Lab တွင် DNS server မရှိပါက host ဖိုင် (hosts file) ကို ပြင်နိုင်သည်။
Linux တွင် `/etc/hosts`၊ Windows တွင်
`C:\Windows\System32\drivers\etc\hosts`၊ macOS တွင် `/private/etc/hosts` ဖြစ်သည်။

```text
192.168.1.43  nats.openuem.example  ocsp.openuem.example  console.openuem.example
```

`192.168.1.43` နေရာတွင် host ၏ LAN IP ကို ထည့်ရသည်။
`localhost` သို့မဟုတ် `127.0.0.1` ကို မသုံးရ။ Container တစ်ခုစီသည်
မိမိကိုယ်ကို ဖြေရှင်းမိသဖြင့် အခြား container ကို မရောက်နိုင်ပါ။

Docker က ဤ host ဖိုင် ထည့်သွင်းချက်များကို container များထဲ ကူးယူပေးသည်။
ထို့ကြောင့် `.env` တွင် သတ်မှတ်ထားသော အမည်များနှင့် hosts ထည့်သွင်းချက်
တိုက်ဆိုင်ရသည်။

## Reverse proxy နှင့် port များ

Reverse proxy မသုံးပါက `REVERSE_PROXY_*` တန်ဖိုးများကို အလွတ် ထားရသည်။

```text
REVERSE_PROXY_HOST=
REVERSE_PROXY_CONSOLE_PORT=
REVERSE_PROXY_AUTH_PORT=
```

Reverse proxy သုံးပါက Caddy ကို အသုံးပြုနိုင်သည်။ Documentation တွင်
Caddy သည် compose deployment အတွက် ပံ့ပိုးထားသော proxy ဖြစ်သည်။
ထို အခြေအနေတွင် host နှင့် port များကို ဖြည့်ရသည်။

**Figure 2 — First startup verification path**

```mermaid
sequenceDiagram
    participant A as "Admin"
    participant C as "Compose"
    participant D as "openuem-db"
    participant W as "console"
    A->>C: "docker compose up -d"
    C->>D: "create db + user (first start)"
    D-->>C: "ready"
    C->>W: "start console"
    A->>C: "docker compose ps"
    C-->>A: "services running"
    A->>W: "http://console:1323"
    W-->>A: "login page"
```

ပုံရှင်းလင်းချက် — ပထမ၊ စီမံခန့်ခွဲသူက compose ကို စတင်သည်။ ဒုတိယ၊ database
container က database နှင့် user ကို ဖန်တီးသည်။ တတိယ၊ console container စတင်သည်။
စတုတ္ထ၊ စီမံခန့်ခွဲသူက `docker compose ps` ဖြင့် အခြေအနေ စစ်သည်။
ပဉ္စမ၊ browser မှ console ကို ဖွင့်ပြီး login page ပေါ်လာခြင်းဖြင့်
အခြေခံ ချိတ်ဆက်မှု အောင်မြင်ကြောင်း အတည်ပြုသည်။

## Upgrade နှင့် ပြန်လည် ရှင်းလင်းခြင်း

```bash
git pull
docker compose pull
docker compose up -d
```

ပထမ command က compose ဖိုင်နှင့် `.env-example` အသစ်ကို ရယူသည်။
ဒုတိယက image tag အသစ်များကို ဆွဲသည်။ တတိယက ပြောင်းလဲသော container များကို
ပြန်လည် ဖန်တီးသည်။ အဆင့်မြှင့်မီ database dump ယူရသည်။

```bash
docker compose down
```

Container များကို ရပ်ပြီး ဖျက်သည်။ Volume များ ကျန်ရှိသဖြင့် ဒေတာ
မပျက်ပါ။

```bash
docker compose down -v
```

`-v` သည် volume များကိုပါ ဖျက်သည်။ Database ဒေတာ အားလုံး ပျက်မည်။
Lab တွင် အစမှ ပြန်စလိုသည့်အခါသာ သုံးရသည်။

| Command | Container | Volume/Data |
|---|---|---|
| `docker compose stop` | ရပ် | ကျန် |
| `docker compose down` | ဖျက် | ကျန် |
| `docker compose down -v` | ဖျက် | ဖျက် |

## Native နှင့် Container နှိုင်းယှဉ်ချက်

| အချက် | Native (Ubuntu 24.04) | Container (compose) |
|---|---|---|
| Install အချိန် | package တစ်ခုချင်း configure | `.env` ဖြည့်ပြီး တစ်ကြိမ်တည်း |
| Service စီမံမှု | `systemctl` | `docker compose` |
| Database | host ၏ PostgreSQL | container + volume |
| Upgrade | apt/dnf | image tag |
| Log | journald / ဖိုင် | `docker compose logs` |
| ပြန်လည် ရှင်းလင်း | package remove + DB drop | `down -v` |
| Production သင့်လျော်မှု | မြင့် | အလယ်အလတ် (single host) |

## လုပ်ငန်းခွင်တွင် သတိပြုရန်

- `.env` သည် secret များ ပါဝင်သဖြင့် permission ကို `600` ထားရသည်။
- `docker compose down -v` ကို အလွယ်တကူ မသုံးရ။ Database ပျက်သည်။
- Port များ ထပ်နေပါက container စတင်၍ မရပါ။ Module 01 တွင် ဖော်ပြထားသော
  port စာရင်းကို ကြိုတင်စစ်ရသည်။
- Hosts override ကို lab တွင်သာ သုံးရသည်။ Production တွင် DNS ကို
  သုံးရသည်။
- Container time zone (`TZ`) ကို သတ်မှတ်ထားခြင်းဖြင့် log အချိန်များ
  ကိုက်ညီစေသည်။
- Reverse proxy မသုံးပါက console ကို HTTP ဖြင့်သာ ရောက်နိုင်သည်။
  Production တွင် HTTPS မဖြစ်မနေ လိုအပ်သည်။

## ကိုယ်တိုင်စစ်ဆေးရန် မေးခွန်းများ

**၁။ `.env` တွင် database host ကို ဘာကြောင့် `localhost` မဟုတ်ဘဲ
service အမည် သုံးရသနည်း။**
Container တစ်ခုစီတွင် `localhost` သည် မိမိကိုယ်ကို ညွှန်သည်။
Compose network အတွင်း အခြား service ကို ရောက်ရန် service အမည်ဖြင့်
ဖြေရှင်းရသည်။

**၂။ `docker compose down` နှင့် `down -v` ကွာခြားချက်က ဘာလဲ။**
`down` သည် container များကိုသာ ဖျက်ပြီး volume ကျန်သည်။
`down -v` သည် volume ကိုပါ ဖျက်သဖြင့် database ဒေတာ ပျက်သည်။

**၃။ Lab တွင် hosts ဖိုင်ထဲ မည်သည့် IP ကို ထည့်ရသနည်း။**
Host ၏ LAN IP ကို ထည့်ရသည်။ `127.0.0.1` မသုံးရ။

**၄။ JWT key ကို ဘယ်လို ဖန်တီးနိုင်သနည်း။**
`openssl rand -hex 16` ဖြင့် hex စာလုံး ၃၂ လုံး ရနိုင်သည်။
မူလ တန်ဖိုးကို မသုံးရ။

## Technical review notes

- `.env` တန်ဖိုးများ၊ hosts override နှင့် Caddy ဆိုင်ရာ အချက်များကို
  openuem.eu/docs (Installation → Server → Docker/Podman) နှင့်
  `open-uem/openuem-docker` repository မှ ရယူထားသည်။
- Compose service အမည် (`openuem-db`) သည် repository ၏ ဖိုင်အလိုက်
  ပြောင်းနိုင်သည် — version အလိုက် ပြန်စစ်ရန် လိုသည်။
- 2025 December 22 မတိုင်မီ deployment များအတွက် ကွဲပြားသော legacy compose
  ဖိုင် ရှိသည်။ ထို အချက်ကို documentation ၏ Legacy section တွင် ကြည့်ရသည်။
- Reverse proxy အတွက် Caddy ကို documentation တွင် ပံ့ပိုးထားသည်။
  အခြား proxy များအတွက် header နှင့် port ကို ကိုယ်တိုင် စမ်းသပ်ရသည်။
