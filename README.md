# yt-dlp-wrapper
 Basic GUI for yt-dlp

# Windows
Uncomment/comment line for windows and run as normal.

# Linux
Uncomment/comment line for linux, install `powershell-bin` from `AUR` with `yay` and run `setup.ps1` in `powershell`.

After running `setup.ps1`, you can run `source .venv\bin\activate` in `bash` to activate `venv` in `bash`

# pyinstaller
- Need to add `--hidden-import='PIL._tkinter_finder'` to the command or you will get
>ModuleNotFoundError: No module named 'PIL._tkinter_finder'

- Copy `asssets` folder into `dist/<programname>/` so the asset can be found

Example: `pyinstaller test.py --hidden-import='PIL._tkinter_finder'`