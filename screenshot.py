import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import mss
from mss import tools


def capture_to_temp_png() -> Path:
    """
    Capture the primary monitor to a temporary PNG file.

    Returns the path to the temp file. Caller is responsible for deleting it.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp_path = Path(tmp.name)

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        sct_img = sct.grab(monitor)
        tools.to_png(sct_img.rgb, sct_img.size, output=str(tmp_path))

    return tmp_path


def show_temp_image(image_path: Path, display_ms: int = 1000) -> None:
    """
    Show an image file in a temporary viewer (mspaint on Windows) for display_ms milliseconds,
    then close the viewer. Does NOT delete the file.
    """
    viewer_proc: Optional[subprocess.Popen] = None

    try:
        # On Windows, use mspaint so we can kill it afterward
        viewer_proc = subprocess.Popen(["mspaint", str(image_path)])

        msec = max(100, display_ms)
        seconds = msec / 1000.0

        import time

        time.sleep(seconds)
    finally:
        if viewer_proc and viewer_proc.poll() is None:
            try:
                viewer_proc.terminate()
            except Exception:
                pass


