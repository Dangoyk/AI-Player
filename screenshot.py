import os
import subprocess
import tempfile
from typing import Optional

import mss
from mss import tools


def capture_and_show(display_ms: int = 1000) -> None:
    """
    Capture the primary monitor, show it in a temporary window for display_ms milliseconds,
    then close the viewer and delete the image file.

    This implementation is Windows-focused and uses mspaint to display the image under our control.
    """
    # Create a temporary PNG file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp_path = tmp.name

    # Capture screen to that file
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        sct_img = sct.grab(monitor)
        tools.to_png(sct_img.rgb, sct_img.size, output=tmp_path)

    viewer_proc: Optional[subprocess.Popen] = None
    try:
        # On Windows, use mspaint so we can kill it afterward
        viewer_proc = subprocess.Popen(["mspaint", tmp_path])
        # Wait while the image is visible
        msec = max(100, display_ms)
        # Convert ms to seconds
        subprocess_time = msec / 1000.0
        # Simple sleep; user controls loop timing from main
        import time

        time.sleep(subprocess_time)
    finally:
        # Try to close the viewer
        if viewer_proc and viewer_proc.poll() is None:
            try:
                viewer_proc.terminate()
            except Exception:
                pass

        # Delete the temporary file
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            # If deletion fails, just ignore; OS will clean temp eventually
            pass


