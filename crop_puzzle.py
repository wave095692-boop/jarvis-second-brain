from PIL import Image

im = Image.open("/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png")
# Crop the puzzle image portion
# Width: 1080, Height: 1920
cropped = im.crop((150, 630, 930, 1100))
cropped.save("/Users/apple/.gemini/antigravity-ide/scratch/crop.png")
print("Cropped image saved. Size:", cropped.size)
