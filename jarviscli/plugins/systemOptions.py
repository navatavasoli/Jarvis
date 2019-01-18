import os
from platform import architecture, dist, release, mac_ver
from platform import system as sys
from colorama import Fore, Style
from plugin import LINUX, MACOS, PYTHON2, PYTHON3, plugin


@plugin(plattform=MACOS, native="pmset")
def screen_off__MAC(jarvis, s):
    """Turn of screen instantly"""
    os.system('pmset displaysleepnow')


@plugin(plattform=LINUX, native="xset")
def screen_off__LINUX(jarvis, s):
    """Turn of screen instantly"""
    os.system('xset dpms force off')


@plugin(plattform=MACOS)
def Os__MAC(jarvis, s):
    """Displays information about your operating system"""
    jarvis.say(Style.BRIGHT + '[!] Operating System Information' + Style.RESET_ALL, Fore.BLUE)
    jarvis.say('[*] Kernel: ' + sys(), Fore.GREEN)
    jarvis.say('[*] Kernel Release Version: ' + release(), Fore.GREEN)
    jarvis.say('[*] macOS System version: ' + mac_ver()[0], Fore.GREEN)
    for _ in architecture():
        if _ is not '':
            jarvis.say('[*] ' + _, Fore.GREEN)


@plugin(plattform=LINUX)
def Os__LINUX(jarvis, s):
    """Displays information about your operating system"""
    jarvis.say('[!] Operating System Information', Fore.BLUE)
    jarvis.say('[*] ' + sys(), Fore.GREEN)
    jarvis.say('[*] ' + release(), Fore.GREEN)
    jarvis.say('[*] ' + dist()[0], Fore.GREEN)
    for _ in architecture():
        jarvis.say('[*] ' + _, Fore.GREEN)


@plugin(python=PYTHON3, plattform=LINUX)
def systeminfo__PY3_LINUX(jarvis, s):
    """Display system information with distribution logo"""
    from archey import archey
    archey.main()


@plugin(python=PYTHON3, plattform=MACOS, native="screenfetch")
def systeminfo__PY3_MAC(jarvis, s):
    """Display system information with distribution logo"""
    os.system("screenfetch")


@plugin(python=PYTHON2, native="screenfetch")
def systeminfo__PY2(jarvis, s):
    """Display system information with distribution logo"""
    os.system("screenfetch")
