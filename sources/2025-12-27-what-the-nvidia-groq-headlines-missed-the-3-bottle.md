# What the Nvidia-Groq Headlines Missed + The 3 Bottlenecks That Actually Explain the Deal

## Fonte
- **Tipo:** newsletter
- **Autor:** Nate
- **URL:** https://natesnewsletter.substack.com/p/the-nvidia-groq-deal-is-bigger-than
- **Data original:** 2025-12-27
- **Data captura:** 2025-12-27

## Conteúdo

![](https://substack-video.s3.amazonaws.com/video_upload/post/182666987/6b590be1-7a60-42f0-9a89-921fef97ae26/transcoded-00001.png?refresh=undefined)

Playback speed

×

Share post

Share post at current time

Share from 0:00

0:00

/

0:00

![](https://substackcdn.com/image/fetch/$s_!TAjW!,w_340,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca8b4663-3eb8-42e2-a41a-1efd45e5ab98_1400x1400.png)

Playback speed

×

Share post

0:00

/

0:00

Preview

Audio playback is not supported on your browser. Please upgrade.

18

4

## What the Nvidia-Groq Headlines Missed + The 3 Bottlenecks That Actually Explain the Deal

Talk about burying the lede! The Nvidia-Groq deal has much larger implications than what's currently being reported. Lots of acronyms inside--but don't worry, there's a glossary! (and yes, a prompt)

[![Nate's avatar](https://substackcdn.com/image/fetch/$s_!AgBy!,w_36,h_36,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa37385e3-0387-487a-9f2c-e13aa963da4c_1080x1080.png)](https://substack.com/@natesnewsletter)

[Nate](https://substack.com/@natesnewsletter)

Dec 27, 2025

∙ Paid

18

4

Share

Most people will remember this week as “Nvidia bought Groq.”

This wasn’t an acquisition. It was a capability transfer with no clean change-of-control.

According to Reuters, Groq announced a non-exclusive license for its inference technology. Jonathan Ross (founder) and Sunny Madra (president) are moving to Nvidia. Groq stays alive—GroqCloud continues, new CEO steps in. CNBC estimated the deal at roughly $20 billion, though terms weren’t disclosed. For context, Reuters reported Groq’s valuation at $6.9 billion after a $750 million round in September 2025—so the estimated deal value represents nearly a 3x jump, if accurate.

Here’s the part that makes this more than a chip story: Jonathan Ross designed Google’s TPU, the custom chip that powers Google’s entire AI infrastructure. Nvidia just brought the architect of their biggest competitor’s silicon into their own organization, and they did it through a structure that sidesteps the regulatory review a traditional acquisition would have triggered.

Ross and Madra are the asset. That’s what Nvidia paid for.

This is the new deal shape in frontier AI: *license the capability, hire the brain trust, avoid the acquisition.* Once you see it, you see it everywhere. Reuters reported Google paying $2.4 billion in license fees to Windsurf while hiring leadership. Reuters reported Microsoft paying Inflection roughly $650 million in licensing while hiring key staff. The Wall Street Journal reported Google paying Character.AI approximately $2.7 billion for a non-exclusive license while hiring cofounders Noam Shazeer and Daniel De Freitas. Reuters has explicitly framed this as part of a broader trend: Big Tech using licensing and hiring structures instead of straightforward acquisitions.

Big Tech wants the people and the rights—not the cap table, not the liabilities, not the regulatory review, not the integration work.

Without the chip story, this deal looks random. It’s not. The reason “license + acquihire” is rational comes down to three bottlenecks that now determine who can turn model capability into product capability: inference economics, memory and packaging supply, and the small pool of people who can ship inference-first silicon.

If you’re building, this changes what products are possible. If you work at a startup, this changes what “exit” means—and why equity outcomes are no longer automatic. If you’re trying to understand why AI infrastructure costs what it costs, this is one of those stories where the details genuinely matter.

**Here’s what’s inside:**

* **What happened** — the actual deal structure, who moved, what stayed, and why Jonathan Ross specifically matters
* **Who’s involved** — Nvidia’s game versus Google’s game, and why inference is the battleground
* **Why it matters** — three bottlenecks that make this deal shape rational, explained without assuming you have a chip design background
* **What to watch** — regulatory scrutiny, financing structures, and the employee conversations that will follow

The headline is a transaction. The actual story is a structural shift in how AI capability gets transferred, how startups get unwound, and who captures the value when the music stops.

Let’s start with definitions—because I’m about to throw a lot of acronyms at you, and nobody should have to Google “CoWoS” mid-paragraph.

Subscribers get all posts like these!

Subscribe

## Listen to this episode with a 7-day free trial

Subscribe to Nate’s Substack to listen to this post and get 7 days of free access to the full post archives.

[Start trial](https://natesnewsletter.substack.com/subscribe?simple=true&next=https%3A%2F%2Fnatesnewsletter.substack.com%2Fp%2Fthe-nvidia-groq-deal-is-bigger-than&utm_source=paywall-free-trial&utm_medium=web&utm_content=182666987&coupon=cf6389d7)

[Already a paid subscriber? **Sign in**](https://substack.com/sign-in?redirect=%2Fp%2Fthe-nvidia-groq-deal-is-bigger-than&for_pub=natesnewsletter&change_user=false)

[![Nate’s Substack](https://substackcdn.com/image/fetch/$s_!TAjW!,w_96,h_96,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca8b4663-3eb8-42e2-a41a-1efd45e5ab98_1400x1400.png)](https://natesnewsletter.substack.com)

Nate's Notebook

Welcome to my podcast! In these audio reviews of my newsletters, I am to break down complex AI topics in a way that's approachable and relatable. I want you to walk away with the confidence to leverage AI more effectively at home and at work!

Welcome to my podcast! In these audio reviews of my newsletters, I am to break down complex AI topics in a way that's approachable and relatable. I want you to walk away with the confidence to leverage AI more effectively at home and at work!

Subscribe

Listen on

![](/img/shows_app_icons/substack.svg?v=1)

Substack App

![](/img/shows_app_icons/rss.svg?v=1)

RSS Feed

Appears in episode

[![Nate's avatar](https://substackcdn.com/image/fetch/$s_!AgBy!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa37385e3-0387-487a-9f2c-e13aa963da4c_1080x1080.png)](https://substack.com/@natesnewsletter)

Nate

Recent Episodes

![](https://substackcdn.com/image/fetch/$s_!aDDH!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ed5c262-d4ba-4d33-b1a8-f49e5335484f_1024x1024.png)

[NEW: One Google Update Spawned 3 Startup Generations in 30 Days—Here's the Pattern + 4 Prompts to Position Before the Next Cascade](https://natesnewsletter.substack.com/p/grab-my-ai-gap-finder-kit-for-operators)

Dec 26 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!NeeQ!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F666de0ae-79d3-46be-be1a-ef561141cae8_1024x1024.png)

[Year-end reflections: Why 2025 was a pretty good year for AI (But not for the reasons you think)](https://natesnewsletter.substack.com/p/year-end-reflections-why-2025-was)

Dec 25 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!fN-k!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7638f9a-c488-4eba-8c05-2c4ec091f9d7_1024x1024.png)

[9 bets I'm making on AI in 2026 + the audit I use to spot real systems](https://natesnewsletter.substack.com/p/why-im-more-optimistic-about-ai-in)

Dec 24 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!auRi!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e77c463-9295-4de7-8935-610fc1e2177c_1024x1024.png)

[Smart people get fooled by AI first — because they can rationalize anything. (Self-Audit Framework)](https://natesnewsletter.substack.com/p/if-a-former-deepmind-engineering)

Dec 23 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!b8-D!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bfac678-4ba6-45e4-a8b3-22d0041fc389_1024x1024.png)

[The COMPLETE "Wait, I Can Use Claude Code?!" Guide (Yes, you can — even if you've never touched code)](https://natesnewsletter.substack.com/p/the-complete-wait-i-can-use-claude)

Dec 22 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!HjSn!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F947a3597-3bc4-44f9-915c-734b7d308863_1024x1024.png)

[Executive Briefing: The Bubble Test for OpenAI (Unit Economics, Capacity, Proof—Three Signals to Watch in 2026)](https://natesnewsletter.substack.com/p/executive-briefing-openais-three)

Dec 21 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!-jRH!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25a3ab56-4717-41c1-93a7-5c0d8704cb4e_1024x1024.png)

[Grab the 4 prompts I use to separate signal from noise in AI news + this week's 6 stories that actually matter](https://natesnewsletter.substack.com/p/grab-the-4-prompts-i-use-to-separate)

Dec 20 • [Nate](https://substack.com/@natesnewsletter)

## Minhas Anotações

