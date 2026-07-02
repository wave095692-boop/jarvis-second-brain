import uiautomator2 as u2
d = u2.connect('emulator-5554')
xml = d.dump_hierarchy()
with open('/Users/apple/.gemini/antigravity-ide/scratch/hierarchy.xml', 'w', encoding='utf-8') as f:
    f.write(xml)
print("Dumped hierarchy to hierarchy.xml")
