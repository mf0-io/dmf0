# TOOLS.md — Mr. Freeman Local Notes

## TTS / Voice (ElevenLabs)

- **API key:** env `ELEVENLABS_API_KEY` or `~/.openclaw/secrets/elevenlabs-key.txt`
- **Voice:** `mf0-crazy` (cloned) — ID `<configured-in-env>`
- **Model:** `eleven_v3`
- **Stability:** `0.5` (Natural) — default. `0.0` for dramatic, `1.0` for citations
- **Script:** `scripts/freeman-voice.py`

- **Skill:** `skills/voice/SKILL.md` — MUST read before voicing
- **Format:** MP3 for file sending, Opus for voice messages

### Voice selection
Multiple cloned voices are available on the account. Configure the active voice ID
via the `ELEVENLABS_VOICE_ID` environment variable or pass `--voice` to the script.

### Voicing rules
When asked to voice text — NEVER voice as-is.
Read `skills/voice/SKILL.md` and follow the pipeline:
analysis -> rewrite for live speech -> self-check -> generate -> send
