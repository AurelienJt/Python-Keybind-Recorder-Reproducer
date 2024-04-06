# Python Keybind Recorder & Reproducer
This program allows users to record keybinds and reproduce them by executing a python script, generated from a recording of the pressed keybinds. It uses the pydirectinput library in order to use scancodes instead of VK's. **Only works for windows.**
## How it Works
Make sure to install the latest release from the release tab.
0. Open a new powershell/command prompt window.
1. Navigate to the project directory: `Path/To/The/Project/Python-Keybind-Recorder-Reproducer/`
2. Run: `pip install -r requirements.txt` in order to install the dependencies.
3. Navigate into the `/src/` folder.
4. Launch `py_key_rep_rec.py` with `python py_key_rec_rep.py <filepath>` Leave `<filepath>` empty to create a `/Recordings/` directory.
5. A window should appear. Make sure it is focused and input your keybind.
6. Press escape or close the window manually to finish the recording.
7. The filepath of your generated file can be found in the terminal.
## Help & Issues
If you encounter issues or would like to request some help, please feel free to submit an issue.

