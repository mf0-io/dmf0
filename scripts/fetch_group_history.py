#!/usr/bin/env python3
"""
Fetch and store messages from community group chat.
Runs periodically to capture all group messages.
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROUP_ID = os.environ.get("TELEGRAM_GROUP_ID")

BASE_DIR = Path(__file__).parent.parent
OUTPUT_FILE = BASE_DIR / "memory" / "group-messages.jsonl"
OFFSET_FILE = BASE_DIR / "memory" / ".telegram-offset.txt"

def get_updates(offset=None, limit=100, timeout=0):
    """Get updates from Telegram Bot API"""
    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set")
        return {"ok": False}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {
        "limit": limit,
        "timeout": timeout
    }
    if offset:
        params["offset"] = offset

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def save_message(message):
    """Save message to JSONL file"""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, 'a') as f:
        json.dump(message, f, ensure_ascii=False)
        f.write('\n')

def load_offset():
    """Load last processed update_id"""
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, 'r') as f:
            return int(f.read().strip())
    return None

def save_offset(offset):
    """Save last processed update_id"""
    os.makedirs(os.path.dirname(OFFSET_FILE), exist_ok=True)
    with open(OFFSET_FILE, 'w') as f:
        f.write(str(offset))

def main():
    if not BOT_TOKEN or not GROUP_ID:
        print("ERROR: Set TELEGRAM_BOT_TOKEN and TELEGRAM_GROUP_ID environment variables")
        return

# Added context
    try:
        # Get last offset
        offset = load_offset()

        # Get new updates
        updates = get_updates(offset=offset)

        if not updates.get("ok"):
            print(f"Error: {updates}")
            return

        results = updates.get("result", [])

        if not results:
            print("No new updates")
            return

        new_messages = 0
        last_update_id = None

        for update in results:
            last_update_id = update["update_id"]

            # Check if this is a message from our group
            if "message" in update:
                message = update["message"]
                chat_id = message.get("chat", {}).get("id")

                if str(chat_id) == GROUP_ID:
                    # Add timestamp for when we fetched it
                    message["fetched_at"] = datetime.utcnow().isoformat() + "Z"
                    save_message(message)
                    new_messages += 1

        # Update offset for next run
        if last_update_id:
            save_offset(last_update_id + 1)  # +1 to confirm we processed this update

        print(f"Processed {len(results)} updates, saved {new_messages} group messages")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
