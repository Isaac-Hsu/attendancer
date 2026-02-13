import pyautogui
import time
import cv2
import numpy as np
import pytesseract
import os


search_words = ["submit", "Code:"] # words to detect
#path = os.path.join(os.path.expanduser("~"), r"Downloads\attendancer") # debug screenshot path
#os.makedirs(path, exist_ok=True) # make path if not found
#debug_image_path = os.path.join(path, "debug_output.jpg") 

# screenshot
time.sleep(1)
screenshot = pyautogui.screenshot()
image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # turn b/w
gray = cv2.bitwise_not(gray) # invert
gray = cv2.convertScaleAbs(gray, alpha=2.0, beta=0) # increase contrast

custom_config = r'--oem 3 --psm 6'  # chooses best engine (3) and treats image as a block of text (6)
data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config=custom_config)

''' # debug, print all words found 
detected_words = [word for word in data['text'] if word.strip() != ""]
print("Detected words:", " ".join(detected_words))

# debug, rectangles around words
for i, word in enumerate(data['text']):
    if word.strip() == "":
        continue
    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
    # Red rectangle for all words
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1)
    # Label with the OCR word
    cv2.putText(image, word, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
'''

# highlight searched words
results = {word: [] for word in search_words}
for i, word in enumerate(data['text']):
    if word.strip() == "":
        continue
    for target in search_words:
        if word.lower() == target.lower():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            results[target].append((x, y, w, h))
            # debug, thicker rectangle for matches
            # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# prints prints search word results
for word, boxes in results.items():
    print(f"Word '{word}' found {len(boxes)} times at positions: {boxes}")

# debug, saves image
# cv2.imwrite(debug_image_path, image)