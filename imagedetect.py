def detect(template_paths, threshold=0.85):
    import cv2
    import numpy as np
    import mss

    if isinstance(template_paths, str):
        template_paths = [template_paths]  # allow passing a single string still

    with mss.mss() as sct:
        monitor = sct.monitors[0]
        screenshot = sct.grab(monitor)
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)

    coords = []
    for template_path in template_paths:
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"Warning: template not found: {template_path}, skipping")
            continue

        h, w = template.shape[:2]
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)

        for pt in zip(*locations[::-1]):
            coords.append((int(pt[0] - 30), int(pt[1] + h // 2)))

    print(f"{len(coords)} total matches across {len(template_paths)} templates")
    return coords