#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Olivier Larrieu'

from gtk import gdk


class ScreenProperties(object):
    """
     Usefull to get basic screen informations
    """

    @classmethod
    def screen_dimension(cls):
        """
            Return a dic with the screen height and screen width
        """
        width = gdk.screen_width()
        height = gdk.screen_height()
        return {'width': width, 'height': height}