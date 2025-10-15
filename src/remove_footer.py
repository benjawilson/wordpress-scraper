import os
from bs4 import BeautifulSoup

# Ask for input file
input_path = input("Enter the path to the HTML file: ").strip()

if not os.path.exists(input_path):
    print("❌ File not found.")
    exit()

# Read the HTML
with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Find the <p> that contains only asterisks or asterisks with spaces
footer_marker = None
for p in soup.find_all("p"):
    if p.get_text(strip=True).replace(" ", "") == "*****":
        footer_marker = p
        break

# If marker found, remove it and everything after
if footer_marker:
    for tag in list(footer_marker.find_all_next()):  # find_all_next gives all tags after marker
        tag.decompose()
    footer_marker.decompose()  # remove the ***** line itself

# Overwrite the original file
with open(input_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"✅ Footer removed. File overwritten: {input_path}")