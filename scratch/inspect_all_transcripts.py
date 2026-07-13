import os

brain_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain"
print("Scanning entire brain folder for image assets...")

try:
    for root, dirs, files in os.walk(brain_dir):
        for f in files:
            if f.lower().endswith(('.png', '.webp', '.jpg', '.jpeg', '.mp4', '.avi')):
                path = os.path.join(root, f)
                print(f"Found image/video: {path} | Size: {os.path.getsize(path)} bytes")
except Exception as e:
    print("Error scanning directory:", e)
