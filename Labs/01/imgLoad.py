from PIL import Image

im = Image.open("testImg.jpg")
print(im)
pix = im.load()
print(pix)

