#!/usr/bin/env python
#https://rosettacode.org/wiki/Keyboard_input/Keypress_check#Python

import sys
import threading
import time

class KeyPress:
    def __init__(self):
        def getch():   # define non-Windows version
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        self._getch = getch
        self._char = None
        self._quitKey = None
        self._defaultHandler = lambda : None
        self._handlersMap = {}

    def registerHandlers(self,hMap):
        self._handlersMap = hMap;

    def registerDefaultHandler(self,handler):
        self._defaultHandler = handler

    def registerQuitKey(self,char):
        self._quitKey = char

    def run(self):
        while True:
            self._char=None
            self._char=self._getch()
            time.sleep(1)

    def start(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._thread.start()
        while True:
            if self._char is not None:
                if self._quitKey is not None and self._char == self._quitKey:
                    return
                elif self._char in self._handlersMap:
                    self._handlersMap[self._char]()
            else:
                self._defaultHandler()
            time.sleep(0.0)
