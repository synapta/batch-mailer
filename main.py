
from cefpython3 import cefpython as cef
import ctypes
import os
import platform
import sys
from threading import Thread
import uvicorn
import time

import app.server as server

def cef_settings():
    if hasattr(sys, '_MEIPASS'):
        # settings when packaged
        settings = {'locales_dir_path': os.path.join(sys._MEIPASS, 'locales'),
                    'resources_dir_path': sys._MEIPASS,
                    'browser_subprocess_path': os.path.join(sys._MEIPASS, 'subprocess.exe')}
    else:
        # settings when unpackaged
        settings = {}
    
    return settings

def launch_cef():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize(settings=cef_settings())
    browser = cef.CreateBrowserSync(url="http://localhost:8000/",
                          window_title="Wikimedia Italia - Invio PEC")
    
    if platform.system() == "Windows":
        window_handle = browser.GetOuterWindowHandle()
        insert_after_handle = 0
        # X and Y parameters are ignored by setting the SWP_NOMOVE flag
        SWP_NOMOVE = 0x0002
        # noinspection PyUnresolvedReferences
        ctypes.windll.user32.SetWindowPos(window_handle, insert_after_handle,
                                          0, 0, 900, 640, SWP_NOMOVE)
    cef.MessageLoop()
    del browser
    cef.Shutdown()


def check_versions():
    ver = cef.GetVersion()
    print("[main.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[main.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[main.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[main.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


def launch_unicorn():
    uvicorn.run(server.app, host="127.0.0.1", port=8000, reload=False)


if __name__ == '__main__':
    t1 = Thread(target=launch_unicorn)
    t2 = Thread(target=launch_cef)
    t1.start()
    time.sleep(3)
    t2.start()
