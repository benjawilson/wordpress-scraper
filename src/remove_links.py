import os
import re
from bs4 import BeautifulSoup

# Ask for input file
input_path = input("Enter the path to the HTML file: ").strip()

if not os.path.exists(input_path):
    print("❌ File not found.")
    exit()

# Read and clean the file before parsing
with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Remove invisible or unwanted Unicode control characters
html = re.sub(r'[\u200B-\u200D\uFEFF]', '', html)  # zero-width / BOM
html = html.replace('\xa0', ' ')                    # non-breaking space

# Parse cleaned HTML
soup = BeautifulSoup(html, "html.parser")

# Remove or unwrap <a> tags appropriately
for a_tag in soup.find_all("a"):
    if a_tag.find("img"):
        # Keep images and nested content
        a_tag.unwrap()
    else:
        # Replace text links with plain text
        a_tag.replace_with(a_tag.get_text())

# Overwrite original file
with open(input_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"✅ Links removed, images preserved, invisible characters cleaned.")
print(f"💾 File overwritten: {input_path}")