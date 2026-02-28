# encoding=utf-8
import time
from typing import Optional

# import pytest
from rich.console import Console
from rich.live import Live
from rich.text import Text


def create_capture_console(
    *, width: int = 60, height: int = 80, force_terminal: Optional[bool] = True
) -> Console:
    return Console(
        width=width,
        height=height,
        force_terminal=force_terminal,
        legacy_windows=False,
        color_system=None,  # use no color system to reduce complexity of output,
        _environ={},
    )


def test_live_state() -> None:
    with Live("") as live:
        assert live._started
        live.start()

        assert live.get_renderable() == ""

        assert live._started
        live.pause()
        assert live._paused and live._started
        live.resume()
        assert live._started and not live._paused
        live.stop()
        assert not live._started

    assert not live._started

def test_paused_resumed_refresh_thread() -> None:
     with Live("", auto_refresh= True) as live:
        live.start()
        live.pause()
        assert live._refresh_thread is None
        live.resume()
        assert live._refresh_thread is not None
        live.stop()
        

def test_pause_resume_twice() -> None:
    console = create_capture_console()
    console.begin_capture()
    with Live(console=console, auto_refresh=False) as live:
        live.start()
        live.pause()
        live.pause()
        assert live._paused
        live.resume()
        live.resume()
        assert not live._paused and live._started

def test_stop_after_pause() -> None:
    console = create_capture_console()
    console.begin_capture()
    with Live(console=console, auto_refresh=False) as live:
        live.start()
        live.pause()
        live.stop()
        assert not live._started and not live._paused

def test_pause_resume_transient_clears_display() -> None:
    console = create_capture_console()
    console.begin_capture()
    with Live(console=console, auto_refresh=False, transient=True) as live:
        live.update("Some content", refresh=True)
        console.end_capture()  # discard the render output
        console.begin_capture()  # start fresh
        live.pause()
        output_at_pause = console.end_capture()
        assert live._live_render._shape is None
        # restore cursor sequence should be present
        assert "\x1b[1A" in output_at_pause  # cursor moved up
        assert "\x1b[2K" in output_at_pause  # line cleared
        assert len(live.console._render_hooks) == 0 # render hooks should be cleared
        console.begin_capture()  # start again to check resume
        live.resume()
        output_at_resume = console.end_capture()
        assert "\x1b[?25l" in output_at_resume  # cursor hidden
        assert len(live.console._render_hooks) > 0 # render hooks should be re-added on resume

def test_pause_non_transient() -> None:
    console = create_capture_console()
    console.begin_capture()
    with Live(console=console, auto_refresh=False, transient=False) as live:
        live.update("Some content", refresh=True)
        console.end_capture()  # discard the render output
        console.begin_capture()  # start fresh
        live.pause()
        output_at_pause = console.end_capture()
    # restore cursor should be skipped for non-transient
    assert output_at_pause == "\x1b[?25h" 

def test_pause_transient_alt() -> None:
    console = create_capture_console()
    console.begin_capture()
    with Live(console=console, screen = True, auto_refresh=False, transient=True) as live:
        live.update("Some content", refresh=True)
        console.end_capture()  # discard the render output
        console.begin_capture()  # start fresh
        live.pause()
        output_at_pause = console.end_capture()
    # restore cursor should be skipped for alt screen
    assert output_at_pause == "\x1b[?25h" 

def test_pause_transient_jupyter() -> None:
    with Console(force_jupyter=True) as console:
        console.begin_capture()
        with Live(console=console, auto_refresh=False, transient=True) as live:
            live.update("Some content", refresh=True)
            console.end_capture()  # discard the render output
            console.begin_capture()  # start fresh
            live.pause()
            output_at_pause = console.end_capture()
            # restore cursor should be skipped in Jupyter
            assert output_at_pause == ""
            assert live._paused is True

def test_growing_display() -> None:
    console = create_capture_console()
    console.begin_capture()
    with Live(console=console, auto_refresh=False) as live:
        display = ""
        for step in range(10):
            display += f"Step {step}\n"
            live.update(display, refresh=True)
    output = console.end_capture()
    print(repr(output))
    assert (
        output
        == "\x1b[?25lStep 0\n\r\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\n\x1b[?25h"
    )


def test_growing_display_transient() -> None:
    console = create_capture_console()
    console.begin_capture()
    with Live(console=console, auto_refresh=False, transient=True) as live:
        display = ""
        for step in range(10):
            display += f"Step {step}\n"
            live.update(display, refresh=True)
    output = console.end_capture()
    assert (
        output
        == "\x1b[?25lStep 0\n\r\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\n\x1b[?25h\r\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K"
    )


def test_growing_display_overflow_ellipsis() -> None:
    console = create_capture_console(height=5)
    console.begin_capture()
    with Live(
        console=console, auto_refresh=False, vertical_overflow="ellipsis"
    ) as live:
        display = ""
        for step in range(10):
            display += f"Step {step}\n"
            live.update(display, refresh=True)
    output = console.end_capture()
    assert (
        output
        == "\x1b[?25lStep 0\n\r\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n                            ...                             \r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n                            ...                             \r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n                            ...                             \r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n                            ...                             \r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n                            ...                             \r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n                            ...                             \r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\n\x1b[?25h"
    )


def test_growing_display_overflow_crop() -> None:
    console = create_capture_console(height=5)
    console.begin_capture()
    with Live(console=console, auto_refresh=False, vertical_overflow="crop") as live:
        display = ""
        for step in range(10):
            display += f"Step {step}\n"
            live.update(display, refresh=True)
    output = console.end_capture()
    assert (
        output
        == "\x1b[?25lStep 0\n\r\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\n\x1b[?25h"
    )


def test_growing_display_overflow_visible() -> None:
    console = create_capture_console(height=5)
    console.begin_capture()
    with Live(console=console, auto_refresh=False, vertical_overflow="visible") as live:
        display = ""
        for step in range(10):
            display += f"Step {step}\n"
            live.update(display, refresh=True)
    output = console.end_capture()
    assert (
        output
        == "\x1b[?25lStep 0\n\r\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\n\x1b[?25h"
    )


def test_growing_display_autorefresh() -> None:
    """Test generating a table but using auto-refresh from threading"""
    console = create_capture_console(height=5)
    console.begin_capture()
    with Live(console=console, auto_refresh=True, vertical_overflow="visible") as live:
        display = ""
        for step in range(10):
            display += f"Step {step}\n"
            live.update(display)
            time.sleep(0.2)

    # no way to truly test w/ multithreading, just make sure it doesn't crash


def test_growing_display_console_redirect() -> None:
    console = create_capture_console()
    console.begin_capture()
    with Live(console=console, auto_refresh=False) as live:
        display = ""
        for step in range(10):
            console.print(f"Running step {step}")
            display += f"Step {step}\n"
            live.update(display, refresh=True)
    output = console.end_capture()
    assert (
        output
        == "\x1b[?25lRunning step 0\n\r\x1b[2KStep 0\n\r\x1b[2K\x1b[1A\x1b[2KRunning step 1\nStep 0\n\r\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KRunning step 2\nStep 0\nStep 1\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KRunning step 3\nStep 0\nStep 1\nStep 2\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KRunning step 4\nStep 0\nStep 1\nStep 2\nStep 3\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KRunning step 5\nStep 0\nStep 1\nStep 2\nStep 3\nStep 4\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KRunning step 6\nStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KRunning step 7\nStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KRunning step 8\nStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KRunning step 9\nStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2KStep 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n\n\x1b[?25h"
    )


def test_growing_display_file_console() -> None:
    console = create_capture_console(force_terminal=False)
    console.begin_capture()
    with Live(console=console, auto_refresh=False) as live:
        display = ""
        for step in range(10):
            display += f"Step {step}\n"
            live.update(display, refresh=True)
    output = console.end_capture()
    assert (
        output
        == "Step 0\nStep 1\nStep 2\nStep 3\nStep 4\nStep 5\nStep 6\nStep 7\nStep 8\nStep 9\n"
    )


def test_live_screen() -> None:
    console = create_capture_console(width=20, height=5)
    console.begin_capture()
    with Live(Text("foo"), screen=True, console=console, auto_refresh=False) as live:
        live.refresh()
    result = console.end_capture()
    print(repr(result))
    expected = "\x1b[?1049h\x1b[H\x1b[?25l\x1b[Hfoo                 \n                    \n                    \n                    \n                    \x1b[Hfoo                 \n                    \n                    \n                    \n                    \x1b[?25h\x1b[?1049l"
    assert result == expected


def test_live_empty() -> None:
    """Regression test for https://github.com/Textualize/rich/issues/3796

    No NL should be written if there was nothing rendered.
    """

    from rich.console import Group

    console = create_capture_console(width=20, height=5)
    console.begin_capture()
    with Live(Group(), console=console, transient=True):
        pass
    result = console.end_capture()
    print(repr(result))
    assert "\n" not in result
    assert result == "\x1b[?25l\r\x1b[2K\x1b[?25h\r"
