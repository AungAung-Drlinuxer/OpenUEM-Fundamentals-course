# Module 06 — အဖြေများ

လေ့ကျင့်ခန်း တစ်ခုစီ၏ အဖြေကို အောက်တွင် ဖော်ပြထားသည်။ Output အကွက်များသည်
`lab.py` ကို run ပြီးရရှိသော output အတိအကျ ဖြစ်သည်။

```bash
python3 modules/06_enrollment_organization/lab.py
```

## Exercise 1 — ခွင့်ပြု/ငြင်းပယ် ဆုံးဖြတ်ချက်များ

ပထမ တောင်းခံမှု လေးခုသည် ဇယားတွင် ပါသော လမ်းကြောင်းများ ဖြစ်သဖြင့် ခွင့်ပြုခံရသည်။
agent-05 နှင့် agent-06 သည် လုပ်ဆောင်နိုင်သော အခြေအနေ မှ admission queue သို့ ပြန်သွားရန်
လမ်းကြောင်း မရှိသဖြင့် ငြင်းပယ်ခံရသည်။ agent-07 သည် အခြေအနေ တူညီသော တောင်းခံမှု
ဖြစ်သဖြင့် အလုပ်မရှိသော တောင်းခံမှု အဖြစ် ငြင်းပယ်ခံရသည်။ စုစုပေါင်း ခွင့်ပြု ၄ ခု၊
ငြင်းပယ် ၃ ခု ဖြစ်သည်။

```text
exercise 1 — agent state transition validation
  agent-01  waiting_for_admission -> enabled               allow: admit from the console
  agent-02  waiting_for_admission -> disabled              allow: reject the admission request
  agent-03  enabled               -> disabled              allow: disable a manageable agent
  agent-04  disabled              -> enabled               allow: re-enable a disabled agent
  agent-05  enabled               -> waiting_for_admission deny: no rule returns to the admission queue
  agent-06  disabled              -> waiting_for_admission deny: no rule returns to the admission queue
  agent-07  enabled               -> enabled               deny: state is already the requested one
  summary: allow=4 deny=3
[OK] exercise_1 — state transitions follow the admission state machine```

ငြင်းပယ်ရသည့် အကြောင်းရင်းမှာ admission queue သည် တစ်ကြိမ်သာ ဖြတ်ကျော်နိုင်သော အဆင့်
ဖြစ်ခြင်း နှင့် ဆက်စပ်သည်။ Agent တစ်ခု လက်ခံပြီးနောက် ထို endpoint ကို ပြန်လည် စစ်ဆေးလိုပါက
Disabled သို့ ပြောင်းပြီး ပြန်လည် ဖွင့်ခြင်းဖြင့် လုပ်ဆောင်ရသည်။

## Exercise 2 — စောင့်ဆိုင်းနေသော agent စာရင်း

Fixture တွင် agent ၁၂ ခု ရှိပြီး disabled ၂ ခု၊ enabled ၅ ခု၊ waiting_for_admission ၅ ခု
ဖြစ်သည်။ စောင့်ဆိုင်းနေသော ငါးခုကို organization အလိုက် ခွဲပါက branch-office ၂ ခု၊
head-office ၂ ခု၊ lab ၁ ခု ဖြစ်သည်။ စောင့်ဆိုင်းချိန် အများဆုံးမှာ PC-007 (၁၈၄၀ မိနစ်)
ဖြစ်သဖြင့် ပထမဆုံး လက်ခံရန် အကြံပြုသည်။

```text
exercise 2 — admission queue summary
  fixture size: 12 agents
  state                   count
  disabled                    2
  enabled                     5
  waiting_for_admission       5
  waiting per organization
  branch-office               2
  head-office                 2
  lab                         1
  oldest waiting (top 3)
  PC-007  branch-office   windows    1840 min
  PC-014  branch-office   macos      1560 min
  PC-009  head-office     linux       920 min
[OK] exercise_2 — queue census and per-organization backlog agree```

စောင့်ဆိုင်းချိန် ၁၈၄၀ မိနစ်သည် နေ့တစ်ခုနှင့် အထက် ဖြစ်သဖြင့် ထို endpoint ကို လက်ခံရန်
မေ့နေကြောင်း အချက်ပြသည်။ Waiting for admission အခြေအနေတွင် report များ ဆက်လက် ရောက်ရှိနေသဖြင့်
ထို endpoint သည် ကွန်ရက် နှင့် ချိတ်ဆက်မှု ကောင်းမွန်နေကြောင်း သိနိုင်သည်။

## Exercise 3 — Organization နှင့် site ဖြေရှင်းမှု

PC-101 တွင် ကော်လံ နှစ်ခုလုံး အလွတ် ဖြစ်သဖြင့် default organization `head-office` ကို
အသုံးပြုပြီး ထို organization ၏ site များ အနက် အက္ခရာ အစဉ်လိုက် ပထမဖြစ်သော `hq-floor1`
ကို ရွေးသည်။ PC-102 တွင် site အလွတ် ဖြစ်သဖြင့် `warehouse` ကို ရသည်။ PC-103 တွင်
ကော်လံ နှစ်ခုလုံး ပြည့်စုံသဖြင့် တိုက်ရိုက် အတည်ပြုသည်။ PC-104 ၏ organization တွင်
site မရှိပါ။ PC-105 ၏ site သည် အခြား organization ၏ site ဖြစ်သည်။ PC-106 ၏ organization
မတည်ရှိပါ။ အောင်မြင်မှု ၃ ခု၊ ငြင်းပယ်မှု ၃ ခု ဖြစ်သည်။

```text
exercise 3 — organization and site assignment resolution
  PC-101  head-office     hq-floor1   ok
  PC-102  branch-office   warehouse   ok
  PC-103  head-office     hq-floor2   ok
  PC-104  lab                         error: organization has no site
  PC-105  branch-office   hq-floor1   error: site does not belong to organization
  PC-106  unknown-org     warehouse   error: unknown organization
  summary: resolved=3 rejected=3
[OK] exercise_3 — default organization and site fallback resolved```

PC-105 သည် အဖြစ် အများဆုံး မှားယွင်းမှု ဖြစ်သည်။ Site အမည် မှန်နေသော်လည်း organization
မှားနေပါက ထို endpoint သည် မှားသော ဌာန ၏ report ထဲ ရောက်သွားမည် ဖြစ်သည်။

## Exercise 4 — CSV import စစ်ဆေးမှု

Organization အတန်း ၅ ခု အနက် အတန်း ၁ နှင့် ၅ သာ အောင်မြင်သည်။ အတန်း ၂ တွင် site
အလွတ် ဖြစ်သည်။ အတန်း ၃ သည် ဖိုင် ထဲတွင် ထပ်နေသော အမည် ဖြစ်သည်။ အတန်း ၄ ၏ အမည်
သည် server တွင် ရှိပြီး ဖြစ်သည်။ User အတန်း ၅ ခု အနက် အတန်း ၁ နှင့် ၅ သာ အောင်မြင်သည်။
အတန်း ၂ ၏ organization မတည်ရှိပါ။ အတန်း ၃ ၏ site သည် ထို organization ၏ site မဟုတ်ပါ။
အတန်း ၄ ၏ email သည် ဖိုင် ထဲတွင် ထပ်နေသည်။

```text
exercise 4 — CSV import validation (organizations then users)
  organization rows: 5  accepted: 2  rejected: 3
    row 2  west-branch   error: site column is empty
    row 3  east-branch   error: duplicate organization name in file
    row 4  head-office   error: organization already exists on the server
  user rows: 5  accepted: 2  rejected: 3
    row 2  b@openuem.example   error: unknown organization ghost-org
    row 3  c@openuem.example   error: site hq-floor1 does not belong to branch-office
    row 4  a@openuem.example   error: duplicate user email in file
  note: organizations are imported before users because row 5 needs east-branch
[OK] exercise_4 — CSV rows rejected for duplicates and missing site```

အတန်း ၅ သည် `east-branch` ကို ရည်ညွှန်းသည်။ ထို organization ကို အတန်း ၁ က ဖန်တီးပေးသဖြင့်
organization import ကို အရင် ပြီးစီးရန် လိုအပ်သည်။ အစီအစဉ် မှားပါက မှန်ကန်သော user အတန်း
တစ်ခု ပါ ငြင်းပယ်ခံရမည် ဖြစ်သည်။

## Exercise 5 — Least privilege အကဲဖြတ်မှု

လိုအပ်သော capability နှစ်ခုကို ဖြည့်ဆည်းပေးနိုင်သော role သုံးမျိုး ရှိသည်။ ပိုလျှံသော
capability အရေအတွက်မှာ operator ၂ ခု၊ administrator ၄ ခု၊ owner ၅ ခု ဖြစ်သည်။
အနည်းဆုံး ဖြစ်သော operator ကို ရွေးသည်။ `helpdesk-01` အတွက် administrator အဆိုပြုချက်
သည် ပိုလျှံသော capability ၄ ခု ပါဝင်သဖြင့် ငြင်းပယ်သည်။

```text
exercise 5 — administrator capability matrix and least privilege
  capability            administrator    operator         owner            read_only
  admit_agent           Y                -                Y                -
  export_reports        Y                Y                Y                Y
  force_report          Y                Y                Y                -
  manage_orgs           -                -                Y                -
  manage_users          Y                -                Y                -
  remote_assistance     Y                Y                Y                -
  view_inventory        Y                Y                Y                Y
  required capabilities: force_report, view_inventory
  candidates (excess capabilities):
    operator        excess 2
    administrator   excess 4
    owner           excess 5
  least privilege role: operator
  proposal helpdesk-01 -> administrator: rejected (operator sufficient, excess 4)
[OK] exercise_5 — smallest sufficient role selected for the duty```

အဆိုပြုချက် ကို ငြင်းပယ်ရသည့် အကြောင်းရင်းမှာ အလုပ်တာဝန် တစ်ခုအတွက် လိုအပ်သည်ထက်
ပိုသော အာဏာ ပေးခြင်းသည် အန္တရာယ် တိုးပွားစေခြင်း ဖြစ်သည်။ administrator role တွင်
user စီမံခွင့် ပါဝင်သဖြင့် helpdesk အကောင့် တစ်ခု ခိုးယူခံရပါက အကောင့် အသစ် ဖန်တီးနိုင်မည်
ဖြစ်သည်။

## Exercise 6 — Certificate အခြေအနေ လမ်းကြောင်း

PC-201 သည် regenerate ပြီးနောက် ပြန်လည် report ပို့သဖြင့် active အခြေအနေတွင် ပြီးဆုံးသည်။
PC-202 သည် revoke ပြီးနောက် revoked ဖြစ်သည်။ PC-203 သည် revoke ပြီးနောက် ဒုတိယ
admission_issue ဖြင့် issued သို့ ပြန်ရောက်သည်။ PC-204 တွင် certificate မရှိသေးဘဲ report
ပို့သဖြင့် ငြင်းပယ်ခံရသည်။ ငြင်းပယ်မှု စုစုပေါင်း ၁ ခု ဖြစ်သည်။

```text
exercise 6 — certificate lifecycle states
  PC-201  admission_issue  absent    -> issued   allow: server.cer/server.key pair created
  PC-201  first_report     issued    -> active   allow: agent reports over TLS with the pair
  PC-201  regenerate       active    -> issued   allow: old certificate revoked, new pair created
  PC-201  first_report     issued    -> active   allow: agent reports over TLS with the pair
  PC-202  admission_issue  absent    -> issued   allow: server.cer/server.key pair created
  PC-202  revoke           issued    -> revoked  allow: administrators revoke the certificate
  PC-203  admission_issue  absent    -> issued   allow: server.cer/server.key pair created
  PC-203  revoke           issued    -> revoked  allow: administrators revoke the certificate
  PC-203  admission_issue  revoked   -> issued   allow: re-admission creates a fresh pair
  PC-204  first_report     absent    -> absent   deny: event is not permitted in the current state
  final states
  PC-201  active
  PC-202  revoked
  PC-203  issued
  PC-204  absent
[OK] exercise_6 — certificate lifecycle states and revocations traced
[PASS] All 6/6 exercises passed successfully.```

PC-203 ၏ ဒုတိယ admission_issue သည် revoked အခြေအနေမှ စတင်သည်။ ထို လမ်းကြောင်းသည်
certificate အဟောင်း ကို ပြန်လည် အသုံးပြုခြင်း မဟုတ်ဘဲ အတွဲ အသစ် တစ်စုံ ထုတ်ပေးခြင်း
ဖြစ်သည်။ PC-204 ၏ အဆုံးသတ် အခြေအနေမှာ absent ဖြစ်ပြီး ထို endpoint ကို လက်ခံရန်
မလုပ်ဆောင်ရသေးကြောင်း ပြသည်။
