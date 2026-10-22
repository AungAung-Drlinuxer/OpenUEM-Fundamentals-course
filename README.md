# OpenUEM Endpoint Management Fundamentals

Self-hosted endpoint management ကို လက်တွေ့ လေ့လာရန် မြန်မာဘာသာ course။
OpenUEM ကို lab တွင် တည်ဆောက်ခြင်းမှ စ၍ agent ဖြန့်ခြင်း၊ enrollment၊
software deployment၊ profile၊ patch စီမံခန့်ခွဲမှု၊ report နှင့်
troubleshooting အထိ module ဆယ့်နှစ်ခုဖြင့် ဖွဲ့စည်းထားသည်။

## ဤ course က ဘယ်သူအတွက်လဲ

- Windows, macOS, Linux endpoint များကို စီမံခန့်ခွဲရသော system administrator
- SaaS endpoint manager မှ self-hosted သို့ ကူးပြောင်းရန် စီစဉ်သူ
- OpenUEM ကို production မတိုင်မီ lab တွင် အပြည့်အစုံ စမ်းသပ်လိုသူ

တစ်ခုချင်း command ကို ရှင်းလင်းချက်နှင့်တကွ ဖော်ပြထားသည်။
Output များကို `# simulated output — illustrative` ဟု အမှတ်အသားပြုထားပြီး
သင့်စက်၏ တကယ့် output မဟုတ်ကြောင်း ရှင်းလင်းထားသည်။

## Module များ

| # | Module | အဓိက အကြောင်းအရာ |
|---|---|---|
| 01 | Introduction to OpenUEM | endpoint management အခြေခံ၊ component map၊ lifecycle |
| 02 | PostgreSQL Preparation | Ubuntu 24.04 တွင် database/role၊ `pg_hba`၊ URI encoding |
| 03 | Ubuntu 24.04 Server Install | apt repo၊ certificate၊ `openuem.ini`၊ systemd၊ reverse proxy |
| 04 | Docker/Podman Deployment | `openuem-docker`၊ `.env`၊ compose၊ hosts override |
| 05 | Agent Deployment | Windows/macOS/Linux agent၊ certificate၊ port |
| 06 | Enrollment & Organization | admission၊ org/site၊ tag၊ user နှင့် role |
| 07 | Device Management | inventory၊ package၊ profile၊ remote assistance |
| 08 | Patch Management | update visibility၊ maintenance window၊ compliance |
| 09 | Reporting & Troubleshooting | report၊ dashboard၊ log၊ connectivity |
| 10 | Capstone | two sites၊ three platforms၊ incident နှင့် review |
| 11 | Server & Agent Upgrade | console/command upgrade၊ wave၊ rollback |
| 12 | RustDesk Remote Desktop | hbbs/hbbr၊ client၊ OpenUEM integration |

## ဘာသာစကား နှစ်မျိုး

Module တိုင်းတွင် မြန်မာဘာသာ ဖိုင်များ (`README.md`, `explanation.md`,
`exercise.md`, `solution.md`) နှင့်အတူ **English edition** ဖြစ်သော
`README.en.md`, `explanation.en.md`, `exercise.en.md`, `solution.en.md`
ဖိုင်များ ပါဝင်သည်။ Lab (`lab.py`) သည် ဘာသာစကား နှစ်မျိုးလုံးအတွက်
တစ်ခုတည်း ဖြစ်သည်။

## Folder တည်ဆောက်ပုံ

```text
OpenUEM-Fundamentals-course/
├── COURSE_OUTLINE.md      # သင်ရိုးညွှန်း
├── MODULE_SPEC.md         # module တစ်ခုချင်း scope နှင့် verified facts
├── WRITING_RULES.md       # စာရေးပုံ စည်းမျဉ်း
├── README.md
├── run_all_labs.py
├── scripts/
│   └── verify_course_build.py
└── modules/
    └── NN_slug/
        ├── README.md
        ├── explanation.md
        ├── exercise.md
        ├── solution.md
        └── lab.py
```

## Lab များ run ခြင်း

Lab တစ်ခုချင်းကို Python standard library သာဖြင့် ရေးထားသည်။
Network သို့မဟုတ် OpenUEM server မလိုအပ်ပါ။

```bash
python3 modules/02_postgres_docker/lab.py
```

Module အားလုံးကို တစ်ပြိုင်နက် စစ်ဆေးရန် —

```bash
python3 run_all_labs.py
```

Course တစ်ခုလုံး၏ structure နှင့် အရည်အသွေးကို စစ်ဆေးရန် —

```bash
python3 scripts/verify_course_build.py --repo . --min-chars 5000 --exercises 6 --runs 3
```

## လိုအပ်ချက်

- Python 3.10 သို့မဟုတ် အထက် (labs အတွက်)
- OpenUEM ကို တကယ် install လုပ်မည်ဆိုပါက Linux host တစ်ခု၊ PostgreSQL
  နှင့် DNS domain တစ်ခု (Module 02 နှင့် 03 တွင် အသေးစိတ်)

## သတိပြုရန်

- Course ထဲက port နှင့် package အမည်များသည် OpenUEM official documentation
  မှ ရယူထားသည်။ Version အလိုက် ပြောင်းလဲနိုင်သည့် အချက်များကို
  `Technical review notes` တွင် မှတ်သားထားသည်။
- Lab output များသည် သင်ကြားရေးအတွက် ဖန်တီးထားသော fixture များဖြစ်သည်။
  မိမိစက်၏ တကယ့် တိုင်းတာချက်အဖြစ် မယူဆရ။