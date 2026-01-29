
import json
import os
import re

# Paths
base_dir = "/Users/mc_ace/_mga14/mga14.lab/✴️ matias.area/07_Scraping/AIx2/mga14_scraping_v0_fundraising"
raw_json = os.path.join(base_dir, "data/raw_scrape.json")
output_md = os.path.join(base_dir, "data/content.md")
icon_dir = os.path.join(base_dir, "assets/icons")

os.makedirs(icon_dir, exist_ok=True)

with open(raw_json, 'r') as f:
    data = json.load(f)

# 1. Save Markdown
markdown_content = data['data']['markdown']
metadata = data['data']['metadata']

with open(output_md, 'w') as f:
    f.write(f"# {metadata.get('title', 'Scraped Content')}\n\n")
    f.write(f"Source: {metadata.get('sourceURL', 'N/A')}\n")
    f.write(f"Scrape ID: {metadata.get('scrapeId', 'N/A')}\n")
    f.write(f"Description: {metadata.get('description', 'N/A')}\n\n")
    f.write("---\n\n")
    f.write(markdown_content)

# 2. Extract SVGs from HTML
html_content = data['data']['html']
# Find all <svg ... </svg>
svgs = re.findall(r'<svg.*?</svg>', html_content, re.DOTALL)

for i, svg in enumerate(svgs):
    # Try to find a class name or something to name it
    # Lucide icons often have 'lucide-[name]' in class
    name_match = re.search(r'lucide-([a-z-]+)', svg)
    if name_match:
        icon_name = name_match.group(1)
    else:
        icon_name = f"icon_{i}"
    
    icon_path = os.path.join(icon_dir, f"{icon_name}.svg")
    with open(icon_path, 'w') as f:
        f.write(svg)

print(f"Processed {len(svgs)} icons and saved markdown.")
