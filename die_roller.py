import board
import digitalio
#from digitalio import DigitalInOut, Direction, Pull
from adafruit_funhouse import FunHouse
import adafruit_bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.filled_polygon import FilledPolygon
#from adafruit_display_shapes.filled_polygon import FilledPolygon
#import adafruit_tmp117
import time

funhouse = FunHouse(
    default_bg=0x0F0F00,
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


"""
#TODO: fill these in with real shapes
def show_6():
    show_circle()
def show_8():
    show_circle()
def show_10():
    show_circle()
def show_12():
    show_circle()
def show_20():
    show_circle()
"""

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

circle_die = Circle(x0=120,y0=80,r=60,fill=0x0000FF,outline=0xFF0000,stroke=2)
hide(circle_die)
funhouse.root_group.append(circle_die)

#TODO:  round_rect?
square_die = Rect(x=60,y=20,width=120,height=120,fill=0x0000FF,outline=0xFF0000,stroke=2)
hide(square_die)
funhouse.root_group.append(square_die)

die_label = label.Label(font=myfont,x=90,y=70,text="0",scale=2)
funhouse.root_group.append(die_label)

funhouse.display.root_group = funhouse.root_group


# button setup

# select next smallest die size (wraps around to largest)
#up_button = digitalio.DigitalInOut(board.BUTTON_UP)
#up_button.switch_to_input(pull=digitalio.Pull.DOWN)

#roll the die
#select_button = digitalio.DigitalInOut(board.BUTTON_SELECT)
#select_button.switch_to_input(pull=digitalio.Pull.DOWN)

# select next largest die size (wraps around to smallest)
#down_button = digitalio.DigitalInOut(board.BUTTON_DOWN)
#down_button.switch_to_input(pull=digitalio.Pull.DOWN)

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

def refresh_die_display():
    die_size = die_sizes[die_idx]
    die_label.text = f"d{'%' if die_size == 100 else die_size}"
    show(circle_die)

def roll_die():
    print("not implemented")

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
        roll_die()
        time.sleep(0.2)


    #hide(square_die)
    #show(circle_die)
    #die_label.text = '12'
    #time.sleep(1)
    #hide(circle_die)
    #show(square_die)
    #die_label.text = '45'
    #time.sleep(1)
