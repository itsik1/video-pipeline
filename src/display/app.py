import time
from multiprocessing import Queue
import cv2
from typing import Any

from src.display.overlay import draw_boxes, draw_clock_top_left


def display_loop(in_q: Queue) -> None:
    try:
        first_ts = None
        wall_start = None
        while True:
            msg = in_q.get()
            mtype = msg.get("type", None)

            if mtype == "eof":
                break
            frame = msg["image"]
            ts = msg["ts"]
            if mtype != "detections" or frame is None or ts is None:
                continue

            boxes = msg["boxes"]

            if first_ts is None:
                first_ts = ts
                wall_start = time.time()

            # schedule display to match original video timestamps
            target = wall_start + (ts - first_ts)
            delay = target - time.time()
            while delay > 0:
                # process GUI events and allow early quit while waiting
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return
                time.sleep(min(delay, 0.01))
                delay = target - time.time()

            draw_boxes(frame, boxes)
            draw_clock_top_left(frame, time.strftime("%H:%M:%S"))
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cv2.destroyAllWindows()
