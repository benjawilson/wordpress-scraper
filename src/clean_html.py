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

# --- 1. Remove or unwrap <a> tags appropriately ---
for a_tag in soup.find_all("a"):
    if a_tag.find("img"):
        # Keep images and nested content
        a_tag.unwrap()
    else:
        # Replace text links with plain text
        a_tag.replace_with(a_tag.get_text())

# --- 2. Remove image boxes and captions ---
for div in soup.find_all("div", class_=lambda x: x and "wp-caption" in x):
    imgs = div.find_all("img")
    if imgs:
        div.replace_with(*imgs)
    else:
        div.decompose()

for p in soup.find_all("p", class_="wp-caption-text"):
    p.decompose()

# --- 3. Remove footer after '*****' ---
footer_marker = None
for p in soup.find_all("p"):
    if p.get_text(strip=True).replace(" ", "") == "*****":
        footer_marker = p
        break

if footer_marker:
    for tag in list(footer_marker.find_all_next()):
        tag.decompose()
    footer_marker.decompose()

# --- 4. Remove emphasis and bold formatting ---
for tag in soup.find_all(["em", "i", "strong", "b"]):
    tag.unwrap()

# --- Save back to original file ---
with open(input_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"✅ HTML cleaned successfully. File overwritten: {input_path}")