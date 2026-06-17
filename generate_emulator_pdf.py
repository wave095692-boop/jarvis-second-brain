import os
import subprocess

html_temp_path = "/Users/apple/.gemini/antigravity-ide/scratch/emulator_setup_temp.html"
pdf_path = "/Users/apple/Desktop/emulator_setup_guide.pdf"

html_content = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ANDROID EMULATOR SETUP GUIDE</title>
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
            content: "AUTOMATION LABORATORY // WIRELESS EMULATOR";
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

        ul, ol {
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

        code {
            font-family: 'IBM Plex Mono', monospace;
            background: rgba(255, 255, 255, 0.08);
            color: var(--white);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 12px;
        }

        pre {
            background: var(--table-bg);
            border: 1px solid var(--border);
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            margin-bottom: 18px;
        }

        pre code {
            background: transparent;
            padding: 0;
            color: var(--neon-cyan);
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
        <span class="eyebrow">Jarvis Wireless Setup Guide</span>
        <h1>คู่มือการติดตั้งแอนดรอยด์จำลอง (AVD) แบบไร้สาย</h1>
        <p class="sub">ขั้นตอนติดตั้งเครื่องมือจำลอง AVD ผ่าน Android Studio บน Mac และเชื่อมโยงบอทควบคุมอัตโนมัติแบบไร้สายผ่าน Localhost</p>
        
        <div class="meta-grid">
            <div class="meta-item">
                <b>№ AVD-SETUP-2026</b>
                <span>รหัสเอกสาร</span>
            </div>
            <div class="meta-item">
                <b>AVD (EMULATOR)</b>
                <span>เป้าหมายจำลองเครื่อง</span>
            </div>
            <div class="meta-item">
                <b>PORT 5554 (ADB)</b>
                <span>เส้นทางการเชื่อมต่อหลัก</span>
            </div>
        </div>
    </div>

    <!-- Section 1 -->
    <h2>1. สิ่งที่ต้องเตรียมการ (Prerequisites)</h2>
    <p>ก่อนเริ่มต้นเปิดระบบเครื่องมือจำลองแบบไร้สาย โปรดติดตั้งโปรแกรมต่าง ๆ เหล่านี้ลงในเครื่อง Mac ของบอส:</p>
    <ul>
        <li><strong>Android Studio (สำหรับสร้าง Emulator):</strong> ดาวน์โหลดฟรีสำหรับเครื่อง Mac (เลือกเวอร์ชันให้ตรงกับชิป เช่น Mac with Apple Chip สำหรับ M1/M2/M3 หรือ Intel Chip)</li>
        <li><strong>Python 3:</strong> สำหรับเปิดรันบอทควบคุม</li>
        <li><strong>เครื่องมือตรวจจับอุปกรณ์ (Android Command Line Tools):</strong> ใน Android Studio จะติดตั้งโปรแกรม `adb` (Android Debug Bridge) มาให้โดยอัตโนมัติ</li>
    </ul>

    <!-- Section 2 -->
    <h2>2. ขั้นตอนการสร้างเครื่องมือจำลอง Android (AVD)</h2>
    <p>ทำตามขั้นตอนดังต่อไปนี้เพื่อตั้งค่าตัวโทรศัพท์จำลองที่มีความเสถียรสูงสุดต่อการรันบอท:</p>
    <ol>
        <li>เปิดโปรแกรม **Android Studio** บน Mac</li>
        <li>คลิกที่เมนู **More Actions** (หรือไอคอนสามจุด) -> เลือกหัวข้อ **Virtual Device Manager** (หรือ Device Manager)</li>
        <li>คลิกที่ปุ่ม **Create Device** (มุมซ้ายบน)</li>
        <li>**เลือกฮาร์ดแวร์จำลอง (Hardware Profile):** แนะนำให้เลือก **Pixel 5** หรือ **Pixel 6** เพื่อให้ได้ขนาดหน้าจอมาตรฐานแนวตั้งทั่วไป จากนั้นคลิก Next</li>
        <li>**เลือกเวอร์ชันระบบปฏิบัติการ (System Image):** แนะนำให้ดาวน์โหลดและเลือก **Android 11.0 (API 30 - R)** หรือ **Android 10.0 (API 29 - Q)** เนื่องจากใช้ทรัพยากรเครื่องน้อยและเสถียรสูงเมื่อนำมาเขียนบอท -> คลิก Next</li>
        <li>**ตั้งค่าเครื่องเพิ่มเติม (Verify Configuration):**
            <ul>
                <li>ตั้งชื่อเครื่อง เช่น `Jarvis_Farming_Device`</li>
                <li>ในหัวข้อ Graphics แนะนำให้เลือกเป็น **Hardware - GLES 2.0** เพื่อดึงพลังการเรนเดอร์จากชิป GPU ของ Mac ช่วยเพิ่มความลื่นไหล</li>
            </ul>
        </li>
        <li>คลิก **Finish** เครื่องจำลองจะไปปรากฏอยู่ในลิสต์รายการ</li>
    </ol>

    <!-- Section 3 -->
    <h2>3. การเปิดใช้งานและเชื่อมต่อแบบไร้สาย (Wireless ADB Connection)</h2>
    
    <div class="card info">
        <div class="card-title">🔌 กลไกการเชื่อมต่อไร้สายผ่าน Local Loopback (Port 5554)</div>
        <p>เนื่องจากตัวจำลอง AVD รันอยู่ในหน่วยความจำหลักของ Mac ระบบปฏิบัติการจะจัดสรรพอร์ตเครือข่ายภายในให้โดยอัตโนมัติ ทำให้บอทสามารถควบคุมได้ทันทีโดยไม่ต้องต่อสาย USB</p>
        <ol>
            <li>ในหน้าต่าง Device Manager ให้กดปุ่ม **Play (สามเหลี่ยมสีเขียว)** ข้างอุปกรณ์ที่คุณสร้างไว้</li>
            <li>รอจนหน้าจอมือถือจำลองแอนดรอยด์บิวต์เสร็จและแสดงผลบนหน้าจอ Mac</li>
            <li>เปิดโปรแกรม **Terminal** บน Mac แล้วรันคำสั่งด้านล่างนี้เพื่อเช็คระบบตรวจจับ:
                <pre><code>adb devices</code></pre>
            </li>
            <li>ระบบจะแสดงชื่ออุปกรณ์ไร้สายในลิสต์ทันที เช่น:
                <pre><code>List of devices attached
emulator-5554   device</code></pre>
            </li>
        </ol>
    </div>

    <!-- Section 4 -->
    <h2>4. การติดตั้งแอปพลิเคชันและทดสอบบอท (Custom Script Playback)</h2>
    <p>ขั้นตอนดาวน์โหลดแอปและรันตัวอย่างสคริปต์บอทที่เราเตรียมไว้:</p>
    <ol>
        <li>**การติดตั้งแอป (เช่น TikTok):** ให้เปิดแอป Google Play Store ในเครื่องจำลองเพื่อดาวน์โหลดโดยตรง หรือลากไฟล์ `.apk` จาก Mac มาวางในหน้าจอจำลองได้ทันที</li>
        <li>**ติดตั้งไลบรารีบอทบนคอมพิวเตอร์:** เปิด Terminal แล้วลงตัวติดตั้งดังนี้:
            <pre><code>pip install uiautomator2 pillow</code></pre>
        </li>
        <li>**รันบอทควบคุมไร้สาย:** สั่งรันสคริปต์ `emulator_bot.py` ที่จาวิสจัดเตรียมไว้:
            <pre><code>python3 emulator_bot.py</code></pre>
            *บอทจะสั่งเปิดแอปพลิเคชัน TikTok สุ่มเวลาสไลด์ปัดหน้าจอ เลียนแบบการกดหัวใจ และควบคุมการทำงานผ่านเครือข่ายภายในเครื่องโดยไม่สะดุด*
        </li>
    </ol>

    <!-- Section 5 -->
    <h2>5. ตารางสรุปการตั้งค่าระบบความปลอดภัย (Security Checklists)</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">ปัญหาที่พบเจอได้</th>
                <th style="width: 35%;">สาเหตุหลัก</th>
                <th style="width: 40%;">วิธีการแก้ไขปัญหา (Troubleshooting)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>ระบบมองไม่เห็น Emulator</strong></td>
                <td>ไม่ได้ติดตั้ง Android Platform Tools หรือไม่ได้ตั้งค่า PATH ของ adb</td>
                <td>ให้ทำการระบุพาธ adb ใน Terminal เช่น <code>~/Library/Android/sdk/platform-tools/adb devices</code></td>
            </tr>
            <tr>
                <td><strong>เครื่องจำลองกระตุก</strong></td>
                <td>ขนาดแรมต่ำหรือไม่ได้เปิด Hardware Acceleration</td>
                <td>แก้ไขการตั้งค่าใน Virtual Device Manager โดยปรับเปลี่ยนตัว Graphics เป็น Hardware และเพิ่ม RAM เป็น 2GB หรือ 3GB</td>
            </tr>
            <tr>
                <td><strong>แอปฟ้องว่าเครื่องโดนรูท</strong></td>
                <td>แอปความปลอดภัยของระบบคลาวด์ตรวจจับแอดมินหรือโปรไฟล์ดีบั๊ก</td>
                <td>ให้เลือกภาพระบบ (System Image) ตอนติดตั้งที่ไม่มีคำว่า "Google APIs" หรือปิดโหมดนักพัฒนาในส่วนตั้งค่าของเครื่องจำลอง</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        WIRELESS LABS · GENERAETD BY JARVIS AT STARK WORKSPACE
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
