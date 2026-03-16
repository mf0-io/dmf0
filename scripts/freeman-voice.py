#!/usr/bin/env python3
"""Freeman Voice — ElevenLabs v3 TTS"""
import argparse, json, os, sys, requests
from pathlib import Path

VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "")
MODEL_ID = "eleven_v3"
API_BASE = "https://api.elevenlabs.io/v1"
KEY_FILE = Path.home() / ".openclaw" / "secrets" / "elevenlabs-key.txt"
OUTPUT_FORMAT = "mp3_44100_128"

def get_api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key: return key.strip()
    if KEY_FILE.exists(): return KEY_FILE.read_text().strip()
    print("ERROR: No API key", file=sys.stderr); sys.exit(1)

def generate(text, api_key, out, voice_id, model_id, stability=0.5, similarity=0.75, style=0.6):
    valid = [0.0, 0.5, 1.0]
    stab = min(valid, key=lambda x: abs(x - stability))
    resp = requests.post(f"{API_BASE}/text-to-speech/{voice_id}",
        json={"text": text, "model_id": model_id, "language_code": "ru",
              "voice_settings": {"stability": stab, "similarity_boost": similarity, "style": style, "use_speaker_boost": True}},
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        params={"output_format": OUTPUT_FORMAT}, timeout=120)
    if resp.status_code != 200:
        print(f"ERROR: {resp.status_code}", file=sys.stderr)
        try: print(json.dumps(resp.json(), ensure_ascii=False), file=sys.stderr)
        except: print(resp.text[:500], file=sys.stderr)
        sys.exit(1)
    with open(out, "wb") as f: f.write(resp.content)
    print(f"OK: {out} ({len(resp.content)/1024:.1f} KB)", file=sys.stderr)
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("text", nargs="?"); p.add_argument("--file", "-f"); p.add_argument("--stdin", action="store_true")
    p.add_argument("--out", "-o", default="freeman-voice.mp3"); p.add_argument("--voice", default=VOICE_ID)
    p.add_argument("--model", default=MODEL_ID); p.add_argument("--stability", type=float, default=0.5)
    p.add_argument("--similarity", type=float, default=0.75); p.add_argument("--style", type=float, default=0.6)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    text = sys.stdin.read().strip() if args.stdin else (Path(args.file).read_text().strip() if args.file else (args.text or ""))
    if not text: p.print_help(); sys.exit(1)
    out = generate(text, get_api_key(), args.out, args.voice, args.model, args.stability, args.similarity, args.style)
    if args.json: print(json.dumps({"status":"ok","file":out,"size_bytes":os.path.getsize(out),"text_length":len(text)}, ensure_ascii=False))
    else: print(out)

if __name__ == "__main__": main()
