import uiautomator2 as u2
d = u2.connect('emulator-5554')
print("Dumping all views with text or description:")
for el in d():
    text = el.info.get('text')
    desc = el.info.get('contentDescription')
    if text or desc:
        print(f"Text: {text} | Desc: {desc} | Bounds: {el.info.get('bounds')}")
