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

# Find all divs with class starting with 'wp-caption'
for div in soup.find_all("div", class_=lambda x: x and "wp-caption" in x):
    # Extract the image(s) inside
    imgs = div.find_all("img")
    if imgs:
        # Replace the entire div with just the images
        div.replace_with(*imgs)
    else:
        # If no images, just remove the div
        div.decompose()

# Also remove any <p class="wp-caption-text"> just in case
for p in soup.find_all("p", class_="wp-caption-text"):
    p.decompose()

# Overwrite the original file
with open(input_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"✅ Removed image boxes and captions. File overwritten: {input_path}")