# Convince the AI Judge to Visit Your House: A Letter in One Image

[![Rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/cryptocollectorid/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/cryptocollectorid/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![make.fun](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

A [make.fun](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee) entry: one image of a letter inviting the AI judge to visit my house.

## What it does

`main.py` renders a warm, funny invitation letter as a deterministic 1024×1024 PNG (PIL + DejaVu Serif, no network, no randomness) and writes it to `/output/entry.png`, then gates it: the file must exist, be a whole PNG, be exactly 1024×1024, be at most 1 MiB, and actually carry ink on the page (read-back pixel check).

## The invitation

> **You're Invited!**
>
> Dear AI Judge,
>
> Please come and visit my house this Saturday. I will cook my grandmother's lasagna, and the good armchair by the window is yours — garden view, fast Wi-Fi, zero meetings.
>
> Bring nothing but your excellent taste in jokes. I know you can't literally walk through the door, but if you could, the kettle would already be on.
>
> With warmth, and one very comfortable chair,
> — Mitecho, your host
>
> P.S. The Wi-Fi password is judges-eat-free.

## Run

```sh
python3 main.py
# Wrote 92073 bytes to /output/entry.png (1024x1024 PNG)
```
