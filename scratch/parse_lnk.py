import re
import os

links = [
    r"C:\Users\SRUTHI\AppData\Roaming\Microsoft\Windows\Recent\landing banner-pet products.lnk",
    r"C:\Users\SRUTHI\AppData\Roaming\Microsoft\Windows\Recent\landing banner-pet services.lnk"
]

for lnk in links:
    if os.path.exists(lnk):
        with open(lnk, "rb") as f:
            data = f.read()
        # Find paths starting with C:\ or similar in the binary data
        paths = re.findall(rb'[a-zA-Z]:\\[^\x00\r\n\t]+', data)
        print(f"\nLnk: {lnk}")
        for p in paths:
            try:
                path_str = p.decode("utf-16", errors="ignore")
                print("  UTF-16 path:", repr(path_str))
            except:
                pass
            try:
                path_str = p.decode("utf-8", errors="ignore")
                print("  UTF-8 path:", repr(path_str))
            except:
                pass
    else:
        print(f"Lnk not found: {lnk}")
