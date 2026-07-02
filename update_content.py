import os

def replace_in_file(filepath, target, replacement):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        if target in content:
            new_content = content.replace(target, replacement)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Successfully updated: {filepath}")
            return True
        else:
            print(f"Target text not found in: {filepath}")
            return False
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

# 1. Update rudedog_content_ideas.md in both brain and scratch folder
target_ideas = """### [D-9] EP.2: คำสารภาพ CEO — ทำไมต้องลด
*ใช้ความจริงใจลดแรงต้านและดึงดูดความรู้สึกเห็นอกเห็นใจ (REACH Phase)*

* **ไอเดียที่ 1 (CEO Confession Vlog): "ผมยอมโดนด่าแต่ไม่อยากจมทุน"**
  * **รูปแบบ:** คลิปวิดีโอบอสเคนนั่งพูดคุยหน้ากล้องดิบๆ สไตล์ Vlog เดินถือกล้องในโกดัง เล่าเรื่องจริงอย่างตรงไปตรงมาว่า *"ผมสั่งผ้าล็อตนี้ล้นคลังและผลิตเกินเป้าไปเยอะ ยอมรับว่าตัวเองคำนวณพลาดครับ ดีกว่าปล่อยทิ้งไว้จนไม่มีที่เดิน ผมขอเอามาหั่นราคาส่งต่อให้ทุกคนถูกๆ ดีกว่า"*
  * **จิตวิทยาการตลาด:** *P2 Pratfall Effect* การยอมรับความผิดพลาดทำให้แบรนด์ดูน่าเชื่อถือและเข้าถึงง่ายขึ้น พร้อมเผยว่าการมาซื้อหน้าคลังช่วยตัดค่า GP ของแพลตฟอร์มออนไลน์ได้ถึง 30% จึงเอาส่วนต่างตรงนั้นมาลดราคาให้ลูกค้าได้เต็มๆ
* **ไอเดียที่ 2 (Reason-Why Info): อินโฟกราฟิก "ชำแหละค่า GP ออนไลน์ vs มาหน้าคลัง"**
  * **รูปแบบ:** กราฟิกชี้แจงเปรียบเทียบค่าธรรมเนียมแพลตฟอร์มออนไลน์ที่โดนหัก เปรียบเทียบกับการจัดงานลดราคาที่โกดัง เพื่ออธิบายเหตุผลว่าทำไมถึงขายราคานี้ได้เฉพาะหน้าโกดังเท่านั้น"""

replacement_ideas = """### [D-9] EP.2: ชาเลนจ์ท้าชนบัญชี — ทำไมต้องลด
*สร้างความสนุกสนานแบบท้าทายควบคู่ความโปร่งใส (REACH Phase)*

* **ไอเดียที่ 1 (Vlog Challenge & Zero-GP Math): "เดิมพันล้างสต๊อกท้าชนฝ่ายบัญชี"**
  * **รูปแบบ:** คลิปวิดีโอบอสเคนพูดหน้ากล้อง ท้าชนแผนกบัญชีที่สบประมาทว่าล้างสต๊อกแสนชิ้นไม่หมดใน 9 วัน บอสเคนเลยยอมหั่นราคาต่ำกว่าทุน โดยใช้เหตุผลความจริงใจว่าเป็นการตัดค่าธรรมเนียม GP ออนไลน์ 30% และค่าเช่าห้างราคาแพง คืนเป็นส่วนลดให้ทุกคนที่มาหาที่โกดังเพื่อทลายสต๊อกร่วมกัน
  * **จิตวิทยาการตลาด:** *P7 Unity (รวมทีม)* ชวนลูกค้ามาร่วมภารกิจดันโบนัสให้พนักงานคลัง + *P3 Reason-Why* ความโปร่งใสของตัวเลข GP 0% เพิ่มความสมจริงน่าเชื่อถือ
* **ไอเดียที่ 2 (Interactive Gamification): กราฟิกนับถอยหลังภารกิจทลายคลัง**
  * **รูปแบบ:** ภาพแบนเนอร์ตารางสรุปราคาสินค้าในชาเลนจ์ 9 วัน พร้อมกระดานไวท์บอร์ดอัปเดตเป้าหมายล้างคลังรายวัน ชวนลูกค้าเข้ามาคอมเมนต์คำว่า "ลุย" เพื่อรายงานตัวเข้าร่วมชาเลนจ์"""

replace_in_file("/Users/apple/.gemini/antigravity-ide/brain/31977e7a-8cdf-4a1a-8989-cd639dc5b055/rudedog_content_ideas.md", target_ideas, replacement_ideas)
replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/campaign_files/rudedog_content_ideas.md", target_ideas, replacement_ideas)


# 2. Update rudedog_fair_10days_content.md
target_10days = """## 🎯 วัน D-9: EP.2 คำสารภาพ CEO — ทำไมต้องลด
*เฟส: REACH — จิตวิทยา: P2 Pratfall, P3 Reason-Why*

### 1. คอนเทนต์หลัก (CEO Confession Video):
> บอสเคนทอล์กสารภาพตรงๆ เรื่องสั่งผ้าล้นคลังจนสต๊อกเกิน (Pratfall Effect) ลดแหลกเพราะหน้างานขายตรงไม่เสียค่า GP 30% ให้แอปออนไลน์ ชวนคอมเมนต์เสื้อรู้ดด็อกตัวแรก

### 2. คอนเทนต์ย่อย (Behind the Scenes):
> คลิปสั้นสัมภาษณ์คนงานบ่นเหนื่อยเพราะเสื้อล้นโกดัง ตัดสลับภาพบอสเคนทำหน้าตึงและสั่งหั่นราคาระบายของด่วน

### 3. คอนเทนต์มีม/รูปภาพ (Reason-Why Info):
> กราฟิกอินโฟชี้แจงคณิตศาสตร์ความคุ้มค่า เปรียบเทียบส่วนลด GP ระบบออนไลน์ที่ทีมงานเอามาเปลี่ยนเป็นส่วนลดหน้างานให้ผู้ซื้อ"""

replacement_10days = """## 🎯 วัน D-9: EP.2 ชาเลนจ์ท้าชนบัญชี — ทำไมต้องลด
*เฟส: REACH — จิตวิทยา: P7 Unity, P3 Reason-Why*

### 1. คอนเทนต์หลัก (Vlog Challenge & Zero-GP Math):
> บอสเคนทอล์กท้าเดิมพันกับแผนกบัญชีที่ว่าล้างสต๊อกแสนชิ้นไม่หมดใน 9 วัน หั่นราคาต่ำกว่าทุนด้วยการตัดค่า GP ออนไลน์ 30% คืนให้ลูกค้า ดึงคนมาร่วมลุยภารกิจดันโบนัสคลังสินค้า

### 2. คอนเทนต์ย่อย (Behind the Scenes):
> คลิปสัมภาษณ์พนักงานคลังและพี่หมีแอบลุ้นโบนัสและเตรียมลุยชาเลนจ์ 9 วัน สลับภาพบอสเคนกอดอกเชียร์ทีมงานแบบเป็นกันเอง

### 3. คอนเทนต์มีม/รูปภาพ (Reason-Why Challenge Info):
> อินโฟกราฟิกท้าชนแผนกบัญชี ตีแผ่ตัวเลขเปรียบเทียบค่าธรรมเนียม GP ที่โดนหัก 30% นำมาเปลี่ยนเป็นส่วนลดให้ผู้ซื้อที่หน้างานจริง"""

replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/campaign_files/rudedog_fair_10days_content.md", target_10days, replacement_10days)


# 3. Update generate_beautiful_pdf.py (Title, script, social copy, mission)
target_beautiful_title = '<h3 class="ep-title">คำสารภาพ CEO — ทำไมต้องลด</h3>'
replacement_beautiful_title = '<h3 class="ep-title">ชาเลนจ์ท้าชนบัญชี — ทำไมต้องลด</h3>'
replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/generate_beautiful_pdf.py", target_beautiful_title, replacement_beautiful_title)

target_beautiful_script = """      <p><b>[0:00 - 0:03] Hook (Pratfall Effect):</b> <i>(กล้องซูมหน้าบอสเคนทำหน้าจริงจัง ถือไมค์พูดแผ่วเบา)</i> "วันนี้ผมต้องออกมาสารภาพตรง ๆ ครับ... ว่างานนี้เกิดขึ้นได้เพราะ 'ความผิดพลาด' ของผมเอง"</p>
      <p><b>[0:04 - 0:25] Body:</b> "ผมประเมินยอดผลิตผิดพลาดครับ สั่งผ้า สั่งตัดของมาเยอะเกินจนล้นโกดัง! แต่ความโชคร้ายของผมรอบนี้... จะกลายเป็นความโชคดีของลูกค้าทุกคนครับ เพราะบอร์ดบริหารบอกผมคำเดียวว่า 'ต้องระบายออกให้หมด' เราเลยจับหั่นราคาลงต่ำกว่าทุน เพื่อเคลียร์พื้นที่โกดัง"</p>
      <p><b>[0:26 - 0:40] Reason-Why:</b> "หลายคนถามว่าลดขนาดนี้ของปลอมหรือเปล่า? ของแท้ร้อยเปอร์เซ็นต์ครับ! ที่เราลดได้ขนาดนี้ เพราะขายตรงหน้าโกดัง ไม่ต้องเสียค่าเช่าห้าง ไม่ต้องโดนหักเปอร์เซ็นต์ระบบออนไลน์เกือบสามสิบเปอร์เซ็นต์ ส่วนต่างตรงนี้ผมคืนให้บอสทุกคนแทนครับ"</p>
      <p><b>[0:41 - 0:45] Outro:</b> "ถามจริง... บอสเคยซื้อเสื้อรู้ดด็อกตัวแรกเมื่อไหร่ ราคาเท่าไหร่ คอมเมนต์บอกกันหน่อยครับ... <b>เหลืออีก 9 วัน... โกดังต้องว่าง!</b>"</p>"""

replacement_beautiful_script = """      <p><b>[0:00 - 0:03] Hook (Accountant Challenge):</b> <i>(บอสเคนยืนหน้ากระดานไวท์บอร์ดที่เขียนเลขเป้าหมาย 9 วัน หรือถือเอกสารงบการเงินทำหน้าจริงจัง)</i> "ฝ่ายบัญชีคัดค้านผมหัวชนฝาครับ... เขาบอกว่าไม่มีทางหรอกที่คนจะแห่มาช่วยเราเคลียร์เสื้อแสนชิ้นหมดโกดังบางใหญ่ได้ใน 9 วัน..."</p>
      <p><b>[0:04 - 0:25] Body:</b> "ผมเลยท้าบัญชีกลับไปว่า... งั้นมาเดิมพันกัน! ผมจะหั่นราคาเสื้อยืด กางเกง หมวก ทุกรุ่นในโกดังลงลึกที่สุดต่ำกว่าทุน! หลายคนถามว่าทำไมลดได้ขนาดนี้? เพราะเราขายตรงหน้าคลัง ไม่ต้องผ่านห้าง ไม่โดนหักค่า GP แอปออนไลน์เกือบ 30% ส่วนต่างตรงนี้ผมตัดทิ้งแล้วเปลี่ยนเป็นส่วนลดคืนให้บอสทุกคนแทน!"</p>
      <p><b>[0:26 - 0:40] Unity & Reward:</b> "งานนี้เดิมพันด้วยความเชื่อใจของผมครับ ถ้าพวกเราช่วยกันเคลียร์สต๊อกจนโล่งเกลี้ยงก่อน 9 วัน ผมจะจ่ายโบนัสพิเศษให้พนักงานคลังสินค้าทุกคนด้วย มาร่วมภารกิจทลายคลังกับพวกเรานะครับ"</p>
      <p><b>[0:41 - 0:45] Outro:</b> "บอสพร้อมลุยชาเลนจ์นี้กับผมไหม? พิมพ์คำว่า <b>'ลุย'</b> ในคอมเมนต์ด่วนเลยครับ... <b>เหลืออีก 9 วัน... โกดังต้องว่าง!</b>"</p>"""

replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/generate_beautiful_pdf.py", target_beautiful_script, replacement_beautiful_script)

target_beautiful_social = """    <div class="copy-box"><b>สารภาพบาปจากใจ CEO... "ผมสั่งของเกินโกดังครับ"</b> 🙏🐶

เมื่อประเมินสต๊อกพลาดจนล้นคลัง ทางออกเดียวที่จะทำให้พนักงานได้มีพื้นที่เดินทำความสะอาดคือ... เทขายในราคาที่บอสทุกคนต้องตะลึง! 

💡 <i>ทำไมถึงลดราคาได้ดุเดือดขนาดนี้?</i>
เพราะงานนี้เราจัดหน้าโกดังเราเองครับ ไม่เสียค่า GP ให้แอปออนไลน์ (เกือบ 30%) ไม่ต้องจ่ายค่าเช่าห้างราคาแพง ส่วนต่างทั้งหมดเราตัดทิ้งแล้วเปลี่ยนเป็นราคาพิเศษคืนให้คุณทันที!

👇 บอสจำเสื้อ RUDEDOG ตัวแรกที่บอสซื้อได้ไหมครับว่าซื้อรุ่นอะไร ราคาเท่าไหร่? คอมเมนต์มาเล่าให้ฟังหน่อยครับ!
#RudedogFair2026 #CEOสารภาพ #ของแท้ราคาโกดัง</div>

    <div class="section-title">ภารกิจคอมเมนต์ประจำวัน</div>
    <div class="mission-box">
      <b>ภารกิจ:</b> ดึงดูดลูกค้าเก่าให้มาร่วมเล่าประวัติการซื้อเสื้อตัวแรก เพื่อดึง Social Proof ออกมายืนยันคุณภาพที่ทนทาน
    </div>"""

replacement_beautiful_social = """    <div class="copy-box"><b>บัญชีท้ามา... บอสเคนท้ากลับ! ชาเลนจ์ทลายโกดังใน 9 วัน!</b> 💥🐶

เมื่อฝ่ายการเงินบอกว่า "ไม่มีทางล้างสต๊อกสินค้าหลักแสนชิ้นหมดใน 9 วันที่บางใหญ่ได้หรอก"
บอสเคนเลยจัดชาเลนจ์สุดบ้าพลัง: หั่นราคาสินค้าทุกรายการต่ำกว่าทุน ท้าทายบอสทุกคนให้มารวมพลังเคลียร์โกดังให้โล่งร่วมกัน!

💡 <i>ทำไมถึงหั่นราคาลงได้ดุเดือดขนาดนี้?</i>
เพราะเราขายตรงหน้าโกดัง ไม่เสียค่า GP หักเปอร์เซ็นต์ให้แอปออนไลน์ (ประหยัดไปเกือบ 30%) ไม่ต้องจ่ายค่าเช่าห้างราคาแพง ส่วนต่างทั้งหมดตรงนี้เราตัดออก แล้วเปลี่ยนเป็นราคาสุดพิเศษคืนให้คุณทันที!

👇 บอสพร้อมลุยชาเลนจ์นี้กับพวกเราไหมครับ? พิมพ์คอมเมนต์รายงานตัวคำว่า "ลุย" ใต้โพสต์นี้ด่วนเลยครับ!
#RudedogFair2026 #ชาเลนจ์9วัน #ภารกิจโกดังต้องว่าง #ของแท้ราคาโกดัง</div>

    <div class="section-title">ภารกิจคอมเมนต์ประจำวัน</div>
    <div class="mission-box">
      <b>ภารกิจ:</b> ดึงดูดลูกค้าให้มามีส่วนร่วมด้วยการพิมพ์คอมเมนต์คำว่า "ลุย" เพื่อปลุกปั้นเอนเกจเมนต์และผลักดันอัลกอริทึม
    </div>"""

replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/generate_beautiful_pdf.py", target_beautiful_social, replacement_beautiful_social)


# 4. Update generate_dark_pdf.py
target_dark = """            <!-- D-9 EP.2 -->
            <div class="card reach">
                <div class="step-num">02</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-9 — EP.2</span>
                        <h2>คำสารภาพ CEO — ทำไมต้องลด</h2>
                    </div>
                    <span class="badge reach">REACH</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (CEO Confession Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">บอสเคนทอล์กสารภาพตรงๆ เรื่องสั่งผ้าล้นคลังจนสต๊อกเกิน (Pratfall Effect) ลดแหลกเพราะหน้างานขายตรงไม่เสียค่า GP 30% ให้แอปออนไลน์ ชวนคอมเมนต์เสื้อรู้ดด็อกตัวแรก</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (Behind the Scenes):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปสั้นสัมภาษณ์คนงานบ่นเหนื่อยเพราะเสื้อล้นโกดัง ตัดสลับภาพบอสเคนทำหน้าตึงและสั่งหั่นราคาระบายของด่วน</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Reason-Why Info):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">กราฟิกอินโฟชี้แจงคณิตศาสตร์ความคุ้มค่า เปรียบเทียบส่วนลด GP ระบบออนไลน์ที่ทีมงานเอามาเปลี่ยนเป็นส่วนลดหน้างานให้ผู้ซื้อ</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> ENG obj ฿1,500/วัน ใส่โพสต์สคริปต์ยาว / คลิปหลักสารภาพ CEO | <b>จิตวิทยา:</b> P2 Pratfall, P3 Reason-Why
                </div>
            </div>"""

replacement_dark = """            <!-- D-9 EP.2 -->
            <div class="card reach">
                <div class="step-num">02</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-9 — EP.2</span>
                        <h2>ชาเลนจ์ท้าชนบัญชี — ทำไมต้องลด</h2>
                    </div>
                    <span class="badge reach">REACH</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Vlog Challenge & Zero-GP Math):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">บอสเคนทอล์กท้าเดิมพันกับแผนกบัญชีที่ว่าล้างสต๊อกแสนชิ้นไม่หมดใน 9 วัน หั่นราคาต่ำกว่าทุนด้วยการตัดค่า GP ออนไลน์ 30% คืนให้ลูกค้า ดึงคนมาร่วมลุยภารกิจดันโบนัสคลังสินค้า</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (Behind the Scenes):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปสัมภาษณ์พนักงานคลังและพี่หมีแอบลุ้นโบนัสและเตรียมลุยชาเลนจ์ 9 วัน สลับภาพบอสเคนกอดอกเชียร์ทีมงานแบบเป็นกันเอง</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Reason-Why Challenge Info):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">อินโฟกราฟิกท้าชนแผนกบัญชี ตีแผ่ตัวเลขเปรียบเทียบค่าธรรมเนียม GP ที่โดนหัก 30% นำมาเปลี่ยนเป็นส่วนลดให้ผู้ซื้อที่หน้างานจริง</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> ENG obj ฿1,500/วัน ใส่โพสต์สคริปต์ยาว / คลิปชาเลนจ์ท้าชนบัญชี | <b>จิตวิทยา:</b> P7 Unity, P3 Reason-Why
                </div>
            </div>"""

replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/generate_dark_pdf.py", target_dark, replacement_dark)


# 5. Update RUDEDOG_FAIR_2026_SCRIPT_10EP.html (detailed storyboard HTML in app)
target_storyboard_tag = '<div class="ep-tagline">คำสารภาพ CEO — ทำไมถึงต้องลด</div>'
replacement_storyboard_tag = '<div class="ep-tagline">ชาเลนจ์ท้าชนบัญชี — ทำไมถึงต้องลด</div>'
replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/jarvis_second_brain/uploads/Friend2/RUDEDOG_FAIR_2026_SCRIPT_10EP.html", target_storyboard_tag, replacement_storyboard_tag)

target_storyboard_psych = """      <div class="ep-psych-row">
        <span class="psych-tag">P2 Pratfall Effect</span>
        <span class="psych-tag">P1 Open Loop</span>
      </div>"""
replacement_storyboard_psych = """      <div class="ep-psych-row">
        <span class="psych-tag">P7 Unity (รวมทีม)</span>
        <span class="psych-tag">P3 Reason-Why</span>
      </div>"""
replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/jarvis_second_brain/uploads/Friend2/RUDEDOG_FAIR_2026_SCRIPT_10EP.html", target_storyboard_psych, replacement_storyboard_psych)

target_storyboard_shots = """    <div class="sb-section">
      <div class="section-label">Storyboard — 4 shots</div>
      <div class="storyboard">
        <div class="sb-frame">
          <span class="sb-time reach">0–3 วิ (HOOK)</span>
          <div class="phone-sketch"><div class="phone-screen">
            <div class="phone-screen-icon">😬</div>
            <div class="phone-screen-desc">บอสนั่งกลางออฟฟิศ<br>หน้าเครียด<br>ถือกระดาษ</div>
          </div></div>
          <div class="sb-caption">นั่งที่โต๊ะทำงานจริง ไม่ต้องจัดฉาก</div>
        </div>
        <div class="sb-frame">
          <span class="sb-time reach">3–15 วิ</span>
          <div class="phone-sketch"><div class="phone-screen">
            <div class="phone-screen-icon">📄</div>
            <div class="phone-screen-desc">ชูใบสั่งซื้อจริง<br>กล้องซูมเห็น<br>ตัวเลข</div>
          </div></div>
          <div class="sb-caption">ใบ PO จริง = ความน่าเชื่อถือ 100%</div>
        </div>
        <div class="sb-frame">
          <span class="sb-time reach">15–45 วิ</span>
          <div class="phone-sketch"><div class="phone-screen">
            <div class="phone-screen-icon">🗣️</div>
            <div class="phone-screen-desc">บอสอธิบาย<br>ตรงกล้อง<br>ยอมรับความผิดพลาด</div>
          </div></div>
          <div class="sb-caption">ยิ่งพูดตรงยิ่งดี อย่า polish</div>
        </div>
        <div class="sb-frame">
          <span class="sb-time reach">45–58 วิ</span>
          <div class="phone-sketch"><div class="phone-screen">
            <div class="phone-screen-icon">💰</div>
            <div class="phone-screen-desc">บอสยิ้มเศร้าๆ<br>"ความซวยของผม<br>= ส่วนลดของคุณ"</div>
          </div></div>
          <div class="sb-caption">จบด้วย line นี้แล้วตัดทันที</div>
        </div>
      </div>
    </div>"""

replacement_storyboard_shots = """    <div class="sb-section">
      <div class="section-label">Storyboard — 4 shots</div>
      <div class="storyboard">
        <div class="sb-frame">
          <span class="sb-time reach">0–3 วิ (HOOK)</span>
          <div class="phone-sketch"><div class="phone-screen">
            <div class="phone-screen-icon">📊</div>
            <div class="phone-screen-desc">บอสยืนกอดอก<br>หน้าไวท์บอร์ด<br>ท้าทาย</div>
          </div></div>
          <div class="sb-caption">ยืนหน้าชาร์ตเป้าหมายหรือเขียนกระดานดิบๆ</div>
        </div>
        <div class="sb-frame">
          <span class="sb-time reach">3–15 วิ</span>
          <div class="phone-sketch"><div class="phone-screen">
            <div class="phone-screen-icon">📄</div>
            <div class="phone-screen-desc">ชูเอกสารงบการเงิน<br>และตัวเลข GP<br>หัก 30%</div>
          </div></div>
          <div class="sb-caption">โชว์ตัวเลขค่าธรรมเนียมออนไลน์ที่โดนหัก</div>
        </div>
        <div class="sb-frame">
          <span class="sb-time reach">15–45 วิ</span>
          <div class="phone-sketch"><div class="phone-screen">
            <div class="phone-screen-icon">🗣️</div>
            <div class="phone-screen-desc">บอสอธิบาย<br>ชาเลนจ์ 9 วัน<br>ทลายสต๊อกเพื่อพนักงาน</div>
          </div></div>
          <div class="sb-caption">ท้าเดิมพันบัญชีเพื่อแจกโบนัสพนักงานคลัง</div>
        </div>
        <div class="sb-frame">
          <span class="sb-time reach">45–58 วิ</span>
          <div class="phone-sketch"><div class="phone-screen">
            <div class="phone-screen-icon">🔥</div>
            <div class="phone-screen-desc">บอสยิ้มท้าทาย<br>"ลุยภารกิจร่วมกัน<br>เคลียร์คลังให้เป็น 0"</div>
          </div></div>
          <div class="sb-caption">จบด้วยการกระตุ้นให้คนคอมเมนต์คำว่า "ลุย"</div>
        </div>
      </div>
    </div>"""
replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/jarvis_second_brain/uploads/Friend2/RUDEDOG_FAIR_2026_SCRIPT_10EP.html", target_storyboard_shots, replacement_storyboard_shots)

target_storyboard_script = """        <div class="script-block hook">
          <span class="block-label">🔴 HOOK — 3 วิแรก (ถือเอกสารขึ้นมา)</span>
"ผมทำพลาดครับ — สั่งของเกินมา และวันนี้ต้องสารภาพให้หมด"
        </div>
        <div class="script-block body">
          <span class="block-label">🎬 BODY — วินาที 4–48</span>
[ชูใบออเดอร์ให้กล้องเห็น]

"นี่คือใบสั่งซื้อจากต้นปีครับ ตอนนั้นผมคิดว่าเทรนด์จะไปทางนั้น
เลยสั่งสต๊อกรุ่น [XX] เพิ่มไว้ก่อน
คิดว่าขายออนไลน์ได้ 3 เดือน

[วางเอกสาร]

ผลคือ... ของยังอยู่ครบเลยครับ ไม่ได้ขายออกเลยสักชิ้น

[พักหายใจ]

แทนที่ผมจะเก็บไว้จนฝุ่นจับ หรือขายลด online แบบที่ต้องเสียค่า platform ไปอีก
ผมเลือกที่จะเปิดโกดัง ลดให้เจ็บจริงๆ
แล้วเอาเงินส่วนนั้นคืนให้คนที่มาถึงหน้างาน

ความผิดพลาดของผม — คือส่วนลดของคุณครับ"
        </div>
        <div class="script-block mission">
          <span class="block-label">💬 ภารกิจคอมเมนต์</span>
"เคยซื้อ RUDEDOG ครั้งแรกตอนไหนครับ?
เล่าให้ฟังหน่อย อยากรู้จริงๆ"
        </div>
        <div class="script-block close-ep">
          <span class="block-label">🔚 ปิดตอน</span>
"เหลืออีก 9 วัน... โกดังต้องว่าง 🐶

พรุ่งนี้พาดูของจริงที่เกิดขึ้นปีที่แล้ว
6,000 คนเดินเข้ามา — แล้วมันเป็นยังไง"
        </div>
      </div>
    </div>

    <div class="sb-section">
      <div class="section-label">Caption + Hashtag (TikTok)</div>
      <div class="caption-block">
        <span class="block-label">📝 Caption</span>สารภาพตรงๆ ครับ 🙏 สั่งของผิดพลาด สต๊อกล้น ทำไงได้ — เปิดโกดังลดให้เจ็บจริง

ความซวยของผม = ส่วนลดของคุณ 😅

แล้วคุณล่ะ เคยซื้อ RUDEDOG ครั้งแรกตอนไหนครับ? เล่าให้ฟังหน่อย 👇
        <div class="hashtags">
          <span class="ht">#RUDEDOGFair2026</span>
          <span class="ht">#CEOสารภาพ</span>
          <span class="ht">#โกดังต้องว่าง</span>
          <span class="ht">#นนทบุรี</span>
          <span class="ht">#ของลดราคา</span>
          <span class="ht">#เรียลมาก</span>
        </div>"""

replacement_storyboard_script = """        <div class="script-block hook">
          <span class="block-label">🔴 HOOK — 3 วิแรก (หน้าไวท์บอร์ด)</span>
"ฝ่ายบัญชีคัดค้านผมหัวชนฝาครับ... เขาบอกว่าไม่มีทางหรอกที่คนจะแห่มาช่วยเราเคลียร์เสื้อแสนชิ้นหมดโกดังบางใหญ่ได้ใน 9 วัน..."
        </div>
        <div class="script-block body">
          <span class="block-label">🎬 BODY — วินาที 4–48</span>
[ชูเอกสารงบการเงินและตัวเลขหัก GP ให้กล้องเห็น]

"ผมเลยท้าบัญชีกลับไปว่า... งั้นมาเดิมพันกัน! ผมจะหั่นราคาเสื้อยืด กางเกง หมวก ทุกรุ่นในโกดังลงลึกที่สุดต่ำกว่าทุน!

หลายคนถามว่าทำไมลดได้ขนาดนี้? 

[ชี้แจงตัวเลข GP 0%]

because we sell directly at the warehouse, saving on online GP and platform fees.

งานนี้เดิมพันด้วยความเชื่อใจครับ ถ้าพวกเราช่วยกันเคลียร์สต๊อกจนโล่งเกลี้ยงก่อน 9 วัน ผมจะจ่ายโบนัสพิเศษให้พนักงานคลังสินค้าทุกคนด้วย มาร่วมภารกิจทลายคลังกับพวกเรานะครับ"
        </div>
        <div class="script-block mission">
          <span class="block-label">💬 ภารกิจคอมเมนต์</span>
"บอสพร้อมลุยชาเลนจ์นี้กับผมไหม?
คอมเมนต์รายงานตัวคำว่า 'ลุย' ใต้คลิปนี้ด่วนเลยครับ"
        </div>
        <div class="script-block close-ep">
          <span class="block-label">🔚 ปิดตอน</span>
"เหลืออีก 9 วัน... โกดังต้องว่าง 🐶

พรุ่งนี้พาดูของจริงที่เกิดขึ้นปีที่แล้ว
6,000 คนเดินเข้ามา — แล้วมันเป็นยังไง"
        </div>
      </div>
    </div>

    <div class="sb-section">
      <div class="section-label">Caption + Hashtag (TikTok)</div>
      <div class="caption-block">
        <span class="block-label">📝 Caption</span>บัญชีท้ามา... บอสเคนท้ากลับ! ชาเลนจ์ทลายโกดังใน 9 วัน! 💥🐶

เมื่อฝ่ายการเงินบอกว่า "ไม่มีทางล้างสต๊อกสินค้าหลักแสนชิ้นหมดใน 9 วันที่โกดังบางใหญ่ได้หรอก"
บอสเคนเลยจัดชาเลนจ์สุดบ้าพลัง: หั่นราคาสินค้าทุกรายการต่ำกว่าทุน ท้าทายบอสทุกคนให้มารวมพลังเคลียร์โกดังให้โล่งร่วมกัน!

เพราะเราขายตรงหน้าโกดัง ไม่เสียค่า GP หักเปอร์เซ็นต์ให้แอปออนไลน์ (ประหยัดไปเกือบ 30%) ไม่ต้องจ่ายค่าเช่าห้างราคาแพง ส่วนต่างทั้งหมดตรงนี้เราตัดออก แล้วเปลี่ยนเป็นราคาสุดพิเศษคืนให้คุณทันที!

👇 บอสพร้อมลุยชาเลนจ์นี้กับพวกเราไหมครับ? พิมพ์คอมเมนต์รายงานตัวคำว่า "ลุย" ใต้โพสต์นี้ด่วนเลยครับ!
        <div class="hashtags">
          <span class="ht">#RUDEDOGFair2026</span>
          <span class="ht">#ชาเลนจ์9วัน</span>
          <span class="ht">#ภารกิจโกดังต้องว่าง</span>
          <span class="ht">#ของแท้ราคาโกดัง</span>
          <span class="ht">#ลุย</span>
        </div>"""

# Wait, let's make sure the body script is in Thai instead of English
replacement_storyboard_script = replacement_storyboard_script.replace("because we sell directly at the warehouse, saving on online GP and platform fees.", 'เพราะเราขายตรงหน้าคลัง ไม่ต้องผ่านห้าง ไม่โดนหักค่า GP แอปออนไลน์เกือบ 30% ส่วนต่างตรงนี้ผมตัดทิ้งแล้วเปลี่ยนเป็นส่วนลดคืนให้บอสทุกคนแทน!')

replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/jarvis_second_brain/uploads/Friend2/RUDEDOG_FAIR_2026_SCRIPT_10EP.html", target_storyboard_script, replacement_storyboard_script)


# 6. Update RUDEDOG_FAIR_2026_WAR_ROOM.html in both campaign_files and Downloads
target_warroom = """      <div class="daytag"><div class="dleft"><span class="dnum">D-9</span><span class="dphase" style="background:var(--reach)">REACH</span></div>
        <div class="dbody"><h3><span class="ep">EP.2</span>คำสารภาพ CEO — ทำไมต้องลด</h3>
          <div style="margin-top: 10px; border-left: 3px solid var(--safety); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--safety);">1. คอนเทนต์หลัก (CEO Confession Video):</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">บอสเคนทอล์กสารภาพตรงๆ เรื่องสั่งผ้าล้นคลังจนสต๊อกเกิน (Pratfall Effect) ลดแหลกเพราะหน้างานขายตรงไม่เสียค่า GP 30% ให้แอปออนไลน์ ชวนคอมเมนต์เสื้อรู้ดด็อกตัวแรก</div>
          </div>
          <div style="margin-top: 8px; border-left: 3px solid var(--believe); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--believe);">2. คอนเทนต์ย่อย (Behind the Scenes):</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">คลิปสั้นสัมภาษณ์คนงานบ่นเหนื่อยเพราะเสื้อล้นโกดัง ตัดสลับภาพบอสเคนทำหน้าตึงและสั่งหั่นราคาระบายของด่วน</div>
          </div>
          <div style="margin-top: 8px; border-left: 3px solid var(--move); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--move);">3. คอนเทนต์มีม/รูปภาพ (Reason-Why Info):</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">กราฟิกอินโฟชี้แจงคณิตศาสตร์ความคุ้มค่า เปรียบเทียบส่วนลด GP ระบบออนไลน์ที่ทีมงานเอามาเปลี่ยนเป็นส่วนลดหน้างานให้ผู้ซื้อ</div>
          </div>
          <div class="drow"><span class="lbl">การยิงโฆษณา</span><span>ENG obj ฿1,500/วัน ใส่โพสต์สคริปต์ยาว / คลิปหลักสารภาพ CEO</span></div>
          <div class="ptags"><span class="ptag">P2 Pratfall</span><span class="ptag">P3 Reason-Why</span></div>
        </div></div>"""

replacement_warroom = """      <div class="daytag"><div class="dleft"><span class="dnum">D-9</span><span class="dphase" style="background:var(--reach)">REACH</span></div>
        <div class="dbody"><h3><span class="ep">EP.2</span>ชาเลนจ์ท้าชนบัญชี — ทำไมต้องลด</h3>
          <div style="margin-top: 10px; border-left: 3px solid var(--safety); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--safety);">1. คอนเทนต์หลัก (Vlog Challenge & Zero-GP Math):</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">บอสเคนทอล์กท้าเดิมพันกับแผนกบัญชีที่ว่าล้างสต๊อกแสนชิ้นไม่หมดใน 9 วัน หั่นราคาต่ำกว่าทุนด้วยการตัดค่า GP ออนไลน์ 30% คืนให้ลูกค้า ดึงคนมาร่วมลุยภารกิจดันโบนัสคลังสินค้า</div>
          </div>
          <div style="margin-top: 8px; border-left: 3px solid var(--believe); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--believe);">2. คอนเทนต์ย่อย (Behind the Scenes):</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">คลิปสัมภาษณ์พนักงานคลังและพี่หมีแอบลุ้นโบนัสและเตรียมลุยชาเลนจ์ 9 วัน สลับภาพบอสเคนกอดอกเชียร์ทีมงานแบบเป็นกันเอง</div>
          </div>
          <div style="margin-top: 8px; border-left: 3px solid var(--move); padding-left: 12px; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--move);">3. คอนเทนต์มีม/รูปภาพ (Reason-Why Challenge Info):</div>
            <div style="font-size: 0.82rem; color: #3a3a36; line-height: 1.45;">อินโฟกราฟิกท้าชนแผนกบัญชี ตีแผ่ตัวเลขเปรียบเทียบค่าธรรมเนียม GP ที่โดนหัก 30% นำมาเปลี่ยนเป็นส่วนลดให้ผู้ซื้อที่หน้างานจริง</div>
          </div>
          <div class="drow"><span class="lbl">การยิงโฆษณา</span><span>ENG obj ฿1,500/วัน ใส่โพสต์สคริปต์ยาว / คลิปชาเลนจ์ท้าชนบัญชี</span></div>
          <div class="ptags"><span class="ptag">P7 Unity</span><span class="ptag">P3 Reason-Why</span></div>
        </div></div>"""

replace_in_file("/Users/apple/.gemini/antigravity-ide/scratch/campaign_files/RUDEDOG_FAIR_2026_WAR_ROOM.html", target_warroom, replacement_warroom)
replace_in_file("/Users/apple/Downloads/RUDEDOG_FAIR_2026_WAR_ROOM.html", target_warroom, replacement_warroom)

print("Update script completed successfully!")
