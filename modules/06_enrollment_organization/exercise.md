# Module 06 — လေ့ကျင့်ခန်းများ

လေ့ကျင့်ခန်း ခြောက်ခုစီတွင် ပေးထားသော ဒေတာ နှင့် စည်းမျဉ်းများ ကို အသုံးပြုပြီး ရလဒ် ကို
ကိုယ်တိုင် တွက်ချက်ရသည်။ အဖြေ များ ကို `solution.md` တွင် ဖတ်ရှုနိုင်သည်။ လေ့ကျင့်ခန်း
တစ်ခုစီ၏ ရလဒ် ကို `lab.py` ဖြင့် အတည်ပြုနိုင်သည်။

## Exercise 1 — State transition validation

Agent တစ်ခု၏ အခြေအနေ ပြောင်းလဲမှု အတွက် အောက်ပါ စည်းမျဉ်းများ သတ်မှတ်ထားသည်။

| မှ | သို့ | လုပ်ဆောင်ချက် |
|---|---|---|
| waiting_for_admission | enabled | admit |
| waiting_for_admission | disabled | reject |
| enabled | disabled | disable |
| disabled | enabled | enable |

အခြား ပြောင်းလဲမှု အားလုံးကို ငြင်းပယ်သည်။ Admission queue သို့ ပြန်သွားသော လမ်းကြောင်း
တစ်ခုမျှ မရှိပါ။ အခြေအနေ တူညီသော ပြောင်းလဲမှု (ဥပမာ enabled မှ enabled) ကို အလုပ်မရှိသော
တောင်းခံမှု အဖြစ် သတ်မှတ်သည်။

အောက်ပါ တောင်းခံမှု ခုနစ်ခုကို စစ်ဆေးပါ —

| Agent | မှ | သို့ |
|---|---|---|
| agent-01 | waiting_for_admission | enabled |
| agent-02 | waiting_for_admission | disabled |
| agent-03 | enabled | disabled |
| agent-04 | disabled | enabled |
| agent-05 | enabled | waiting_for_admission |
| agent-06 | disabled | waiting_for_admission |
| agent-07 | enabled | enabled |

တာဝန် —

1. တောင်းခံမှု တစ်ခုစီအတွက် ခွင့်ပြု/ငြင်းပယ် ဆုံးဖြတ်ချက် နှင့် အကြောင်းရင်း ကို ဖော်ပြပါ။
2. ခွင့်ပြုသည့် အရေ နှင့် ငြင်းပယ်သည့် အရေ ကို ရေတွက်ပါ။
3. enabled မှ waiting_for_admission သို့ ပြောင်းလဲမှု ကို ဘာကြောင့် ငြင်းပယ်ရသည် ကို
   တစ်ကြောင်း ဖြင့် ရှင်းပြပါ။

## Exercise 2 — Admission queue summary

အောက်ပါ fixture တွင် agent ၁၂ ခု ပါဝင်သည်။ `wait_minutes` သည် လက်ခံရန် စောင့်ဆိုင်းနေသည့်
အချိန် ဖြစ်ပြီး အခြား အခြေအနေ များတွင် သုည ဖြစ်သည်။

| Agent | Organization | Platform | State | Wait (min) |
|---|---|---|---|---|
| PC-001 | head-office | windows | enabled | 0 |
| PC-002 | head-office | linux | enabled | 0 |
| PC-003 | branch-office | windows | disabled | 0 |
| PC-004 | head-office | macos | waiting_for_admission | 240 |
| PC-005 | lab | linux | enabled | 0 |
| PC-006 | branch-office | windows | enabled | 0 |
| PC-007 | branch-office | windows | waiting_for_admission | 1840 |
| PC-008 | lab | macos | disabled | 0 |
| PC-009 | head-office | linux | waiting_for_admission | 920 |
| PC-011 | lab | linux | waiting_for_admission | 75 |
| PC-012 | head-office | windows | enabled | 0 |
| PC-014 | branch-office | macos | waiting_for_admission | 1560 |

တာဝန် —

1. အခြေအနေ တစ်မျိုးစီတွင် agent မည်မျှ ရှိသည် ကို ဇယား အဖြစ် ဖော်ပြပါ။
2. စောင့်ဆိုင်းနေသော agent များကို organization အလိုက် ရေတွက်ပါ။
3. စောင့်ဆိုင်းချိန် အများဆုံး agent သုံးခုကို အစဉ်လိုက် ဖော်ပြပါ။
4. ထို စာရင်း အရ ပထမဆုံး လက်ခံသင့်သော agent မည်ခု ဖြစ်သည် ကို အကြံပြုပါ။

## Exercise 3 — Organization and site resolution

အောက်ပါ organization များ တည်ရှိသည်။ `head-office` သည် default organization ဖြစ်သည်။

| Organization | Site များ |
|---|---|
| branch-office | warehouse |
| head-office | hq-floor1, hq-floor2 |
| lab | (မရှိ) |

ဖြေရှင်းမှု စည်းမျဉ်းများ —

1. Organization ကော်လံ အလွတ် ဖြစ်ပါက default organization ကို အသုံးပြုသည်။
2. Site ကော်လံ အလွတ် ဖြစ်ပါက ထို organization ၏ site များကို အက္ခရာ အစဉ်လိုက် စီပြီး
   ပထမ site ကို ရွေးသည်။
3. Organization မတည်ရှိပါက ငြင်းပယ်သည်။
4. Site သည် ထို organization ၏ site မဟုတ်ပါက ငြင်းပယ်သည်။
5. Organization တွင် site မရှိပါက ငြင်းပယ်သည်။

တောင်းခံမှုများ —

| Endpoint | Organization | Site |
|---|---|---|
| PC-101 | (အလွတ်) | (အလွတ်) |
| PC-102 | branch-office | (အလွတ်) |
| PC-103 | head-office | hq-floor2 |
| PC-104 | lab | (အလွတ်) |
| PC-105 | branch-office | hq-floor1 |
| PC-106 | unknown-org | warehouse |

တာဝန် —

1. တောင်းခံမှု တစ်ခုစီ၏ ရလဒ် (organization၊ site၊ ok/error) ကို ဖော်ပြပါ။
2. အောင်မြင်သည့် အရေ နှင့် ငြင်းပယ်သည့် အရေ ကို ရေတွက်ပါ။
3. PC-101 ၏ site ကို မည်သည့် စည်းမျဉ်းဖြင့် ရွေးချယ်သည် ကို ရှင်းပြပါ။

## Exercise 4 — CSV import validation

Organization CSV ၏ ကော်လံများမှာ `name` နှင့် `site` ဖြစ်သည်။ Server တွင် `head-office`
နှင့် `branch-office` ရှိပြီး ဖြစ်သည်။ အတန်း နံပါတ် သည် ဖိုင် ထဲ ပါဝင်သည့် အစဉ်လိုက်
နံပါတ် ဖြစ်သည်။

| အတန်း | name | site |
|---|---|---|
| 1 | east-branch | depot-a |
| 2 | west-branch | (အလွတ်) |
| 3 | east-branch | depot-b |
| 4 | head-office | hq-floor3 |
| 5 | central | depot-c |

User CSV ၏ ကော်လံများမှာ `email`၊ `organization` နှင့် `site` ဖြစ်သည်။

| အတန်း | email | organization | site |
|---|---|---|---|
| 1 | a@openuem.example | head-office | hq-floor1 |
| 2 | b@openuem.example | ghost-org | depot |
| 3 | c@openuem.example | branch-office | hq-floor1 |
| 4 | a@openuem.example | head-office | hq-floor2 |
| 5 | d@openuem.example | east-branch | depot-a |

စည်းမျဉ်းများ — Organization အတန်းများကို အရင် စစ်ဆေးပြီး အောင်မြင်သော organization များ
ကို နောက် user အတန်းများ အတွက် အသုံးပြုနိုင်သည်။ User အတန်း တစ်ခုစီတွင် email ထပ်နေမှု
ကို စစ်ဆေးသည်။

တာဝန် —

1. Organization အတန်း တစ်ခုစီ၏ ရလဒ် ကို ဖော်ပြပါ။ အောင်မြင်သည့် အတန်း နှင့် ပယ်ချခံရသည့်
   အတန်း အရေအတွက် ကို ရေတွက်ပါ။
2. User အတန်း တစ်ခုစီ၏ ရလဒ် ကို ဖော်ပြပါ။ အောင်မြင်သည့် အတန်း နှင့် ပယ်ချခံရသည့်
   အတန်း အရေအတွက် ကို ရေတွက်ပါ။
3. အတန်း ၅ ၏ ရလဒ် သည် အတန်း ၁ ၏ ရလဒ် အပေါ် မည်သို့ မှီခိုနေသည် ကို ရှင်းပြပါ။

## Exercise 5 — Capability matrix and least privilege

Capability ခုနစ်မျိုး နှင့် role လေးမျိုး အတွက် အောက်ပါ ဇယား ကို အသုံးပြုပါ။

| Capability | administrator | operator | owner | read_only |
|---|---|---|---|---|
| admit_agent | ရှိ | မရှိ | ရှိ | မရှိ |
| export_reports | ရှိ | ရှိ | ရှိ | ရှိ |
| force_report | ရှိ | ရှိ | ရှိ | မရှိ |
| manage_orgs | မရှိ | မရှိ | ရှိ | မရှိ |
| manage_users | ရှိ | မရှိ | ရှိ | မရှိ |
| remote_assistance | ရှိ | ရှိ | ရှိ | မရှိ |
| view_inventory | ရှိ | ရှိ | ရှိ | ရှိ |

လုပ်ငန်း တာဝန်တစ်ခုအတွက် လိုအပ်သော capability များမှာ `force_report` နှင့်
`view_inventory` ဖြစ်သည်။ အုပ်ချုပ်သူ တစ်ဦးက `helpdesk-01` အကောင့် ကို administrator
role ဖြင့် သတ်မှတ်ရန် အဆိုပြုသည်။

တာဝန် —

1. ထို တာဝန် အတွက် လိုအပ်ချက် ကို ဖြည့်ဆည်းပေးနိုင်သော role များကို စာရင်းပြုပါ။
2. Role တစ်ခုစီတွင် ပိုလျှံနေသော capability အရေအတွက် ကို တွက်ပါ။
3. Least privilege အရ အနည်းဆုံး လုံလောက်သော role ကို ရွေးပါ။
4. `helpdesk-01` အတွက် အဆိုပြုချက် ကို လက်ခံ/ငြင်းပယ် ဆုံးဖြတ်ပြီး အကြောင်းရင်း ဖော်ပြပါ။

## Exercise 6 — Certificate lifecycle states

Certificate အခြေအနေ လေးမျိုး ရှိသည် — absent၊ issued၊ active၊ revoked။ ခွင့်ပြုထားသော
ဖြစ်ရပ်များမှာ အောက်ပါအတိုင်း ဖြစ်သည်။

| မှ | ဖြစ်ရပ် | သို့ |
|---|---|---|
| absent | admission_issue | issued |
| issued | first_report | active |
| issued | revoke | revoked |
| active | regenerate | issued |
| issued | regenerate | issued |
| active | revoke | revoked |
| revoked | admission_issue | issued |

`regenerate` ဖြစ်ရပ်တွင် certificate အဟောင်း ကို revoke လုပ်ပြီး အတွဲ အသစ် ထုတ်ပေးသည်။
ဇယားတွင် မပါသည့် ဖြစ်ရပ် ဖြစ်ပေါ်ပါက ငြင်းပယ်ပြီး အခြေအနေ မ ပြောင်းလဲပါ။

Agent လေးခု၏ ဖြစ်ရပ် အစဉ်များမှာ အောက်ပါအတိုင်း ဖြစ်သည်။

| Agent | ဖြစ်ရပ် အစဉ် |
|---|---|
| PC-201 | admission_issue → first_report → regenerate → first_report |
| PC-202 | admission_issue → revoke |
| PC-203 | admission_issue → revoke → admission_issue |
| PC-204 | first_report |

တာဝန် —

1. Agent တစ်ခုစီအတွက် ဖြစ်ရပ် တစ်ခုချင်းစီ၏ အခြေအနေ ကူးပြောင်းမှု ကို ဖော်ပြပါ။
2. Agent တစ်ခုစီ၏ အဆုံးသတ် အခြေအနေ ကို ဖော်ပြပါ။
3. ငြင်းပယ်ခံရသော ဖြစ်ရပ် စုစုပေါင်း အရေအတွက် ကို ရေတွက်ပါ။
4. PC-203 ၏ ဒုတိယ `admission_issue` သည် မည်သည့် အခြေအနေမှ စတင်သည် ကို ဖော်ပြပါ။
