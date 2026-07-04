import os
import glob
import time

scratch_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch"
py_files = glob.glob(os.path.join(scratch_dir, "*.py"))

files_with_time = []
for path in py_files:
    mtime = os.path.getmtime(path)
    files_with_time.append((path, mtime))

# Sort by mtime descending
files_with_time.sort(key=lambda x: x[1], reverse=True)

print("Recent Python scripts in scratch:")
for path, mtime in files_with_time[:10]:
    print(f"  {os.path.basename(path)} | Modified: {time.ctime(mtime)}")
