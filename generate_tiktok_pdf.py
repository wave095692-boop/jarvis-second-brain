import os
import subprocess

html_temp_path = "/Users/apple/.gemini/antigravity-ide/scratch/tiktok_farming_temp.html"
pdf_path = "/Users/apple/Desktop/tiktok_farming_guide.pdf"

html_content = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TIKTOK ACCOUNT FARMING GUIDE</title>
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;700;800&family=IBM+Plex+Mono:wght@400;600;700&family=Anuphan:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0b10;
            --card-bg: #11131c;
            --border: #1f2335;
            --text-primary: #c0caf5;
            --text-dim: #787c99;
            --primary: #00ffcc;
            --secondary: #ff0050;
            --yellow: #ff9e64;
            --blue: #7aa2f7;
            --dark: #000;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Anuphan', sans-serif;
            background-color: var(--bg);
            color: var(--text-primary);
            margin: 0;
            padding: 40px;
            -webkit-print-color-adjust: exact;
            line-height: 1.6;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        .header {
            border-bottom: 4px solid var(--primary);
            padding-bottom: 25px;
            margin-bottom: 35px;
            position: relative;
        }

        .header::after {
            content: "SECURE AUTOMATION LAB";
            position: absolute;
            bottom: -15px;
            right: 0;
            background: var(--secondary);
            color: #fff;
            font-family: 'IBM Plex Mono';
            font-size: 0.65rem;
            padding: 2px 8px;
            font-weight: 700;
            letter-spacing: 0.1em;
        }

        .eyebrow {
            display: inline-block;
            background: var(--primary);
            color: var(--dark);
            font-family: 'Kanit';
            font-weight: 800;
            font-size: 0.75rem;
            padding: 4px 12px;
            letter-spacing: 0.1em;
            margin-bottom: 15px;
            border-radius: 2px;
            text-transform: uppercase;
        }

        h1 {
            font-family: 'Kanit';
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0 0 10px 0;
            line-height: 1.1;
            color: #fff;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
        }

        .sub {
            font-size: 0.95rem;
            color: var(--text-dim);
            margin: 0;
            line-height: 1.5;
        }

        .meta-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 25px;
        }

        .meta-item {
            border: 1px solid var(--border);
            padding: 12px 18px;
            background: var(--card-bg);
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }

        .meta-item b {
            display: block;
            font-family: 'IBM Plex Mono';
            font-size: 1.1rem;
            color: var(--primary);
        }

        .meta-item span {
            font-size: 0.75rem;
            color: var(--text-dim);
            font-weight: 500;
        }

        h2 {
            font-family: 'Kanit';
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
            margin-top: 40px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        h3 {
            font-family: 'Kanit';
            font-size: 1.15rem;
            font-weight: 600;
            color: #fff;
            margin-top: 25px;
            margin-bottom: 12px;
        }

        p {
            margin-top: 0;
            margin-bottom: 15px;
            color: var(--text-primary);
        }

        /* Styling lists */
        ul {
            margin-top: 0;
            margin-bottom: 20px;
            padding-left: 20px;
        }

        li {
            margin-bottom: 8px;
            color: var(--text-primary);
        }

        li strong {
            color: #fff;
        }

        /* Cyberpunk styling cards */
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-left: 5px solid var(--primary);
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 4px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            page-break-inside: avoid;
        }

        .card.danger {
            border-left-color: var(--secondary);
        }

        .card.warning {
            border-left-color: var(--yellow);
        }

        .card.info {
            border-left-color: var(--blue);
        }

        .card-title {
            font-family: 'Kanit';
            font-weight: 700;
            font-size: 1.05rem;
            color: #fff;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Table design */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 4px;
            overflow: hidden;
        }

        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            background-color: rgba(0, 255, 204, 0.05);
            font-family: 'Kanit';
            font-weight: 700;
            color: var(--primary);
            font-size: 0.9rem;
        }

        td {
            font-size: 0.85rem;
            color: var(--text-primary);
        }

        td strong {
            color: #fff;
        }

        tr:last-child td {
            border-bottom: none;
        }

        .badge-step {
            display: inline-block;
            background: rgba(255, 0, 80, 0.15);
            color: var(--secondary);
            font-family: 'IBM Plex Mono';
            font-weight: 700;
            font-size: 0.75rem;
            padding: 2px 6px;
            border-radius: 3px;
            border: 1px solid rgba(255, 0, 80, 0.3);
            margin-right: 8px;
        }

        .footer {
            margin-top: 60px;
            border-top: 1px solid var(--border);
            padding-top: 20px;
            text-align: center;
            font-family: 'IBM Plex Mono';
            font-size: 0.75rem;
            color: var(--text-dim);
            letter-spacing: 0.05em;
        }

        @media print {
            body {
                background: #fff;
                color: #000;
                padding: 20px;
            }
            .card {
                background: #f8f9fa;
                border-color: #dee2e6;
                color: #000;
            }
            h1, h2, h3, .card-title, td strong, li strong {
                color: #000;
            }
            .meta-item {
                background: #f8f9fa;
                border-color: #dee2e6;
            }
            th {
                background-color: #f1f3f5;
                color: #000;
            }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <span class="eyebrow">Jarvis Intelligence Report</span>
        <h1>คู่มือระบบฟาร์มและปั้นบัญชี TikTok</h1>
        <p class="sub">การจำลองสภาพแวดล้อม ความปลอดภัยเครือข่าย ซอฟต์แวร์ควบคุม และสูตรการเลี้ยงช่องเพื่อป้องกันสิทธิ์การมองเห็นโดนบล็อก (Shadowban) ในสเกลใหญ่</p>
        
        <div class="meta-grid">
            <div class="meta-item">
                <b>№ TT-FARM-2026</b>
                <span>รหัสรายงานความปลอดภัย</span>
            </div>
            <div class="meta-item">
                <b>3 ARCHITECTURES</b>
                <span>โครงสร้างระบบควบคุม</span>
            </div>
            <div class="meta-item">
                <b>7-DAY PROTOCOL</b>
                <span>โปรโตคอลการวอร์มอัปบัญชี</span>
            </div>
        </div>
    </div>

    <!-- Section 1 -->
    <h2>1. แนวคิดและระบบป้องกันของ TikTok</h2>
    <p>TikTok เป็นแพลตฟอร์มที่มีระบบตรวจจับบอท (Anti-Bot) และการตรวจจับพฤติกรรมผิดปกติที่เข้มงวดที่สุดในปัจจุบัน โดยมี AI คอยตรวจสอบปัจจัยต่าง ๆ เพื่อคัดกรอง "บัญชีขยะ" หรือการโกงยอดการมองเห็นดังนี้:</p>
    <ul>
        <li><strong>Device Fingerprint (ลายนิ้วมืออุปกรณ์):</strong> TikTok สามารถอ่านค่าฮาร์ดแวร์ลึกมาก เช่น รุ่นชิปเซ็ต, ระดับแบตเตอรี่, ไจโรสโคป, ความถี่ของ CPU, ฟอนต์เครื่อง และรหัสประจำเครื่อง (IMEI/UUID) หากระบบตรวจพบเครื่องเล่นจำลอง (Emulator) บนคอมพิวเตอร์ทั่วไปโดยไม่มีการตั้งค่าป้องกัน บัญชีจะถูกบล็อกการมองเห็นทันที</li>
        <li><strong>IP Reputation & Geolocation (ความน่าเชื่อถือของเน็ต):</strong> การเข้าสู่ระบบหลายบัญชีผ่าน IP เดียวกัน หรือการเปลี่ยนตำแหน่งพื้นที่อินเทอร์เน็ตไปมาในเวลาอันสั้น จะส่งสัญญาณเตือนภัยเข้าระบบความปลอดภัย</li>
        <li><strong>Behavioral Signatures (ลายนิ้วมือพฤติกรรม):</strong> บอทที่ปัดหน้าจอด้วยความเร็วสม่ำเสมอ หรือเข้าสมัครบัญชีแล้วอัปโหลดคลิปทันทีโดยไม่มีการรับชมคลิปอื่นเลย จะโดนแบนเงียบ (Shadowban) ยอดการมองเห็นจะเป็น 0 วิวถาวร</li>
    </ul>

    <!-- Section 2 -->
    <h2>2. สถาปัตยกรรมระบบฟาร์ม (3 Farming Models)</h2>
    
    <div class="card info">
        <div class="card-title">📱 โมเดล A: Hardware Phone Farm (ดีที่สุดและปลอดภัยสูงสุด)</div>
        <p>การใช้โทรศัพท์มือถือแอนดรอยด์จริง (สเปคราคาประหยัด เช่น Xiaomi, Samsung หรือมือสอง) โดยทำการเชื่อมต่อสาย USB เข้ากับคอมพิวเตอร์เพื่อคุมกลุ่มระบบ</p>
        <ul>
            <li><strong>ซอฟต์แวร์ควบคุมหลัก:</strong> **TikMatrix** หรือ **TikControl** หรือโปรแกรมควบคุมจอคอมพิวเตอร์อย่าง **Total Control** / **Scrcpy**</li>
            <li><strong>ขั้นตอนการทำ:</strong> เสียบโทรศัพท์เข้ากับ USB Hub คุณภาพสูง รันสคริปต์ส่งสัญญาณสัมผัสจากคอมพิวเตอร์เพื่อคุมจอพร้อมกัน 20-100 เครื่อง ทำให้มีอัตราความสำเร็จสูงเนื่องจากเป็นการทำงานบนฮาร์ดแวร์แท้ 100%</li>
        </ul>
    </div>

    <div class="card warning">
        <div class="card-title">💻 โมเดล B: Anti-Detect Browsers (จำลองหน้าเว็บ - ดีสำหรับงาน Affiliate)</div>
        <p>การใช้โปรแกรมจำลองเบราว์เซอร์ลบลายนิ้วมือฮาร์ดแวร์เพื่อล็อกอินใช้งานผ่านเว็บบนคอมพิวเตอร์ เหมาะสำหรับระบบขายของ พันธมิตร (TikTok Shop Affiliate)</p>
        <ul>
            <li><strong>ซอฟต์แวร์ควบคุมหลัก:</strong> **AdsPower**, **Multilogin**, **Dolphin{anty}**, หรือ **GoLogin**</li>
            <li><strong>ขั้นตอนการทำ:</strong> สร้างโปรไฟล์แยกจากกันอย่างเด็ดขาด โดยแต่ละโปรไฟล์จะปลอมแปลงระบบ WebGL, Canvas, ลิสต์ฟอนต์ และ WebRTC ไม่ให้ชนกัน แล้วใช้ระบบควบคุมอัตโนมัติ (เช่น RPA ใน AdsPower) เพื่อสั่งงาน</li>
        </ul>
    </div>

    <div class="card danger">
        <div class="card-title">☁️ โมเดล C: Cloud Android Emulator (สำหรับระบบเสมือนที่ต้องการสเกลด่วน)</div>
        <p>การเช่าบริการโทรศัพท์มือถือระบบคลาวด์จากเซิร์ฟเวอร์ภายนอกเพื่อติดตั้งแอปพลิเคชันและรันบอท</p>
        <ul>
            <li><strong>ซอฟต์แวร์ควบคุมหลัก:</strong> **VMOS Cloud**, **Redfinger**, หรือ **LDCloud**</li>
            <li><strong>ขั้นตอนการทำ:</strong> สั่งเช่าเครื่องโทรศัพท์จำลอง Android OS เสมือน จากนั้นเขียนบอทสคริปต์สั่งรันในเครื่องคลาวด์ ข้อดีคือไม่ต้องซื้อเครื่องจริงและเปิดระบบทิ้งไว้ได้ตลอด 24 ชั่วโมง แต่มีโอกาสโดนบล็อกสูงที่สุด</li>
        </ul>
    </div>

    <!-- Section 3 -->
    <h2>3. ระบบเครือข่าย & พร็อกซี (Network Setups)</h2>
    <p>พร็อกซี (Proxy) คือหัวใจสำคัญของการป้องกันบัญชีโดนแบน หากเลือกใช้ผิดประเภท ระบบจะคัดกรองทิ้งทันที:</p>
    <ul>
        <li><strong>4G/5G Mobile Proxies (เน็ตมือถือ - แนะนำสูงสุด):</strong> การต่อพ่วง 4G Dongle หรือใช้โทรศัพท์แชร์เน็ตมือถือจริง เนื่องจากไอพีของเน็ตมือถือจะสลับสับเปลี่ยนไปเรื่อย ๆ ทำให้ระบบของ TikTok แยกแยะไม่ออกระหว่างบอทกับทราฟฟิกของผู้ใช้จริง</li>
        <li><strong>Residential Proxies (พร็อกซีไอพีบ้าน):</strong> พร็อกซีที่ซื้อผ่านผู้ให้บริการเพื่อชี้เป้าหมายว่าเป็นไอพีของบ้านเรือนทั่วไป มีความน่าเชื่อถือสูงกว่าดาต้าเซ็นเตอร์ (Datacenter) บริการที่นิยมเช่น **Proxy-Seller**, **IPRoyal**, **Bright Data**</li>
        <li><strong>กฎเหล็กความปลอดภัย:</strong> ห้ามใช้ไอพีสาธารณะ หรือพร็อกซีของดาต้าเซ็นเตอร์ราคาถูก (Datacenter Proxy) เด็ดขาดเนื่องจากมักจะโดน TikTok ขึ้นบัญชีดำไว้แล้ว</li>
    </ul>

    <!-- Section 4 -->
    <h2>4. โปรโตคอลการเลี้ยงบัญชี 7 วัน (7-Day Warmup Protocol)</h2>
    <p>เพื่อทำให้บัญชีมี "ความประพฤติเหมือนมนุษย์จริง" ก่อนการเริ่มอัปโหลดคลิปหรือขายสินค้า ต้องทำตามโปรโตคอลนี้อย่างเคร่งครัด:</p>
    
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">ช่วงเวลา</th>
                <th style="width: 40%;">กิจกรรมการเลี้ยงบัญชี (Warmup Process)</th>
                <th style="width: 45%;">คำอธิบายความปลอดภัย</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>วันแรก (Day 1)</strong></td>
                <td>สมัครบัญชีด้วยซิมการ์ดจริงหรืออีเมลสะอาด (เลี่ยงบริการรับ SMS เบอร์จำลอง) กรอกรายละเอียดข้อมูลส่วนตัวและรูปโปรไฟล์อย่างพอประมาณ ทิ้งเครื่องไว้อย่างน้อย 24 ชั่วโมงโดยห้ามทำอะไร</td>
                <td>ป้องกันไม่ให้ระบบตรวจจับสัญญานการปั๊มสมัครบัญชีทันที (Mass Registration)</td>
            </tr>
            <tr>
                <td><strong>วันที 2-3</strong></td>
                <td>เข้าปัดหน้าฟีด (FYP) สุ่มรับชมคลิปทั่วไปรวม 15-20 นาทีต่อวัน ดูคลิปให้จบครบความยาว (ห้ามรีบปัดทิ้ง) กดหัวใจหรือคอมเมนต์ให้คลิปอย่างเป็นธรรมชาติเพียง 2-3 ครั้งเท่านั้น</td>
                <td>เป็นการสะสมประวัติพฤติกรรม (User Interaction History) ให้กับประวัติของเบราว์เซอร์หรือเครื่อง</td>
            </tr>
            <tr>
                <td><strong>วันที 4-5</strong></td>
                <td>เริ่มค้นหาคำสำคัญ (Keywords) ในกลุ่มเป้าหมายที่จะปั้นช่อง (Niche) เช่น เรื่องหมา/แมว แฟชั่น หรือไอที แล้วดูคลิปกลุ่มนั้นจนจบ กดติดตามช่องคู่แข่งระดับท็อป 2-3 ช่อง</td>
                <td>เพื่อให้ระบบแนะนำเนื้อหา (Recommendation Engine) เริ่มติดฉลากหมวดหมู่ให้กับช่องของคุณ (Niche Categorization)</td>
            </tr>
            <tr>
                <td><strong>วันที 6</strong></td>
                <td>เข้ามาร่วมกิจกรรมทั่วไป กดแชร์คลิป หรือทดลองกดใช้แผ่นเสียงยอดฮิตเก็บไว้ในรายการโปรด</td>
                <td>เพิ่มความน่าเชื่อถือและความลึกของกิจกรรมบัญชีในฐานข้อมูลความปลอดภัยของ TikTok</td>
            </tr>
            <tr>
                <td><strong>วันที 7</strong></td>
                <td>อัปโหลดวิดีโอคลิปทดสอบแรก ความยาว 10-15 วินาที โดยไม่ใส่แฮชแท็กเยอะจนเกินไป จากนั้นปล่อยทิ้งไว้และเช็คยอดการเข้าชมหลัง 24 ชั่วโมง</td>
                <td><strong>การประเมินผล:</strong> ยอดวิว 200+ = บัญชีปกติปลอดภัย / ยอดวิว 0 วิว = ติดเงา Shadowban (ต้องล้างเครื่องและเริ่มปั้นใหม่)</td>
            </tr>
        </tbody>
    </table>

    <!-- Section 5 -->
    <h2>5. การทำเนื้อหาและป้องกันการบล็อกวิดีโอซ้ำ (Bulk Content & Anti-Duplication)</h2>
    <p>การอัปโหลดคลิปที่ดาวน์โหลดซ้ำจากช่องอื่นจะทำให้ช่องถูกจับได้ทันทีและจะไม่มีการส่งไปหน้าฟีด (0 วิวถาวร) โปรแกรมและเทคนิคที่ใช้ในระบบอัตโนมัติประกอบด้วย:</p>
    <ul>
        <li><strong>ล้างค่า Metadata ลึกด้วย Script:</strong> การลบรหัส EXIF และข้อมูลกล้องของวิดีโอดั้งเดิมเพื่อทำลายลายนิ้วมือดิจิทัลของไฟล์</li>
        <li><strong>การแก้ไขวิดีโอด้วยเทคนิคข้าม AI:</strong>
            <ul>
                <li>สลับด้านซ้ายขวาของวิดีโอ (Mirror)</li>
                <li>เร่งหรือลดความเร็วในการเล่นเพียงเล็กน้อย (Speed adjustment 1-2%)</li>
                <li>ปรับโทนสีแสง (Color grading) และทำการครอปขอบวิดีโอออก 1-3% (Crop/Zoom)</li>
            </ul>
        </li>
        <li><strong>โปรแกรมตัดต่ออัตโนมัติ:</strong> การใช้เฟรมเวิร์กอย่าง <strong>ffmpeg</strong> หรือ **Python MoviePy** เขียนโปรแกรมสุ่มเปลี่ยนค่าสีและสลับเฟรม หรือการเรนเดอร์สเกลใหญ่ผ่าน **CapCut Bulk Rendering**</li>
    </ul>

    <!-- Section 6 -->
    <h2>6. สรุปรายการซอฟต์แวร์หลักที่ต้องติดตั้ง (Software Stack Summary)</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">ประเภทเครื่องมือ</th>
                <th style="width: 35%;">ชื่อซอฟต์แวร์ยอดนิยม</th>
                <th style="width: 40%;">บทบาทหน้าที่ในระบบฟาร์ม</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>ระบบจำลองอุปกรณ์ (Environment)</strong></td>
                <td>AdsPower, Multilogin, Dolphin{anty}</td>
                <td>จำลองลายนิ้วมือเว็บเบราว์เซอร์ ปลอมแปลงฮาร์ดแวร์เพื่อล็อกอินบิลด์บัญชีจำนวนมาก</td>
            </tr>
            <tr>
                <td><strong>ตัวควบคุมกลุ่ม (Group Control)</strong></td>
                <td>TikMatrix, TikControl, VMOS Cloud</td>
                <td>ควบคุมโทรศัพท์มือถือจริง หรือคลาวด์แอนดรอยด์หลายหน้าจอพร้อมกันผ่านเครื่องคอมพิวเตอร์เดียว</td>
            </tr>
            <tr>
                <td><strong>ระบบอินเทอร์เน็ต (Proxy)</strong></td>
                <td>Proxy-Seller, Smartproxy, Bright Data</td>
                <td>จัดสรรพร็อกซีประเภทบ้านเรือน (Residential) หรือเน็ตมือถือ แยกสตรีมกันในแต่ละบัญชี</td>
            </tr>
            <tr>
                <td><strong>ระบบทำงานอัตโนมัติ (Automation)</strong></td>
                <td>Python (Playwright / Appium), AdsPower RPA</td>
                <td>สั่งให้หน้าจอเลื่อนหน้าฟีด รับชมคลิป และกดปุ่มอัปโหลดเนื้อหาตามเวลาที่กำหนด</td>
            </tr>
            <tr>
                <td><strong>โปรแกรมสร้างคลิป (Content Tool)</strong></td>
                <td>ffmpeg, Python MoviePy, CapCut Bulk Render</td>
                <td>ตัดต่อคลิปวิดีโอ แก้ไขความเร็ว โทนสี เสียงพากย์ และลบค่า MetaData อัตโนมัติคราวละหลักร้อยไฟล์</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        TIKTOK FARMING ANALYSIS LAB · GENERATED BY JARVIS AT STARK WORKSPACE
    </div>
</div>

</body>
</html>
"""

with open(html_temp_path, "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
command = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    html_temp_path
]

try:
    print("กำลังเริ่มสร้างไฟล์ PDF ด้วย Google Chrome Headless...")
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"สำเร็จ! ไฟล์ PDF ถูกเขียนลงที่ตำแหน่ง: {pdf_path}")
    if os.path.exists(html_temp_path):
        os.remove(html_temp_path)
except Exception as e:
    print(f"เกิดข้อผิดพลาดในการรัน Google Chrome เพื่อสร้าง PDF: {e}")
