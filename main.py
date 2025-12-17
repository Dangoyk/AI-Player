import argparse
import time

from pathlib import Path

from screenshot import capture_to_temp_png, show_temp_image
from ai_client import ask_ai_with_image, OpenAIConfigError

import tkinter as tk
from tkinter import messagebox


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


def show_text_popup(text: str) -> None:
    """
    Show the AI's response in a simple popup window.
    Blocks until the user closes it.
    """
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("AI Suggestion", text)
    root.destroy()


def main() -> None:
    args = parse_args()
    interval = max(0.5, args.interval)  # prevent spammy sub-second loops
    display_ms = max(100, args.display_ms)  # keep window at least 100ms

    # Ask the user for their goal / command at startup
    goal = input(
        "Enter your goal/command for the AI "
        "(e.g. 'Get me into a Roblox match and ready to play'): "
    ).strip()
    if not goal:
        goal = "Help me figure out what to do next."

    print(f"[INFO] Capturing screen every {interval} seconds.")
    print(f"[INFO] Each capture is visible for {display_ms} ms in a temporary viewer.")
    print("[INFO] Press Ctrl+C in the terminal to stop.")

    try:
        while True:
            # Capture screen to temp PNG
            img_path = capture_to_temp_png()

            try:
                # Ask AI what to do next based on the screenshot
                answer = ask_ai_with_image(
                    img_path,
                    (
                        "You are helping me use this computer / play this game.\n"
                        f"My current goal is: {goal}\n"
                        "Look at the screenshot and tell me, in one short sentence, "
                        "what I should do next to move toward that goal."
                    ),
                )
                print(f"[AI] {answer}")
            except OpenAIConfigError as cfg_err:
                print(f"[ERROR] {cfg_err}")
                # Don't continue looping if config is bad
                break
            except Exception as exc:  # noqa: BLE001
                print(f"[ERROR] OpenAI request failed: {exc}")
                answer = "Error talking to AI. Check the console for details."

            # Show the latest image
            show_temp_image(img_path, display_ms=display_ms)

            # Show the AI response in a popup
            try:
                show_text_popup(answer)
            except Exception as exc:  # noqa: BLE001
                print(f"[WARN] Failed to show popup: {exc}")

            # Clean up temp file
            try:
                if img_path.exists():
                    img_path.unlink()
            except Exception:
                pass

            # Sleep so that the total cycle time is approximately `interval`
            sleep_time = max(0.0, interval - display_ms / 1000.0)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")


if __name__ == "__main__":
    main()


