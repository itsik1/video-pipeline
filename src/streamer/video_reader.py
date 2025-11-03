from typing import Optional, Iterator, Tuple

import cv2
import numpy as np


class VideoOpenError(RuntimeError):
    pass


class VideoReader:
    def __init__(self, source: str) -> None:
        self.source = source
        self._cap: Optional[cv2.VideoCapture] = None

    def open(self) -> None:
        self._cap = cv2.VideoCapture(self.source)
        if not self._cap or not self._cap.isOpened():
            raise VideoOpenError(f"Cannot open video source: {self.source}")

    def close(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def __enter__(self) -> "VideoReader":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def frames(self) -> Iterator[Tuple[int, float, np.ndarray]]:
        if self._cap is None:
            raise RuntimeError("VideoReader is not opened. Use .open() or a context manager.")

        frame_id = 0
        while True:
            ok, frame = self._cap.read()
            if not ok or frame is None:
                break

            video_ts = self._cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            yield frame_id, video_ts, frame
            frame_id += 1
