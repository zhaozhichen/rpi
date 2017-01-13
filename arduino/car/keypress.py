#!/usr/bin/env python
#https://rosettacode.org/wiki/Keyboard_input/Keypress_check#Python


class KeyPress:
    def __init__(self):
        import __future__
        import sys
        if sys.version_info.major < 3:
            import thread as _thread
        else:
            import _thread
        import time
        try:
            from msvcrt import getch  # try to import Windows version
            self._getch = getch
        except ImportError:
            # print "no msvcrt"
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
        self._quitKey = 'q'
        self._defaultHandler = lambda : None
        self._handlersMap = {}

    def registerHandlers(self,hMap):
        self._handlersMap = hMap;

    def registerDefaultHandler(self,handler):
        self._defaultHandler = handler

    def registerQuitKey(self,char):
        self._quitKey = char

    def start(self):
        # _thread.start_new_thread(pressFn, ())
        while True:
            self._char = self._getch()
            if self._char is not None:
                if self._char == self._quitKey:
                    break
                elif self._char in self._handlersMap:
                    self._handlersMap[self._char]()
            else:
                self._defaultHandler()
