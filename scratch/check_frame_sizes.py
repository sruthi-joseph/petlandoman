import os

desktop_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\frames\hero_desktop"
if os.path.exists(desktop_dir):
    files = [f for f in os.listdir(desktop_dir) if f.endswith('.png')]
    sizes = [os.path.getsize(os.path.join(desktop_dir, f)) for f in files]
    print(f"Total desktop frames: {len(files)}")
    if sizes:
        print(f"Average frame size: {sum(sizes) / len(sizes) / 1024:.2f} KB")
        print(f"Total size: {sum(sizes) / 1024 / 1024:.2f} MB")
else:
    print("Desktop frames directory not found")

mobile_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\frames\hero_mobile"
if os.path.exists(mobile_dir):
    files = [f for f in os.listdir(mobile_dir) if f.endswith('.png')]
    sizes = [os.path.getsize(os.path.join(mobile_dir, f)) for f in files]
    print(f"Total mobile frames: {len(files)}")
    if sizes:
        print(f"Average frame size: {sum(sizes) / len(sizes) / 1024:.2f} KB")
        print(f"Total size: {sum(sizes) / 1024 / 1024:.2f} MB")
else:
    print("Mobile frames directory not found")
