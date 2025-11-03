from datetime import time

import cv2
from typing import List, Tuple

Box = Tuple[int, int, int, int]  # (x, y, w, h)
box_color = (0, 255, 0)
box_thickness = 2


def draw_boxes(image, boxes: List[Box]) -> None:
    for (x, y, w, h) in boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), box_color, box_thickness)


def draw_clock_top_left(image, current_time: str) -> None:
    cv2.putText(
        image, current_time, (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
    )


def blur_regions(image, boxes: List[Box], ksize: int = 21) -> None:
    if ksize % 2 == 0:
        ksize += 1  # דרישה של GaussianBlur למספר אי-זוגי
    for (x, y, w, h) in boxes:
        roi = image[y:y + h, x:x + w]
        if roi.size == 0:
            continue
        blurred = cv2.GaussianBlur(roi, (ksize, ksize), 0)
        image[y:y + h, x:x + w] = blurred
