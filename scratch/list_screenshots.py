import os
import glob

artifacts_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\22fa6263-8c42-49d6-9c65-fef095efda85"
files = glob.glob(os.path.join(artifacts_dir, "*.png")) + glob.glob(os.path.join(artifacts_dir, "**", "*.png"), recursive=True)
files = sorted(files, key=os.path.getmtime, reverse=True)

print("Found PNG files (sorted by modification time, newest first):")
for f in files[:10]:
    print(f"  {f} - Size: {os.path.getsize(f)} bytes - ModTime: {os.path.getmtime(f)}")
