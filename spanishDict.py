#!/usr/bin/env python3
import os
from PIL import Image
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from openai import OpenAI

OPENAI_APIKEY = os.environ["OPENAI_APIKEY"]
PATH = os.path.dirname(__file__)

client = OpenAI(
    api_key=OPENAI_APIKEY
)
# Set up the correct display and scaling factors

inky_display = auto(ask_user=True, verbose=True)
inky_display.set_border(inky_display.WHITE)
# inky_display.set_rotation(180)

def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)


# This function will take a quote as a string, a width to fit
# it into, and a font (one that's been loaded) and then reflow
# that quote with newlines to fit into the space required.
def reflow_quote(quote, width, font):
    words = quote.split(" ")
    reflowed = '"'
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = getsize(font, word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n  " + word

    reflowed = reflowed.rstrip() + '"'

    return reflowed

WIDTH = inky_display.width
HEIGHT = inky_display.height
font_size = 24

padding = 5
max_width = WIDTH - padding
font = ImageFont.truetype(FredokaOne, font_size)
max_height = HEIGHT - padding - getsize(font, "ABCD ")[1]

with open(os.path.join(PATH,"spanishWordlist.txt"),"r+") as spanishWordListFile:
    wordOfTheday=spanishWordListFile.readline()
    
    definition = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a spanish teacher."},
        {
            "role": "user",
            "content": "Translate the word "+ wordOfTheday +" and use it in a sentence"
        }
    ]
)
    
    

    x = (WIDTH - max_width) / 2
    y = (HEIGHT - max_height) 


    img = Image.new("P", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)


    #hatch_spacing = 12

    #for x in range(0, 2 * WIDTH, hatch_spacing):
    #    draw.line((x, 0, x - WIDTH, HEIGHT), fill=inky_display.WHITE, width=3)



    print(definition)
    #draw.text((6, 8), "this is a test", fill ="red", font = font,  
    #          spacing = 50, align ="right") 
    draw.text((6,8), reflow_quote(str(definition.choices[0].message.content),600,font), fill=inky_display.WHITE, font=font, spacing=padding,  align="left")
    inky_display.set_image(img)
    inky_display.show()
    os.system("tail -n +2 spanishWordlist.txt > tmpfile.txt  && mv  tmpfile.txt spanishWordlist.txt")
