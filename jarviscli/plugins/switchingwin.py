import os
from plugin import plugin, require


@require(native='wmctrl')
@plugin
def go_to(jarvis, s):
    os.system("wmctrl -a " + s)  # switch to already opened app/software.


@require(native='wmctrl')
@plugin
def workspace(jarvis, s):
    if s == 'one':
        s = 1
    num = str(int(s) - 1)
    os.system("wmctrl -s " + num)  # switch workspace.


@plugin
def run(jarvis, s):
    os.system(s)  # run the command in terminal.
