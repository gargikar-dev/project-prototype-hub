import json

conv_id = "bfcbdd17-8587-4be2-ba19-2706837e675a"
path = rf"C:\Users\crypt\.gemini\antigravity-ide\brain\{conv_id}\.system_generated\logs\transcript_full.jsonl"

with open(path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data.get("type") == "BROWSER_SUBAGENT":
            c = data.get("content", "")
            idx = c.find("### Step 50:")
            if idx != -1:
                print(c[idx:idx+2500])
