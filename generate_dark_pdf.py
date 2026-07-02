import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RUDEDOG FAIR 2026 — WAR ROOM: 10-Day Strategy</title>
<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;700;800&family=IBM+Plex+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
    :root {
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
    }
    
    * {
        box-sizing: border-box;
    }
    
    body { 
        font-family: 'Kanit', sans-serif; 
        background-color: var(--bg); 
        color: var(--text); 
        margin: 0; 
        padding: 40px 30px;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    
    .container { 
        max-width: 900px; 
        margin: 0 auto; 
    }
    
    .header {
        text-align: left;
        margin-bottom: 40px;
        border-left: 8px solid var(--secondary);
        padding-left: 25px;
        page-break-inside: avoid;
    }
    
    h1 { 
        font-size: 38px; 
        margin: 0; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--text);
        font-weight: 800;
    }
    
    .subtitle { 
        color: var(--primary); 
        font-size: 18px; 
        font-weight: 400;
        margin-top: 5px;
        letter-spacing: 0.05em;
    }
    
    .meta-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-top: 25px;
        page-break-inside: avoid;
    }

    .meta-item {
        background: var(--card-bg);
        border: 1px solid var(--border);
        padding: 12px 18px;
        border-radius: 12px;
    }

    .meta-item b {
        display: block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.15rem;
        color: var(--primary);
    }

    .meta-item span {
        font-size: 0.75rem;
        color: var(--text-dim);
    }
    
    .card-list {
        display: flex;
        flex-direction: column;
        gap: 30px;
        margin-top: 35px;
    }
    
    .card { 
        background: var(--card-bg); 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
        page-break-inside: avoid;
    }

    .card.reach { border-left: 6px solid var(--reach); }
    .card.believe { border-left: 6px solid var(--believe); }
    .card.move { border-left: 6px solid var(--move); }
    
    .step-num {
        position: absolute;
        top: -10px;
        right: 15px;
        font-size: 70px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.035);
        font-family: 'IBM Plex Mono', monospace;
        user-select: none;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 12px;
        margin-bottom: 18px;
    }

    .ep-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        color: var(--text-dim);
        font-weight: 500;
    }

    .card h2 {
        margin: 4px 0 0 0;
        font-size: 1.25rem;
        color: var(--text);
        font-weight: 700;
    }
    
    .badge {
        color: white;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge.reach { background: var(--secondary); }
    .badge.believe { background: var(--primary); }
    .badge.move { background: var(--success); color: #0a0a0f; }

    .section-title {
        font-size: 0.85rem;
        color: var(--primary);
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 16px;
        margin-bottom: 6px;
        letter-spacing: 0.05em;
    }

    .script-box {
        font-size: 0.82rem;
        line-height: 1.5;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 12px 15px;
        border-radius: 10px;
        color: #e2e2e8;
    }

    .highlight-box {
        background: linear-gradient(90deg, rgba(255,0,80,0.08) 0%, rgba(0,242,254,0.08) 100%);
        padding: 25px;
        border-radius: 24px;
        border: 1px dashed var(--primary);
        margin-top: 35px;
        page-break-inside: avoid;
    }
    
    .highlight-box h3 {
        margin-top: 0;
        color: var(--text);
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.1rem;
    }
    .highlight-box p {
        color: var(--text-dim);
        font-size: 0.85rem;
        line-height: 1.6;
        margin: 0;
    }
    
    .footer {
        text-align: center;
        margin-top: 50px;
        color: var(--text-dim);
        font-size: 13px;
        font-family: 'IBM Plex Mono', monospace;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 20px;
    }

    @media print {
        body {
            background-color: #0a0a0f !important;
            color: #ffffff !important;
        }
        .card {
            background-color: #16161e !important;
            border-color: #2a2a35 !important;
        }
        .script-box {
            background-color: rgba(255, 255, 255, 0.02) !important;
        }
        .highlight-box {
            background: linear-gradient(90deg, rgba(255,0,80,0.08) 0%, rgba(0,242,254,0.08) 100%) !important;
        }
    }
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
            
            <!-- D-10 EP.1 -->
            <div class="card reach">
                <div class="step-num">01</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-10 — EP.1</span>
                        <h2>ประกาศ: "โกดังจะแตกแล้วครับ"</h2>
                    </div>
                    <span class="badge reach">REACH</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Reality Talk Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">บอสเคนทอล์กเตือนภัยรถติดย่านนนทบุรี บางใหญ่ บางบัวทอง จากแคมเปญล้างสต๊อกลุยหั่นครึ่งราคา ชวนพิมพ์คอมเมนต์ "ไปแน่" เพื่อสะสม Social Proof และบูสต์ Algorithm</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (TikTok Fast Hook):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปสั้น 15 วิ แพนฟุตเทจคลังสินค้าถล่มล้นโกดัง พร้อมแคปชันนับถอยหลัง 10 วันด่วนๆ เร้าความสนใจอย่างรวดเร็ว</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Interactive Graphic):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">ภาพแบนเนอร์บอสเคนประกาศเตือนรถติดอย่างเป็นทางการ ชวนแท็กเพื่อนซี้ในคอมเมนต์เพื่อชิงสิทธิ์เข้าช้อปกลุ่มแรก</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> REACH obj ฿2,500/วัน (Boost ทันที 20:00 หลังโพสต์ 3 ชม. หาก ThruPlay >= 25%) | <b>จิตวิทยา:</b> P1 Open Loop, P7 Unity
                </div>
            </div>

            <!-- D-9 EP.2 -->
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
            </div>

            <!-- D-8 EP.3 -->
            <div class="card reach">
                <div class="step-num">03</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-8 — EP.3</span>
                        <h2>หลักฐานปีที่แล้ว — footage 6,000 คน</h2>
                    </div>
                    <span class="badge reach">REACH</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Footage Compilation):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">วิดีโอตัดฟุตเทจงานปีก่อนแถวยาวลานจอดรถแตก เตือนไซส์ M และ L สีฮิตหมดไวมากตั้งแต่เที่ยงวันแรก ชวนแท็กเพื่อนซี้ที่ปีที่แล้วพลาดงานนี้ไปด่วน</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (TikTok Customer Review):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปสอยรีวิวและสัมภาษณ์ความประทับใจลูกค้าเก่าที่ต่อแถวงานแฟร์ปีก่อน การันตีของฮิตไปไวจริง กระตุ้น Loss Aversion</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Grid Photo Album):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">โพสต์อัลบั้มภาพฝูงชนปีก่อนและภาพบรรยากาศลานจอดรถ เพื่อดึงคุณค่าทางสังคม (Social Proof) แบบ Organic</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> REACH obj ฿3,000/วัน (ตัวเปิดหลักกลุ่มเย็นชาเพื่อปูทางคนเข้างาน) | <b>จิตวิทยา:</b> P4 Social Proof, P5 Loss Aversion
                </div>
            </div>

            <!-- D-7 EP.4 -->
            <div class="card reach">
                <div class="step-num">04</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-7 — EP.4</span>
                        <h2>Myth Busting — "ของลด = ของโละ?"</h2>
                    </div>
                    <span class="badge reach">REACH</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Quality Verification Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">บอสเคนหยิบเสื้อลายฮิตมาดึงโชว์ความเหนียวแน่นของใยผ้า AeroTwill ยืนยันเกรด A+ ช็อปเดียวกับบนห้าง ชวนพิมพ์ถามข้อกังขา บอสตอบเองทุกคอมเมนต์</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (TikTok Fast QA):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปสั้นตอบด่วนประเด็นตำหนิ/ย้อมแมว นำเสนอแบบจริงใจ กระตุ้นความน่าเชื่อถือจากเหตุผลที่ลด (Reason-Why)</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Fuzzy Comparison):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">ภาพกราฟิกเปรียบเทียบผ้า AeroTwill ของแท้ปะทะเกรดเสื้อโละทั่วไป ชี้จุดต่างใยผ้าให้คน 30+ เห็นชัดๆ</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> ENG obj ฿2,000/วัน (เน้นเซฟ/แชร์เป็นคอนเทนต์อ้างอิงความเชื่อมั่น) | <b>จิตวิทยา:</b> P3 Reason-Why, P2 Pratfall
                </div>
            </div>

            <!-- D-6 EP.5 -->
            <div class="card believe">
                <div class="step-num">05</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-6 — EP.5</span>
                        <h2>พาเดินดูของ + เปิดราคาจริง</h2>
                    </div>
                    <span class="badge believe">BELIEVE</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Warehouse Tour Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">บอสเคนถือไฟฉายย่องพาทัวร์กล่องสต๊อก แอบแกะสปอยล์ราคาเสื้อยืดและกางเกงชิโน่ (ใส่เสียงเซนเซอร์บี๊บ) ชวนทายราคาเสื้อลุ้นสิทธิ์หน้างาน</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (TikTok Fast Spoil):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปแพนกล่องและราวเสื้อผ้าสเปเชียลแบบไวๆ 15 วินาที ดึงอารมณ์ความคุ้มค่าและความจำกัดของสต๊อกล่วงหน้า</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Price List Teaser):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">แบนเนอร์ตารางสรุปราคาสินค้ากลุ่ม Hero Items คัดเน้นๆ โชว์ส่วนต่างราคาห้างปะทะราคาล้างคลัง</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> เริ่มชั้น Retargeting ยิงใส่คนดูวิดีโอย้อนหลัง >= 50% + Engage เพจ ฿1,500/วัน | <b>จิตวิทยา:</b> P5 Scarcity, P6 Commitment
                </div>
            </div>

            <!-- D-5 EP.6 -->
            <div class="card believe">
                <div class="step-num">06</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-5 — EP.6</span>
                        <h2>เสื้อตัวเดียว ชีวิต 30+ ทั้งใบ</h2>
                    </div>
                    <span class="badge believe">BELIEVE</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Lifestyle Insight Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">เรื่องเล่าวิถีผู้ชาย 30+ ไม่ต้องคิดเยอะ เสื้อรู้ดด็อกตัวเดียวตอบโจทย์ใส่คุ้มทั้งวัน ทนทาน ซักง่ายไม่หดย้วย ชวนส่งต่อชวนเพื่อนเปลี่ยนตู้</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (TikTok POV POV):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิป POV คุณแฟนแกล้งแฟนหนุ่มที่ชอบใส่เสื้อรู้ดด็อกตัวเก่าลายคลาสสิกซ้ำๆ แซวชวนจูงมือมาซื้อเหมาเซ็ตใหม่ที่งานแฟร์</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ ( lifestyle Album):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">โพสต์อัลบั้มภาพถ่ายนายแบบคนทำงานใส่เสื้อยืดสีพื้นแนวเรียบหรู คลาสสิก เหมาะกับครอบครัวและพ่อบ้านยุคใหม่</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> ENG ฿2,000 + RT ฿1,500/วัน (เป้าหมาย LINE Adds สะสมต้องแตะ 1,200 คนวันรุ่งขึ้น) | <b>จิตวิทยา:</b> P7 Unity, P6 Commitment
                </div>
            </div>

            <!-- D-4 EP.7 -->
            <div class="card believe">
                <div class="step-num">07</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-4 — EP.7</span>
                        <h2>Utility: ไปยังไง จอดตรงไหน</h2>
                    </div>
                    <span class="badge believe">BELIEVE</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Route Navigation Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คู่มือเดินทางไปโกดังบางใหญ่ แนะนำพิกัดลานจอดรถฟรี 500 คัน และสถานี MRT สามแยกบางใหญ่ ชวนคอมเมนต์ย่านพักอาศัยเพื่อส่งลิงก์นำทางให้ทางแชท</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (Quick Directions Clip):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปสั้นชี้จุดทางลัดเลี่ยงเส้นทางติดขัดรอบรัศมีปากเกร็ด/รัตนาธิเบศร์ นำเสนออย่างรวดเร็วและเป็นมิตร</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Map Infographic):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">ภาพแผนที่ลายแทงจุดจอดรถและพิกัด MRT สรุปขั้นตอนแบบรูปเดียวจบพร้อมปุ่มแอด LINE OA (เซฟและปักหมุดเพจทันที)</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> RT เป้าหมาย Traffic -> ส่งคนแอด LINE OA ฿2,000/วัน (คลิปนำทางคือตัวแปลงคนมางานดีที่สุด) | <b>จิตวิทยา:</b> P6 Commitment, P7 Unity
                </div>
            </div>

            <!-- D-3 EP.8 -->
            <div class="card believe">
                <div class="step-num">08</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-3 — EP.8</span>
                        <h2>ภูเขาสต๊อก + พี่หมีหน้าเครียด (BTS)</h2>
                    </div>
                    <span class="badge believe">BELIEVE</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Warehouse Behind Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">พาชมความยุ่งเหยียดการจัดกล่องสต๊อกของทีมแพ็ค แซว "พี่หมีคุมคลัง" ทำหน้าเครียดเพราะกลัวขายของไม่หมด ชวนเล่นเกมทายจำนวนกล่องในภูเขาสต๊อกเพื่อรับของรางวัลหน้างาน</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (TIMELAPSE Packing):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปเร่งความเร็วโชว์พนักงานเติมราวผ้าและแพ็คกล่อง แสดงถึงความพร้อมและความยิ่งใหญ่ระดับ 6,000 คนปีก่อน</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Countdown Banner 3 Days):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">แบนเนอร์นับถอยหลัง 3 วันสุดท้าย โทนสีย้อนแสง HUD นีออน สปอยล์ของรางวัลพิเศษที่จะนำมาแจกหน้าบูธ</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> Boost ฿2,500 + RT ฿2,000/วัน (ใช้เกมดึงยอดคอมเมนต์กระตุ้น Organic Reach ตามธรรมชาติ) | <b>จิตวิทยา:</b> P4 Social Proof, P1 Open Loop
                </div>
            </div>

            <!-- D-2 EP.9 -->
            <div class="card move">
                <div class="step-num">09</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-2 — EP.9</span>
                        <h2>จัดอันดับ 5 อย่างที่จะหมดก่อนเพื่อน</h2>
                    </div>
                    <span class="badge move">MOVE</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Loss Aversion Countdown Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">บอสเคนแถลงจัดอันดับ 5 สินค้าฮิตขายดีปีก่อน (กางเกงชิโน่, หมวกปักลายหมาใหญ่, เสื้อคอลเลกชันลิมิเต็ด) ชวนระบุคอมเมนต์เป้าหมายแรกที่จะวิ่งไปช้อป</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (TikTok Scarcity Warning):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปเตือนความหายากของไซส์ยอดนิยมเกลี้ยงไวใน 2 วันด่วนๆ ย้ำหมดแล้วหมดเลยไม่มีมาเพิ่ม</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Pre-Shopping Checklist):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">แผ่นอินโฟกราฟิกเช็คลิสต์เตรียมความพร้อมก่อนลุยงานวันเปิดคลังวันพรุ่งนี้ (ตารางไซส์เสื้อยืดและราคาหั่นลดคีย์บอร์ดสั่น)</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> RT อัดแน่นใส่ผู้มุ่งหวังทั้งหมด ฿3,500/วัน (ความถี่สูงได้เนื่องจากเหลือเวลา 2 วันสุดท้าย) | <b>จิตวิทยา:</b> P5 Loss Aversion, P8 Goal Gradient
                </div>
            </div>

            <!-- D-1 EP.10 -->
            <div class="card move">
                <div class="step-num">10</div>
                <div class="card-header">
                    <div>
                        <span class="ep-label">DAY D-1 — EP.10</span>
                        <h2>Final Call + ทิ้งเซอร์ไพรส์ปิดงาน</h2>
                    </div>
                    <span class="badge move">MOVE</span>
                </div>
                
                <div style="margin-top: 12px; border-left: 3px solid var(--secondary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--secondary);">1. คอนเทนต์หลัก (Final Sweep Video):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">แถลงการณ์โค้งสุดท้าย ทิ้งปริศนารางวัลสุดพิเศษเฉลยเฉพาะ 10 คนแรกหน้าลานวันเปิดประตู นัดเจอไลฟ์ 09:30 และเปิดงาน 10:00 พรุ่งนี้เช้า</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--primary); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary);">2. คอนเทนต์ย่อย (TikTok Setup Tour):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">คลิปสปอยล์แสงสีความพร้อมและพาทัวร์ตู้ลอยรอบคลังคืนสุดท้าย ชวนกดเปิดกระดิ่งแจ้งเตือนไลฟ์เช้า</div>
                </div>
                <div style="margin-top: 10px; border-left: 3px solid var(--success); padding-left: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--success);">3. คอนเทนต์มีม/รูปภาพ (Countdown 24 Hours):</div>
                    <div style="font-size: 0.82rem; color: var(--text-dim); line-height: 1.45; margin-top: 3px;">ภาพกราฟิกนับถอยหลัง 24 ชม. สุดท้ายคุมโทนนีออน ชวนคอมเมนต์อีโมจิไฟลุก "🔥" เพื่อรายงานตัว</div>
                </div>
                <div class="section-title">ฝ่ายยุทธวิธีและงบประมาณ</div>
                <div class="script-box" style="font-size:0.78rem;">
                    <b>งบโฆษณา:</b> RT ฿3,500 + REACH รัศมีแคบ 10 กม. รอบโกดังแบบถี่ยิบ ดึงคนออกจากบ้านจริง | <b>จิตวิทยา:</b> P1 Open Loop, P8 Goal Gradient
                </div>
            </div>

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
html_path = "/Users/apple/.gemini/antigravity-ide/scratch/rudedog_fair_pdf_temp.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Run Headless Chrome to print to PDF
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
pdf_path = "/Users/apple/Desktop/rudedog_fair_10days_content.pdf"

command = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    html_path
]

try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"PDF successfully compiled via headless Chrome at: {pdf_path}")
    # Remove temporary HTML
    if os.path.exists(html_path):
        os.remove(html_path)
except subprocess.CalledProcessError as e:
    print(f"Error compiling PDF: {e}")
    print(f"Stderr: {e.stderr.decode('utf-8')}")
