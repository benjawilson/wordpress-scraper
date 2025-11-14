import os
import re
import requests
from bs4 import BeautifulSoup

def is_footer_marker(p_tag):
    """Return True if a <p> tag looks like the footer marker (a line of asterisks)."""
    text = p_tag.get_text() or ""
    # remove normal whitespace and NBSP, zero-width spaces
    text = re.sub(r'[\s\u00A0\u200B-\u200D\uFEFF]+', '', text)
    # match 3 or more literal asterisks (***** or * * * * * etc.)
    return bool(re.fullmatch(r'\*{3,}', text))

# === STEP 1: Fetch article from URL ===
url = input("Enter the WordPress article URL: ").strip()

print(f"🌐 Fetching: {url}")
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Extract title
title_tag = soup.find("h1", class_="entry-title")
title_text = title_tag.get_text(strip=True) if title_tag else "Untitled Article"

# Extract article content
article = soup.find("div", class_="entry-content")

if not article:
    print("❌ Could not find article content on that page.")
    exit()

# Remove navigation, footer, and other unwanted sections inside the article
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

# Create directory for output
output_dir = "html"
os.makedirs(output_dir, exist_ok=True)

# Sanitize filename
safe_title = "".join(c for c in title_text if c.isalnum() or c in (" ", "_", "-")).rstrip()
filename = os.path.join(output_dir, f"{safe_title}.html" if safe_title else "article.html")

# Save raw scraped file
with open(filename, "w", encoding="utf-8") as f:
    f.write(clean_html)

print(f"✅ Article saved to: {filename}")

# === STEP 2: Clean the saved HTML ===

# Read and clean invisible characters
with open(filename, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Remove BOM and zero-width, keep regular spaces
html = re.sub(r'[\u200B-\u200D\uFEFF]', '', html)
html = html.replace('\xa0', ' ')

soup = BeautifulSoup(html, "html.parser")

# --- 1. Remove or unwrap <a> tags appropriately ---
for a_tag in soup.find_all("a"):
    if a_tag.find("img"):
        a_tag.unwrap()  # keep images
    else:
        a_tag.replace_with(a_tag.get_text())

# --- 2. Remove image boxes and captions ---
for div in soup.find_all("div", class_=lambda x: x and "wp-caption" in x):
    imgs = div.find_all("img")
    if imgs:
        # replace the div with the images (keeps imgs in document order)
        div.replace_with(*imgs)
    else:
        div.decompose()

for p in soup.find_all("p", class_="wp-caption-text"):
    p.decompose()

# --- 3. Remove footer after '*****' (robust detection) ---
footer_marker = None
# search only inside the article body if possible
article_container = soup.find("div", class_="entry-content") or soup.body
for p in article_container.find_all("p"):
    if is_footer_marker(p):
        footer_marker = p
        break

if footer_marker:
    # remove footer marker and everything after it in the document order
    for tag in list(footer_marker.find_all_next()):
        try:
            tag.decompose()
        except Exception:
            # ignore if already removed or not decomposable
            pass
    try:
        footer_marker.decompose()
    except Exception:
        pass

# --- 4. Remove emphasis and bold formatting ---
for tag in soup.find_all(["em", "i", "strong", "b"]):
    tag.unwrap()

# --- Save cleaned HTML ---
with open(filename, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"🧹 Cleaned and saved final HTML: {filename}")