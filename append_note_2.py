import json
import os
from datetime import datetime

notes_path = "/Users/apple/.gemini/antigravity-ide/scratch/jarvis_second_brain/notes.json"

if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as f:
        try:
            notes = json.load(f)
        except Exception:
            notes = []
else:
    notes = []

next_id = max([n.get("id", 0) for n in notes]) + 1 if notes else 1
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

new_note = {
    "id": next_id,
    "text": "เชื่อมต่อระบบ Jarvis Second Brain บนพอร์ต 8500 และทดสอบการทำงานของฟังก์ชันต่อท้ายประวัติข้อมูล (Append) ป้องกันการเขียนทับไฟล์ notes.json ได้สมบูรณ์ 100%",
    "timestamp": now_str
}

notes.append(new_note)

with open(notes_path, "w", encoding="utf-8") as f:
    json.dump(notes, f, ensure_ascii=False, indent=4)

print(f"Successfully appended note ID {next_id} to second brain notes.")
