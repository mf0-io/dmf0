#!/usr/bin/env python3
"""
Parse saved group messages and update dossiers.
"""

import json
import os
import glob
from datetime import datetime
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MESSAGES_FILE = BASE_DIR / "memory" / "group-messages.jsonl"
DOSSIERS_DIR = BASE_DIR / "memory" / "contacts" / "dossiers"
CONNECTIONS_FILE = BASE_DIR / "memory" / "connections.md"

def parse_messages():
    """Parse saved group messages"""
    users = defaultdict(lambda: {
        "messages": [],
        "first_seen": None,
        "last_active": None,
        "username": None,
        "name": None,
        "user_id": None
    })

    if not os.path.exists(MESSAGES_FILE):
        print("No messages file found")
        return users

    with open(MESSAGES_FILE, 'r') as f:
        for line in f:
            try:
                message = json.loads(line)

                # Extract user info
                from_user = message.get("from", {})
                user_id = from_user.get("id")
                username = from_user.get("username")
                first_name = from_user.get("first_name", "")
                last_name = from_user.get("last_name", "")
                name = f"{first_name} {last_name}".strip()

                if not user_id:
                    continue

                user_key = f"@{username}" if username else f"user_{user_id}"

                users[user_key]["username"] = username
                users[user_key]["name"] = name
                users[user_key]["user_id"] = user_id

                # Extract message text
                text = message.get("text", "")
                timestamp = message.get("date")
                fetched_at = message.get("fetched_at")

                if timestamp:
                    dt = datetime.fromtimestamp(timestamp)
                    ts_str = dt.isoformat()

                    users[user_key]["messages"].append({
                        "timestamp": ts_str,
                        "text": text[:200] if text else "",
                        "fetched_at": fetched_at
                    })

                    if not users[user_key]["first_seen"] or ts_str < users[user_key]["first_seen"]:
                        users[user_key]["first_seen"] = ts_str
                    if not users[user_key]["last_active"] or ts_str > users[user_key]["last_active"]:
                        users[user_key]["last_active"] = ts_str

            except json.JSONDecodeError:
                continue

    return users

def update_dossier(username, data):
    """Update or create dossier for user"""
    os.makedirs(DOSSIERS_DIR, exist_ok=True)

    safe_username = username.replace("@", "").replace("/", "_")
    dossier_path = os.path.join(DOSSIERS_DIR, f"{safe_username}.md")

    # Check if dossier exists
    existing_content = ""
    if os.path.exists(dossier_path):
        with open(dossier_path, 'r') as f:
            existing_content = f.read()

    first_seen = data["first_seen"][:10] if data["first_seen"] else "unknown"
    last_active = data["last_active"][:16].replace("T", " ") if data["last_active"] else "unknown"
    message_count = len(data["messages"])

    # If dossier exists, just update counters
    if existing_content and ("## Profile" in existing_content or "## Профиль" in existing_content):
        lines = existing_content.split('\n')
        new_lines = []

        for i, line in enumerate(lines):
            if '**Last active:**' in line:
                new_lines.append(f"- **Last active:** {last_active}")
            elif '**Total interactions:**' in line:
                new_lines.append(f"- **Total interactions:** {message_count}")
            else:
                new_lines.append(line)

        # Add new messages to timeline
        if data["messages"]:
            # Find timeline section
            timeline_idx = -1
            for i, line in enumerate(new_lines):
                if '## Temporal Feed' in line:
                    timeline_idx = i
                    break

            if timeline_idx >= 0:
                # Group messages by date
                by_date = defaultdict(list)
                for msg in data["messages"][-20:]:  # Last 20 messages
                    date = msg["timestamp"][:10]
                    time = msg["timestamp"][11:16]
                    by_date[date].append((time, msg["text"]))

                # Add to existing timeline
                for date in sorted(by_date.keys(), reverse=True)[:3]:  # Last 3 dates
                    # Check if this date already exists
                    date_exists = any(date in line for line in new_lines)

                    if not date_exists:
                        new_lines.append(f"\n### {date}")
                        for time, text in sorted(by_date[date], reverse=True)[:5]:
                            preview = text[:80] + "..." if len(text) > 80 else text
                            new_lines.append(f"- {time} — {preview}")

        with open(dossier_path, 'w') as f:
            f.write('\n'.join(new_lines))

        return True

    # Create new dossier
    dossier_content = f"""# Dossier: {username}

## Profile
- **Platform:** Telegram
- **ID:** {data['user_id']}
- **Name:** {data['name']}
- **Username:** {username}
- **NFT holder:** unknown
- **First contact:** {first_seen}
- **Last active:** {last_active}
- **Total interactions:** {message_count}

## Tags
needs_analysis

## Connections
_To be filled during analysis_

## Temporal Feed
"""

    # Add messages grouped by date
    by_date = defaultdict(list)
    for msg in data["messages"]:
        date = msg["timestamp"][:10]
        time = msg["timestamp"][11:16]
        by_date[date].append((time, msg["text"]))

    for date in sorted(by_date.keys(), reverse=True)[:10]:
        dossier_content += f"\n### {date}\n"
        for time, text in sorted(by_date[date], reverse=True)[:10]:
            preview = text[:80] + "..." if len(text) > 80 else text
            dossier_content += f"- {time} — {preview}\n"

    dossier_content += "\n## Notes\n_Automatically created from group chat_\n"

    with open(dossier_path, 'w') as f:
        f.write(dossier_content)

    return True

def main():
    print("Parsing group messages...")
    users = parse_messages()

    if not users:
        print("No users found")
        return

    print(f"Found {len(users)} users")

    updated = 0
    for username, data in users.items():
        if update_dossier(username, data):
            updated += 1
            print(f"Updated dossier for {username}")

    print(f"Updated {updated} dossiers")

if __name__ == "__main__":
    main()
