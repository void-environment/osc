import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "socket", "threading", "yaml", "pythonosc", "webview", "clr"],
    "include_files": ["template/", "config.yaml"],
    "excludes": ["tkinter"]
}

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"  

setup(
    name="TestApp",
    version="1.0",
    description="Test OSC",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", base=base)]
)
