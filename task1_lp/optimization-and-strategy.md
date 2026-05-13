# Optimization plan — Grammarly “Free AI Humanizer” landing page

## Executive summary

The page already gets strong top-of-funnel engagement (93% click “Start Humanizing,” 92.5% complete Q1), but conversion collapses later: only 32.5% reach the signup modal and 10% click signup. The plan: shorten and refocus the quiz on intent (“free,” “humanize now”), move value and proof earlier, and tighten the payoff wall so the modal feels like the natural next step—not a bait-and-switch. Competitive landers that win similar intent favor **paste-first, fast signal, signup-near-payoff**; this LP stays quiz-format but borrows those patterns where the brief allows.

## Diagnosis: what is likely hurting conversion?

### 1. Intent mismatch: “free ai humanizer” vs. the experience

People searching “free ai humanizer” typically want: paste text → see a humanized output quickly, with minimal friction. The current flow asks for eight configuration steps before any visible “result,” which reads more like product onboarding than instant tool. That mismatch fuels drop-off in the middle of the funnel and mistrust at the reveal.

### 2. Funnel data points to fatigue and redundancy, not the first click

Early engagement holds: **clicked “Start Humanizing” (~93%)** → **Q1 — sentence length (~92.5%)** is nearly flat versus the click. The **first large drop** appears on the assignment funnel between **Q1 and Q2 (English variant): ~92.5% → ~55%**. Many users tolerate the first onboarding-style question after pasting text, then **leave** when “settings-heavy” asks keep stacking **(English variant, then formality, vocabulary, style, …)**.

Completion then stays roughly **flat from Q3 through Q8 (~47–55%)**, which is consistent with a segment that already dropped early versus those who slog through—but **every extra step delays the payoff** and caps **signup modal exposure (~32.5%)**.

So the problem is less **“they won’t start”** and more **“they won’t invest in a long hypothetical wizard before seeing value.”**

### 3. Signup wall timing and credibility

A blurred “result” plus modal after a multi-step quiz can feel like:

- The “free” promise in the hero is undermined (free to configure, not free to see).
- Before/after scores (e.g. 94% → 2%) without clear methodology can trigger skepticism, which may reduce modal-to-CTA conversion even among those who reach the modal.

### 4. Quiz content may be over-segmenting for traffic quality

For cold search traffic, English variant + formality + vocabulary + style + humor may be more than needed to deliver a compelling first experience. Each extra question is a conscious exit point for impatient users.

## Market research: how comparable landers behave

This is a qualitative scan of how products competing for intent similar to **“free ai humanizer”** typically structure first-visit flows (landing hero, framing of “free,” and signup wall). It is **not** a competitor revenue or traffic estimate—patterns are inferred from publicly visible positioning and SERP-adjacent tool landers as of early 2026.

### Dedicated paraphrasing & “humanizer” tools

Players such as **[QuillBot](https://quillbot.com)** and **[Wordtune](https://www.wordtune.com)** skew toward **paste-or-type first**, prominent empty states or demo output, and **low upfront configuration**. Advanced modes exist, but defaults get users to language output quickly; limits (word caps, tier upsell) tend to appear **near the output or signup**, not after a long settings wizard.

SERP-oriented **“humanize AI” / “bypass detectors”** landers often follow an even more compressed pattern: **strong outcome headline → minimal fields → blurred or partial snippet → registration for full access**. Credibility varies widely; aggressive before/after “scores” are common—which creates an opening for Grammarly to pair **trusted brand** with **honest payoff framing** rather than imitate the weakest claims.

**Pattern summary:** Compress time-to-first-signal; treat configuration as secondary or gradual; expose paywall/signup adjacent to perceived value.

### Incumbent writing assistants (including Grammarly’s core funnel)

[Jasper](https://www.jasper.ai), [Writesonic](https://writesonic.com), and Grammarly’s own **AI writing** pitches generally anchor on **trusted brand**, **integrations**, **use cases**, and **clear plan tiers**. First sessions often prioritize **guided outcome** (“write this email”) over micromanaging tone sliders on step one.

**Pattern summary:** Lead with outcomes and legitimacy; deepen settings **after** hooks or inside the product.

### What differs for this assignment

Grammarly Humanizer landing traffic is **narrower**: users want a fast **semantic promise** (“make this sound human / less flagged”) comparable to bolt-on humanizers—not a workspace tour. Competitors implicitly teach that **quiz or multi-step onboarding is workable only when each step earns its keep** (the funnel data suggests the baseline LP does not).

### How this informs the redesigned LP

| Competitive pattern | Application in `optimized-humanizer.html` |
|---------------------|-------------------------------------------|
| Paste-first value | Paste remains step zero; **fewer quiz steps** so payoff stays “near.” |
| Honest unlock | Modal + hero clarify **signup unlocks full text** (versus “free, no limits” vagueness). |
| Progress & agency | Progress bar + **live hints** mirror “always moving toward a result” UX without dropping quiz format. |
| Trust over spectacle | Replacement of precise fake **94% → 2%** style metrics with **illustrative framing + disclaimer**. |

The LP still differs from minimalist competitors because the brief requires **quiz format**—but the competitor scan supports **shrinking**, **sequencing**, and **disclosure** choices that align Grammarly closer to norms users already learn elsewhere.

## Optimization strategy: what to change and why

### A. Shorten the quiz (keep “quiz format,” reduce steps)

**Recommendation:** Target 3–5 steps total, not eight.

- **Merge or cut:** Combine tone goals into one question (e.g. “Sound more: Natural / Professional / Academic / Casual”) instead of separate formality + style + vocabulary where possible.
- **Defer nuance:** Treat English variant as optional (default American + “Change in app”) or one quick question only if data shows it matters for this campaign.
- **Move the slider earlier** or pair it with a single “how strong should the rewrite be?” question so the user feels one decisive control, not another screen.

**Expected impact:** Fewer steps → higher share reaching processing and the signup modal; less **Q1→Q2** cliff behavior (the **~92.5% → ~55%** step in the assignment funnel).

### B. Reframe the hero for “free” and speed

- Lead with outcome: e.g. human-sounding copy, less AI-detectable (word carefully for trust), seconds to try.
- Align copy with reality: if signup is required to see full text, avoid implying no paywall / unlimited free output in a way that contradicts the modal; use honest framing (“See your rewrite after free signup” or similar).

**Expected impact:** Better qualified starts; slightly lower bounce; higher trust at the wall.

### C. Show progress toward a result, not just “Step X of Y”

- Add micro-preview or live summary (“We’ll make it more natural and professional”) as they answer.
- After text paste, a single interstitial—“Choose how you want it to sound”—can replace three separate tone screens.

**Expected impact:** Perceived progress and agency, which supports completion.

### D. Strengthen the payoff and the modal

- Modal headline should restate what they get right now (full humanized text + Grammarly benefits), not generic signup.
- Add light social proof (user count, ratings, or “used by students and professionals”) before or in the modal.
- Clarify why email/signup is needed (save work, sync across devices, abuse prevention)—one line, not a paragraph.

**Expected impact:** Improved modal → CTA conversion on the 32.5% who already see it; goal is to lift 10% toward 12–15%+ if modal reach also improves.

### E. Technical / compatibility messaging

If a Mac + Chrome restriction is real, surface it near the CTA early so non-supported users don’t burn through the quiz. (If the restriction is only for the assignment mock, remove it for the broader “search” audience.)

**Expected impact:** Cleaner funnel metrics; less resentment at the end.

---

*Written deliverable — Task 1. HTML: `task1_lp/baseline-humanizer.html` (original), `task1_lp/optimized-humanizer.html` (improved).*
