from typing import List, Tuple, Optional

import cv2
import numpy as np
import imutils


class MotionDetector:
    prev_gray: Optional[np.ndarray] = None

    def detect(self, frame_bgr: np.ndarray) -> List[Tuple[int, int, int, int]]:
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is None:
            self.prev_gray = gray
            return []

        diff = cv2.absdiff(gray, self.prev_gray)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        boxes = [cv2.boundingRect(c) for c in cnts if cv2.contourArea(c) > 100]  # -> list of (x, y, w, h)
        return boxes
