import re

with open("/Users/apple/Downloads/RUDEDOG_FAIR_2026_WAR_ROOM.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

from html.parser import HTMLParser

class EpHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.in_daytag = False
        self.daytags_html = []
        self.html_accumulator = ""
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "div" and attrs_dict.get("class") == "daytag":
            self.in_daytag = True
            self.depth = 0
            self.html_accumulator = ""
        
        if self.in_daytag:
            self.depth += 1
            attr_str = " ".join([f'{k}="{v}"' for k, v in attrs])
            self.html_accumulator += f"<{tag} {attr_str}>" if attr_str else f"<{tag}>"

    def handle_endtag(self, tag):
        if self.in_daytag:
            self.html_accumulator += f"</{tag}>"
            self.depth -= 1
            if self.depth == 0:
                self.in_daytag = False
                self.daytags_html.append(self.html_accumulator)

    def handle_data(self, data):
        if self.in_daytag:
            self.html_accumulator += data

parser = EpHTMLParser()
parser.feed(html)

out_lines = []
out_lines.append(f"Extracted {len(parser.daytags_html)} daytags.")

for idx, d_html in enumerate(parser.daytags_html):
    dnum_match = re.search(r'class="dnum">(.*?)</span>', d_html)
    dnum = dnum_match.group(1).strip() if dnum_match else "N/A"
    
    dphase_match = re.search(r'class="dphase".*?>(.*?)</span>', d_html)
    dphase = dphase_match.group(1).strip() if dphase_match else "N/A"
    
    ep_match = re.search(r'class="ep">(.*?)</span>', d_html)
    ep = ep_match.group(1).strip() if ep_match else "N/A"
    
    h3_match = re.search(r'<h3.*?>(.*?)</h3>', d_html, re.DOTALL)
    h3 = re.sub(r'<.*?>', '', h3_match.group(1)).strip() if h3_match else "N/A"
    h3 = h3.replace(ep, "").strip()
    
    rows = []
    drows = re.findall(r'<div class="drow">.*?</div>', d_html, re.DOTALL)
    for dr in drows:
        lbl_match = re.search(r'<span class="lbl">(.*?)</span>', dr)
        lbl = lbl_match.group(1).strip() if lbl_match else ""
        content_match = re.search(r'</span>(.*?)</div>', dr, re.DOTALL)
        content = re.sub(r'<.*?>', '', content_match.group(1)).strip() if content_match else ""
        rows.append(f"{lbl}: {content}")
        
    details = []
    sub_divs = re.findall(r'<div style="margin-top:.*?border-left:.*?>.*?</div>\s*</div>', d_html, re.DOTALL)
    for sd in sub_divs:
        t_match = re.search(r'color:.*?;">(.*?)</div>', sd)
        title = t_match.group(1).strip() if t_match else ""
        text_match = re.search(r'color: #3a3a36.*?>(.*?)</div>', sd, re.DOTALL)
        text = re.sub(r'<.*?>', '', text_match.group(1)).strip() if text_match else ""
        details.append(f"{title}: {text}")
        
    out_lines.append(f"Index: {idx+1}")
    out_lines.append(f"[{dnum}] Phase: {dphase} | {ep} | Title: {h3}")
    for r in rows:
        out_lines.append(f"  Row: {r}")
    for d in details:
        out_lines.append(f"  Detail: {d}")
    out_lines.append("-" * 50)

with open("/Users/apple/.gemini/antigravity-ide/scratch/all_episodes.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print("Done writing to all_episodes.txt")
