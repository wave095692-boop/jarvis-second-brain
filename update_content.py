import os
import subprocess

BRAIN_DIR = "/Users/apple/.gemini/antigravity-ide/brain/8107daaa-f0f2-4535-b751-7c4d1a1f6591"
SCRATCH_DIR = "/Users/apple/.gemini/antigravity-ide/scratch"
DOWNLOADS_DIR = "/Users/apple/Downloads"
DESKTOP_DIR = "/Users/apple/Desktop"

# 10-Day Strategy Data with 3 content variations each
DAYS_DATA = [
    {
        'day': 'D-10',
        'phase': 'REACH',
        'ep': 'EP.1',
        'title': 'ประกาศ: "โกดังจะแตกแล้วครับ"',
        'color': '#ff0050',
        'c1_name': '1. คอนเทนต์หลัก (Reality Talk Video):',
        'c1_desc': 'บอสเคนทอล์กเตือนภัยรถติดย่านนนทบุรี บางใหญ่ บางบัวทอง จากแคมเปญล้างสต๊อกลุยหั่นครึ่งราคา ชวนพิมพ์คอมเมนต์ "ไปแน่" เพื่อสะสม Social Proof และบูสต์ Algorithm',
        'c2_name': '2. คอนเทนต์ย่อย (TikTok Fast Hook):',
        'c2_desc': 'คลิปสั้น 15 วิ แพนฟุตเทจคลังสินค้าถล่มล้นโกดัง พร้อมแคปชันนับถอยหลัง 10 วันด่วนๆ เร้าความสนใจอย่างรวดเร็ว',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Interactive Graphic):',
        'c3_desc': 'ภาพแบนเนอร์บอสเคนประกาศเตือนรถติดอย่างเป็นทางการ ชวนแท็กเพื่อนซี้ในคอมเมนต์เพื่อชิงสิทธิ์เข้าช้อปกลุ่มแรก',
        'budget': 'REACH obj ฿2,500/วัน (Boost ทันที 20:00 หลังโพสต์ 3 ชม. หาก ThruPlay >= 25%)',
        'psych': 'P1 Open Loop, P7 Unity'
    },
    {
        'day': 'D-9',
        'phase': 'REACH',
        'ep': 'EP.2',
        'title': 'คำสารภาพ CEO — ทำไมต้องลด',
        'color': '#ff0050',
        'c1_name': '1. คอนเทนต์หลัก (CEO Confession Video):',
        'c1_desc': 'บอสเคนทอล์กสารภาพตรงๆ เรื่องสั่งผ้าล้นคลังจนสต๊อกเกิน (Pratfall Effect) ลดแหลกเพราะหน้างานขายตรงไม่เสียค่า GP 30% ให้แอปออนไลน์ ชวนคอมเมนต์เสื้อรู้ดด็อกตัวแรก',
        'c2_name': '2. คอนเทนต์ย่อย (Behind the Scenes):',
        'c2_desc': 'คลิปสั้นสัมภาษณ์คนงานบ่นเหนื่อยเพราะเสื้อล้นโกดัง ตัดสลับภาพบอสเคนทำหน้าตึงและสั่งหั่นราคาระบายของด่วน',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Reason-Why Info):',
        'c3_desc': 'กราฟิกอินโฟชี้แจงคณิตศาสตร์ความคุ้มค่า เปรียบเทียบส่วนลด GP ระบบออนไลน์ที่ทีมงานเอามาเปลี่ยนเป็นส่วนลดหน้างานให้ผู้ซื้อ',
        'budget': 'ENG obj ฿1,500/วัน ใส่โพสต์สคริปต์ยาว / คลิปหลักสารภาพ CEO',
        'psych': 'P2 Pratfall, P3 Reason-Why'
    },
    {
        'day': 'D-8',
        'phase': 'REACH',
        'ep': 'EP.3',
        'title': 'หลักฐานปีที่แล้ว — footage 6,000 คน',
        'color': '#ff0050',
        'c1_name': '1. คอนเทนต์หลัก (Footage Compilation):',
        'c1_desc': 'วิดีโอตัดฟุตเทจงานปีก่อนแถวยาวลานจอดรถแตก เตือนไซส์ M และ L สีฮิตหมดไวมากตั้งแต่เที่ยงวันแรก ชวนแท็กเพื่อนซี้ที่ปีที่แล้วพลาดงานนี้ไปด่วน',
        'c2_name': '2. คอนเทนต์ย่อย (TikTok Customer Review):',
        'c2_desc': 'คลิปสอยรีวิวและสัมภาษณ์ความประทับใจลูกค้าเก่าที่ต่อแถวงานแฟร์ปีก่อน การันตีของฮิตไปไวจริง กระตุ้น Loss Aversion',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Grid Photo Album):',
        'c3_desc': 'โพสต์อัลบั้มภาพฝูงชนปีก่อนและภาพบรรยากาศลานจอดรถ เพื่อดึงคุณค่าทางสังคม (Social Proof) แบบ Organic',
        'budget': 'REACH obj ฿3,000/วัน (ตัวเปิดหลักกลุ่มเย็นชาเพื่อปูทางคนเข้างาน)',
        'psych': 'P4 Social Proof, P5 Loss Aversion'
    },
    {
        'day': 'D-7',
        'phase': 'REACH',
        'ep': 'EP.4',
        'title': 'Myth Busting — "ของลด = ของโละ?"',
        'color': '#ff0050',
        'c1_name': '1. คอนเทนต์หลัก (Quality Verification Video):',
        'c1_desc': 'บอสเคนหยิบเสื้อลายฮิตมาดึงโชว์ความเหนียวแน่นของใยผ้า AeroTwill ยืนยันเกรด A+ ช็อปเดียวกับบนห้าง ชวนพิมพ์ถามข้อกังขา บอสตอบเองทุกคอมเมนต์',
        'c2_name': '2. คอนเทนต์ย่อย (TikTok Fast QA):',
        'c2_desc': 'คลิปสั้นตอบด่วนประเด็นตำหนิ/ย้อมแมว นำเสนอแบบจริงใจ กระตุ้นความน่าเชื่อถือจากเหตุผลที่ลด (Reason-Why)',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Fuzzy Comparison):',
        'c3_desc': 'ภาพกราฟิกเปรียบเทียบผ้า AeroTwill ของแท้ปะทะเกรดเสื้อโละทั่วไป ชี้จุดต่างใยผ้าให้คน 30+ เห็นชัดๆ',
        'budget': 'ENG obj ฿2,000/วัน (เน้นเซฟ/แชร์เป็นคอนเทนต์อ้างอิงความเชื่อมั่น)',
        'psych': 'P3 Reason-Why, P2 Pratfall'
    },
    {
        'day': 'D-6',
        'phase': 'BELIEVE',
        'ep': 'EP.5',
        'title': 'พาเดินดูของ + เปิดราคาจริง',
        'color': '#00f2fe',
        'c1_name': '1. คอนเทนต์หลัก (Warehouse Tour Video):',
        'c1_desc': 'บอสเคนถือไฟฉายย่องพาทัวร์กล่องสต๊อก แอบแกะสปอยล์ราคาเสื้อยืดและกางเกงชิโน่ (ใส่เสียงเซนเซอร์บี๊บ) ชวนทายราคาเสื้อลุ้นสิทธิ์หน้างาน',
        'c2_name': '2. คอนเทนต์ย่อย (TikTok Fast Spoil):',
        'c2_desc': 'คลิปแพนกล่องและราวเสื้อผ้าสเปเชียลแบบไวๆ 15 วินาที ดึงอารมณ์ความคุ้มค่าและความจำกัดของสต๊อกล่วงหน้า',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Price List Teaser):',
        'c3_desc': 'แบนเนอร์ตารางสรุปราคาสินค้ากลุ่ม Hero Items คัดเน้นๆ โชว์ส่วนต่างราคาห้างปะทะราคาล้างคลัง',
        'budget': 'เริ่มชั้น Retargeting ยิงใส่คนดูวิดีโอย้อนหลัง >= 50% + Engage เพจ ฿1,500/วัน',
        'psych': 'P5 Scarcity, P6 Commitment'
    },
    {
        'day': 'D-5',
        'phase': 'BELIEVE',
        'ep': 'EP.6',
        'title': 'เสื้อตัวเดียว ชีวิต 30+ ทั้งใบ',
        'color': '#00f2fe',
        'c1_name': '1. คอนเทนต์หลัก (Lifestyle Insight Video):',
        'c1_desc': 'เรื่องเล่าวิถีผู้ชาย 30+ ไม่ต้องคิดเยอะ เสื้อรู้ดด็อกตัวเดียวตอบโจทย์ใส่คุ้มทั้งวัน ทนทาน ซักง่ายไม่หดย้วย ชวนส่งต่อชวนเพื่อนเปลี่ยนตู้',
        'c2_name': '2. คอนเทนต์ย่อย (TikTok POV POV):',
        'c2_desc': 'คลิป POV คุณแฟนแกล้งแฟนหนุ่มที่ชอบใส่เสื้อรู้ดด็อกตัวเก่าลายคลาสสิกซ้ำๆ แซวชวนจูงมือมาซื้อเหมาเซ็ตใหม่ที่งานแฟร์',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ ( lifestyle Album):',
        'c3_desc': 'โพสต์อัลบั้มภาพถ่ายนายแบบคนทำงานใส่เสื้อยืดสีพื้นแนวเรียบหรู คลาสสิก เหมาะกับครอบครัวและพ่อบ้านยุคใหม่',
        'budget': 'ENG ฿2,000 + RT ฿1,500/วัน (เป้าหมาย LINE Adds สะสมต้องแตะ 1,200 คนวันรุ่งขึ้น)',
        'psych': 'P7 Unity, P6 Commitment'
    },
    {
        'day': 'D-4',
        'phase': 'BELIEVE',
        'ep': 'EP.7',
        'title': 'Utility: ไปยังไง จอดตรงไหน',
        'color': '#00f2fe',
        'c1_name': '1. คอนเทนต์หลัก (Route Navigation Video):',
        'c1_desc': 'คู่มือเดินทางไปโกดังบางใหญ่ แนะนำพิกัดลานจอดรถฟรี 500 คัน และสถานี MRT สามแยกบางใหญ่ ชวนคอมเมนต์ย่านพักอาศัยเพื่อส่งลิงก์นำทางให้ทางแชท',
        'c2_name': '2. คอนเทนต์ย่อย (Quick Directions Clip):',
        'c2_desc': 'คลิปสั้นชี้จุดทางลัดเลี่ยงเส้นทางติดขัดรอบรัศมีปากเกร็ด/รัตนาธิเบศร์ นำเสนออย่างรวดเร็วและเป็นมิตร',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Map Infographic):',
        'c3_desc': 'ภาพแผนที่ลายแทงจุดจอดรถและพิกัด MRT สรุปขั้นตอนแบบรูปเดียวจบพร้อมปุ่มแอด LINE OA (เซฟและปักหมุดเพจทันที)',
        'budget': 'RT เป้าหมาย Traffic -> ส่งคนแอด LINE OA ฿2,000/วัน (คลิปนำทางคือตัวแปลงคนมางานดีที่สุด)',
        'psych': 'P6 Commitment, P7 Unity'
    },
    {
        'day': 'D-3',
        'phase': 'BELIEVE',
        'ep': 'EP.8',
        'title': 'ภูเขาสต๊อก + พี่หมีหน้าเครียด (BTS)',
        'color': '#00f2fe',
        'c1_name': '1. คอนเทนต์หลัก (Warehouse Behind Video):',
        'c1_desc': 'พาชมความยุ่งเหยียดการจัดกล่องสต๊อกของทีมแพ็ค แซว "พี่หมีคุมคลัง" ทำหน้าเครียดเพราะกลัวขายของไม่หมด ชวนเล่นเกมทายจำนวนกล่องในภูเขาสต๊อกเพื่อรับของรางวัลหน้างาน',
        'c2_name': '2. คอนเทนต์ย่อย (TIMELAPSE Packing):',
        'c2_desc': 'คลิปเร่งความเร็วโชว์พนักงานเติมราวผ้าและแพ็คกล่อง แสดงถึงความพร้อมและความยิ่งใหญ่ระดับ 6,000 คนปีก่อน',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Countdown Banner 3 Days):',
        'c3_desc': 'แบนเนอร์นับถอยหลัง 3 วันสุดท้าย โทนสีย้อนแสง HUD นีออน สปอยล์ของรางวัลพิเศษที่จะนำมาแจกหน้าบูธ',
        'budget': 'Boost ฿2,500 + RT ฿2,000/วัน (ใช้เกมดึงยอดคอมเมนต์กระตุ้น Organic Reach ตามธรรมชาติ)',
        'psych': 'P4 Social Proof, P1 Open Loop'
    },
    {
        'day': 'D-2',
        'phase': 'MOVE',
        'ep': 'EP.9',
        'title': 'จัดอันดับ 5 อย่างที่จะหมดก่อนเพื่อน',
        'color': '#00f576',
        'c1_name': '1. คอนเทนต์หลัก (Loss Aversion Countdown Video):',
        'c1_desc': 'บอสเคนแถลงจัดอันดับ 5 สินค้าฮิตขายดีปีก่อน (กางเกงชิโน่, หมวกปักลายหมาใหญ่, เสื้อคอลเลกชันลิมิเต็ด) ชวนระบุคอมเมนต์เป้าหมายแรกที่จะวิ่งไปช้อป',
        'c2_name': '2. คอนเทนต์ย่อย (TikTok Scarcity Warning):',
        'c2_desc': 'คลิปเตือนความหายากของไซส์ยอดนิยมเกลี้ยงไวใน 2 วันด่วนๆ ย้ำหมดแล้วหมดเลยไม่มีมาเพิ่ม',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Pre-Shopping Checklist):',
        'c3_desc': 'แผ่นอินโฟกราฟิกเช็คลิสต์เตรียมความพร้อมก่อนลุยงานวันเปิดคลังวันพรุ่งนี้ (ตารางไซส์เสื้อยืดและราคาหั่นลดคีย์บอร์ดสั่น)',
        'budget': 'RT อัดแน่นใส่ผู้มุ่งหวังทั้งหมด ฿3,500/วัน (ความถี่สูงได้เนื่องจากเหลือเวลา 2 วันสุดท้าย)',
        'psych': 'P5 Loss Aversion, P8 Goal Gradient'
    },
    {
        'day': 'D-1',
        'phase': 'MOVE',
        'ep': 'EP.10',
        'title': 'Final Call + ทิ้งเซอร์ไพรส์ปิดงาน',
        'color': '#00f576',
        'c1_name': '1. คอนเทนต์หลัก (Final Sweep Video):',
        'c1_desc': 'แถลงการณ์โค้งสุดท้าย ทิ้งปริศนารางวัลสุดพิเศษเฉลยเฉพาะ 10 คนแรกหน้าลานวันเปิดประตู นัดเจอไลฟ์ 09:30 และเปิดงาน 10:00 พรุ่งนี้เช้า',
        'c2_name': '2. คอนเทนต์ย่อย (TikTok Setup Tour):',
        'c2_desc': 'คลิปสปอยล์แสงสีความพร้อมและพาทัวร์ตู้ลอยรอบคลังคืนสุดท้าย ชวนกดเปิดกระดิ่งแจ้งเตือนไลฟ์เช้า',
        'c3_name': '3. คอนเทนต์มีม/รูปภาพ (Countdown 24 Hours):',
        'c3_desc': 'ภาพกราฟิกนับถอยหลัง 24 ชม. สุดท้ายคุมโทนนีออน ชวนคอมเมนต์อีโมจิไฟลุก "🔥" เพื่อรายงานตัว',
        'budget': 'RT ฿3,500 + REACH รัศมีแคบ 10 กม. รอบโกดังแบบถี่ยิบ ดึงคนออกจากบ้านจริง',
        'psych': 'P1 Open Loop, P8 Goal Gradient'
    }
]

def generate_markdown():
    path = os.path.join(BRAIN_DIR, "rudedog_fair_10days_content.md")
    print(f"Generating markdown: {path}")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write("# RUDEDOG FAIR 2026 — แผนปฏิบัติการคอนเทนต์ 10 วัน (1 หัวคิด 3 คอนเทนต์)\n\n")
        f.write("เอกสารฉบับปรับปรุงนี้ รวบรวมแนวคิดแคมเปญหลัก 10 วัน โดยแต่ละวันมีการประมวลผล **3 รูปแบบคอนเทนต์ (คอนเทนต์หลัก คอนเทนต์ย่อยคลิปสั้น และโพสต์อินเตอร์แอคทีฟรูปภาพ)** เพื่อตอบโจทย์กลยุทธ์การตลาดและเพิ่มยอดคนเข้างานแฟร์ให้ทะลุ 8,000 คน\n\n---\n\n")
        
        for d in DAYS_DATA:
            f.write(f"## 🎯 วัน {d['day']}: {d['ep']} {d['title']}\n")
            f.write(f"*เฟส: {d['phase']} — จิตวิทยา: {d['psych']}*\n\n")
            f.write(f"### {d['c1_name']}\n> {d['c1_desc']}\n\n")
            f.write(f"### {d['c2_name']}\n> {d['c2_desc']}\n\n")
            f.write(f"### {d['c3_name']}\n> {d['c3_desc']}\n\n")
            f.write(f"### ⚙️ ฝ่ายยุทธวิธีและงบประมาณ\n*   **การยิงงบโฆษณา:** {d['budget']}\n\n---\n\n")
            
    print("Markdown file successfully generated.")

def generate_war_room_html():
    path = os.path.join(DOWNLOADS_DIR, "RUDEDOG_FAIR_2026_WAR_ROOM.html")
    print(f"Generating WAR ROOM HTML in downloads: {path}")
    
    # Let's read first 170 lines of current WAR ROOM HTML to preserve styles and structure
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    head_part = []
    for line in lines:
        head_part.append(line)
        if "<!-- ============ 04 10-DAY MANIFEST ============ -->" in line:
            break
            
    head_content = "".join(head_part)
    
    # We will construct the body tags dynamically based on DAYS_DATA
    days_html = []
    days_html.append('\n<style>\n.phasebar{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}\n.phasechip{font-family:\'Kanit\';font-weight:700;font-size:.8rem;color:#fff;padding:5px 14px}\n.day-rail{display:grid;gap:16px}\n.daytag{background:var(--card);border:2px solid var(--ink);display:grid;grid-template-columns:120px 1fr;position:relative}\n.daytag::before{content:"";position:absolute;left:104px;top:0;bottom:0;border-left:2px dashed var(--steel)}\n.daytag .dleft{padding:16px 12px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}\n.daytag .dnum{font-family:\'IBM Plex Mono\';font-weight:700;font-size:1.5rem}\n.daytag .dphase{font-family:\'Kanit\';font-weight:700;font-size:.7rem;color:#fff;padding:2px 10px}\n.daytag .dbody{padding:16px 18px 14px 28px}\n.daytag h3{font-size:1.05rem}\n.daytag h3 .ep{color:var(--safety);font-family:\'IBM Plex Mono\';font-size:.85rem;margin-right:6px}\n.drow{display:flex;gap:8px;font-size:.85rem;margin-top:6px;align-items:baseline}\n.drow .lbl{font-family:\'Kanit\';font-weight:700;font-size:.7rem;min-width:86px;color:var(--steel);letter-spacing:.04em}\n.ptags{margin-top:8px}\n.ptag{display:inline-block;font-family:\'IBM Plex Mono\';font-size:.68rem;font-weight:700;border:1px solid var(--ink);padding:1px 7px;margin-right:5px;background:var(--paper)}\n@media(max-width:560px){.daytag{grid-template-columns:88px 1fr}.daytag::before{left:76px}.daytag .dbody{padding-left:20px}}\n</style>\n<section id="plan">\n  <div class="wrap">\n    <div class="sec-head"><span class="no">04</span><h2>ปฏิบัติการ 10 วัน — ใบงานรายวัน (1 หัวคิด 3 คอนเทนต์)</h2></div>\n    <div class="phasebar">\n      <span class="phasechip" style="background:var(--reach)">REACH — ทั้งนนท์ต้องรู้ (D-10→D-7)</span>\n      <span class="phasechip" style="background:var(--believe)">BELIEVE — เชื่อว่าคุ้มจริง (D-6→D-3)</span>\n      <span class="phasechip" style="background:var(--move)">MOVE — ออกจากบ้านมาจริง (D-2→D-0)</span>\n    </div>\n    <p class="sec-lead">ปรับปรุงกลยุทธ์ใหม่: <b>ทุกๆ แนวคิดหลัก (หัวข้อรายวัน) ทีมงานจะได้รับ 3 คอนเทนต์ทางเลือกเพื่อกระจายรูปแบบความเหมาะสม</b> ทั้งสคริปต์หลักคลิปทอล์ก คลิปสั้น TikTok และภาพมีมกระตุ้นการมีส่วนร่วม</p>\n    <div class="day-rail">\n')
    
    for d in DAYS_DATA:
        days_html.append(f'''
      <div class="daytag"><div class="dleft"><span class="dnum">{d['day']}</span><span class="dphase" style="background:var(--{d['phase'].lower()})">{d['phase']}</span></div>
        <div class="dbody"><h3><span class="ep">{d['ep']}</span>{d['title']}</h3>
          <div style="margin-top: 10px; border-left: 3px solid var(--safety); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--safety);">{d['c1_name']}</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">{d['c1_desc']}</div>
          </div>
          <div style="margin-top: 8px; border-left: 3px solid var(--believe); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--believe);">{d['c2_name']}</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">{d['c2_desc']}</div>
          </div>
          <div style="margin-top: 8px; border-left: 3px solid var(--move); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--move);">{d['c3_name']}</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">{d['c3_desc']}</div>
          </div>
          <div class="drow"><span class="lbl">การยิงโฆษณา</span><span>{d['budget']}</span></div>
          <div class="ptags"><span class="ptag">{d['psych'].split(',')[0]}</span>{f'<span class="ptag">{d["psych"].split(",")[1].strip()}</span>' if len(d['psych'].split(',')) > 1 else ''}</div>
        </div></div>
''')
        
    days_html.append('\n    </div>\n  </div>\n</section>\n')
    
    # Let's find index where section budget starts in original HTML to preserve it
    budget_start_line = -1
    for i, line in enumerate(lines):
        if '<!-- ============ 05 BUDGET & CHANNEL ============ -->' in line:
            budget_start_line = i
            break
            
    if budget_start_line != -1:
        tail_part = "".join(lines[budget_start_line:])
    else:
        tail_part = "</body></html>"
        
    full_html = head_content + "".join(days_html) + tail_part
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print("WAR ROOM HTML in downloads successfully updated.")

def generate_dark_pdf_script():
    path = os.path.join(SCRATCH_DIR, "generate_dark_pdf.py")
    print(f"Modifying dark PDF generator script: {path}")
    
    # We will generate the complete generate_dark_pdf.py code with the updated HTML template
    # Let's write the HTML structure inside generate_dark_pdf.py
    
    days_cards = []
    for idx, d in enumerate(DAYS_DATA):
        step_num = str(idx + 1).zfill(2)
        days_cards.append(f'''
            <!-- {d['day']} {d['ep']} -->
            <div class="card {d['phase'].lower()}">
                <div class="step-num">{step_num}</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY {d['day']} — {d['ep']}</span>
                        <h2>{d['title']}</h2>
                    </div>
                    <span class="badge {d['phase'].lower()}">{d['phase']}</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">{d['c1_name']}</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">{d['c1_desc']}</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">{d['c2_name']}</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">{d['c2_desc']}</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">{d['c3_name']}</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">{d['c3_desc']}</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> {d['budget']} | <b>จิตวิทยา:</b> {d['psych']}
                </div>
            </div>
''')

    cards_joined = "".join(days_cards)
    
    code_content = f'''import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RUDEDOG FAIR 2026 — WAR ROOM: 10-Day Strategy</title>
<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;700;800&family=IBM+Plex+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
    :root {{
        --primary: #00f2fe;     /* Neon Cyan */
        --secondary: #ff0050;   /* Neon Pink */
        --success: #00f576;     /* Neon Green */
        --bg: #0a0a0f;          /* Deep Dark Background */
        --card-bg: #16161e;     /* Dark Card Background */
        --text: #ffffff;        /* White text */
        --text-dim: #a0a0b0;    /* Muted Text */
        --border: #2a2a35;      /* Border Color */
        --reach: #ff0050;
        --believe: #00f2fe;
        --move: #00f576;
    }}
    
    * {{
        box-sizing: border-box;
    }}
    
    body {{ 
        font-family: 'Kanit', sans-serif; 
        background-color: var(--bg); 
        color: var(--text); 
        margin: 0; 
        padding: 40px 30px;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}
    
    .container {{ 
        max-width: 900px; 
        margin: 0 auto; 
    }}
    
    .header {{
        text-align: left;
        margin-bottom: 40px;
        border-left: 8px solid var(--secondary);
        padding-left: 25px;
        page-break-inside: avoid;
    }}
    
    h1 {{ 
        font-size: 38px; 
        margin: 0; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--text);
        font-weight: 800;
    }}
    
    .subtitle {{ 
        color: var(--primary); 
        font-size: 18px; 
        font-weight: 400;
        margin-top: 5px;
        letter-spacing: 0.05em;
    }}
    
    .meta-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-top: 25px;
        page-break-inside: avoid;
    }}

    .meta-item {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        padding: 12px 18px;
        border-radius: 12px;
    }}

    .meta-item b {{
        display: block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.15rem;
        color: var(--primary);
    }}

    .meta-item span {{
        font-size: 0.75rem;
        color: var(--text-dim);
    }}
    
    .card-list {{
        display: flex;
        flex-direction: column;
        gap: 30px;
        margin-top: 35px;
    }}
    
    .card {{ 
        background: var(--card-bg); 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
        page-break-inside: avoid;
    }}

    .card.reach {{ border-left: 6px solid var(--reach); }}
    .card.believe {{ border-left: 6px solid var(--believe); }}
    .card.move {{ border-left: 6px solid var(--move); }}
    
    .step-num {{
        position: absolute;
        top: -10px;
        right: 15px;
        font-size: 70px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.035);
        font-family: 'IBM Plex Mono', monospace;
        user-select: none;
    }}
    
    .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 12px;
        margin-bottom: 18px;
    }}

    .ep-label {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        color: var(--text-dim);
        font-weight: 500;
    }}

    .card h2 {{
        margin: 4px 0 0 0;
        font-size: 1.25rem;
        color: var(--text);
        font-weight: 700;
    }}
    
    .badge {{
        color: white;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .badge.reach {{ background: var(--secondary); }}
    .badge.believe {{ background: var(--primary); }}
    .badge.move {{ background: var(--success); color: #0a0a0f; }}

    .section-title {{
        font-size: 0.85rem;
        color: var(--primary);
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 16px;
        margin-bottom: 6px;
        letter-spacing: 0.05em;
    }}

    .script-box {{
        font-size: 0.82rem;
        line-height: 1.5;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 12px 15px;
        border-radius: 10px;
        color: #e2e2e8;
    }}

    .highlight-box {{
        background: linear-gradient(90deg, rgba(255,0,80,0.08) 0%, rgba(0,242,254,0.08) 100%);
        padding: 25px;
        border-radius: 24px;
        border: 1px dashed var(--primary);
        margin-top: 35px;
        page-break-inside: avoid;
    }}
    
    .highlight-box h3 {{
        margin-top: 0;
        color: var(--text);
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.1rem;
    }}
    .highlight-box p {{
        color: var(--text-dim);
        font-size: 0.85rem;
        line-height: 1.6;
        margin: 0;
    }}
    
    .footer {{
        text-align: center;
        margin-top: 50px;
        color: var(--text-dim);
        font-size: 13px;
        font-family: 'IBM Plex Mono', monospace;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 20px;
    }}

    @media print {{
        body {{
            background-color: #0a0a0f !important;
            color: #ffffff !important;
        }}
        .card {{
            background-color: #16161e !important;
            border-color: #2a2a35 !important;
        }}
        .script-box {{
            background-color: rgba(255, 255, 255, 0.02) !important;
        }}
        .highlight-box {{
            background: linear-gradient(90deg, rgba(255,0,80,0.08) 0%, rgba(0,242,254,0.08) 100%) !important;
        }}
    }}
</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>RDF-2026-MID: WAR ROOM</h1>
            <div class="subtitle">ปฏิบัติการ 10 วัน — ใบงานรายวัน (1 หัวคิด 3 คอนเทนต์ HUD Edition)</div>
            <div style="margin-top: 15px;">
                <a href="https://boswave-gamer.loca.lt" target="_blank" style="display: inline-block; background: var(--secondary); color: white; text-decoration: none; padding: 8px 16px; font-size: 13px; font-weight: 700; border-radius: 8px; border: 1px solid var(--secondary); box-shadow: 0 0 10px rgba(255,0,80,0.3); text-transform: uppercase; font-family: 'IBM Plex Mono', monospace;">💻 WEB PORTAL: boswave-gamer.loca.lt</a>
            </div>
        </div>

        <div class="meta-grid">
            <div class="meta-item">
                <b>№ RDF-2026-MID</b>
                <span>WORK ORDER STATUS: ACTIVE</span>
            </div>
            <div class="meta-item">
                <b>10-DAY COUNTDOWN</b>
                <span>CAMPAIGN CLOCK</span>
            </div>
            <div class="meta-item">
                <b>NONTHABURI RAD-20</b>
                <span>TARGET GEOGRAPHY</span>
            </div>
        </div>

        <div class="card-list">
            {cards_joined}
        </div>

        <div class="highlight-box">
            <h3>💡 Jarvis AI Insight</h3>
            <p>แผนปฏิบัติการความต้องการรายวันรอบนี้ปรับปรุงเป็นระบบ 1 หัวคิด 3 คอนเทนต์ ช่วยเติมเต็มสัดส่วนรูปแบบคอนเทนต์ของทีมให้มีทิศทางเลือกมากขึ้น ทั้งคลิป Reality, คลิปสั้นจับแนว TikTok Viral และแบนเนอร์รูปภาพคีย์เวิร์ด การันตียอดคนแห่เข้างาน 8,000 คนสำเร็จแน่นอนครับคุณโทนี่!</p>
        </div>

        <div class="footer">
            Generated by Gemini Jarvis AI for RUDEDOG® Team · คุณโทนี่ สตาร์ก
        </div>
    </div>
</body>
</html>
"""

# Save temporary HTML file
html_path = "/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/rudedog_fair_pdf_temp.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Run Headless Chrome to print to PDF
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
pdf_path = "/Users/apple/Desktop/rudedog_fair_10days_content.pdf"

command = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={{pdf_path}}",
    html_path
]

try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"PDF successfully compiled via headless Chrome at: {{pdf_path}}")
    # Remove temporary HTML
    if os.path.exists(html_path):
        os.remove(html_path)
except subprocess.CalledProcessError as e:
    print(f"Error compiling PDF: {{e}}")
    print(f"Stderr: {{e.stderr.decode('utf-8')}}")
'''
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(code_content)
        
    print("generate_dark_pdf.py successfully rewritten.")

if __name__ == "__main__":
    generate_markdown()
    generate_war_room_html()
    generate_dark_pdf_script()
    
    # Execute the dark pdf generator script to update the desktop PDF file
    print("Compiling Desktop PDF...")
    result = subprocess.run(['python3', os.path.join(SCRATCH_DIR, "generate_dark_pdf.py")], capture_output=True, text=True)
    print("Compile Output:", result.stdout)
    if result.stderr:
        print("Compile Error:", result.stderr)
