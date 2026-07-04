import os
import json

log_path = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\d7344ec0-3c55-4d54-9497-0adca2bc614e\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Scanning previous session logs...")
    with open(log_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "grooming_shower.png" in line:
                try:
                    obj = json.loads(line)
                    step = obj.get("step_index", 0)
                    if step < 140:
                        print(f"Step {step} | Type: {obj.get('type')} | Status: {obj.get('status')}")
                        tool_calls = obj.get("tool_calls", [])
                        if tool_calls:
                            for tc in tool_calls:
                                print(f"  Tool: {tc.get('name')}")
                                # Print args nicely
                                args = tc.get("args", {})
                                for k, v in args.items():
                                    if k in ["CommandLine", "TargetFile", "Instruction", "Description"]:
                                        print(f"    {k}: {v}")
                except Exception as e:
                    pass
else:
    print("Log file not found at:", log_path)
