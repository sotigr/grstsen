import os
import threading
import webview

from time import time

window = None
class Api:
    def fullscreen(self):
        window.toggle_fullscreen()

    def save_content(self, content):
        filename = window.create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename[0], 'w') as f:
            f.write(content)

    def select_file(self, content):
        open_file_dialog(window)
        
    def ls(self):
        return os.listdir('.')


def get_entrypoint():
    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists('../gui/index.html'): # unfrozen development
        return '../gui/index.html'

    if exists('../Resources/gui/index.html'): # frozen py2app
        return '../Resources/gui/index.html'

    if exists('./gui/index.html'):
        return './gui/index.html'

    raise Exception('No index.html found')


def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

def set_state(name, value):
    if window != None:
        window.evaluate_js('window.pywebview.state && window.pywebview.state.set_{}("{}")'.format(name,value) )



entry = get_entrypoint()


def open_file_dialog(window):
    file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')

    result = window.create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
    )
    print(result)

@set_interval(1)
def update_ticker():
    set_state('ticker', time())

if __name__ == '__main__':
    window = webview.create_window('pywebview-react boilerplate', entry, js_api=Api())
    webview.start(update_ticker, debug=False)
