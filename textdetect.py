def debugger(thresh, log, results, search_words, path):
    import cv2
    import os
    
    # debug images for each PSM mode
    psm_modes = [3, 6, 11]
    
    for psm in psm_modes:
        img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        
        # draw all detections for this PSM mode
        psm_logs = [log for log in log if f"PSM{psm}" in log['method']]
        
        for log in psm_logs:
            x, y, w, h = log['bbox']
            word = log['word']
            is_dup = log['duplicate']
            
            # green for unique, orange for duplicate
            color = (0, 150, 255) if is_dup else (0, 255, 0)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            
            label = f"{word} [PSM{psm}]" + (" DUP" if is_dup else "")
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        # save debug image
        path = os.path.join(path, f"debug_HighContrast_PSM{psm}.jpg")
        cv2.imwrite(path, img)
        print(f"PSM{psm}, {len(psm_logs)} detections")
        
    # detection summary
    if log:
        print(f"Detections:")
        for log in log:
            marker = " [duplicate]" if log['duplicate'] else " [counted]"
            print(f"'{log['word']}' by {log['method']}{marker} ({log['coord'][0]:.0f}, {log['coord'][1]:.0f})")
    else:
        print("\nno target words found")
        
    # final results
    print("\nFinal Results:")
    for word, coords in results.items():
        if coords:
            print(f"'{word}': {len(coords)} unique instance(s)")
            # show which PSM modes detected it
            methods = [log['method'] for log in log 
                      if log['word'] == word and not log['duplicate']]
            print(f"First detected by: {methods[0] if methods else 'N/A'}")
            # show all PSM modes that found it
            all_methods = list(set([log['method'] for log in log if log['word'] == word]))
            print(f"Detected by PSM modes: {', '.join([m.split('_')[1] for m in all_methods])}")
        else:
            print(f"'{word}': NOT FOUND")

def detectwords(search_words, debug=False): 
    import pyautogui
    import time
    import cv2
    import numpy as np
    import pytesseract
    import os
    
    path = os.path.join(os.path.expanduser("~"), r"Downloads\attendancer")
    os.makedirs(path, exist_ok=True)
    
    # Screenshot
    time.sleep(1)
    screenshot = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Upscale
    up = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(up, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)  # Invert
    
    # High contrast preprocessing
    contrast_enhanced = cv2.convertScaleAbs(gray, alpha=2.5, beta=0)
    _, thresh = cv2.threshold(contrast_enhanced, 200, 255, cv2.THRESH_BINARY)
    
    # OCR detection
    results = {word: [] for word in search_words}
    log = [] if debug else None  # Only collect if debugging
    
    psm_modes = [3, 6, 11]
    
    for psm in psm_modes:
        method_name = f"HighContrast_PSM{psm}"
        custom_config = f'--oem 3 --psm {psm} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:'
        
        try:
            data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT, config=custom_config)
            
            for i, word in enumerate(data['text']):
                if word.strip() == "":
                    continue
                
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                
                # check for target words
                for target in search_words:
                    if word.lower() == target.lower():
                        coord = (x + w / 2, y + h / 2)
                        
                        # Check for duplicates within 50 pixels
                        duplicate = False
                        for existing_coord in results[target]:
                            if abs(existing_coord[0] - coord[0]) < 50 and \
                               abs(existing_coord[1] - coord[1]) < 50:
                                duplicate = True
                                break
                                
                        if not duplicate:
                            results[target].append(coord)
                            
                        # log detection only if debugging
                        if debug:
                            log.append({'word': target, 'method': method_name, 'coord': coord, 'bbox': (x, y, w, h), 'duplicate': duplicate})
        except Exception as e:
            if debug:
                print(f"{method_name} failed: {e}")
            continue
    
    # debug visualization if enabled
    if debug:
        debugger(thresh, log, results, search_words, path)
    
    # return results
    all_coords = []
    for coords in results.values():
        all_coords.extend(coords)
    
    return len(all_coords), all_coords