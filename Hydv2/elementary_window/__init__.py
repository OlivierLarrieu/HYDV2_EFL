# -*- coding:utf-8 -*-
__author__ = 'larrieu'
from efl import elementary
from efl.elementary.window import Window, ELM_WIN_BASIC, ELM_WIN_DESKTOP, ELM_WIN_DOCK

class _Window(object):
    def __init__(self, *args, **kwargs):
        try:
            title = kwargs['title']
        except:
            title = ""
        try:
            window_type = kwargs['window_type']
        except:
            window_type = ELM_WIN_BASIC
        try:
            width = kwargs['width']
        except:
            width = 500
        try:
            height = kwargs['height']
        except:
            height = 500
        try:
            pos_x = kwargs['pos_x']
        except:
            pos_x = 500
        try:
            pos_y = kwargs['pos_y']
        except:
            pos_y = 500
        try:
            transparent = kwargs['transparent']
        except:
            transparent = False

        self.win = Window("window-states",
                           window_type,
                           title=title,
                           autodel=True,
                           size=(width, height))

        self.win.move(pos_x, pos_y)
        self.win.callback_delete_request_add(lambda o: elementary.exit())
        self.win.alpha = transparent
        try:
            show = kwargs['show']
            if show:
                self.win.show()
            else:
                self.win.hide()
        except:
            self.win.hide()


