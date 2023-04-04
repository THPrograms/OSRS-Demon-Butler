from PIL import Image
from PIL import ImageFilter
import random
import os
import math

def gaussian_blur(image):
    width, height = image.size
    top_left = (10, 10)
    top_right = (width - 24, 10)
    bottom_left = (10, height - 45.5)
    bottom_right = (width - 24, height - 45.5)
    print (top_left, top_right, bottom_left, bottom_right)
    imagecrop = image.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
    blurred_image = imagecrop.filter(ImageFilter.GaussianBlur(radius=1.5))
    final_image = image.copy()
    final_image.paste(blurred_image, (11, 11))
    final_image.save(r"C:\Users\THerndon\Pictures\Final_Interface.png")


def extendinterface():
    default_image = Image.open(r"C:\Users\THerndon\Pictures\Chat_Interface.png")
    default_image.save(r"C:\Users\THerndon\Pictures\Stacked_Interface.png")
    chunkdirectory = r"C:\Users\THerndon\Pictures\OSRSInterfaceChunks\\"

    for i in range(1, 100) :
        # Load the image
        image = Image.open(r"C:\Users\THerndon\Pictures\Stacked_Interface.png")
        chunknumber = random.choice(range(1, 11))

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
    gaussian_blur(new_image)
    return new_image

print (extendinterface())




