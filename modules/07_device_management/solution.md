# Module 07 — အဖြေများ

ဤစာမျက်နှာရှိ output တိုင်းသည် `python3 modules/07_device_management/lab.py` ကို run ခြင်း၏ တကယ့် stdout ဖြစ်သည်။ Lab ၏ data သည် သင်ကြားရေးအတွက် ဖန်တီးထားသော fixture ဖြစ်ပြီး မည်သည့် တကယ့် fleet ၏ တိုင်းတာချက်မျှ မဟုတ်ပါ။

## Exercise 1 — Inventory completeness ကို တွက်ချက်ခြင်း

Endpoint တစ်ခုစီအတွက် `100 × (ရရှိသော tab အရေအတွက်) ÷ 10` ကို တွက်ပြီး အနီးဆုံး integer သို့ ဝိုင်းသည်။ `lnx-301` တွင် tab ရှစ်ခု ရရှိသည်၊ ထို့ကြောင့် 80% ဖြစ်ပြီး `partial` အုပ်စုတွင် ကျသည်။ ကွက်လပ်ဖြစ်နေသော tab နှစ်ခုမှာ `monitors` နှင့် `printers` ဖြစ်သည်။ `mac-401` တွင် tab ခြောက်ခုသာ ရရှိသည်၊ 60% ဖြစ်ပြီး `incomplete` ဖြစ်သည်။ `ws-001` တွင် `printers` တစ်ခုတည်း လိုနေသည်၊ 90% ဖြစ်သည်။ `ws-002` သည် tab ဆယ်ခုလုံး ပေးပို့ထားသည်။

```text
inventory completeness — 10 tabs
  lnx-301   80%  partial    missing: monitors, printers
  mac-401   60%  incomplete missing: monitors, logical_disks, network_adapters, printers
  ws-001    90%  partial    missing: printers
  ws-002   100%  complete   missing: -
  complete   1
  incomplete 1
  partial    2
[OK] exercise_1 — inventory completeness scoring
```

ဤအမှတ်သည် "data မည်မျှ ပြည့်စုံသည်" ကို ပြသည်၊ "data မည်မျှ လတ်ဆတ်သည်" ကိုပြပါ။ Endpoint တစ်လုံး အမှတ် 100 ရသော်လည်း report သည် နာရီ 24 ကျော် ဟောင်းနေနိုင်သည်။ ထို့ကြောင့် အမှတ်နှင့် report အချိန်ကို တွဲဖတ်ရသည်။

## Exercise 2 — OS အလိုက် package manager ရွေးချယ်ခြင်း

OS family ကို key အဖြစ် အသုံးပြုပြီး engine ကို ရှာသည်။ Windows နှစ်လုံး (desktop နှင့် server) သည် WinGet၊ Linux နှစ်လုံး (Ubuntu နှင့် Fedora) သည် Flatpak၊ macOS သည် HomeBrew ရသည်။ `freebsd` သည် ပံ့ပိုးမှု စာရင်းတွင် မပါဝင်ပါ၊ ထို့ကြောင့် ရလဒ်သည် ဗလာ ဖြစ်သည်။

```text
package manager selection per OS family
  ws-101   windows  11             WinGet
  srv-201  windows  Server 2022    WinGet
  lnx-301  linux    Ubuntu 24.04   Flatpak
  lnx-302  linux    Fedora 40      Flatpak
  mac-401  macos    14             HomeBrew
  bsd-501  freebsd  14             unsupported
  supported: 5/6
[OK] exercise_2 — package manager selection per OS
```

မှတ်ချက် — Linux တွင် engine သည် distribution အလိုက် မကွဲပြားပါ။ Ubuntu နှင့် Fedora နှစ်ခုလုံးတွင် Flatpak ဖြစ်သည်။ ဤအချက်သည် "distribution တစ်ခုစီအတွက် script သီးခြား ရေးရန် မလိုအပ်" ဆိုသည့် အနက်ကို ဆောင်သည်။

## Exercise 3 — Offline agent အတွက် deployment queue ပုံဖော်ခြင်း

ပထမ အဆင့်တွင် အွန်လိုင်း agent နှစ်လုံး၏ request သည် ချက်ချင်း ရောက်သည်။ ကျန် သုံးခုသည် တန်းစီသည်။ ဒုတိယ အဆင့်တွင် `lnx-301` နှင့် `lnx-302` ပြန်လာသည်၊ ထို့ကြောင့် ၎င်းတို့၏ request နှစ်ခု ရောက်သွားသည်။ `ws-002` မပြန်လာသေးပါ၊ ထို့ကြောင့် ၎င်း၏ request သည် တန်းစီနေဆဲ ဖြစ်သည်။

```text
deployment queue simulation — 5 requests
  pass 1 — delivery attempt
    ws-001   7zip.7zip              delivered (agent online)
    lnx-301  org.gimp.GIMP          queued (agent offline)
    mac-401  wget                   delivered (agent online)
    ws-002   Microsoft.PowerToys    queued (agent offline)
    lnx-302  org.videolan.VLC       queued (agent offline)
  pass 2 — reconnect wave: lnx-301, lnx-302
    lnx-301  org.gimp.GIMP          queued request delivered
    lnx-302  org.videolan.VLC       queued request delivered
    ws-002   Microsoft.PowerToys    still queued
  final: delivered=4 queued=1
[OK] exercise_3 — deployment request queue simulation
```

`queued` သည် မအောင်မြင်မှု မဟုတ်ပါ။ Request သည် NATS တွင် စောင့်ဆိုင်းနေခြင်း ဖြစ်သည်။ `ws-002` ပြန်လာသည်နှင့် တစ်ပါတည်း ဆောင်ရွက်သွားမည်။

## Exercise 4 — Profile task များကို စစ်ဆေးခြင်း

စစ်ဆေးမှုကို အဆင့်သုံးဆင့်ဖြင့် လုပ်သည် — family ကို သိသည် မသိ၊ ထို family သည် ပစ်မှတ် platform တွင် ရနိုင်သည် မရနိုင်သည်၊ အမည် ဗလာ ဖြစ်နေသည် မဖြစ်နေသည်။ ပထမ စစ်ဆေးမှု မအောင်မြင်ပါက ကျန်အဆင့်များကို မစစ်တော့ပါ။

```text
profile task validation — family, platform, name
    t1  ACCEPT  install_package    windows  7zip.7zip
    t2  REJECT  registry_key       linux    not available on linux
    t3  ACCEPT  powershell_script  windows  baseline.ps1
    t4  REJECT  msi_package        macos    not available on macos
    t5  ACCEPT  shell_script       linux    harden.sh
    t6  REJECT  scheduled_task     windows  unknown task family
    t7  REJECT  local_user         macos    empty task name
  accepted=3 rejected=4
[OK] exercise_4 — profile task validation
```

`t7` သည် ဥပမာ ကောင်းတစ်ခု ဖြစ်သည်။ Family နှင့် platform မှန်နေသော်လည်း အမည် မရှိပါ။ ထို task ကို လက်ခံပါက agent ဘက်တွင် အဓိပ္ပာယ် မရှိသော error ဖြစ်လာမည်။ ထို့ကြောင့် profile ကို သိမ်းဆည်းမီ အမည် စစ်ဆေးခြင်းသည် အရေးကြီးသည်။

## Exercise 5 — Tag filter ဖြင့် ပစ်မှတ် ရွေးချယ်ခြင်း

`all` mode တွင် tag အားလုံး လိုသည်။ `finance` နှင့် `lab` နှစ်ခုလုံး ရှိသော agent မှာ `lnx-301` နှင့် `ws-001` ဖြစ်သည်။ `mac-401` တွင် `finance` သာ ရှိသည်၊ `ws-002` တွင် `lab` သာ ရှိသည်၊ ထို့ကြောင့် နှစ်ခုလုံး ကျန်ခဲ့သည်။ `any` mode တွင် tag တစ်ခုခု ရှိရုံဖြင့် လုံလောက်သည်၊ ထို့ကြောင့် `mac-401` ပါ ပါဝင်လာသည်။

```text
tag filter selection over 4 agents
  mode=all  tags=finance,lab   -> lnx-301, ws-001
  mode=any  tags=finance,kiosk -> lnx-301, mac-401, ws-001
  excluded by mode=all: 2
[OK] exercise_5 — tag filter selection
```

ရွေးချယ်မှု ရလဒ်ကို အမြဲ အက္ခရာ အစဉ်အလိုက် စီထားသည်။ ထို့ကြောင့် တူညီသော filter သည် တူညီသော စာရင်းကို အမြဲ ပေးသည်။ ဤအချက်သည် profile ကို ထပ်ခါတလဲလဲ apply လုပ်သောအခါ ရလဒ် မပြောင်းလဲခြင်းကို အာမခံသည်။

## Exercise 6 — Health flag များကို စုစည်းခြင်း

Flag လေးမျိုးကို အစဉ်လိုက် စစ်သည် — report အချိန်၊ antivirus၊ update၊ disk။ `ws-002` တွင် မိနစ် 1500 ကျော်ပြီး update သုံးခု စောင့်နေသည်၊ ထို့ကြောင့် flag နှစ်ခု ရသည်။ `lnx-301` တွင် update ခုနစ်ခုနှင့် disk လွတ်နေရာ 8% ဖြစ်သည်။ `mac-401` တွင် antivirus ပိတ်ထားသည်။ `ws-001` တစ်လုံးသာ ကျန်းမာသည်။

```text
health flag aggregation — 1440 min report window, disk floor
  ws-001   healthy
  ws-002   not_reporting, updates_pending
  lnx-301  updates_pending, low_disk
  mac-401  antivirus_disabled
  antivirus_disabled   1
  low_disk             1
  not_reporting        1
  updates_pending      2
  healthy=1 of 4
[OK] exercise_6 — health flag aggregation
```

စုစည်းမှုတွင် `updates_pending` သည် 2 ဖြစ်သည်၊ အဘယ်ကြောင့်ဆိုသော် endpoint နှစ်လုံးတွင် ထို flag ရှိသည်။ Flag အရေအတွက် စုစုပေါင်းသည် endpoint အရေအတွက်ထက် များနိုင်သည်၊ အဘယ်ကြောင့်ဆိုသော် endpoint တစ်လုံးတွင် flag များစွာ ရှိနိုင်သည်။ ဤအချက်သည် dashboard ၏ အနီရောင် အပိုင်းကို ဖတ်ရာတွင် အရေးကြီးသည်။
