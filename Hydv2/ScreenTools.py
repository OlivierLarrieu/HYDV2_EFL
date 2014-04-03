#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Olivier Larrieu'


class ScreenProperties(object):
    """
     Usefull to get basic screen informations
    """

    @classmethod
    def screen_dimension(cls):
        """
            Return a dic with the screen height and screen width
        """
        from Xlib import display
        display = display.Display()
        root = display.screen().root
        desktop = root.get_geometry()

        return {'width': desktop.width, 'height': desktop.height}