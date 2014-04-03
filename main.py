#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'olivier larrieu'

import sys
from efl import elementary
if __name__ == "__main__":
    try:
        from efl import elementary
    except ImportError:
        print "Please check if python EFL 1.9 is installed or do not launch directly Hydv2 from here."
        sys.exit(1)
    from Hydv2.Panel import Panel
    from Hydv2.Backround import BackgroundWindow
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("--disable_background", dest="background",
                      help="Disable the background.")

    (options, args) = parser.parse_args()

    # elementary initialisation
    elementary.init()

    # The panel implementation
    panel = Panel()

    if options.background:
        print("Background disable.")
    else:
        print("Background enable.")
        # The background implementation
        background = BackgroundWindow()

    # elementary loop
    elementary.run()
    elementary.shutdown()
