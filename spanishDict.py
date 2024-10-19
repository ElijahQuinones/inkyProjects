#!/usr/bin/env python3
import os
from PIL import Image
from inky.auto import auto

PATH = os.path.dirname(__file__)

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You Need to update the Inky library to >= v1.1.0")

try:
    inky_display.set_border(inky_display.BLACK)
except NotImplementedError:
    pass

img =Image.open(os.path.join(PATH,"images/Flag-Puerto-Rico.jpg"))
img = img.resize(inky_display.resolution)

inky_display.set_image(img)
inky_display.show()