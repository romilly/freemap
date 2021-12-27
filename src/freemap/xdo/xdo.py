
import subprocess
import os
from time import sleep


FREEPLANE = '/home/romilly/library/freeplane-1.9.12/freeplane.sh'
PROJECT_HOME = '/home/romilly/git/active/freemap'
DATA_DIR = os.path.join(PROJECT_HOME, 'data')
for fn in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, fn)
    if os.path.isfile(path) and fn.endswith('.png'):
        os.remove(path)


class WindowNotFound(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class Xdo:
    def __init__(self, window_name, path_to_app, *app_params):
        self.window_name = window_name
        self.path_to_app = path_to_app
        self.app_params = app_params

    def activate_window(self):
        return subprocess.call(["xdotool", "search", "--sync", "--name", self.window_name, "windowactivate"],
                               stderr=open('/dev/null'))

    def open_app(self):
        so = open('/dev/null')
        params = [self.path_to_app] + list(self.app_params)
        print('opening app with %s' % params)
        subprocess.Popen(params
                         ,stdout=so, stderr=so
                         )

    def export_png(self):
        subprocess.call(["xdotool", "search", "--name", self.window_name, "windowactivate"])
        subprocess.call(["xdotool", "key", "alt+f", "alt+e", "Return"])

    def open_map(self, name):
        self.activate_window()
        sleep(0.1)
        subprocess.call(["xdotool", "key", "ctrl+o", "type", name,])
        subprocess.call(["xdotool", "key","Return"])

    # def close_current_map(self):
    #     subprocess.call(["xdotool", "search", "--name", self.window_name, "windowactivate"])
    #     sleep(0.1)
    #     subprocess.call(["xdotool", "key", "Escape", "ctrl+w"])

    def quit_app(self):
        self.activate_window()
        sleep(0.1)
        # the next command closes the app without cleanup
        subprocess.call(["xdotool", "search", "--sync", "--name", self.window_name, "windowactivate", "windowclose"])
        # so we need to remove the single instance lock
        os.remove('%s/1.9.x/single_instance.lock' % PROJECT_HOME)


xdo = Xdo('Freeplane', FREEPLANE, '-U%s' % PROJECT_HOME, '%s/data/Mindmap.mm' % PROJECT_HOME)
xdo.open_app()
sleep(5)
# # xdo.wait_for_window()
#
# xdo.open_map('Mindmap.mm')
xdo.export_png()
#
#
# xdo.open_map('test1.mm')
# #sleep(1)
# xdo.export_png()
# #
# # # xdo.close_current_map()
# # sleep(2)
# print('closing app')
# xdo.quit_app()






