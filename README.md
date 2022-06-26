# Virtual env (optional)
```shell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

# Install requirements
```shell
pip3 install pyserial numpy appjar scipy pyofdm
python -m pip install -U matplotlib
```

# Run
```shell
python gui.py
```

# Create exe
Attention!
Comment out:
```shell
.\venv\Lib\site-packages\komm\__init__.py, line 21:
__version__ = _get_distribution('komm').version
```
Do:
```shell
pip3 install pyinstaller
python -O -m PyInstaller --windowed --onefile gui.py
```
