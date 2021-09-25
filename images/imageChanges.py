from PIL import Image

image1 = Image.open("Background1.png")
# image1.show()

image1_resize = image1.resize((1000, 600))
image1_resize.show()

# Save resized Image
image1_resize.save("Background1_resize.png")