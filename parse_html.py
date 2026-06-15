import re

with open("/Users/apple/Downloads/RUDEDOG_FAIR_2026_WAR_ROOM.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Let's extract all <div class="daytag"> ... </div>
daytags = re.findall(r'<div class="daytag">.*?</div>\s*</div>', html, re.DOTALL)
print(f"Found {len(daytags)} daytags")

for i, tag in enumerate(daytags):
    # print first 300 chars of tag to inspect
    clean_tag = re.sub(r'\s+', ' ', tag)
    print(f"Tag {i+1}: {clean_tag[:400]}...\n")
