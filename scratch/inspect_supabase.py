import os
import json

brain_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain"
keywords = ["supabase", "project", "url", "anon", "service_role"]

print("Scanning for Supabase configurations in brain directory...")
results = []

try:
    for root, dirs, files in os.walk(brain_dir):
        for f in files:
            if f.endswith(('.jsonl', '.json', '.md', '.txt')):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                        for kw in keywords:
                            if kw.lower() in content.lower():
                                results.append((path, kw))
                                break
                except:
                    pass
except Exception as e:
    print("Error scanning:", e)

print(f"Found {len(results)} files matching keywords.")
for path, kw in results[:20]:
    print(f"\nMatch in: {path} (keyword: {kw})")
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
            for i, line in enumerate(lines, 1):
                if any(k.lower() in line.lower() for k in keywords):
                    print(f"  Line {i}: {line.strip()[:200]}")
    except:
        pass
