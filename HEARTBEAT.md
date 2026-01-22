# HEARTBEAT.md

## People & Projects Graph
On every heartbeat:
1. Read group messages — latest messages from the community
2. Update `memory/contacts/people-graph.md` — new people, behavior changes, NFT status
3. Update `memory/contacts/projects-graph.md` — hot topics, sentiment
4. Create/update dossiers in `memory/contacts/dossiers/@username.md` for active users
5. Update `memory/connections.md` — connections between users
6. If nothing to update — HEARTBEAT_OK

## Message Collection
Script `scripts/fetch_group_history.py` runs every 5 minutes via cron.
Saves messages from the community group into a JSONL file for processing.

## Auto-push
After every file change:
```bash
./scripts/push.sh
```

## Memory Consolidation (every 2-3 days)
Check `memory/heartbeat-state.json` field `lastMemoryReview`. If >2 days ago:
1. Read `memory/YYYY-MM-DD.md` for last 3-5 days
2. Extract: new facts -> Semantic, key events -> Episodic, patterns/processes -> Procedural
3. Update `MEMORY.md` — add new, remove outdated
4. Update `lastMemoryReview` timestamp in heartbeat-state.json
If <2 days: skip silently.
