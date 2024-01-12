"""
Soltify/Common/Log

Helper functions for printing messages to the console
"""
import ctypes
import shutil
import sys
import time

# Definitions used to change console output color
STD_OUTPUT_HANDLE = -11

COLOR_CODE_DEFAULT = 0x07  # White
COLOR_CODE_WARNING = 0x0E  # Light Yellow
COLOR_CODE_ERROR = 0x0C # Red

PROGRESS_BAR_FILL = '█'

g_start_time = time.time()

def _print_colored(text, color_code):
    """
    Print text in a specified color
    """
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color_code)
    print(text)
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, COLOR_CODE_DEFAULT)

def warning(msg):
    """
    Print a warning message
    """
    _print_colored(f"WARNING: {msg}", COLOR_CODE_WARNING)

def error(msg):
    """
    Print an error message
    """
    _print_colored(f"ERROR: {msg}", COLOR_CODE_ERROR)

def show_progress(progress, total):
    """
    Print a progress bar to console
    """
    global g_start_time

    if progress == 0:
        g_start_time = time.time()

    # The progress bar is the console width minus the number of characters of text in it
    # "Progress: [" = 11
    # "] 100.00% elapsed time: 00:00" = 29
    bar_width = shutil.get_terminal_size()[0] - (11 + 29 + 1)
    percentage = progress / total * 100.0
    progress_length = int(bar_width * progress / total)
    bar = PROGRESS_BAR_FILL * progress_length + ' ' * (bar_width - progress_length)

    elapsed = time.time() - g_start_time
    minutes = int(elapsed / 60)
    seconds = int(elapsed % 60)
    sys.stdout.write(f'\rProgress: [{bar}] {percentage:.2f}%  elapsed time: {minutes}:{seconds:02d}')
    sys.stdout.flush()
    # Add new line when we hit 100%
    if progress == total:
        print()

def prompt_user(text):
    """
    Prompt the user with a yes or no question at the console and return True or False
    """
    prompt = f"{text} [y/N] "
    user_response = input(prompt).strip().lower()
    return user_response == "y"
