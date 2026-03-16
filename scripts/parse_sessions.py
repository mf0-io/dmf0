#!/usr/bin/env python3
"""
Parse session files to extract user interactions.
Updates dossier files in memory/contacts/dossiers/
"""

import json
import os
import glob
from datetime import datetime
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SESSIONS_DIR = os.environ.get("SESSIONS_DIR", str(BASE_DIR / "sessions"))
DOSSIERS_DIR = BASE_DIR / "memory" / "contacts" / "dossiers"

def parse_sessions():
    users = defaultdict(lambda: {
        "interactions": [],
        "first_seen": None,
        "last_active": None,
        "platforms": set(),
        "usernames": set(),
        "ids": set()
    })

    # Find all session files
    session_files = glob.glob(f"{SESSIONS_DIR}/*.jsonl")

    for session_file in session_files:
        try:
            with open(session_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data.get('type') != 'message':
                            continue
                        if data.get('message', {}).get('role') != 'user':
                            continue

                        content = data['message'].get('content', [])
                        if not content or not isinstance(content, list):
                            continue

                        text = content[0].get('text', '') if content else ''

                        # Extract user info from metadata
                        if 'conversation_label' in text:
                            import re
                            match = re.search(r'@(\w+).*?id:(\d+)', text)
                            if match:
                                username = match.group(1)
                                user_id = match.group(2)

                                user_key = f"@{username}"
                                users[user_key]['usernames'].add(username)
                                users[user_key]['ids'].add(user_id)
                                users[user_key]['platforms'].add('telegram')

                                timestamp = data.get('timestamp', '')
                                if timestamp:
                                    users[user_key]['interactions'].append({
                                        'timestamp': timestamp,
                                        'session': os.path.basename(session_file)[:8]
                                    })

                                    if not users[user_key]['first_seen'] or timestamp < users[user_key]['first_seen']:
                                        users[user_key]['first_seen'] = timestamp
                                    if not users[user_key]['last_active'] or timestamp > users[user_key]['last_active']:
                                        users[user_key]['last_active'] = timestamp

                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
        except Exception as e:
            print(f"Error reading {session_file}: {e}")
            continue

    return users

def update_dossiers(users):
    os.makedirs(DOSSIERS_DIR, exist_ok=True)

    for username, data in users.items():
        if not data['usernames']:
            continue

        dossier_path = os.path.join(DOSSIERS_DIR, f"{username}.md")

        # Check if dossier exists
        if os.path.exists(dossier_path):
            # Update existing dossier
            with open(dossier_path, 'r') as f:
                content = f.read()

            # Update last activity and interaction count
            lines = content.split('\n')
            new_lines = []
            in_timeline = False

            for line in lines:
                if '## Temporal Feed' in line:
                    in_timeline = True

                new_lines.append(line)

            # Add new interactions
            if data['interactions']:
                # This is simplified — in production would parse and merge properly
                pass

        else:
            # Create new dossier
            first_seen = data['first_seen'][:10] if data['first_seen'] else 'unknown'
            last_active = data['last_active'][:16].replace('T', ' ') if data['last_active'] else 'unknown'

            dossier_content = f"""# Dossier: {username}

## Profile
- **Platform:** {', '.join(data['platforms'])}
- **ID:** {', '.join(data['ids'])}
- **Name:** {username}
- **NFT holder:** unknown
- **First contact:** {first_seen}
- **Last active:** {last_active}
- **Total interactions:** {len(data['interactions'])}

## Tags
needs_analysis

## Connections
_To be filled during analysis_

## Temporal Feed
"""

            # Add interactions grouped by date
            interactions_by_date = defaultdict(list)
            for interaction in data['interactions']:
                date = interaction['timestamp'][:10]
                time = interaction['timestamp'][11:16]
                interactions_by_date[date].append(time)

            for date in sorted(interactions_by_date.keys(), reverse=True):
                dossier_content += f"\n### {date}\n"
                for time in sorted(interactions_by_date[date], reverse=True):
                    dossier_content += f"- {time} — session interaction\n"

            dossier_content += "\n## Notes\n_Automatically created by parser_\n"

            with open(dossier_path, 'w') as f:
                f.write(dossier_content)
                print(f"Created dossier for {username}")

if __name__ == "__main__":
    print("Parsing sessions...")
    users = parse_sessions()
    print(f"Found {len(users)} users")

    print("Updating dossiers...")
    update_dossiers(users)
    print("Done")
