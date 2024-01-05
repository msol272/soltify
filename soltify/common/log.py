"""
Soltify/Common/Log

Helper functions for printing messages to the console
"""
import ctypes

# Definitions used to change console output color
STD_OUTPUT_HANDLE = -11

COLOR_CODE_DEFAULT = 0x07  # White
COLOR_CODE_WARNING = 0x0E  # Light Yellow
COLOR_CODE_ERROR = 0x0C # Red

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
