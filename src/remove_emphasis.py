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

# Unwrap tags that create emphasis or bold
for tag in soup.find_all(["em", "i", "strong", "b"]):
    tag.unwrap()

# Overwrite the original file
with open(input_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"✅ All emphasis and bold formatting removed. File overwritten: {input_path}")