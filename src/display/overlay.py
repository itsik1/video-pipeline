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
