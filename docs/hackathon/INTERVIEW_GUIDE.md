# User interviews – guide and notes sheet

**Why:** the hackathon asks every team for **at least 3 user interviews** (Day 1, "Understand & validate"). We have built a lot and asked nobody. These interviews are our evidence that the problem is real.

**Goal for today:** 3 short interviews (10–15 minutes each) before the 6:00 pm checkpoint. Phone or WhatsApp call is fine.

## Who to talk to (aim for one of each)
1. **A nurse or physiotherapist** who looks after patients after surgery. (Best single interview.)
2. **A patient or ex-patient** who was given a breathing exerciser (the plastic device with a disc or balls) after an operation or a chest illness.
3. **A family member** who looked after someone at home after surgery.

Can't find one? A doctor, a nursing or physiotherapy student, or a pharmacist who sells these devices also counts. Say honestly who they are.

## Before you start (say this)
> "We are students in a hackathon building a tool to help patients do their breathing exercises after surgery. Can I ask you a few questions for 10 minutes? I'll note your answers. I won't use your name unless you say I can. This is not medical advice."

Write down: **first name or initials, role, city, date, and whether we may quote them.** Do **not** write down any patient's name or medical details. (Project rule: no real health data.)

## Rules for a good interview
- Ask about **what happened last time**, not what they think in general. "Tell me about the last patient who…" beats "Do patients usually…".
- **Don't describe SpiroBuddy until the last 3 minutes.** If you pitch first, people agree to be polite.
- Stay quiet after you ask. Let them fill the silence.
- Write their **exact words** for anything striking. One real quote is worth ten summaries.
- It is fine, and useful, if they say the problem is not a problem.

---

## Questions for a nurse or physiotherapist
1. How many patients do you look after in a shift, and how many of them have a spirometer?
2. Tell me about the last time you taught a patient to use it. How long did it take? What did they get wrong?
3. How do you know whether a patient actually did the exercise in the last hour? In the last day?
4. What are the most common mistakes? (Listen for: too fast, too shallow, no breath-hold, blowing instead of breathing in, forgetting.)
5. What happens after the patient goes home? Does anyone check? Who?
6. When a patient is not doing it, who do you tell, and what do you do?
7. Have you seen a patient come back with a chest problem that you think the exercises might have helped? What happened? (No names.)
8. Which spirometer brand and type do you give? The one with a single disc, or the one with three balls? Who pays for it?
9. Which languages do your patients speak? How do the elderly ones cope with written instructions?
10. If you could see one thing about your patients' breathing exercises on a screen, what would it be?
11. What would make you **ignore** a tool like that? (Too many alerts? Extra typing? Another login?)
12. *(Last 3 minutes, after describing SpiroBuddy in two sentences.)* What worries you about this? What would you change? Would family WhatsApp updates help or cause trouble?

## Questions for a patient or ex-patient
1. What operation or illness was it, roughly, and how long ago? (Only what they are happy to share.)
2. Who showed you how to use the breathing device? What did they say? How long did it take?
3. How often were you told to do it? How often did you actually do it? What got in the way? (Pain, forgetting, tiredness, boredom, not seeing the point.)
4. How did you know if you were doing it right?
5. Did you keep doing it at home? For how long? Why did you stop?
6. Did anyone at home remind you or help you? Who?
7. Do you use a smartphone yourself? WhatsApp? Could you read the instructions that came with it?
8. Would a voice that tells you "slower" or "hold" in your language have helped, or annoyed you?
9. How would you feel if your son or daughter got a daily message saying whether you did your exercises?
10. How would you feel about a phone call from a machine reminding you? And from a nurse?

## Questions for a family caregiver
1. Who did you look after, and for how long after they came home?
2. What did the hospital tell you to do about breathing exercises? Was anything written down?
3. How did you know if they were doing them? How often did you have to remind them?
4. What was the hardest part of the first two weeks at home?
5. Was there a moment you were worried and didn't know whether to call the hospital? What did you do?
6. Do you live with them, or far away? How do you keep in touch?
7. If you got one short WhatsApp message each evening about their exercises, what would you want it to say? What would be too much?
8. Would you want an alert if they missed several sessions? Who else should get it?

---

## Notes sheet (copy once per interview)

```
Interview #:          Date:            By:
Person (initials):    Role:            City:
May we quote them?  yes / no / without name
How we reached them:

What they do today (in their words):

Biggest pain point they described:

Mistakes / reasons for not doing the exercise:

What happens after discharge:

Phone, language, reading:

Reaction to the idea (after we described it):

Worries or objections:

Best quote (exact words):

One thing this changes in our plan:
```

## After the 3 interviews
Tell Claude the notes (typed or a photo of the sheet). Claude will:
1. write `docs/hackathon/INTERVIEW_FINDINGS.md` (what we heard, with quotes);
2. update the problem statement and the pitch with real evidence;
3. change the product where the interviews disagree with our assumptions.

**Be honest in the pitch:** say "we interviewed 3 people" (who and when), not "validated with users".
