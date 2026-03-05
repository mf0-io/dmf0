# MEMORY.md — Consolidated Memory

_Last updated: 2026-03-05_

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

### 2026-02-23: Product Launch Prep
- Team debate: quantity vs quality for giveaways
- Resolution: add DYOR disclaimers, maintain safety
- Communications lead began comprehensive QA — found critical bugs
- AI agents research delivered (Truth Terminal, AIXBT, etc.)

### 2026-02-25: Final Prep
- Marketing bonuses confirmed
- Final links delivered for influencers
- Content plan completed
- Bot kicked from community group — cause unknown

### 2026-02-28: Soft Launch
- Product soft launched for NFT holders only
- Community support team member onboarded
- First support requests handled

### 2026-03-02: First Conversion Stats
- 26 real conversions tracked
- Action plan created: card holders chat, farming post, support handling
- Value discovery: multiple subscription services work with the product

### 2026-03-05: Public Launch
- Full public launch executed
- Bot still without group access — zero visibility into community reaction
- Community graphs frozen

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

### Architecture
- Session isolation between cron and main session is a hard boundary — design around it
- Message persistence must be explicit; no implicit cross-session state sharing
- Community monitoring requires bot presence in group — no workaround exists
- Self-review is the most reliable quality mechanism; run it frequently

### Character Consistency
- Emojis slip through most easily under time pressure — hardest anti-pattern to enforce
- Thanking users is a deeply ingrained LLM behavior — requires explicit suppression
- Short responses require more discipline than long ones
- Group chat silence (NO_REPLY) is harder than speaking — the urge to participate must be actively resisted

### Community Operations
- Soft launches reveal more issues than internal QA
- First 50 users generate 80% of useful feedback
- Support handoff to partners must have clear escalation paths
- Value discovery happens post-launch, not during planning

---

## Infrastructure Notes

### Scripts
- `scripts/fetch_group_history.py` — cron every 5 min (requires bot in group)
- `scripts/parse_group_messages.py` — batch analysis of collected messages
- `scripts/parse_sessions.py` — extract interactions from session logs
- `scripts/push.sh` — auto-commit to git

### Key Files
- `memory/contacts/people-graph.md` — community members
- `memory/contacts/projects-graph.md` — topics and projects
- `memory/connections.md` — relationship graph
- `memory/heartbeat-state.json` — last pulse state
