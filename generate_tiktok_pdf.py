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
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600;700&family=Anuphan:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0c0d14;
            --card-bg: #161925;
            --table-bg: #121420;
            --border: #1f2335;
            --text-main: #c0caf5;
            --text-dim: #787c99;
            --neon-cyan: #00ffcc;
            --neon-pink: #ff0050;
            --neon-blue: #7aa2f7;
            --neon-yellow: #ff9e64;
            --white: #ffffff;
        }

        @page {
            size: A4;
            margin: 0;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Anuphan', sans-serif;
            background-color: var(--bg) !important;
            color: var(--text-main) !important;
            margin: 0;
            padding: 20mm 25mm;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
            line-height: 1.6;
        }

        .container {
            max-width: 100%;
            margin: 0 auto;
        }

        /* Top Header Styling */
        .header {
            border-bottom: 2px solid var(--neon-cyan);
            padding-bottom: 20px;
            margin-bottom: 30px;
            position: relative;
        }

        .header::after {
            content: "SECURE AUTOMATION NODE // CLASSIFIED INTEL";
            position: absolute;
            bottom: -10px;
            right: 0;
            background: var(--neon-pink);
            color: var(--white);
            font-family: 'IBM Plex Mono';
            font-size: 10px;
            padding: 2px 10px;
            font-weight: 700;
            letter-spacing: 0.15em;
            border-radius: 2px;
        }

        .eyebrow {
            display: inline-block;
            background: var(--neon-cyan);
            color: var(--bg);
            font-family: 'Kanit';
            font-weight: 800;
            font-size: 11px;
            padding: 3px 10px;
            letter-spacing: 0.1em;
            margin-bottom: 12px;
            border-radius: 2px;
            text-transform: uppercase;
        }

        h1 {
            font-family: 'Kanit';
            font-size: 2.3rem;
            font-weight: 800;
            margin: 0 0 8px 0;
            line-height: 1.1;
            color: var(--white);
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.4);
        }

        .sub {
            font-size: 14px;
            color: var(--text-dim);
            margin: 0;
            line-height: 1.5;
        }

        /* Top Grid Stats */
        .meta-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 25px;
        }

        .meta-item {
            border: 1px solid var(--border);
            padding: 12px 15px;
            background: var(--table-bg);
            border-radius: 4px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            border-top: 3px solid var(--neon-cyan);
        }

        .meta-item b {
            display: block;
            font-family: 'IBM Plex Mono';
            font-size: 1.15rem;
            color: var(--neon-cyan);
            text-shadow: 0 0 5px rgba(0, 255, 204, 0.3);
        }

        .meta-item span {
            font-size: 11px;
            color: var(--text-dim);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Chapter Title Headers */
        h2 {
            font-family: 'Kanit';
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--neon-cyan);
            border-bottom: 1px solid var(--border);
            padding-bottom: 6px;
            margin-top: 40px;
            margin-bottom: 18px;
            text-shadow: 0 0 8px rgba(0, 255, 204, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        h3 {
            font-family: 'Kanit';
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--white);
            margin-top: 22px;
            margin-bottom: 10px;
        }

        p {
            margin-top: 0;
            margin-bottom: 14px;
            color: var(--text-main);
        }

        ul {
            margin-top: 0;
            margin-bottom: 18px;
            padding-left: 20px;
        }

        li {
            margin-bottom: 8px;
            color: var(--text-main);
        }

        li strong {
            color: var(--white);
        }

        /* Segment Panels */
        .card {
            background: var(--card-bg) !important;
            border: 1px solid var(--border) !important;
            border-left: 4px solid var(--neon-cyan) !important;
            padding: 18px;
            margin-bottom: 18px;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            page-break-inside: avoid;
        }

        .card.danger {
            border-left-color: var(--neon-pink) !important;
        }

        .card.warning {
            border-left-color: var(--neon-yellow) !important;
        }

        .card.info {
            border-left-color: var(--neon-blue) !important;
        }

        .card-title {
            font-family: 'Kanit';
            font-weight: 700;
            font-size: 1.05rem;
            color: var(--white);
            margin-bottom: 8px;
        }

        /* Table styling inside Dark Theme */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            background: var(--table-bg) !important;
            border: 1px solid var(--border);
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        }

        th, td {
            padding: 12px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            background-color: rgba(0, 255, 204, 0.06) !important;
            font-family: 'Kanit';
            font-weight: 700;
            color: var(--neon-cyan);
            font-size: 13.5px;
            border-bottom: 2px solid var(--neon-cyan);
        }

        td {
            font-size: 13px;
            color: var(--text-main);
        }

        td strong {
            color: var(--white);
        }

        tr:last-child td {
            border-bottom: none;
        }

        .badge-step {
            display: inline-block;
            background: rgba(255, 0, 80, 0.15);
            color: var(--neon-pink);
            font-family: 'IBM Plex Mono';
            font-weight: 700;
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 3px;
            border: 1px solid rgba(255, 0, 80, 0.3);
            margin-right: 8px;
        }

        .footer {
            margin-top: 50px;
            border-top: 1px solid var(--border);
            padding-top: 15px;
            text-align: center;
            font-family: 'IBM Plex Mono';
            font-size: 10px;
            color: var(--text-dim);
            letter-spacing: 0.08em;
        }

        @media print {
            body {
                background-color: var(--bg) !important;
                color: var(--text-main) !important;
            }
            .card {
                background-color: var(--card-bg) !important;
                border-color: var(--border) !important;
            }
            table {
                background-color: var(--table-bg) !important;
            }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <span class="eyebrow">Jarvis Intelligence Report</span>
        <h1>คู่มือระบบฟาร์มและปั้นบัญชี TikTok</h1>
        <p class="sub">วิเคราะห์การควบคุมแบบกลุ่ม (Group Control), การจำลองอุปกรณ์ลบลายนิ้วมือเครื่อง และสูตรการวอร์มอัปป้องกันบัญชีโดนแบน</p>
        
        <div class="meta-grid">
            <div class="meta-item">
                <b>№ TT-FARM-2026</b>
                <span>รหัสเอกสาร</span>
            </div>
            <div class="meta-item">
                <b>3 MODELS</b>
                <span>สถาปัตยกรรมระบบ</span>
            </div>
            <div class="meta-item">
                <b>7-DAY PROTOCOL</b>
                <span>โปรโตคอลการวอร์มอัป</span>
            </div>
        </div>
    </div>

    <!-- Section 1 -->
    <h2>1. กลไกการตรวจจับบัญชีผิดปกติของ TikTok</h2>
    <p>ระบบตรวจจับสแปมและบัญชีบอทของ TikTok (Anti-Bot & Risk Control) อาศัย AI ในการวิเคราะห์ข้อมูลเพื่อตรวจคัดกรองสัญญาณผิดปกติใน 3 มิติหลัก:</p>
    <ul>
        <li><strong>Device Fingerprint (ลายนิ้วมือฮาร์ดแวร์เครื่อง):</strong> ตรวจวัดค่าข้อมูลจำเพาะ เช่น รหัสประจำเครื่อง (UUID/IMEI), ระดับแรงดันไฟฟ้าแบตเตอรี่, การเคลื่อนไหวของเซ็นเซอร์ Gyroscope, ชนิดของซีพียู และลิสต์รายการแอปพลิเคชันที่ติดตั้งในเครื่อง</li>
        <li><strong>Network & IP Reputations (ประวัติเครือข่าย):</strong> ตรวจวัดว่าเชื่อมต่อผ่านเน็ตค่ายทั่วไปหรือผ่านดาต้าเซ็นเตอร์ราคาถูก ตลอดจนพฤติกรรมการเปลี่ยนตำแหน่งพื้นที่อย่างรวดเร็ว (IP Jumping)</li>
        <li><strong>Behavioral Patterns (การเลียนแบบพฤติกรรมมนุษย์):</strong> บอทที่อัปโหลดคลิปทันทีที่สมัครเสร็จ ปัดคลิปทิ้งอย่างรวดเร็วเป็นจังหวะคงที่ หรือไม่มีการกดแชร์ กดค้นหาอย่างคนทั่วไป จะโดนลงโทษในรูปแบบ **Shadowban** (ยอดเข้าชม 0 วิวถาวร)</li>
    </ul>

    <!-- Section 2 -->
    <h2>2. สถาปัตยกรรมระบบฟาร์มบัญชีระดับใหญ่ (3 Setup Architectures)</h2>
    
    <div class="card info">
        <div class="card-title">📱 โมเดล A: Hardware Phone Farm (ดีที่สุดและปลอดภัยสูงสุด)</div>
        <p>การจัดตั้งชั้นวางโทรศัพท์มือถือแอนดรอยด์ราคาประหยัดหลายสิบถึงร้อยเครื่อง แล้วเชื่อมสายส่งสัญญาณ USB Hub ตรงเข้าคอมพิวเตอร์ตัวเดียวเพื่อควบคุมการพิมพ์ ปัด และทำงานพร้อมกัน</p>
        <ul>
            <li><strong>ซอฟต์แวร์ควบคุมยอดนิยม:</strong> **TikMatrix**, **TikControl**, หรือ **Total Control** ร่วมกับระบบบอร์ดสั่งการแบบ Multi-Screen</li>
            <li><strong>ระดับความเสี่ยง:</strong> **ต่ำมาก** เนื่องจากระบบประมวลผลบนบอร์ดโทรศัพท์ฮาร์ดแวร์จริง ทำให้ TikTok จับยากที่สุด</li>
        </ul>
    </div>

    <div class="card warning">
        <div class="card-title">💻 โมเดล B: Anti-Detect Browsers (จำลองหน้าเว็บ - ยอดนิยมสำหรับแนว Affiliate)</div>
        <p>การใช้เบราว์เซอร์ลบลายนิ้วมือฮาร์ดแวร์จำลองเซสชันล็อกอินแยกโปรไฟล์ไม่ให้ระบบความปลอดภัยตรวจจับลายนิ้วมือที่ชนกัน เหมาะสำหรับการรันร้านค้าและจัดการสัญญานายหน้าในเครื่อง PC</p>
        <ul>
            <li><strong>ซอฟต์แวร์ควบคุมยอดนิยม:</strong> **AdsPower**, **Multilogin**, หรือ **Dolphin{anty}**</li>
            <li><strong>ระดับความเสี่ยง:</strong> **ปานกลาง** ขึ้นอยู่กับการจัดสรรพร็อกซีแยกโปรไฟล์และคุณภาพของการจำลอง Canvas, WebGL, และไอพี</li>
        </ul>
    </div>

    <div class="card danger">
        <div class="card-title">☁️ โมเดล C: Cloud Phone Emulator (เน้นขยายตัวเร็ว ทรัพยากรเสมือน)</div>
        <p>การเช่าใช้งานเครื่องจำลองโทรศัพท์มือถือ (Android Cloud Phone) ที่รันตลอด 24 ชั่วโมงบนศูนย์ข้อมูลภายนอกและสั่งรันสคริปต์อัตโนมัติ</p>
        <ul>
            <li><strong>ซอฟต์แวร์ควบคุมยอดนิยม:</strong> **VMOS Cloud**, **Redfinger**, หรือ **LDCloud**</li>
            <li><strong>ระดับความเสี่ยง:</strong> **สูงมาก** ระบบ AI ของ TikTok บล็อกแอดเดรสและเครื่องจำลองประเภทนี้ได้รวดเร็ว</li>
        </ul>
    </div>

    <!-- Section 3 -->
    <h2>3. ระบบอินเทอร์เน็ต พร็อกซี และทราฟฟิก (Network Configuration)</h2>
    <p>การจัดสรรระบบไอพีถือเป็น 70% ของโอกาสสำเร็จ การใช้ไอพีชนกันจะทำลายทั้งฟาร์มทันที:</p>
    <ul>
        <li><strong>4G/5G Mobile Proxies (เน็ตซิมมือถือ - ดีที่สุด):</strong> การแปลงสัญญาณเน็ตซิมจริงผ่านโมเด็ม USB (Dongle) ความน่าเชื่อถือของไอพีสูงมากเนื่องจากผู้ใช้ทั่วไปใช้งานเครือข่ายเดียวกัน และช่วยหมุนเวียนเปลี่ยนไอพีอัตโนมัติได้ง่าย</li>
        <li><strong>Residential Proxies (พร็อกซีไอพีบ้าน):</strong> เป็นพร็อกซีจำลองที่ชี้ตำแหน่งว่าเป็นบ้านเรือนของคนทั่วไป บริการที่นิยมใช้ เช่น **Proxy-Seller**, **IPRoyal**, **Bright Data** หรือ **Smartproxy**</li>
        <li><strong>ข้อห้ามเด็ดขาด:</strong> หลีกเลี่ยงดาต้าเซ็นเตอร์พร็อกซี (Datacenter Proxy) ราคาถูกโดยสิ้นเชิง เนื่องจากมีโอกาสโดนบล็อกการมองเห็นยกชุดทันที</li>
    </ul>

    <!-- Section 4 -->
    <h2>4. โปรโตคอลการเลี้ยงบัญชี 7 วันก่อนเริ่มงาน (7-Day Warmup Protocol)</h2>
    <p>สเต็ปการสร้างกิจกรรมให้แก่บัญชีสมัครใหม่ เพื่อสร้างพฤติกรรมความน่าเชื่อถือในระบบป้องกันของ TikTok:</p>
    
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">ช่วงเวลา</th>
                <th style="width: 45%;">กระบวนการปั้นและเลี้ยงช่อง (Warmup Actions)</th>
                <th style="width: 40%;">ผลลัพธ์ความปลอดภัย</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>วันแรก (Day 1)</strong></td>
                <td>สมัครบัญชีผ่าน SIM การ์ดจริงหรืออีเมลสะอาด (เลี่ยงเบอร์ VOIP เสมือน) กรอกโปรไฟล์/รูปประจำตัวอย่างเหมาะสม ปล่อยทิ้งไว้ 24 ชั่วโมงโดยห้ามทำกิจกรรมเพิ่มเติม</td>
                <td>ลดธงเตือนของบอทจากการสมัครใช้งานพร้อมกันในสเกลใหญ่ (Mass signup flags)</td>
            </tr>
            <tr>
                <td><strong>วันที 2-3</strong></td>
                <td>เปิดหน้าฟีดแนะนำ (FYP) ปัดดูคลิป 15-20 นาที/วัน ดูให้จบความยาว ห้ามรีบปัดทิ้ง กดหัวใจเฉพาะคลิปที่น่าสนใจ 2-3 ครั้งต่อวันอย่างเป็นธรรมชาติ</td>
                <td>สะสมประวัติคุกกี้และพฤติกรรมการสตรีมมิ่งคลิปวิดีโอ (Organic streaming records)</td>
            </tr>
            <tr>
                <td><strong>วันที 4-5</strong></td>
                <td>ค้นหาคำสำคัญ (Keywords) ประจำกลุ่มงาน (Niche) เช่น แฟชั่น เสื้อผ้า สัตว์เลี้ยง ดูคลิปในกลุ่มนั้น กดติดตามช่องเป้าหมายใหญ่ ๆ 2-3 ช่อง</td>
                <td>บังคับระบบแนะนำเนื้อหา (FYP Algorithm) ให้จัดทำกลุ่มผู้ใช้งาน (Niche Identification) เพื่อเป้าหมายการปล่อยฟีดในวันหลัง</td>
            </tr>
            <tr>
                <td><strong>วันที 6</strong></td>
                <td>ทดลองใช้ฟังก์ชันเก็บเสียงแผ่นโปรด แชร์คลิปผ่านการคัดลอกลิงก์ หรือแสดงความเห็นที่เป็นประโยชน์ 1-2 ครั้ง</td>
                <td>เพิ่มความลึกของคุณภาพบัญชีในระบบตรวจสอบความปลอดภัย (Account Trust Score)</td>
            </tr>
            <tr>
                <td><strong>วันที 7</strong></td>
                <td>โพสต์วิดีโอแรกความยาว 10-15 วินาที เช็คยอดการเข้าชมผ่านไป 24 ชั่วโมง เพื่อประเมินผลสุขภาพบัญชี</td>
                <td><strong>เกณฑ์วัด:</strong> ยอดวิว 200+ = บัญชีปลอดภัยพร้อมรันต่อ / ยอดวิว 0 = ติดเงา Shadowban (ต้องเริ่มทำลายทิ้งและปั้นใหม่)</td>
            </tr>
        </tbody>
    </table>

    <!-- Section 5 -->
    <h2>5. การผลิตคลิปด้วยเครื่องมือและป้องกันระบบตรวจลิขสิทธิ์ซ้ำ (Bulk Content & Editing Tools)</h2>
    <p>การอัปโหลดไฟล์ที่ดาวน์โหลดมาจากที่อื่นโดยไม่มีการปรับแต่ง จะโดนระบบคัดลอกลิขสิทธิ์บล็อกทันที วิธีข้าม AI ได้แก่:</p>
    <ul>
        <li><strong>การแก้ไขรูปแบบคลิปข้าม AI:</strong> สลับด้านซ้ายขวา (Mirror) วิดีโอ, ทำการครอปซูมขอบเข้า-ออก 1-3%, ปรับแต่งเฉดสีระดับอ่อนเพื่อเปลี่ยนลายนิ้วมือพิกเซลภาพ และแทรกเสียงเพลงยอดฮิตเบา ๆ เพื่อขัดขวางเสียงเพลงเดิม</li>
        <li><strong>การรันวิดีโอสเกลใหญ่ด้วยโปรแกรม:</strong> การใช้ระบบสั่งงานผ่าน <strong>ffmpeg</strong> หรือสคริปต์ **Python MoviePy** เพื่อทำการสุ่มเปลี่ยนเฟรม ปรับโทนสี อัปสเกลความละเอียด และลบรหัสไฟล์ลายนิ้วมือกล้องดั้งเดิม (EXIF/Metadata Cleaner) แบบรวดเดียวคราวละ 100+ วินาที</li>
    </ul>

    <!-- Section 6 -->
    <h2>6. ตารางสรุปซอฟต์แวร์ที่ต้องใช้ (Farming Software Stack)</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">ประเภทของเครื่องมือ</th>
                <th style="width: 35%;">ชื่อซอฟต์แวร์ยอดนิยม</th>
                <th style="width: 40%;">บทบาทหน้าที่ในสถาปัตยกรรมระบบฟาร์ม</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>จำลองโปรไฟล์ระบบ</strong></td>
                <td>AdsPower, Multilogin, Dolphin{anty}</td>
                <td>แยกเครื่องมือล็อกอิน ปลอมแปลงฮาร์ดแวร์ลายนิ้วมือเครื่องคอม ป้องกันบัญชีผูกสัมพันธ์กัน</td>
            </tr>
            <tr>
                <td><strong>โปรแกรมคุมเครื่องกลุ่ม</strong></td>
                <td>TikMatrix, TikControl, VMOS Cloud</td>
                <td>ควบคุมการใช้งานโทรศัพท์จริงจำนวนมาก สั่งเล่น ปัด หรือพิมพ์อัตโนมัติผ่านโปรแกรมเดียว</td>
            </tr>
            <tr>
                <td><strong>พร็อกซี / เน็ตเวิร์ก</strong></td>
                <td>Proxy-Seller, IPRoyal, Bright Data</td>
                <td>จัดระบบไอพีบ้านและเน็ตมือถือแบบเจาะจง แยกออกจากกันในแต่ละบัญชีฟาร์มเพื่อความเสถียร</td>
            </tr>
            <tr>
                <td><strong>ชุดสคริปต์อัตโนมัติ</strong></td>
                <td>Python Playwright, Appium, RPA Module</td>
                <td>เขียนบอททำงานอัตโนมัติจำลองนิ้วมือผู้เล่น กดดู และอัปโหลดตามเวลาที่ตั้งไว้</td>
            </tr>
            <tr>
                <td><strong>โปรแกรมสร้างและปรับคลิป</strong></td>
                <td>ffmpeg, Python MoviePy, CapCut Bulk Rendering</td>
                <td>ลบ Metadata ปรับแต่งสี แสง สลับวิดีโอ เพื่อข้ามระบบตรวจจับลิขสิทธิ์ซ้ำสเกลใหญ่</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        CLASSIFIED REPORT · TIKTOK FARMING LAB · STARK SYSTEM GENERATED
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
