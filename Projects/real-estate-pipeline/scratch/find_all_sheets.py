import os

target = "1k8aPzpsR3E"
root = r"C:\Users\crypt\.gemini\antigravity-ide\brain"

for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        if f.endswith(".jsonl") or f.endswith(".md") or f.endswith(".txt"):
            p = os.path.join(dirpath, f)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    if target in content:
                        idx = content.find(target)
                        print(p, "-->", content[max(0, idx-30):min(len(content), idx+100)])
            except Exception as e:
                pass
