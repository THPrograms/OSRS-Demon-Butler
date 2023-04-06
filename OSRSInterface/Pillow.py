from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import random
import os
import math

lvlup = [['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],['pLaYEr','sTrenGth ', 1, 5],]
mssgbar = 'Placeholder'

def gaussian_blur(newimage):
    width, height = newimage.size
    top_left = (10, 10)
    top_right = (width - 24, 10)
    bottom_left = (10, height - 45.5)
    bottom_right = (width - 24, height - 45.5)
    print (top_left, top_right, bottom_left, bottom_right)
    imagecrop = newimage.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
    blurred_image = imagecrop.filter(ImageFilter.GaussianBlur(radius=3))
    final_image = newimage.copy()
    final_image.paste(blurred_image, (11, 11))
    final_image.save(r"C:\Users\THerndon\Pictures\Final_Interface.png")
    return final_image


def extendinterface(lvlup):
    default_image = Image.open(r"C:\Users\THerndon\Pictures\Chat_Interface.png")
    default_image.save(r"C:\Users\THerndon\Pictures\Stacked_Interface.png")
    chunkdirectory = r"C:\Users\THerndon\Pictures\OSRSInterface\OSRSInterfaceChunks\\"
    if len(lvlup) > 7:
        for i in lvlup[7:]:
            # Load the image
            image = Image.open(r"C:\Users\THerndon\Pictures\Stacked_Interface.png")
            chunknumber = random.choice(range(0, 5))

            # Get the original dimensions
            width, height = image.size

            # Calculate the split point
            split_point = height // 2

            # Split the image in half
            top_half = image.crop((0, 0, width, split_point))
            bottom_half = image.crop((0, split_point, width, height))
            randommiddlefile = os.listdir(chunkdirectory)[chunknumber]
            print (randommiddlefile)
            middle_half = Image.open(r""+chunkdirectory+randommiddlefile)

            # Get the dimensions of the images
            width1, height1 = top_half.size
            width2, height2 = middle_half.size
            width3, height3 = bottom_half.size

            # Calculate the dimensions for the new image
            new_width = max(width1, width2, width3)
            new_height = height1 + height2 + height3

            # Create a new image with the calculated dimensions
            new_image = Image.new("RGB", (new_width, new_height))

            # Paste the images onto the new image

            new_image.paste(top_half, (0, 0))
            new_image.paste(middle_half, (0, height1))
            new_image.paste(bottom_half, (0, height1 + height2))
            new_image.save(r"C:\Users\THerndon\Pictures\Stacked_Interface.png")

        addtext(lvlup, gaussian_blur(new_image))
        return new_image
    else: addtext(lvlup, default_image)

def addtext(lvlup, useimage):
    image = useimage
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"C:\Users\THerndon\Pictures\OSRSInterface\runescape_uf\runescape_uf.ttf", 15)
    textheight = 43
    draw.text((11, height - 43), mssgbar, (0, 0, 0), font=font)
    for i in lvlup:
        textheight = textheight + 16
        draw.text((11, height - textheight), (str(i[0]) + " Has Gotten Stronger! " + str(i[1]) + ": " + str(i[2]) + " -> " + str(i[3])), (0, 0, 0), font=font)



    image.save(r"C:\Users\THerndon\Pictures\TestInterface.png")
    print ('It done did it')





"""print (extendinterface())"""
extendinterface(lvlup)
