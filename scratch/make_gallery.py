import os

img_dir = r"c:\Users\SRUTHI\Desktop\petland oman\Hygiene suppliments\bioline\bioline"
files = os.listdir(img_dir)

html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Bioline Products Gallery</title>
    <style>
        body { font-family: sans-serif; background: #f0f0f0; margin: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
        .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }
        .card img { max-width: 100%; max-height: 200px; object-fit: contain; }
        .filename { margin-top: 10px; font-weight: bold; font-size: 0.9em; word-break: break-all; }
    </style>
</head>
<body>
    <h1>Bioline Products Gallery</h1>
    <div class="grid">
"""

for f in files:
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif')):
        # relative path from scratch/gallery.html is ../Hygiene suppliments/bioline/bioline/filename
        rel_path = f"../Hygiene suppliments/bioline/bioline/{f}"
        html_content += f"""        <div class="card">
            <img src="{rel_path}" alt="{f}">
            <div class="filename">{f}</div>
        </div>
"""

html_content += """    </div>
</body>
</html>
"""

output_path = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\gallery.html"
with open(output_path, "w", encoding="utf-8") as out:
    out.write(html_content)

print("Gallery HTML generated at:", output_path)
