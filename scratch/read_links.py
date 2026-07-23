import win32com.client
import os

shell = win32com.client.Dispatch("WScript.Shell")

links = [
    r"c:\Users\SRUTHI\AppData\Roaming\Microsoft\Windows\Recent\landing banner-pet products.lnk",
    r"c:\Users\SRUTHI\AppData\Roaming\Microsoft\Windows\Recent\landing banner-pet services.lnk"
]

for lnk in links:
    if os.path.exists(lnk):
        shortcut = shell.CreateShortCut(lnk)
        print(f"Lnk: {lnk} -> Target: {shortcut.TargetPath}")
    else:
        print(f"Lnk not found: {lnk}")
