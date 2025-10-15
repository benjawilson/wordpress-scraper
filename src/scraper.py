import os
import requests
from bs4 import BeautifulSoup

# Ask for the URL
url = input("Enter the WordPress article URL: ").strip()

print(f"Fetching: {url}")
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Extract title
title_tag = soup.find("h1", class_="entry-title")
title_text = title_tag.get_text(strip=True) if title_tag else "Untitled Article"

# Extract article content
article = soup.find("div", class_="entry-content")

if article:
    # Remove unwanted elements
    for tag in article.find_all(["nav", "footer", "aside", "script", "style"]):
        tag.decompose()

    # Build the HTML content
    clean_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_text}</title>
</head>
<body>
    <h1>{title_text}</h1>
    {str(article)}
</body>
</html>"""

    # Make a directory for output if it doesn’t exist
    output_dir = "html"
    os.makedirs(output_dir, exist_ok=True)

    # Create a safe filename from the title
    safe_title = "".join(c for c in title_text if c.isalnum() or c in (" ", "_", "-")).rstrip()
    filename = os.path.join(output_dir, f"{safe_title}.html" if safe_title else "article.html")

    # Write the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(clean_html)

    print(f"✅ Article saved to: {filename}")
else:
    print("❌ Could not find article content on that page.")
