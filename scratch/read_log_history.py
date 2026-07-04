import os
import json

log_path = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\d7344ec0-3c55-4d54-9497-0adca2bc614e\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Found log file! Searching...")
    with open(log_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "grooming_shower.png" in line:
                try:
                    obj = json.loads(line)
                    # Print step details
                    print(f"Step {obj.get('step_index')} | Type: {obj.get('type')} | Status: {obj.get('status')}")
                    # If it's a tool call, print tool info
                    tool_calls = obj.get("tool_calls", [])
                    if tool_calls:
                        for tc in tool_calls:
                            print(f"  Tool: {tc.get('name')} | Args: {tc.get('args')}")
                except Exception as e:
                    print(f"Error parsing line {idx}: {e}")
else:
    print("Log file not found at:", log_path)
