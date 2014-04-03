#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Olivier Larrieu'

import ScreenTools
from Hydv2.elementary_window import _Window
from efl.elementary.grid import Grid
from efl.elementary.background import Background
from efl.elementary.window import ELM_WIN_DESKTOP
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL
import os

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL

screen_x = ScreenTools.ScreenProperties.screen_dimension()['width']
screen_y = ScreenTools.ScreenProperties.screen_dimension()['height']

BACKGROUND_FILE = os.path.dirname(__file__) +"/Images/Fusion.png"


class BackgroundWindow(object):
    """
        Display a full screen background window .
        The window type hint is Desktop, so under all other windows.
    """

    def __init__(self):
        # principal window construction
        self.window = _Window(title="",
                              window_type=ELM_WIN_DESKTOP,
                              width=screen_x,
                              height=screen_y,
                              pos_x=0,
                              pos_y=0,
                              show=True)

        # principal window grid
        self.window_grid = Grid(self.window.win, size=(screen_x, screen_y), size_hint_weight=EXPAND_BOTH,
                                size_hint_align=FILL_BOTH)
        self.window.win.resize_object_add(self.window_grid)
        self.window_grid.show()

        # the window background with image
        self.window_background = Background(self.window.win, file=BACKGROUND_FILE, size_hint_weight=EXPAND_BOTH)
        self.window_grid.pack(self.window_background, 0, 0, screen_x, screen_y)
        self.window_background.show()