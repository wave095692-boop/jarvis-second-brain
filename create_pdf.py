import re
import os
import subprocess

md_path = "/Users/apple/.gemini/antigravity-ide/brain/31977e7a-8cdf-4a1a-8989-cd639dc5b055/rudedog_content_ideas.md"
pdf_path = "/Users/apple/Desktop/rudedog_content_ideas.pdf"
html_temp_path = "/Users/apple/.gemini/antigravity-ide/scratch/rudedog_content_ideas_temp.html"

if not os.path.exists(md_path):
    print(f"Error: Markdown file not found at {md_path}")
    exit(1)

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's parse the markdown content to structured data
# Split by markdown headers "### "
episodes_raw = content.split("### ")[1:]

episodes = []
for ep_raw in episodes_raw:
    lines = [line.strip() for line in ep_raw.split("\n") if line.strip()]
    if not lines:
        continue
    
    # First line is the header: [D-10] EP.1: ประกาศ: "โกดังจะแตกแล้วครับ"
    header = lines[0]
    
    # Extract D-X, EP.X, Title
    d_num = "N/A"
    ep_num = "N/A"
    title = header
    
    d_match = re.search(r'\[(D-\d+)\]', header)
    if d_match:
        d_num = d_match.group(1)
        
    ep_match = re.search(r'(EP\.\d+|LIVE)', header)
    if ep_match:
        ep_num = ep_match.group(1)
        
    # Title is the rest
    clean_title = header
    clean_title = re.sub(r'\[D-\d+\]', '', clean_title)
    clean_title = re.sub(r'(EP\.\d+:?|LIVE:?)', '', clean_title)
    clean_title = clean_title.replace(":", "").strip()
    
    # Second line is usually the phase/description: *เน้นสร้างความตระหนักรู้และการแชร์วงกว้าง (REACH Phase)*
    phase_line = lines[1] if len(lines) > 1 else ""
    phase = "REACH"
    if "BELIEVE" in phase_line.upper():
        phase = "BELIEVE"
    elif "MOVE" in phase_line.upper() or "LIVE" in phase_line.upper():
        phase = "MOVE"
        
    # Extract ideas
    # Ideas start with "* **ไอเดียที่"
    ideas = []
    current_idea = None
    
    for line in lines[2:]:
        if line.startswith("* **ไอเดียที่"):
            if current_idea:
                ideas.append(current_idea)
            idea_title = re.sub(r'\*\*', '', line).replace("* ", "").strip()
            current_idea = {"title": idea_title, "details": []}
        elif line.startswith("*") and current_idea:
            # Bullet point detail
            clean_detail = re.sub(r'\*\*', '<b>', line, 1) # Replace first ** with <b>
            clean_detail = re.sub(r'\*\*', '</b>', clean_detail, 1) # Replace second ** with </b>
            clean_detail = clean_detail.replace("* ", "").strip()
            current_idea["details"].append(clean_detail)
        elif line.startswith("-") and current_idea:
            # Sub bullet
            clean_detail = re.sub(r'\*\*', '<b>', line, 1)
            clean_detail = re.sub(r'\*\*', '</b>', clean_detail, 1)
            clean_detail = clean_detail.replace("- ", "").strip()
            current_idea["details"].append(clean_detail)
            
    if current_idea:
        ideas.append(current_idea)
        
    episodes.append({
        "d_num": d_num,
        "ep_num": ep_num,
        "title": clean_title,
        "phase": phase,
        "phase_desc": phase_line.replace("*", "").strip(),
        "ideas": ideas
    })

# Build beautiful HTML content
html_cards = []
for ep in episodes:
    phase_class = ep["phase"].lower()
    
    ideas_html = []
    for idx, idea in enumerate(ep["ideas"]):
        details_html = []
        for det in idea["details"]:
            details_html.append(f"<li>{det}</li>")
        
        ideas_html.append(f"""
        <div class="idea-box">
            <div class="idea-title">💡 ไอเดียที่ {idx+1}: {idea["title"].replace("ไอเดียที่ " + str(idx+1) + ":", "").replace("ไอเดียที่ " + str(idx+1), "").strip()}</div>
            <ul class="idea-details">
                {"".join(details_html)}
            </ul>
        </div>
        """)
        
    html_cards.append(f"""
    <div class="card {phase_class}">
        <div class="card-header">
            <div class="ep-info">
                <span class="ep-num">{ep["d_num"]} ({ep["phase"]}) — {ep["ep_num"]}</span>
                <h3 class="ep-title">{ep["title"]}</h3>
            </div>
            <span class="badge {phase_class}">{ep["phase"]}</span>
        </div>
        <div class="phase-desc">{ep["phase_desc"]}</div>
        {"".join(ideas_html)}
    </div>
    """)

html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>RUDEDOG FAIR 2026 — WAR ROOM CONTENT IDEAS</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;600;700;800&family=Anuphan:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;700&display=swap');

:root {{
  --primary: #FF4D00; /* Safety Orange */
  --dark: #121212;
  --bg: #FAF9F6;
  --card-bg: #FFFFFF;
  --steel: #85837C;
  --border: #D1CFCA;
  
  --reach: #FF4D00;
  --believe: #0E6BA8;
  --move: #1F7A3D;
}}

* {{
  box-sizing: border-box;
}}

body {{
  font-family: 'Anuphan', sans-serif;
  background-color: var(--bg);
  color: var(--dark);
  margin: 0;
  padding: 40px;
  -webkit-print-color-adjust: exact;
}}

.container {{
  max-width: 900px;
  margin: 0 auto;
}}

.header {{
  border-bottom: 4px solid var(--dark);
  padding-bottom: 20px;
  margin-bottom: 25px;
}}

.eyebrow {{
  display: inline-block;
  background: var(--dark);
  color: #fff;
  font-family: 'Kanit';
  font-weight: 700;
  font-size: 0.75rem;
  padding: 4px 12px;
  letter-spacing: 0.1em;
  margin-bottom: 10px;
}}

h1 {{
  font-family: 'Kanit';
  font-size: 2.2rem;
  font-weight: 800;
  margin: 0 0 8px 0;
  line-height: 1.1;
  text-transform: uppercase;
}}

.sub {{
  font-size: 0.95rem;
  color: #444;
  margin: 0;
  line-height: 1.5;
}}

.meta-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-top: 20px;
}}

.meta-item {{
  border: 2px solid var(--dark);
  padding: 10px 15px;
  background: #fff;
  box-shadow: 3px 3px 0 var(--dark);
}}

.meta-item b {{
  display: block;
  font-family: 'IBM Plex Mono';
  font-size: 1.3rem;
  color: var(--primary);
}}

.meta-item span {{
  font-size: 0.75rem;
  color: #555;
  font-weight: 500;
}}

/* Episode Cards */
.card {{
  background: var(--card-bg);
  border: 2px solid var(--dark);
  border-left: 10px solid var(--dark);
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 4px 4px 0 var(--dark);
  position: relative;
  page-break-inside: avoid;
}}

.card.reach {{ border-left-color: var(--reach); }}
.card.believe {{ border-left-color: var(--believe); }}
.card.move {{ border-left-color: var(--move); }}

.card-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 2px solid var(--dark);
  padding-bottom: 10px;
  margin-bottom: 12px;
}}

.ep-info {{
  display: flex;
  flex-direction: column;
}}

.ep-num {{
  font-family: 'IBM Plex Mono';
  color: var(--primary);
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
}}

.ep-title {{
  font-family: 'Kanit';
  font-size: 1.3rem;
  font-weight: 700;
  margin: 4px 0 0 0;
}}

.badge {{
  font-family: 'Kanit';
  font-weight: 700;
  font-size: 0.75rem;
  color: #fff;
  padding: 5px 12px;
  border-radius: 2px;
  text-transform: uppercase;
}}

.badge.reach {{ background: var(--reach); }}
.badge.believe {{ background: var(--believe); }}
.badge.move {{ background: var(--move); }}

.phase-desc {{
  font-size: 0.85rem;
  font-style: italic;
  color: var(--steel);
  margin-bottom: 16px;
}}

.idea-box {{
  background: #FAF9F6;
  border: 1px solid var(--border);
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 4px;
}}

.idea-box:last-child {{
  margin-bottom: 0;
}}

.idea-title {{
  font-family: 'Kanit';
  font-size: 1rem;
  font-weight: 600;
  color: var(--dark);
  margin-bottom: 8px;
  border-bottom: 1px dashed var(--border);
  padding-bottom: 6px;
}}

.idea-details {{
  margin: 0;
  padding-left: 20px;
  font-size: 0.88rem;
  line-height: 1.5;
}}

.idea-details li {{
  margin-bottom: 6px;
}}

.idea-details li:last-child {{
  margin-bottom: 0;
}}

.footer {{
  text-align: center;
  font-family: 'IBM Plex Mono';
  font-size: 0.75rem;
  color: var(--steel);
  margin-top: 40px;
  border-top: 1px solid var(--border);
  padding-top: 20px;
}}
</style>
</head>
<body>

<div class="container">

  <div class="header">
    <span class="eyebrow">RUDEDOG FAIR — MID YEAR SALE 2026</span>
    <h1>ไอเดียคอนเทนต์ล้างสต๊อกรายวัน</h1>
    <p class="sub">แผนงานไอเดียคอนเทนต์สร้างสรรค์ที่ออกแบบมาเพื่อการเคลียร์สต๊อกโกดัง RUDEDOG 10 วันสุดท้าย (ภารกิจโกดังต้องว่าง) พร้อมการประยุกต์ใช้จิตวิทยาการตลาดในการเปลี่ยนผู้ชมทางโซเชียลมีเดียให้กลายเป็นลูกค้ามางานจริง</p>
    
    <div class="meta-grid">
      <div class="meta-item">
        <b>№ RDF-2026-IDEAS</b>
        <span>แผนไอเดียคอนเทนต์</span>
      </div>
      <div class="meta-item">
        <b>11 หัวข้อ</b>
        <span>22 ไอเดียคอนเทนต์รายวัน</span>
      </div>
      <div class="meta-item">
        <b>นนทบุรี + บางใหญ่</b>
        <span>รัศมีเป้าหมายการเจาะกลุ่ม</span>
      </div>
    </div>
  </div>

  {"".join(html_cards)}

  <div class="footer">
    RUDEDOG FAIR 2026 — WAR ROOM PLANNER · GENERATED BY JARVIS
  </div>

</div>

</body>
</html>
"""

with open(html_temp_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Compile to PDF using headless Chrome
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
command = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    html_temp_path
]

try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"PDF successfully compiled at: {pdf_path}")
    # Remove temp HTML
    if os.path.exists(html_temp_path):
        os.remove(html_temp_path)
except Exception as e:
    print(f"Error compiling PDF: {e}")
