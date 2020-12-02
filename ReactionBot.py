import os
import time
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import pygetwindow as gw
import re
#TotalFreedom Reaction Bot By DragonSlayer2189

#Replace "Insert latest.log" with the path to your latest.log file
LogFile = 'Insert lateset.log'

#Replace "Insert Text File" with the path to the included Untitled.txt
files = "Insert Text File"



#Code Shit
#Made by DragonSlayer2189
keyboard = KeyboardController()
mouse = MouseController()
while True:
    with open(LogFile) as myfile:
        text = list(myfile)[-1]
    print(text)

    if "[Reaction] Type the string" in text:
        
        text_file = open(files, "w")
        n = text_file.write(text)
        text_file.close()
        with open(files) as r:
            file_contents = [line.strip() for line in r.readlines()]
        capture_pattern = re.compile(r"Type the string (\w+) to win")
        for chatline in file_contents:
            try:
                result = capture_pattern.search(chatline).group(1)
            except:
                result = None
        time.sleep(0.1)
        keyboard.press('t')
        time.sleep(0.1)
        keyboard.type(result)
        time.sleep(0.1)
        keyboard.press(Key.enter)
        time.sleep(0.2)
        print(result)
    else:
        pass
