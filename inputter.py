from textdetect import detectwords
import time
import pyautogui
import threading


'''
start_time = time.perf_counter()
print(detectwords(search_words = ["Submit"]))
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")
'''

#tempcoords = (6, [(301, 475), (859, 475), (1495, 475), (301, 1126), (859, 1126), (1495, 1126)])


def process_coordinates(num_coords, coords, start=100, end=110):
    print("2.5s to start")
    time.sleep(2.5)
    
    for number in range(start, end + 1):
        for coord in coords:
            pyautogui.click(coord[0], coord[1]) # click coord
            time.sleep(0.1)
            pyautogui.write(str(number)) # type number
            pyautogui.press('enter') # hit enter
            time.sleep(1)

numcoords = 6
tempcoords = [(301, 475), (859, 475), (1495, 475), (301, 1126), (859, 1126), (1495, 1126)]

# Run it
process_coordinates(numcoords, tempcoords)