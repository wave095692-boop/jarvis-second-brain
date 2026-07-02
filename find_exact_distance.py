from PIL import Image
import numpy as np

# Load cropped image
im = Image.open("/Users/apple/.gemini/antigravity-ide/scratch/crop.png")
# Convert to grayscale
gray = im.convert("L")
arr = np.array(gray)

# We know the puzzle piece is on the left (X from 0 to 180)
# The target gap is somewhere in X from 250 to 600, Y from 50 to 300
# Let's print the average horizontal profile of brightness in that region
y_start, y_end = 80, 250
sub_arr = arr[y_start:y_end, :]

# Calculate average brightness per column
col_avg = np.mean(sub_arr, axis=0)

# The gap is very dark (lower values) but has a bright white outline on the left/right.
# Let's find the minimum brightness column in the range [300, 550]
search_min = 300 + np.argmin(col_avg[300:550])
print(f"Minimum brightness column in range [300, 550]: {search_min} (absolute X: {150 + search_min})")

# Let's check the puzzle piece left edge in range [0, 50]
piece_min = np.argmin(col_avg[0:80])
print(f"Piece column in range [0, 80]: {piece_min} (absolute X: {150 + piece_min})")

# Let's also print the difference
dx = search_min - 35 # Piece center in crop is roughly 75-85
print(f"Suggested dx: {search_min - 75}")
