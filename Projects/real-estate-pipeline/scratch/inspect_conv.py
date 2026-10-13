import json

conv_id = "93848b55-b6d9-44f3-a5dc-e127706bc5cf"
path = rf"C:\Users\crypt\.gemini\antigravity-ide\brain\{conv_id}\.system_generated\logs\transcript_full.jsonl"

with open(path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        t = data.get("type")
        content = data.get("content") or ""
        tool_calls = data.get("tool_calls", [])
        
        # Check if browser_subagent or google or sheet is mentioned
        for tc in tool_calls:
            if "browser" in tc.get("name", ""):
                print(f"Step {data.get('step_index')} browser call: {json.dumps(tc['args'])[:200]}")
        if "sheet" in content.lower() or "google" in content.lower():
            print(f"Step {data.get('step_index')} [{t}] mentions sheet/google (len {len(content)})")
