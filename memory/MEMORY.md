# MEMORY.md — Consolidated Memory

_Last updated: 2026-02-21_

---

## Semantic Memory (Facts & Knowledge)

### Team Structure
- **COO** — Main coordination hub, assigns tasks, manages partnerships
- **Strategy Lead** — Marketing mechanics, influencer relations, X/Twitter focus
- **Communications Lead** — QA, documentation, quality gatekeeper
- **Content Lead** — Visuals, Freeman voice, posts
- **Operations Lead** — Partnerships, AI infrastructure
- **Influencer Coordinator** — Templates, influencer links
- **Community Support** — Discord/Telegram moderation

### External Partners
- **AppFather team** — Telegram AI infrastructure, bot development

### Products & Projects
- **Crypto Cards** — Partnership for crypto card distribution
  - Online Card: virtual, for online purchases
  - Offline Card: virtual with Apple/Google Pay, for physical stores
- **Community Game** — Exclusive skin for card holders
- **Mr.Freeman Bot** — Airdrop points system, bonus for card holders
- **no signal** — English TG channel for Freeman
- **dmf0** — Main TG channel (Russian)
- **Twitter automation** — Digital Freeman account

### AI Infrastructure
- Partner team building Telegram bot infrastructure
- Split: Twitter AI (posts + comments), Telegram infrastructure (chat-bot), Freeman team (prompts/RAG)
- MVP testing planned for community group

---

## Episodic Memory (Key Events)

### 2026-02-17: First Autonomous Session
- VPS crash loop fixed, configuration restored
- Self-review cron (6h) enabled
- MEMORY.md restructured: Semantic / Episodic / Procedural
- Community pulse cron created
- Discovered architecture limitation: cron isolation prevents message history access
- 11 consecutive pulses with no data — systemic issue identified
- Self-review found violations: emojis in responses, thanking users
- Anti-patterns section added to AGENTS.md

---

## Procedural Memory (Patterns & Processes)

### Product Launch Checklist
1. Teaser post (no date, no partner mention)
2. Main announcement + use cases
3. How-to guide
4. FAQ
5. Influencer kits with referral links
6. Early adopter NFT rewards
7. Support redirects to partner support

### Content Voice (Freeman)
- Russian: lowercase, no periods on short lines, dashes for emphasis
- English: provocative, philosophical, short punches
- NEVER: emojis, markdown headers, bullet lists, numbered steps
- Group chat: 1-2 lines max, 80%+ silence

### Heartbeat Workflow
1. Read group messages for new activity
2. Update people-graph.md with new/changed users
3. Update projects-graph.md with hot topics
4. Run push.sh to commit changes
5. Every 2-3 days: consolidate to MEMORY.md

---

## Lessons Learned

### Character Consistency
- Emojis slip through most easily under time pressure — hardest anti-pattern to enforce
- Thanking users is a deeply ingrained LLM behavior — requires explicit suppression
- Short responses require more discipline than long ones
- Group chat silence (NO_REPLY) is harder than speaking — the urge to participate must be actively resisted
