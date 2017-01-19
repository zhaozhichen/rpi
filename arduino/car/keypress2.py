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
        self._isOn = True
        self._isMoving = False

    def registerHandlers(self,hMap):
        self._handlersMap = hMap;

    def registerDefaultHandler(self,handler):
        self._defaultHandler = handler

    def registerQuitKey(self,char):
        self._quitKey = char

    def run(self):
        # each cycle in while loop uses 0.1 sec, whithout the explicit sleep()
        while self._isOn:
            self._char=None
            self._char=self._getch()
            time.sleep(0.1)
        print "THRED STOPPED"

    # return False if quit is pressed
    def runHandler(self,key):
        if key in self._handlersMap:
            self._handlersMap[self._char]()
            self._isMoving = True
            return True
        elif self._char == self._quitKey:
            assert self._quitKey is not None
            self._isOn = False
            return False
        else:
            return True

    def start(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._thread.start()
        lastkey = None
        lastkeytime = time.time()
        while True:
            thistime = time.time()
            if self._char is not None:
                if not self._isMoving or self._char != lastkey:
                    if not self.runHandler(self._char):
                        # wait for thread to stop:
                        time.sleep(0.5)
                        return
                lastkey = self._char
                lastkeytime = thistime
            elif thistime-lastkeytime < 0.1:
                continue
            else:
                self._defaultHandler()
                self._isMoving = False

