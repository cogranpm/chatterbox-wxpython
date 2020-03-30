# a class that wraps the objectlistview control
import wx
import wx.xrc
from ObjectListView import ObjectListView, ColumnDefn


class CustomList(ObjectListView):

    def __init__(self, *args, **kwargs):
        super().__init__(self, args, kwargs)
