from multiprocessing import Queue

from src.detector.motion import MotionDetector


def detect_loop(in_q: Queue, out_q: Queue) -> None:
    det = MotionDetector()

    while True:
        msg = in_q.get()
        if msg["type"] == "eof":
            out_q.put({"type": "eof"})
            break
        if msg["type"] != "frame":
            continue

        frame = msg["frame"]
        boxes = det.detect(frame)
        out_q.put(
            {
                "type": "detections",
                "frame_id": msg["frame_id"],
                "ts": msg["ts"],
                "boxes": boxes,
                "image": frame,
            }
        )
