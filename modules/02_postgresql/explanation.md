# Module 02 — PostgreSQL ပြင်ဆင်ခြင်း (Ubuntu 24.04)

## Database ကို ဘာကြောင့် ဦးစွာ ပြင်ဆင်ရသည်

OpenUEM ၏ component တိုင်း — console၊ agent worker၊ cert-manager worker၊
notification worker — သည် PostgreSQL ကို ဖတ်ရ၊ ရေးရသည်။ Installer က
ပထမဆုံး မေးသော မေးခွန်းမှာ `DATABASE_URL` ဖြစ်သည်။ Database မရှိပါက
installer သည် schema ဖန်တီး၍ မရနိုင်သဖြင့် လုပ်ငန်းစဉ် ရပ်တန့်သည်။

ထို့ကြောင့် အဆင့်စဉ်မှာ ဤသို့ ဖြစ်သည်။

```text
PostgreSQL install → role + database ဖန်တီး → URI ဖြင့် စမ်းသပ်
→ OpenUEM install (schema ဖန်တီး) → worker များ ချိတ်ဆက်
```

Database အဆင့်တွင် မှားယွင်းပါက နောက်ပိုင်း တွင်မည့် အမှားများသည်
"connection refused" သို့မဟုတ် "password authentication failed" ကဲ့သို့
ရှုပ်ထွေးသော ပုံစံဖြင့် ပေါ်လာပြီး အကြောင်းရင်း ရှာရ ခက်သည်။
ဤ module တွင် database အဆင့်ကို သီးခြား စမပ်ပြီး ကျန်အဆင့်များအတွက်
အခြေခံ ခိုင်မာစေသည်။

## Ubuntu 24.04 တွင် PostgreSQL install လုပ်ခြင်း

Ubuntu ၏ မူလ repository တွင် PostgreSQL ပါဝင်သည်။ Version ကို
သီးခြား သတ်မှတ်ရန် မလိုအပ်ပါ။

```bash
sudo apt update
sudo apt install -y postgresql postgresql-client
```

`postgresql` သည် server ဖြစ်ပြီး `postgresql-client` သည် `psql` အပါအဝင်
client tool များကို ပေးသည်။

```bash
sudo systemctl enable --now postgresql
```

Boot လုပ်သည့်အခါ အလိုအလျောက် စတင်ရန် enable လုပ်ပြီး ယခု အချိန်တွင်
စတင်ရန် `--now` ကို သုံးသည်။

```bash
systemctl status postgresql --no-pager
pg_lsclusters
ss -ltnp | grep 5432
```

ပထမ command က service အခြေအနေ၊ ဒုတိယက cluster အမည်နှင့် version၊
တတိယက 5432 port ကို မည်သည့် process က ဖွင့်ထားသည်ကို ပြသည်။
Ubuntu 24.04 ၏ မူလ package သည် PostgreSQL 16 ဖြစ်သည် — version အလိုက်
ပြန်စစ်ရန် လိုသည်။

## Database နှင့် role ဖန်တီးခြင်း

PostgreSQL တွင် `postgres` ဟူသော superuser ရှိသည်။ ထို account ဖြင့်
`psql` ထဲ ဝင်ရသည်။

```bash
sudo -u postgres psql
```

ထို့နောက် database နှင့် သီးခြား role တစ်ခု ဖန်တီးသည်။

```sql
CREATE DATABASE openuem;
CREATE USER openuem_app WITH ENCRYPTED PASSWORD 'change-this-password';
GRANT ALL PRIVILEGES ON DATABASE openuem TO openuem_app;
ALTER DATABASE openuem OWNER TO openuem_app;
\c openuem
GRANT ALL ON SCHEMA public TO openuem_app;
\q
```

လိုင်းတစ်ခုချင်း၏ အဓိပ္ပာယ် —

- `CREATE DATABASE openuem;` — OpenUEM အတွက် database အသစ် ဖန်တီးသည်။
- `CREATE USER ... WITH ENCRYPTED PASSWORD ...` — application အတွက် role
  တစ်ခု ဖန်တီးသည်။ Password ကို hash အဖြစ် သိမ်းရန် `ENCRYPTED` ကို သုံးသည်။
- `GRANT ALL PRIVILEGES ON DATABASE ...` — database အဆင့် ခွင့်ပြုချက် ပေးသည်။
- `ALTER DATABASE ... OWNER TO ...` — database ၏ ပိုင်ရှင်ကို သတ်မှတ်သည်။
- `\c openuem` — ထို database သို့ ချိတ်ဆက်သည်။
- `GRANT ALL ON SCHEMA public TO ...` — PostgreSQL 15 နှင့် အထက်တွင်
  `public` schema တွင် table ဖန်တီးခွင့်ကို ပုံမှန်အားဖြင့် ပိတ်ထားသည်။
  OpenUEM က table များ ဖန်တီးနိုင်ရန် ဤ grant လိုအပ်သည်။

> Superuser `postgres` ကို OpenUEM ၏ connection user အဖြစ် မသုံးရ။
> Application တစ်ခုစီအတွက် သီးခြား role သုံးခြင်းသည် လုံခြုံရေး အခြေခံ
> သဘောတရား ဖြစ်သည်။

## Connection URI ဖွဲ့စည်းခြင်း

OpenUEM က ချိတ်ဆက်ရန် URI တစ်ခု လိုအပ်သည်။ ပုံစံမှာ —

```text
postgres://USER:PASSWORD@HOST:PORT/DATABASE
```

နမူနာ —

```text
postgres://openuem_app:change-this-password@localhost:5432/openuem
```

Password တွင် အထူးစာလုံး ပါဝင်ပါက percent-encoding လုပ်ရသည်။
PostgreSQL ၏ connection string စည်းမျဉ်းအရ `:`၊ `/`၊ `@`၊ `?`၊ `#`၊
`&` နှင့် `=` ကဲ့သို့သော စာလုံးများကို ကုဒ်ပြောင်းရသည်။

| စာလုံး | ကုဒ် | စာလုံး | ကုဒ် |
|---|---|---|---|
| space | `%20` | `=` | `%3D` |
| `/` | `%2F` | `?` | `%3F` |
| `:` | `%3A` | `#` | `%23` |
| `@` | `%40` | `&` | `%26` |

ဥပမာ — password သည် `te=st` ဖြစ်ပါက URI တွင် `te%3Dst` ဟု ရေးရသည်။
မကုဒ်ပြောင်းပါက URI ကို မှားယွင်းစွာ ခွဲခြမ်းပြီး password အမှား ဖြစ်သည်။

**Figure 1 — Database preparation order**

```mermaid
flowchart TD
    A["PostgreSQL install<br/>apt / docker"] --> B["role + database<br/>CREATE USER / DATABASE"]
    B --> C["GRANT on schema public"]
    C --> D["URI တည်ဆောက်<br/>percent-encoding"]
    D --> E{"psql ဖြင့် စမ်းသပ်"}
    E -->|"မအောင်မြင်"| F["pg_hba / password / port စစ်"]
    F --> D
    E -->|"အောင်မြင်"| G["OpenUEM installer<br/>schema ဖန်တီး"]
```

ပုံရှင်းလင်းချက် — ပထမ၊ PostgreSQL ကို install လုပ်သည်။ ဒုတိယ၊ role နှင့်
database ကို ဖန်တီးသည်။ တတိယ၊ `public` schema အပေါ် ခွင့်ပြုချက် ပေးသည်။
စတုတ္ထ၊ password ကို percent-encoding လုပ်ပြီး URI တည်ဆောက်သည်။
ပဉ္စမ၊ `psql` ဖြင့် တိုက်ရိုက် စမ်းသပ်သည်။ မအောင်မြင်ပါက `pg_hba.conf`၊
password နှင့် port ကို ပြန်စစ်ပြီး URI ကို ပြင်သည်။ အောင်မြင်မှသာ
OpenUEM installer ကို ဆက်လုပ်သည်။ Installer သည် ဤအဆင့်တွင် table များ
ဖန်တီးသည်။

## `pg_hba.conf` နှင့် authentication method

PostgreSQL က ချိတ်ဆက်မှုတိုင်းကို `pg_hba.conf` ဖြင့် စစ်ဆေးသည်။
Ubuntu တွင် ဖိုင်သည် `/etc/postgresql/<version>/main/pg_hba.conf` ဖြစ်သည်။

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

ဤ command က အသုံးပြုနေသော ဖိုင်၏ လမ်းကြောင်းကို ပြသည်။

မူလအားဖြင့် local socket အတွက် `peer`၊ TCP (`127.0.0.1/32`) အတွက်
`scram-sha-256` သို့မဟုတ် `md5` ဖြစ်သည်။ OpenUEM က TCP ဖြင့် ချိတ်ဆက်သဖြင့်
`127.0.0.1/32` လိုင်းတွင် password authentication ဖွင့်ထားရသည်။
RPM-based host များတွင် `ident` ကို `md5` သို့ ပြောင်းရန် documentation က
သတ်မှတ်ထားသည်။

```bash
sudo systemctl restart postgresql
```

`pg_hba.conf` ကို ပြင်ပြီးတိုင်း restart လုပ်ရသည်။ reload ဖြင့် လုံလောက်သည့်
အခြေအနေများ ရှိသော်လည်း သင်ကြားရေး lab တွင် restart ကို အသုံးပြုသည်။

**Figure 2 — Connection path from a worker to the database**

```mermaid
sequenceDiagram
    participant W as "Agent worker"
    participant P as "PostgreSQL"
    participant H as "pg_hba.conf"
    W->>P: "postgres://openuem_app:...@localhost:5432/openuem"
    P->>H: "rule ရှာ (host 127.0.0.1/32)"
    H-->>P: "scram-sha-256"
    P->>P: "password စစ်"
    P-->>W: "connection accepted"
    W->>P: "CREATE TABLE ... (schema)"
    P-->>W: "OK"
```

ပုံရှင်းလင်းချက် — worker က URI ဖြင့် ချိတ်ဆက်သည်။ PostgreSQL က ချိတ်ဆက်မှု
အမျိုးအစားနှင့် လိပ်စာအလိုက် `pg_hba.conf` မှ သက်ဆိုင်ရာ လိုင်းကို ရှာသည်။
ထို လိုင်းက authentication method ကို ပြန်ပေးသည်။ password မှန်ပါက
ချိတ်ဆက်မှု လက်ခံပြီး worker က table ဖန်တီးနိုင်သည်။ ဤပုံတွင် မည်သည့်
အဆင့်တွင် မအောင်မြင်နိုင်သည်ကို မြင်နိုင်သည် — rule မကိုက်ညီခြင်း၊
method မှားခြင်း၊ password မှားခြင်း ဖြစ်သည်။

## ချိတ်ဆက်မှုကို စမ်းသပ်ခြင်း

Installer မစမီ URI ကို တိုက်ရိုက် စမ်းသပ်ရသည်။

```bash
psql "postgres://openuem_app:change-this-password@localhost:5432/openuem" -c "SELECT current_user, current_database();"
```

```text
# simulated output — illustrative
 current_user | current_database
--------------+------------------
 openuem_app  | openuem
(1 row)
```

ဤ output တွင် user နှင့် database အမည် မှန်ကန်ကြောင်း အတည်ပြုနိုင်သည်။
Password ကို shell history တွင် မထင်စေရန် `PGPASSWORD` ကို အသုံးပြုနိုင်သည်။

```bash
PGPASSWORD='change-this-password' psql -h localhost -U openuem_app -d openuem -c "SELECT 1;"
```

`-h localhost` က TCP ဖြင့် ချိတ်ဆက်ရန် ညွှန်ကြားသည်။ `-h` မပါပါက
local socket ကို သုံးပြီး `peer` authentication ဖြင့် စမ်းသပ်မိသည်။
ထို့ကြောင့် OpenUEM ၏ အခြေအနေနှင့် မတူနိုင်ပါ။

## Backup နှင့် ပြန်လည် ရယူခြင်း

Database သည် OpenUEM ၏ အချက်အလက်အားလုံး — agent report၊ deployment မှတ်တမ်း၊
user နှင့် certificate metadata — ကို သိမ်းထားသည်။ Certificate folder နှင့်
အတူ backup လုပ်ရသည်။

```bash
pg_dump -Fc -h localhost -U openuem_app -d openuem -f openuem.dump
```

`-Fc` သည် custom format ဖြစ်ပြီး `pg_restore` ဖြင့် ပြန်လည် ထည့်နိုင်သည်။

```bash
createdb -h localhost -U openuem_app openuem_restore
pg_restore -h localhost -U openuem_app -d openuem_restore openuem.dump
```

ပြန်လည် ရယူသည့်အခါ OpenUEM service များကို ရပ်ထားရသည်။
မဟုတ်ပါက worker များက မပြီးသော transaction များဖြင့် ရောနှောနိုင်သည်။

## ပြန်လည် ရှင်းလင်းခြင်း (clean reinstall)

Lab တွင် အစမှ ပြန်စလိုပါက နည်းလမ်း နှစ်ခု ရှိသည်။

1. **Database ကို ဖျက်ပြီး အသစ် ဖန်တီးခြင်း** — အရှင်းဆုံး နည်းလမ်း။
   `DROP DATABASE openuem;` ပြီးနောက် ပြန် ဖန်တီးသည်။
2. **Table များကို ဖျက်ခြင်း** — database ကို ထိန်းထားပြီး OpenUEM table
   များကိုသာ ဖျက်သည်။ Documentation တွင် `\c openuem` ပြီးနောက်
   `DROP TABLE "agents" CASCADE;` စသည်ဖြင့် စာရင်း ပေးထားသည်။

```sql
\c openuem
DROP TABLE "certificates" CASCADE;
DROP TABLE "agents" CASCADE;
DROP TABLE "computers" CASCADE;
DROP TABLE "deployments" CASCADE;
DROP TABLE "profiles" CASCADE;
DROP TABLE "tasks" CASCADE;
DROP TABLE "users" CASCADE;
\q
```

ဖျက်သည့်အခါ `CASCADE` က ဆက်စပ် foreign key များကိုပါ ဖျက်သည်။
ထို့ကြောင့် လိုအပ်သော data ရှိပါက အရင် backup လုပ်ရသည်။

## Container ဖြင့် database ထည့်သွင်းခြင်း

`openuem-docker` ကို သုံးပါက PostgreSQL ကို compose က အလိုအလျောက်
ဖန်တီးပေးသည်။ `.env` ထဲတွင် ဤတန်ဖိုးများ သတ်မှတ်ရသည်။

```text
DATABASE_DB_NAME=openuem
DATABASE_PORT=5432
DATABASE_USER=openuem
DATABASE_PASSWORD=change-this-dbpassword
OPENUEM_DATABASE_URL=postgres://openuem:change-this-dbpassword@openuem-db:5432/openuem
```

ဤနေရာတွင် host အမည်သည် `localhost` မဟုတ်ဘဲ compose service အမည်
(`openuem-db`) ဖြစ်သည်။ Container များသည် တစ်ခုနှင့်တစ်ခု service အမည်ဖြင့်
ချိတ်ဆက်သည်။

| အချက် | Native PostgreSQL | Compose PostgreSQL |
|---|---|---|
| install | `apt install postgresql` | image ကို အလိုအလျောက် ဆွဲ |
| ဒေတာ တည်ရှိမှု | `/var/lib/postgresql` | named volume |
| backup | `pg_dump` | `docker compose exec` + `pg_dump` |
| upgrade | package upgrade | image tag ပြောင်း |
| ထိန်းသိမ်းမှု | ကိုယ်တိုင် | compose က စီမံ |
| သင့်လျော်သည့် နေရာ | production၊ သီးခြား DB server | lab၊ single-host deployment |

## လုပ်ငန်းခွင်တွင် သတိပြုရန်

- Password ကို `.env` သို့မဟုတ် `openuem.ini` တွင် ထည့်သည့်အခါ file
  permission ကို ကန့်သတ်ရသည် (`chmod 600`)။
- Database port (5432) ကို အင်တာနက်သို့ မဖွင့်ရ။ OpenUEM component များ
  ရှိသော host မှသာ ချိတ်ဆက်နိုင်ရမည်။
- Disk နေရာ လုံလောက်မှုကို ကြိုတင်စစ်ရသည်။ Agent report များ စုပုံလာသည်နှင့်
  database ကြီးထွားသည်။
- PostgreSQL version upgrade မတိုင်မီ `pg_dump` ဖြင့် backup ယူပြီး
  restore ကို သီးခြား host တွင် စမ်းသပ်ရသည်။
- Time zone နှင့် clock ကို NTP ဖြင့် ကိုက်ညီအောင် ထားရသည်။
  Certificate နှင့် log အချိန်များ မှားယွင်းနိုင်သည်။

## ကိုယ်တိုင်စစ်ဆေးရန် မေးခွန်းများ

**၁။ `GRANT ALL ON SCHEMA public` ကို ဘာကြောင့် လိုအပ်သနည်း။**
PostgreSQL 15 နှင့် အထက်တွင် `public` schema တွင် table ဖန်တီးခွင့်ကို
ပုံမှန် user များအတွက် ပိတ်ထားသည်။ OpenUEM က schema ဖန်တီးနိုင်ရန်
ဤ grant လိုအပ်သည်။

**၂။ Password တွင် `@` ပါဝင်ပါက URI တွင် ဘယ်လိုရေးရသည်။**
`%40` ဟု ကုဒ်ပြောင်းရသည်။ မဟုတ်ပါက URI parser က host အစိတ်အပိုင်းအဖြစ်
မှားယွင်း ခွဲခြမ်းသည်။

**၃။ `psql` ဖြင့် စမ်းသပ်သည့်အခါ `-h localhost` ကို ဘာကြောင့် ထည့်ရသည်။**
`-h` မပါပါက local Unix socket ကို သုံးပြီး `peer` authentication ဖြစ်သည်။
OpenUEM က TCP ဖြင့် ချိတ်ဆက်သဖြင့် တူညီသော လမ်းကြောင်းဖြင့် စမ်းသပ်ရသည်။

**၄။ Compose deployment တွင် `OPENUEM_DATABASE_URL` ၏ host က ဘာဖြစ်သနည်း။**
`localhost` မဟုတ်ဘဲ database service ၏ အမည် (နမူနာ `openuem-db`) ဖြစ်သည်။
Container network အတွင်း service အမည်ဖြင့် ဖြေရှင်းသည်။

## Technical review notes

- SQL နှင့် `pg_hba.conf` ဆိုင်ရာ အချက်များကို openuem.eu/docs
  (Advanced Topics → Postgres) မှ ရယူထားသည်။
- Ubuntu 24.04 ၏ PostgreSQL version (16) သည် distribution အလိုက်
  ပြောင်းနိုင်သည် — version အလိုက် ပြန်စစ်ရန် လိုသည်။
- `GRANT ALL ON SCHEMA public` သည် PostgreSQL 15+ ၏ မူလအပြောင်းအလဲကို
  အခြေခံသည်။ ရှေးဟောင်း version များတွင် မလိုအပ်နိုင်ပါ။
- OpenUEM table စာရင်းအပြည့်အစုံသည် version အလိုက် ပြောင်းနိုင်သဖြင့်
  documentation ၏ စာရင်းကို အသုံးပြုရန် လိုသည်။
