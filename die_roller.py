import board
import random
import os
import digitalio
#from digitalio import DigitalInOut, Direction, Pull
from adafruit_funhouse import FunHouse
import adafruit_bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.filled_polygon import FilledPolygon
#from adafruit_display_shapes.filled_polygon import FilledPolygon
#import adafruit_tmp117
import time

funhouse = FunHouse(
    default_bg=0x078f86,
    #scale=2, # gives us a 120x120 grid to address based on the 240x240 pixel display
    scale=1 #filled polygons behave strangely at any scale other than 1 - the fill color acts as if scale=1
)

#display handling
""" TODO: something else here
def show_die(num_sides):
    if num_sides == 6:
        show_6()
    elif num_sides == 8:
        show_8()
    elif num_sides == 10:
        show_10()
    elif num_sides == 12:
        show_12()
    elif num_sides == 20:
        show_20()
    else:
        show_circle()
"""

def show(shape):
    shape.hidden = False

def hide(shape):
    shape.hidden = True

#poly1 = FilledPolygon(
#    points=[(10,80),(20, 70),(30,80),(30,100),(20,110),(10,100)],
#    outline=0xFFFFFF,
#    fill=0x000000,
#    close=True,
#    #colors=1,
#    stroke=1)
#funhouse.root_group.append(die_shape)

funhouse.display.root_group = None

myfont = adafruit_bitmap_font.bitmap_font.load_font('fonts/Jellee-Bold-21.bdf')

circle_die = Circle(x0=120,y0=80,r=60,fill=0x1da861,outline=0x0000FF,stroke=2)
hide(circle_die)
funhouse.root_group.append(circle_die)

triangle_die = Triangle(x0=120,y0=20,x1=50,y1=140,x2=190,y2=140,fill=0x1da861,outline=0x0000FF)
hide(triangle_die)
funhouse.root_group.append(triangle_die)

square_die = RoundRect(x=60,y=20,width=120,height=120,fill=0x1da861,outline=0x0000FF,stroke=2,r=15)
hide(square_die)
funhouse.root_group.append(square_die)

hexagon_die = FilledPolygon(points=[(90,20),(150,20),(190,80),(150,140),(90,140),(50,80)],fill=0x1da861,outline=0x0000FF,stroke=2)
hide(hexagon_die)
funhouse.root_group.append(hexagon_die)

die_label = label.Label(font=myfont,x=90,y=80,text="0",scale=2)
funhouse.root_group.append(die_label)

funhouse.display.root_group = funhouse.root_group

#general state vars
die_sizes = [4,6,8,10,12,20,50,100]
die_idx = 0

#helper functions
def smaller_die():
    global die_idx
    die_idx = die_idx - 1
    print(f"switching to die idx: {die_idx}")
    if die_idx < 0:
        die_idx = len(die_sizes) - 1
    refresh_die_display()

def larger_die():
    global die_idx
    die_idx = die_idx + 1
    print(f"switching to die idx: {die_idx}")
    if die_idx > len(die_sizes) - 1:
        die_idx = 0
    refresh_die_display()

def hide_all_dice():
    hide(square_die)
    hide(circle_die)
    hide(triangle_die)
    hide(hexagon_die)

def refresh_die_display():
    die_size = die_sizes[die_idx]
    die_label.text = f"d{'%' if die_size == 100 else die_size}"
    die_label.x = 90
    hide_all_dice()
    if die_size == 4:
        show(triangle_die)
    elif die_size == 6:
        show(square_die)
    elif die_size == 8:
        show(hexagon_die)
    else:
        show(circle_die)


def roll(sides):
    # the docs recommend using os.urandom() for truly random numbers
    # (https://docs.circuitpython.org/en/latest/shared-bindings/random/)
    b = os.urandom(10)
    # that function returns bytes, though, so we convert to an int
    i = int.from_bytes(b)
    #print(b)
    #print(i)
    # use that value to seed the random module
    random.seed(i)
    # randrange is zero-based, so add 1 before we return (test this with roll(2) to see it in action)
    #return random.randrange(sides) + 1
    #die_label.text = f"{random.randrange(sides) + 1}"
    center = random.randrange(sides) + 1
    die_label.text = f"{center}"
    die_label.x = 105 if center < 10 else 90

refresh_die_display()

while True:
    #if down_button.value:
    if funhouse.peripherals.button_down:
        #select next smallest die
        smaller_die()
        time.sleep(0.2)
    if funhouse.peripherals.button_up:
        #select next largest die
        larger_die()
        time.sleep(0.2)
    if funhouse.peripherals.button_sel:
        #roll the selected die
        roll(die_sizes[die_idx])
        time.sleep(0.2)


    #hide(square_die)
    #show(circle_die)
    #die_label.text = '12'
    #time.sleep(1)
    #hide(circle_die)
    #show(square_die)
    #die_label.text = '45'
    #time.sleep(1)
