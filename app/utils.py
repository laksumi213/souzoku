import os
from pathlib import Path
import platform
import configparser

if platform.system() == 'Windows':
    import ctypes
else:
    import subprocess


def ime_on():
    # print('platform.system():', platform.system())
    if platform.system() == 'Windows':
        user32 = ctypes.WinDLL(name="user32")
        imm32 = ctypes.WinDLL(name="imm32")
        h_wnd = user32.GetForegroundWindow()
        h_imc = imm32.ImmGetContext(h_wnd)
        imm32.ImmSetOpenStatus(h_imc, True)
        imm32.ImmReleaseContext(h_wnd, h_imc)
        # print('Windows ime_on')
    else:
        # applescript = r'tell application "System Events" to keystroke (key code {104})'
        # subprocess.run(["osascript", "-e", applescript])
        applescript = '''
        tell application "System Events"
            keystroke (key code {104})
        end tell
        '''
        subprocess.Popen(['osascript', '-e', applescript])
        # print('mac ime_on')


def ime_off():
    if platform.system() == 'Windows':
        user32 = ctypes.WinDLL(name="user32")
        imm32 = ctypes.WinDLL(name="imm32")
        h_wnd = user32.GetForegroundWindow()
        h_imc = imm32.ImmGetContext(h_wnd)
        imm32.ImmSetOpenStatus(h_imc, False)
        imm32.ImmReleaseContext(h_wnd, h_imc)
    else:
        applescript = r'tell application "System Events" to keystroke (key code 102)'  # IME OFF
        subprocess.run(["osascript", "-e", applescript])


def get_parent_path():
    return Path(os.path.dirname(__file__)).parent


def get_database_path():
    parent_path = get_parent_path()
    return str(Path(parent_path, 'database', 'inheritance.db'))


def get_config_path():
    return str(Path(get_parent_path(), 'config', 'config.ini'))


def read_config():
    config = configparser.ConfigParser()
    config.read(get_config_path(), encoding='CP932')
    return config
