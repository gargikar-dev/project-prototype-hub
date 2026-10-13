import json

conv_id = "bfcbdd17-8587-4be2-ba19-2706837e675a"
path = rf"C:\Users\crypt\.gemini\antigravity-ide\brain\{conv_id}\.system_generated\logs\transcript_full.jsonl"

with open(path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data.get("type") == "BROWSER_SUBAGENT":
            c = data.get("content", "")
            for part in c.split("### Step "):
                if "cell-input" in part or "34DEBB1DF86981C74C910302E7CD4911" in part:
                    print("STEP:", part[:200].replace('\n', ' '))
