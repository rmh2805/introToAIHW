from PIL import Image

im = Image.open("Inputs/mpTerrain.png")
print(im)

width, height = im.size
pix = im.load()

for row in range(0, height):
    for col in range(0, width):
        if pix[col, row][3] != 255:
            print('(' + str(row) + ', ' + str(col) + ')')
