import argparse
from multiprocessing import Queue

from .video_reader import VideoReader


def stream_to_queue(video_path: str, out_queue: Queue, put_eof: bool = True) -> None:
    try:
        with VideoReader(video_path) as reader:
            for frame_id, video_ts, frame in reader.frames():
                out_queue.put(
                    {
                        "type": "frame",
                        "frame_id": frame_id,
                        "ts": video_ts,
                        "frame": frame
                    }
                )
    finally:
        if put_eof:
            out_queue.put({"type": "eof"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Streamer process")
    parser.add_argument("--source", required=True, help="Path to video file or camera index")
    args = parser.parse_args()

    q = Queue()
    stream_to_queue(args.source, q)

    while True:
        msg = q.get()
        if msg["type"] == "eof":
            print("Reached EOF, stopping streamer.")
            break
        print(f"Frame {msg['frame_id']} at t={msg['ts']:.2f}s")
