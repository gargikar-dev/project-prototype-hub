import json
import re

path = r"C:\Users\crypt\.gemini\antigravity-ide\brain\93848b55-b6d9-44f3-a5dc-e127706bc5cf\.system_generated\logs\transcript_full.jsonl"
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        matches = re.findall(r"https://docs\.google\.com/spreadsheets/d/[a-zA-Z0-9_\-]+[^\s\"']*", line)
        if matches:
            for m in set(matches):
                print("FOUND:", m)
