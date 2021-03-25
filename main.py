
from cefpython3 import cefpython as cef
import platform
import sys
from threading import Thread
import uvicorn

import server

def launch_cef():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url="http://localhost:8000/",
                          window_title="Wikimedia Italia - Invio PEC")
    cef.MessageLoop()
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
    t2.start()