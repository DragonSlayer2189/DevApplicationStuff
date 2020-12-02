import phue
from phue import Bridge
import tkinter
from tkinter import *
import time
import os
import colorama
import random

BridgeIP = 'Redacted'

#startup code
colorama.init()
BLACK = colorama.Fore.BLACK
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
MAGENTA = colorama.Fore.MAGENTA
CYAN = colorama.Fore.CYAN
WHITE = colorama.Fore.WHITE
RESET = colorama.Fore.RESET
b = Bridge(BridgeIP)
try:
    b.get_api()
except phue.PhueRequestTimeout:
    print('Could not connect due to Timeout request. reloading')
    time.sleep(3)
    b.get_api()
lights = b.lights
# Print light names
for l in lights:
    print(MAGENTA + l.name + RESET)
lights = b.get_light_objects('id')
#GUI Stuff
def show_values():
    print(f'{RED} Red:')
    print(red.get())
    print(f'{GREEN}Green:')
    print(green.get())
    print(f'{BLUE}Blue:')
    print(blue.get())
    print(f'{YELLOW}Brightness:')
    print(bright.get())
    print(f'{CYAN}Light Status:')
    if check1.get() is True:
        print(GREEN + b.get_light(1,'name') + ': is on!')
    else:
        print(RED + b.get_light(1,'name') + ': is off!')

    if check2.get() is True:
        print(GREEN + b.get_light(2,'name') + ': is on!')
    else:
        print(RED + b.get_light(2,'name') + ': is off!')

    if check3.get() is True:
        print(GREEN + b.get_light(3,'name') + ': is on!')
    else:
        print(RED + b.get_light(3,'name') + ': is off!')

    if check4.get() is True:
        print(GREEN + b.get_light(4,'name') + ': is on!')
    else:
        print(RED + b.get_light(4,'name') + ': is off!')

    if check5.get() is True:
        print(GREEN + b.get_light(5,'name') + ': is on!')
    else:
        print(RED + b.get_light(5,'name') + ': is off!')
    print(RESET)
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb    
def convertColor(hexCode):
    R = int(hexCode[:2],16)
    G = int(hexCode[2:4],16)
    B = int(hexCode[4:6],16)

    total = R + G + B

    if R == 0:
        firstPos = 0
    else:
        firstPos = R / total
    
    if G == 0:
        secondPos = 0
    else:
        secondPos = G / total

    return [firstPos, secondPos]
master = Tk()
master.geometry("420x760") 
#Sliders
w = Label(master, text="Philips Hue™ Controler \n Made by Eric Bennett (DragonSlayer2189) \n\nRed:")
w.pack()
red = Scale(master, from_=0, to=255, orient=HORIZONTAL)
red.pack()
w1 = Label(master, text="\n Green:")
w1.pack()
green = Scale(master, from_=0, to=255, orient=HORIZONTAL)
green.pack()
w2 = Label(master, text="\n Blue:")
w2.pack()
blue = Scale(master, from_=0, to=255, orient=HORIZONTAL)
blue.pack()
w3 = Label(master, text="\n Brightness:")
w3.pack()
bright = Scale(master, from_=0, to=255, orient=HORIZONTAL)
bright.pack()
#Checkboxes
horizontal_frame = Frame(master)
horizontal_frame.pack()
check1 = BooleanVar()
c1 = Checkbutton(master, text = '\n' + b.get_light(1,'name'), variable = check1)
c1.pack()
check2 = BooleanVar()
c2 = Checkbutton(master, text = '\n' + b.get_light(2,'name'), variable = check2)
c2.pack()
check3 = BooleanVar()
c3 = Checkbutton(master, text = '\n' + b.get_light(3,'name'), variable = check3)
c3.pack()
check4 = BooleanVar()
c4 = Checkbutton(master, text = '\n' + b.get_light(4,'name'), variable = check4)
c4.pack()
check5 = BooleanVar()
c5 = Checkbutton(master, text = '\n' + b.get_light(5,'name'), variable = check5)
c5.pack()
#Buttons
w4 = Label(master, text="\n")
w4.pack()
Button(master, text='Show Variables', command=show_values).pack()
def set_color_light():
    if check1.get() is True:
        b.set_light(1, 'on', True)
    else:
        b.set_light(1, 'on', False)

    if check2.get() is True:
        b.set_light(2, 'on', True)
    else:
        b.set_light(2, 'on', False)  

    if check3.get() is True:
        b.set_light(3, 'on', True)
    else:
        b.set_light(3, 'on', False)   

    if check4.get() is True:
        b.set_light(4, 'on', True)
    else:
        b.set_light(4, 'on', False)

    if check5.get() is True:
        b.set_light(5, 'on', True)
    else:
        b.set_light(5, 'on', False)      
    color = rgb_to_hex((red.get(), green.get(), blue.get()))
    xycolor = convertColor(color)
    print(WHITE)
    print(xycolor)
    lights = b.get_light_objects()
    time.sleep(0.5)
    for light in lights:
        light.brightness = bright.get()
        time.sleep(0.1)
        light.xy = xycolor
    print(f'{GREEN}Color\'s set successfully!{RESET}')

Button(master, text='Set Lights To Above Settings', command=set_color_light).pack()

root = Tk()
w6 = Label(root, text="\n Other Options:\n")
w6.pack()
lights = b.get_light_objects()
def random_colors():
    for light in lights:
        light.brightness = bright2.get()
        light.xy = [random.random(),random.random()]
Button(root, text='Randomize Light Colors', command=random_colors).pack()
def random_colors_loop():
    i = 0
    while i < loop.get()*20:
        for light in lights:
            light.brightness = bright2.get()
            time.sleep(0.05)
            light.xy = [random.random(),random.random()]
            i = i+1
Button(root, text='Looped', command=random_colors_loop).pack()
w3 = Label(root, text="\n Loop Length (seconds):")
w3.pack()
loop = Scale(root, from_=0, to=3600, orient=HORIZONTAL)
loop.pack()
w3 = Label(root, text="\n Brightness:")
w3.pack()
bright2 = Scale(root, from_=0, to=255, orient=HORIZONTAL)
bright2.pack()
mainloop()