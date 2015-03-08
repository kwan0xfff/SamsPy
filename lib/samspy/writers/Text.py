#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""Text formatters for SamsPy reports.
"""

class Text:
    """Text formatters class.
    """

    def __init__(self, outstrm):
        """Text output formatters.
        outstrm is opened stream to use for output.
        """
        self.outstrm = outstrm

    def putitem(self, item):
        """Write a single item to output stream.
        """
        self.outstrm.write( item + '\n')
 
    def putfmtrow(self, label, fmt, datalist):
        """Write a report row with label, format, datalist.
        All labels have a common width.
        """
        line = "    %-24s" % label
        for item in datalist:
            line = line + ' ' + fmt % item
        self.outstrm.write( line + '\n')

#set sw=4 tw=80 :
