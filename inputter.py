import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

from imagedetect import detect
from textdetect import detectwords
from split import split
import time
import pyautogui
def debug():
    import cv2
    import numpy as np
    import mss

    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[0])
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
    
    cv2.imwrite("debug_screenshot.png", screen)
    print(f"Screenshot resolution: {screen.shape[1]}x{screen.shape[0]}")
    
    template = cv2.imread("submit.png", cv2.IMREAD_COLOR)
    print(f"Template resolution: {template.shape[1]}x{template.shape[0]}")

def input_number(coord, number):
    print(number)
    pyautogui.click(coord[0] - 30, coord[1] + 5)
    time.sleep(0.1)
    pyautogui.write(str(number))
    pyautogui.press('enter')
    time.sleep(0.2)

def find_coords():
    
    coords = detect(["submit.png", "submit2.png"])
    if coords:
        print(f"image {len(coords)}")
        return coords
    
    coords = detectwords(search_words=["Submit"])
    if coords:
        print(f"text {len(coords)}")
        return coords
       
    raise RuntimeError("no coords found")

def parallelprocess(coords, start=100, end=999):
    print("Starting in 2.5s")
    time.sleep(2.5)
    
    ranges = split(start, end, len(coords))
    sequences = [list(range(r_start, r_end + 1)) for r_start, r_end in ranges]
    
    max_len = max(len(s) for s in sequences)
    for i in range(max_len):
        for coord_idx, (coord, sequence) in enumerate(zip(coords, sequences)):
            if i < len(sequence):
                input_number(coord, sequence[i])

debug()
coords = find_coords()
start_time = time.time()
parallelprocess(coords)
print(time.time() - start_time)