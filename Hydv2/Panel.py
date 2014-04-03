#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Olivier Larrieu'

import os

from efl.elementary.grid import Grid
from efl.elementary.icon import Icon
from efl.elementary.clock import Clock
from efl.elementary.button import Button
from efl.elementary.window import ELM_WIN_DOCK
from efl.elementary.background import Background
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL

import ScreenTools
from AppsWindow import AppsMenu
from elementary_window import _Window


EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL

screen_x = ScreenTools.ScreenProperties.screen_dimension()['width']
screen_y = ScreenTools.ScreenProperties.screen_dimension()['height']

DEBUG = False
LOGO = os.path.dirname(__file__) + "/Images/Logo_.png"


class Panel(object):
    """
        The panel of Hydv2
            - full width
            - menu button
            - top and bottom position buttons
            - clock
            - favarites applications place
    """
    def __init__(self, *args, **kwargs):
        # starting point for favorites apps
        self.favorite_apps_start_point = 270

        # Applications Menu Window
        self.apps_window = AppsMenu(self)
        self.apps_window.is_open = False
        
        # position of panel on the screen TODO: configuration file
        self.screen_position = "top"

        # principal panel window
        self.window = _Window(title="",
                              window_type=ELM_WIN_DOCK,
                              width=screen_x,
                              height=40,
                              pos_x=0,
                              pos_y=0,
                              show=True,
                              transparent=False).win
        # the popup window
        self.popup = _Window(title="",
                             window_type=ELM_WIN_DOCK,
                             width=200,
                             height=20,
                             pos_x=0,
                             pos_y=0,
                             show=False,
                             transparent=False).win

        # the principal panel window background
        self.window_background = Background(self.window,
                                            size_hint_weight=EXPAND_BOTH)
        self.window_background.show()
        self.window.resize_object_add(self.window_background)

        # the popup background
        self.popup_background = Background(self.popup,
                                           size_hint_weight=EXPAND_BOTH)
        self.popup_background.show()
        self.popup.resize_object_add(self.popup_background)

        # the principal window grid
        self.window_grid = Grid(self.window, size=(screen_x, 40),
                                size_hint_weight=EXPAND_BOTH,
                                size_hint_align=FILL_BOTH)
        self.window.resize_object_add(self.window_grid)
        self.window_grid.show()

        # the menu button
        menu_button_icon = Icon(self.window, scale=2,
                                file=LOGO, resizable=(False, False),
                                size_hint_weight=EXPAND_BOTH, )
        button_hymenu = Button(self.window,
                               text="HyMenu",
                               content=menu_button_icon)
        button_hymenu.callback_clicked_add(self.show_menu)
        self.window_grid.pack(button_hymenu, 0, 0, 110, 40)
        button_hymenu.show()
        menu_button_icon.show()

        #====================== TODO ==================================#
        # the Hybryde button
        button_hybryde = Button(self.window, text="Hybryde")
        self.window_grid.pack(button_hybryde, 110, 0, 100, 20)
        button_hybryde.show()

        # the Magic button
        button_magic = Button(self.window, text="Magic")
        self.window_grid.pack(button_magic, 110, 20, 100, 20)
        button_magic.show()
        #====================== END TODO ==============================#

        # the top button
        button_top = Button(self.window, text="top")
        button_top.callback_clicked_add(self.top)
        self.window_grid.pack(button_top, 110, 0, 142, 20)
        button_top.show()

        # the bottom button
        button_bottom = Button(self.window, text="bottom")
        button_bottom.callback_clicked_add(self.bottom)
        self.window_grid.pack(button_bottom, 110, 20, 142, 20)
        button_bottom.show()

        # the clock
        self.clock = Clock(self.window, show_seconds=True)
        self.window_grid.pack(self.clock, screen_x - 60, 10, 60, 20)
        self.clock.show()

        # reserve space on the screen
        from Xlib import display
        self.disp = display.Display()
        self.reserve_win = self.disp.create_resource_object('window', self.window.xwindow_xid)
        self.top(None)

    def add_fav_app(self, datas):
        """
            Calling by self.apps_window and panel initialisation
            Add the favorite apps in the bar
            datas is a dic like this {"name":string, "icon": path, "command": string, "callback": function}
        """
        new_icon = Icon(self.window,
                        file=datas['icon'],
                        resizable=(True, True), size=(30, 30),
                        size_hint_weight=EXPAND_BOTH,
                        size_hint_align=FILL_BOTH)
        new_icon.callback_clicked_add(self.launch_app, datas['command'])
        self.window_grid.pack(new_icon, self.favorite_apps_start_point, 5, 30, 30)
        new_icon.on_mouse_in_add(self.mouseover)
        new_icon.on_mouse_out_add(self.mouseout)
        new_icon.pos = (self.favorite_apps_start_point, 0)
        new_icon.show()
        self.favorite_apps_start_point += 35

    def mouseover(self, icon, y):
        """
            mouseover event of favorite apps icons
        """
        icon.size = (28, 28)
        self.popup.move(icon.pos[0] - 80, 50)
        self.popup.show()

    def mouseout(self, icon, y):
        """
            mouseout event of favorite apps icons
        """
        icon.size = (30, 30)
        self.popup.hide()

    def launch_app(self, emitter, command):
        os.system('cd $HOME;'+command + ' &')

    def top(self, emitter):
        self.reserve_win.change_property(self.disp.intern_atom('_NET_WM_STRUT'),
                                         self.disp.intern_atom('CARDINAL'),
                                         32,
                                         [0, 0, 40, 0])
        self.disp.sync()

        self.apps_window.window.move(0, 40)
        self.window.move(0, 0)
        self.screen_position = "top"

    def bottom(self, emitter):
        self.reserve_win.change_property(self.disp.intern_atom('_NET_WM_STRUT'),
                                         self.disp.intern_atom('CARDINAL'),
                                         32,
                                         [0, 0, 0, 40])
        self.disp.sync()

        self.apps_window.window.move(0, screen_y - 440)
        self.window.move(0, screen_y - 40)
        self.screen_position = "bottom"

    def show_menu(self, emitter):
        if self.screen_position == "top":
            self.apps_window.window.move(0, 40)
        else:
            self.apps_window.window.move(0, screen_y - 440)
        if self.apps_window.is_open:
            self.apps_window.window.hide()
            self.apps_window.is_open = False
        else:
            self.apps_window.window.show()
            self.apps_window.is_open = True

    def reserve_spaces(self):
        #reserve space on top and bottom of the screen with Xlib
        from Xlib import display

        disp = display.Display()
        reserve_win = disp.create_resource_object('window',
                                                  self.window.xwindow_xid)
        reserve_win.change_property(disp.intern_atom('_NET_WM_STRUT'),
                                         disp.intern_atom('CARDINAL'),
                                         32,
                                         [0, 0, 40, 40])
        disp.sync()
