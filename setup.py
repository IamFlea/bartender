from cx_Freeze import setup, Executable
import os
#os.environ['TCL_LIBRARY'] = 'c:\\Users\\Flea\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6'
#os.environ['TK_LIBRARY'] = 'c:\\Users\\Flea\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6'

executables = [Executable("bartender.py", base = "Win32GUI")]

packages = ["pygame",
            "win32api",
            "win32con",
            "win32gui",
            "win32ui",
            "PIL",
            "cv2",
            "numpy",
            ## modules
            "research_queue",
            "screen_parser",
            "screenshooter",
            "pygame_window",
            "technologies",
            "os"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files': ["icon.png", "georgia.ttf", "georgiab.ttf"]
    },


}

setup(
    name = "AoE II - Bartender",
    options = options,
    version = "0.0",
    description = 'AoE II - Bartender',
    executables = executables
)
