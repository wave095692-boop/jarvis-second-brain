import uiautomator2 as u2
d = u2.connect('emulator-5554')
print("Listing all clickable elements on Sign up page:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
