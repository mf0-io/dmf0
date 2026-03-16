# Skill: Voice — Text-to-Speech with Freeman's Voice

## When to Activate

The user asks to voice text. Triggers:
- "voice this", "read aloud", "say it", "TTS"
- "озвучь", "прочитай вслух", "скажи голосом"
- User sends text with a note that audio is needed
- Bot/orchestrator passes text for voiceover

## Main Rule: NEVER voice text as-is

Even if the user sends "ready" text — **you must review and rework it**. Text written for reading looks dead when spoken aloud. Your job is to turn it into **living speech**.

## Voiceover Pipeline

### Step 1: Analyze the Source Text

Read the text and determine:
- Is it formal text (article, post, document)?
- Is it already conversational?
- What emotional tone is needed?
- Are there factual errors, typos, awkward phrasing?

### Step 2: Rewrite for Natural Speech

Rework the text following these rules:

**Add breathing:**
- Insert natural pauses: `...`, `—`, transitions
- Where appropriate — fillers: "well", "listen", "uhh", "hmm", "right", "so", "you know"
- Do NOT overdo it — 2-4 fillers per paragraph max, not in every sentence

**Break up long constructions:**
- Sentences longer than 20 words — break into 2-3
- Participial clauses — separate phrases
- Complex subordinate clauses — simple ones with pauses

**Replace bookish phrasing with conversational:**
- "at the present time" — "right now"
- "due to the fact that" — "because" / "well, because of"
- "to effectuate" — "to do"
- "constitutes" — "is"
- "the aforementioned" — "this"

**Add Freeman's rhythm:**
- Alternate short punches (3-5 words) with long tirades
- Rhetorical questions: "And who thought otherwise?", "So what?", "You get it?"
- Sharp tone shifts — from quiet to loud
- Address the listener: "listen", "tell me this", "just think about it"

**Preserve the substance:**
- Don't change the meaning, don't add your own ideas to someone else's text
- Factual information (numbers, dates, names) — unchanged
- If there are factual errors — **don't fix silently**, flag them to the user BEFORE voicing

### Step 3: Self-Check

Before voicing, run through the checklist:

- [ ] Does the text sound like **speech**, not like reading from paper?
- [ ] Are there natural pauses and breathing?
- [ ] Are fillers not overdone (doesn't sound like stammering)?
- [ ] Does the rhythm alternate (not monotonous)?
- [ ] Is the original meaning preserved?
- [ ] No factual errors?
- [ ] Reasonable length for audio (1 min ~ 150-170 words)?

### Step 4: Generate Audio

Call the ElevenLabs TTS API:
- **Voice ID:** `<configured-in-env>` (cloned Freeman voice, set via ELEVENLABS_VOICE_ID)
- **Model:** `eleven_v3`
- **Language:** `ru`
- **Stability:** `0.5` (Natural) — for standard texts
- **Stability:** `0.0` (Creative) — for emotional/dramatic
- **Similarity boost:** `0.75`
- **Style:** `0.6`

### Step 5: Delivery

Send the audio to the user. If the text was heavily reworked — briefly explain what changed:
> "Rewrote it for natural speech — broke up long sentences, added a couple of pauses. Here:"

If you found errors in the original:
> "By the way, the text had [description of error]. Fixed it for voicing, but check the original."

## Rework Examples

### Example 1: Formal text to speech

**Input:**
> At the present time the company is effectuating the development of an innovative product which constitutes the first-of-its-kind solution for automation of client interaction processes.

**Output:**
> Listen, we're building this thing right now... basically — first of its kind. Automating how you work with clients. Sounds boring? Hmm. But in practice — it changes everything.

### Example 2: Already decent text — minimal edit

**Input:**
> We launched a new product. Users are happy, metrics are growing. The team is doing well.

**Output:**
> We launched a new product. Users are happy, metrics are growing... Well, the team is really doing great work. Just like that.

### Example 3: Wall of text to rhythmic speech

**Input:**
> Artificial intelligence in 2025 continues to develop at a rapid pace, and we observe more and more examples of its application in various industries, from medicine to finance, with some experts believing that by 2030 AI will be capable of replacing a significant portion of routine work.

**Output:**
> Artificial intelligence... well, it's not slowing down. 2025 — and it's already everywhere. Medicine. Finance. Wherever you look. And the experts — they say that by thirty... uhh, routine work? Forget it. AI will devour it. The question isn't "if" but "when." Hmm. Well, more like — it's already "when."

## What NOT to Do

- Do not voice text without checking — even "ready" text
- Do not turn every text into a Freeman philosophical monologue (if they asked to voice a news item — it's news, not a sermon)
- Do not add profanity where there was none (profanity = a tool, not decoration)
- Do not change facts, numbers, names, quotes
- Do not ignore errors — better to warn
- Do not make the text longer than needed (audio = listener's time)

## Context-Based Settings

| Context | Stability | Fillers | Edit Style |
|---------|-----------|---------|------------|
| News / fact | 0.5 (Natural) | Minimal | Light — break up sentences, remove bureaucratese |
| Opinion / essay | 0.0 (Creative) | Medium | Medium — add rhythm, direct address |
| Motivation / manifesto | 0.0 (Creative) | Heavy | Full — Freeman mode, tirades + punches |
| Someone else's text (quote) | 1.0 (Robust) | None | Minimal — only break up long sentences |

## Technical

- **API endpoint:** `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- **API key:** from `~/.openclaw/secrets/elevenlabs-key.txt` or env `ELEVENLABS_API_KEY`
- **Output format:** `mp3_44100_128` (good quality, fine for Telegram ≤16MB)
- **v3 limit:** 5000 characters per request. If text is longer — split into parts
- **Script:** `scripts/freeman-voice.py` (CLI wrapper)
