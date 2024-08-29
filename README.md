# Installation
```pycon
pip install psutil pystray pypresence pillow auto-py-to-exe
```

# Run
```pycon
python main.py
```

# Info
1. After launching the program, an icon will appear in the tray. Right-click on it and select open
2. If you see the message Connected to Discord RPC successfully! - then the program is working
3. Open any program from the list in the file `programs.py `

# Build
1. Use `python -m auto_py_to_exe`
2. Add `assets/icon.ico` to additional files and to the folder with `main.exe`
3. OPTIONAL: With `inno-setup` compile the installer. Add `assets/icon.ico` everywhere!
