#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Olivier Larrieu'

import ScreenTools
import HydvMenu
import os
from Hydv2.elementary_window import _Window
from efl.elementary.grid import Grid
from efl.elementary.box import Box
from efl.elementary.icon import Icon
from efl.elementary.list import List
0

from efl.elementary.background import Background
from efl.elementary.window import ELM_WIN_DOCK

from efl.elementary.genlist import Genlist, GenlistItemClass, \
                                   ELM_GENLIST_ITEM_NONE, ELM_GENLIST_ITEM_GROUP, \
                                   ELM_OBJECT_SELECT_MODE_DISPLAY_ONLY
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL, \
                     EVAS_ASPECT_CONTROL_VERTICAL


EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL

screen_x = ScreenTools.ScreenProperties.screen_dimension()['width']
screen_y = ScreenTools.ScreenProperties.screen_dimension()['height']

ADD_ICON = os.path.dirname(__file__) + "/Images/add.png"


class ItemClass(GenlistItemClass):
    # override GenlisItemClass for integrate icons in item
    def content_get(self, obj, part, datas):
        if part == "elm.edit.icon.2":
            # add favorite apps icon
            icon = Icon(obj, file=ADD_ICON,
                      propagate_events=False,
                      size_hint_aspect=(EVAS_ASPECT_CONTROL_VERTICAL, 2, 1))
            # connect icon click to callback function
            icon.callback_clicked_add(datas['callback'], datas)

            return icon
        elif part == "elm.edit.icon.1":
            # icon of the application
            try:
                icon = Icon(obj, file=datas['icon'],
                           propagate_events=False,
                           size_hint_aspect=(EVAS_ASPECT_CONTROL_VERTICAL, 1, 1))

                return icon
            except:
                return
        else:
            return


class AppsMenu(object):
    def __init__(self, Bar):
        # bar is here for interact with favorites apps place
        # in waiting a dbus implementation
        # TODO : I do not know yet how to integrate a dbus service in the elementary loop
        self.Bar = Bar

        # principal menu window
        self.window = _Window(title="",
                              window_type=ELM_WIN_DOCK,
                              width=250,
                              height=400,
                              pos_x=10,
                              pos_y=screen_y - 440,
                              show=False,
                              transparent=False).win
        self.window.move(0, 40)

        # the principal menu window background
        self.window_bg = Background(self.window, size_hint_weight=EXPAND_BOTH)
        self.window.resize_object_add(self.window_bg)
        self.window_bg.show()

        # principal window grid
        self.window_grid = Grid(self.window, size=(250, 410), size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.window.resize_object_add(self.window_grid)
        self.window_grid.show()

        self.window_list_box = Box(self.window, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.window_grid.pack(self.window_list_box, 5, 5, 245, 400)
        self.window_list_box.show()

        self.window_list = List(self.window, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        self.window_list_box.pack_end(self.window_list)
        self.window_list.show()

        self.application_list = Genlist(self.window, size_hint_align=FILL_BOTH, size_hint_weight=EXPAND_BOTH)
        self.application_list.decorate_mode = True
        self.window.resize_object_add(self.application_list)
        self.application_list.show()

        self.application_header = ItemClass(item_style="default", decorate_all_item_style="edit",
                                            text_get_func=self.gl_text_get)
        self.category_header = GenlistItemClass(item_style="group_index",
                                                text_get_func=self.glg_text_get,
                                                content_get_func=self.glg_content_get)

        # generate the list of all applications
        self.generate_applications_list()

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
        # sort categories in alphabetic order TODO : directly in  HydvMenu.HydvDesktopEntries
        categories.sort()
        for item in categories:
            self.git = self.application_list.item_append(self.category_header,
                                                         {'name': item,
                                                          'icon': HydvMenu.HydvDesktopEntries.findicon(item)},
                                                         flags=ELM_GENLIST_ITEM_GROUP)
            self.git.select_mode_set(ELM_OBJECT_SELECT_MODE_DISPLAY_ONLY)
            # sort applications in alphabetic order TODO : directly in  HydvMenu.HydvDesktopEntries
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

    def add_fav_apps(self, element, datas):
        self.Bar.add_fav_app(datas)


    def launch_app(self, li, element, args):
        # disable the clicked line, or this is staying selected
        li.selected = False
        os.system('cd $HOME;'+args['command'] + ' &')