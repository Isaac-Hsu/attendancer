def detect(template_path, delay=2.5, threshold=0.85):
    import pyautogui
    import time
    import cv2
    import numpy as np
    
    print(f"Waiting {delay}s before capture…")
    time.sleep(delay)
    
    # Screenshot
    screenshot = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Load template
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template not found: {template_path}")
        
    h, w = template.shape[:2]
    
    # Template matching
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    
    coords = []
    for pt in zip(*locations[::-1]):
        # center = (pt[0] + w // 2, pt[1] + h // 2)
        coords.append((int(pt[0]), int(pt[1] + h // 2)))
        
    print(f"{len(coords)} matches")
    return coords
