import board
#from digitalio import DigitalInOut, Direction, Pull
from adafruit_funhouse import FunHouse
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

funhouse.display.root_group = None
die_shape = None
funhouse.root_group.append(die_shape)
funhouse.display.root_group = funhouse.root_group

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

def show_circle():
    die_shape = Circle(x0=120,y0=80,r=60,fill=0x0000FF,outline=0xFF0000,stroke=2)

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


#poly1 = FilledPolygon(
#    points=[(10,80),(20, 70),(30,80),(30,100),(20,110),(10,100)],
#    outline=0xFFFFFF,
#    fill=0x000000,
#    close=True,
#    #colors=1,
#    stroke=1)
#funhouse.root_group.append(die_shape)

def clear_display():
    die_shape = None

def refresh_display():
    #funhouse.root_group.append(die_shape)
    funhouse.display.root_group = funhouse.root_group

while True:
    show_circle()
    time.sleep(.1)
    clear_shapes()
    time.sleep(.1)
