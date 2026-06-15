#!/bin/bash
set -e

SRC_ICON="/Users/apple/.gemini/antigravity-ide/brain/ee47d0c3-d8d7-456b-820c-af5637523a8b/youtube_premium_icon_1781169533238.png"
ICONSET_DIR="/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/youtube_icon.iconset"
APP_PATH="/Users/apple/Desktop/BOS WAVE.app"
SCRIPT_PATH="/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/launcher.applescript"

# Delete old apps if they exist
if [ -d "/Users/apple/Desktop/YouTube Premium.app" ]; then
    rm -rf "/Users/apple/Desktop/YouTube Premium.app"
fi
if [ -d "/Users/apple/Desktop/NETPHRIK.app" ]; then
    rm -rf "/Users/apple/Desktop/NETPHRIK.app"
fi

echo "Generating icons..."
mkdir -p "$ICONSET_DIR"
sips -s format png -z 16 16     "$SRC_ICON" --out "$ICONSET_DIR/icon_16x16.png"
sips -s format png -z 32 32     "$SRC_ICON" --out "$ICONSET_DIR/icon_16x16@2x.png"
sips -s format png -z 32 32     "$SRC_ICON" --out "$ICONSET_DIR/icon_32x32.png"
sips -s format png -z 64 64     "$SRC_ICON" --out "$ICONSET_DIR/icon_32x32@2x.png"
sips -s format png -z 128 128   "$SRC_ICON" --out "$ICONSET_DIR/icon_128x128.png"
sips -s format png -z 256 256   "$SRC_ICON" --out "$ICONSET_DIR/icon_128x128@2x.png"
sips -s format png -z 256 256   "$SRC_ICON" --out "$ICONSET_DIR/icon_256x256.png"
sips -s format png -z 512 512   "$SRC_ICON" --out "$ICONSET_DIR/icon_256x256@2x.png"
sips -s format png -z 512 512   "$SRC_ICON" --out "$ICONSET_DIR/icon_512x512.png"
sips -s format png -z 1024 1024 "$SRC_ICON" --out "$ICONSET_DIR/icon_512x512@2x.png"

iconutil -c icns "$ICONSET_DIR" -o "/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/youtube_icon.icns"

echo "Compiling macOS App Bundle..."
if [ -d "$APP_PATH" ]; then
    rm -rf "$APP_PATH"
fi
osacompile -o "$APP_PATH" "$SCRIPT_PATH"

echo "Applying custom app icon..."
cp "/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/youtube_icon.icns" "$APP_PATH/Contents/Resources/applet.icns"

echo "Cleaning up..."
rm -rf "$ICONSET_DIR"
rm -f "/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/youtube_icon.icns"

touch "$APP_PATH"

echo "Build complete! App is located at $APP_PATH"
