import argparse
import time

from screenshot import capture_and_show


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture a screenshot every X seconds and show it briefly."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Seconds between captures (start of one capture to the next). Default: 5.0",
    )
    parser.add_argument(
        "--display-ms",
        type=int,
        default=1000,
        help="How long to show each capture in milliseconds. Default: 1000 (1s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    interval = max(0.5, args.interval)  # prevent spammy sub-second loops
    display_ms = max(100, args.display_ms)  # keep window at least 100ms

    print(f"[INFO] Capturing screen every {interval} seconds.")
    print(f"[INFO] Each capture is visible for {display_ms} ms in a temporary viewer.")
    print("[INFO] Press Ctrl+C in the terminal to stop.")

    try:
        while True:
            capture_and_show(display_ms=display_ms)

            # Sleep so that the total cycle time is approximately `interval`
            sleep_time = max(0.0, interval - display_ms / 1000.0)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")


if __name__ == "__main__":
    main()


