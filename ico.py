from PIL import Image

# Open your image
img = Image.open("ICO.jpg")

# Save as .ico
# We define standard icon sizes so it looks good at different zoom levels
img.save("icon.ico", format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

print("Conversion complete: icon.ico created.")