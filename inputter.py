from imagedetect import detect
from split import split
import time
import pyautogui
import threading
from concurrent.futures import ThreadPoolExecutor


'''
start_time = time.perf_counter()
print(detectwords(search_words = ["Submit"]))
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")
'''

# Thread lock to prevent simultaneous mouse/keyboard actions
lock = threading.Lock()


def input(coord, number):
    with lock:  # Ensure only one thread controls mouse/keyboard at a time
        pyautogui.click(coord[0] - 20, coord[1])
        time.sleep(0.1)
        pyautogui.write(str(number))
        pyautogui.press('enter')
        time.sleep(0.5)
        
def process_range(coord, start, end):
    for number in range(start, end + 1):
        input(coord, number)
        
def parallelprocess(coords, start=100, end=999):
    print("Starting in 2.5s")
    time.sleep(2.5)
    
    ranges = split(start, end, len(coords))
    
    with ThreadPoolExecutor(max_workers=len(coords)) as executor:
        for coord, (r_start, r_end) in zip(coords, ranges):
            executor.submit(process_range, coord, r_start, r_end)
            
#coords = detectwords(search_words = ["Submit"], debug=True)
coords = detect_image("submit.png")
parallelprocess(coords)