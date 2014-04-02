__author__ = 'larrieu'
__version__ = '0.1'

DEBUG = False
LOGO = "Images/Logo_.png"
BACKGROUND_FILE = "Images/Fusion.png"
ADD_ICON = "Images/add.png"

import os

import sys
import HydvMenu

sys.path.append(os.path.realpath('.') + '/EFL1.9/lib/python2.7/dist-packages/')

from gi.repository import Gdk

screen_x, screen_y = Gdk.Screen.width(), Gdk.Screen.height()

from efl import elementary
from efl.elementary.box import Box
from efl.elementary.icon import Icon
from elementary_window import _Window
from efl.elementary.window import Window, ELM_WIN_BASIC, ELM_WIN_DESKTOP, ELM_WIN_DOCK
from efl.elementary.background import Background
from efl.elementary.image import Image
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl.elementary.grid import Grid
from efl.elementary.button import Button
from efl.elementary.entry import Entry
from efl.elementary.layout import Layout
from efl.elementary.check import Check
from efl.elementary.frame import Frame
from efl.elementary.label import Label

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL, \
    EVAS_ASPECT_CONTROL_VERTICAL, Rectangle

from efl.elementary.genlist import Genlist, GenlistItem, GenlistItemClass, \
    ELM_GENLIST_ITEM_NONE, ELM_OBJECT_SELECT_MODE_ALWAYS, \
    ELM_OBJECT_SELECT_MODE_DEFAULT, ELM_GENLIST_ITEM_GROUP, \
    ELM_OBJECT_SELECT_MODE_DISPLAY_ONLY

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL

elementary.init()


class BackgroundWindow(object):
    def __init__(self):
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

        self.window_background = Background(self.window.win, file=BACKGROUND_FILE, size_hint_weight=EXPAND_BOTH)

        self.window_grid.pack(self.window_background, 0, 0, screen_x, screen_y)
        self.window_background.show()


class ItemClass(GenlistItemClass):
    def content_get(self, obj, part, data):
        if part == "elm.edit.icon.2":
            ic = Icon(obj, file=ADD_ICON,
                      propagate_events=False,
                      size_hint_aspect=(EVAS_ASPECT_CONTROL_VERTICAL, 1, 1))
            ic.callback_clicked_add(data['callback'], data)

            return ic
        elif part == "elm.edit.icon.1":
            try:
                icn = Icon(obj, file=data['icon'],
                           propagate_events=False,
                           size_hint_aspect=(EVAS_ASPECT_CONTROL_VERTICAL, 1, 1))

                return icn
            except:
                return
        else:
            return


class AppsMenu(object):
    def __init__(self, Bar):
        self.Bar = Bar
        self.window = _Window(title="",
                              window_type=ELM_WIN_DOCK,
                              width=250,
                              height=400,
                              pos_x=10,
                              pos_y=screen_y - 440,
                              show=False,
                              transparent=False).win
        self.window.move(0, 40)
        self.window_bg = Background(self.window, size_hint_weight=EXPAND_BOTH)
        self.window.resize_object_add(self.window_bg)
        self.window_bg.show()

        # principal window grid
        self.window_grid = Grid(self.window, size=(250, 410), size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.window.resize_object_add(self.window_grid)
        self.window_grid.show()

        from efl.elementary.list import List, ELM_LIST_LIMIT, ELM_LIST_COMPRESS

        self.window_list_box = Box(self.window, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        #self.window.resize_object_add(self.window_list_box)
        self.window_grid.pack(self.window_list_box, 5, 5, 245, 400)  #---
        self.window_list_box.show()

        self.window_list = List(self.window, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.window_list_box.pack_end(self.window_list)
        self.window_list.show()

        self.application_list = Genlist(self.window, size_hint_align=FILL_BOTH, size_hint_weight=EXPAND_BOTH)
        self.application_list.decorate_mode = True
        #self.application_list.select_mode = ELM_OBJECT_SELECT_MODE_ALWAYS

        self.window.resize_object_add(self.application_list)
        self.application_list.show()

        self.application_header = ItemClass(item_style="default", decorate_all_item_style="edit",
                                            text_get_func=self.gl_text_get)
        self.category_header = GenlistItemClass(item_style="group_index",
                                                text_get_func=self.glg_text_get,
                                                content_get_func=self.glg_content_get)

        self.generate_applications_list()
        self.count = 0

    def glg_content_get(self, a, part, data):
        try:
            ic = Icon(self.window, file=data['icon'],
                      size_hint_aspect=(EVAS_ASPECT_CONTROL_VERTICAL, 1, 1))
            ic.callback_clicked_add(self.test)
            return ic
        except:
            pass


    def gl_text_get(self, obj, part, item_data):
        return "%s" % (item_data['name'])


    def glg_text_get(self, obj, part, item_data):
        return "%s" % (item_data['name'])

    def generate_applications_list(self):
        apps_dic = HydvMenu.HydvDesktopEntries.get_applications()
        categories = [cat for cat in apps_dic]
        categories.sort()
        for item in categories:
            self.git = self.application_list.item_append(self.category_header,
                                                         {'name': item,
                                                          'icon': HydvMenu.HydvDesktopEntries.findicon(item)},
                                                         flags=ELM_GENLIST_ITEM_GROUP)
            self.git.select_mode_set(ELM_OBJECT_SELECT_MODE_DISPLAY_ONLY)
            apps_dic[item].sort()
            for cat in apps_dic[item]:
                for app in cat.keys():
                    try:
                        self.application_list.item_append(self.application_header,
                                                          {'name': cat[app]['name'], 'command': cat[app]['command'],
                                                           'icon': cat[app]['icon'], "callback": self.add_fav_apps},
                                                          self.git,
                                                          flags=ELM_GENLIST_ITEM_NONE, func=self.launch_app)
                        self.application_list.callback_drag_start_down_add(func=self.launch_app,
                                                                           args=cat[app]['command'])

                    except:
                        pass

    def add_fav_apps(self, a, datas):
        self.Bar.add_fav_app(datas)


    def launch_app(self, li, u, args):
        li.selected = False
        os.system(args['command'] + ' &')


class Bar(object):
    def __init__(self):
        # Applications Menu Window
        self.apps_window = AppsMenu(self)
        # Desktop Window
        self.background_window = BackgroundWindow()
        # principal window
        self.window = _Window(title="",
                              window_type=ELM_WIN_DOCK,
                              width=screen_x,
                              height=40,
                              pos_x=0,
                              pos_y=0,
                              show=True,
                              transparent=False).win

        self.popup = _Window(title="",
                              window_type=ELM_WIN_DOCK,
                              width=200,
                              height=20,
                              pos_x=0,
                              pos_y=0,
                              show=False,
                              transparent=False).win

        # principal window background
        self.window_background = Background(self.window, size_hint_weight=EXPAND_BOTH)
        self.window_background.show()
        self.window.resize_object_add(self.window_background)

        # principal window background
        self.popup_background = Background(self.popup, size_hint_weight=EXPAND_BOTH)
        self.popup_background.show()
        self.popup.resize_object_add(self.popup_background)

        # principal window grid
        self.window_grid = Grid(self.window, size=(screen_x, 40), size_hint_weight=EXPAND_BOTH,
                                size_hint_align=FILL_BOTH)
        self.window.resize_object_add(self.window_grid)
        self.window_grid.show()
        # Hymenu button
        menu_button_icon = Icon(self.window, scale=2, file=LOGO, resizable=(False, False),
                                size_hint_weight=EXPAND_BOTH, )
        button_hymenu = Button(self.window, text="HyMenu", content=menu_button_icon)
        button_hymenu.callback_clicked_add(self.show_menu)
        self.window_grid.pack(button_hymenu, 0, 0, 110, 40)
        button_hymenu.show()
        menu_button_icon.show()
        # Hybryde button
        button_hybryde = Button(self.window, text="Hybryde")
        self.window_grid.pack(button_hybryde, 110, 0, 100, 20)
        button_hybryde.show()
        # Magic button
        button_magic = Button(self.window, text="Magic")
        self.window_grid.pack(button_magic, 110, 20, 100, 20)
        button_magic.show()
        # top button
        button_top = Button(self.window, text="top")
        button_top.callback_clicked_add(self.top)
        self.window_grid.pack(button_top, 110, 0, 142, 20)
        button_top.show()
        # bottom button
        button_bottom = Button(self.window, text="bottom")
        button_bottom.callback_clicked_add(self.bottom)
        self.window_grid.pack(button_bottom, 110, 20, 142, 20)
        button_bottom.show()

        from efl.elementary.clock import Clock, ELM_CLOCK_EDIT_HOUR_DECIMAL, \
            ELM_CLOCK_EDIT_MIN_DECIMAL, ELM_CLOCK_EDIT_SEC_DECIMAL

        self.clock = Clock(self.window, show_seconds=True)
        self.window_grid.pack(self.clock, screen_x - 60, 10, 60, 20)
        self.clock.show()

        self.open = False
        self.screen_position = "top"
        self.start_point = 270

    def add_fav_app(self, data):
        ic = Icon(self.window, file=data['icon'],
                  resizable=(True, True), size=(30, 30),
                  size_hint_weight=EXPAND_BOTH,
                  size_hint_align=FILL_BOTH)
        ic.callback_clicked_add(self.launch_app, data['command'])
        self.window_grid.pack(ic, self.start_point, 5, 30, 30)
        ic.on_mouse_in_add(self.mouseover)
        ic.on_mouse_out_add(self.mouseout)

        ic.pos =(self.start_point,0)

        ic.show()
        self.start_point += 35

    def mouseover(self, ic,y):
        ic.size = (32,32)
        self.popup.move(ic.pos[0]-80, 50)
        self.popup.show()

    def mouseout(self, ic,y):
        ic.size = (30,30)
        self.popup.hide()


    def launch_app(self, u, command):
        os.system(command + ' &')

    def top(self, e):
        self.apps_window.window.move(0, 40)
        self.window.move(0, 0)
        self.screen_position = "top"


    def bottom(self, e):
        self.apps_window.window.move(0, screen_y - 440)
        self.window.move(0, screen_y - 40)
        self.screen_position = "bottom"


    def resize(self, ic):
        ic.resize(10, 10)


    def show_menu(self, b):
        if self.screen_position == "top":
            self.apps_window.window.move(0, 40)
        else:
            self.apps_window.window.move(0, screen_y - 440)
        if self.open:
            self.apps_window.window.hide()
            self.open = False
        else:
            self.apps_window.window.show()
            self.open = True

if __name__ == "__main__":
    bar = Bar()
    elementary.run()
    elementary.shutdown()
