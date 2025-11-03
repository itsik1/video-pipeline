import argparse
import multiprocessing as mp
import time

from src.detector.app import detect_loop
from src.display.app import display_loop
from src.streamer.app import stream_to_queue


def run_pipeline(video_path: str) -> None:
    q_size = 8
    mp.set_start_method("spawn", force=True)
    frames_q: mp.Queue = mp.Queue(maxsize=q_size)
    det_q: mp.Queue = mp.Queue(maxsize=q_size)
    p_stream = mp.Process(
        target=stream_to_queue,
        args=(video_path, frames_q),
        kwargs={"put_eof": True},
    )
    p_detect = mp.Process(
        target=detect_loop,
        args=(frames_q, det_q),
        name="detector",
    )
    p_display = mp.Process(
        target=display_loop,
        args=(det_q,),
        name="display",
    )

    procs = [p_stream, p_detect, p_display]

    for p in procs:
        p.start()

    try:
        while True:
            if not p_display.is_alive():
                break
            if any(p.exitcode not in (0, None) for p in procs):
                print("[orchestrator] A subprocess exited with error. Stopping all...")
                break
            time.sleep(0.3)

    except KeyboardInterrupt:
        pass
    for p in procs:
        if p.is_alive():
            p.terminate()
    for p in procs:
        p.join(timeout=3)


def main():
    parser = argparse.ArgumentParser(description="Run the 3-process video pipeline")
    parser.add_argument("--source", required=True, help="Path/URL to video file (or camera index like 0)")

    args = parser.parse_args()
    run_pipeline(
        video_path=args.source,
    )


if __name__ == "__main__":
    main()
