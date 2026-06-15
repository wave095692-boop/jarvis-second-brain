import json
import os
from datetime import datetime

notes_path = "/Users/apple/.gemini/antigravity-ide/scratch/jarvis_second_brain/notes.json"

# Read existing notes
if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as f:
        try:
            notes = json.load(f)
        except Exception:
            notes = []
else:
    notes = []

# Find next ID
next_id = max([n.get("id", 0) for n in notes]) + 1 if notes else 1

# Current timestamp in format YYYY-MM-DD HH:MM:SS
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

new_note = {
    "id": next_id,
    "text": "สร้างแผนไอเดียคอนเทนต์ล้างสต๊อกรายวันแคมเปญ RUDEDOG FAIR 2026 (รวมทั้งหมด 22 ไอเดียสำหรับ 10 วันและวันไลฟ์จริง) พร้อมแปลงไฟล์ PDF ดีไซน์พรีเมียมไว้ที่หน้า Desktop เรียบร้อย",
    "timestamp": now_str
}

# Append and save
notes.append(new_note)

with open(notes_path, "w", encoding="utf-8") as f:
    json.dump(notes, f, ensure_ascii=False, indent=4)

print(f"Successfully appended note ID {next_id} to second brain notes.")
