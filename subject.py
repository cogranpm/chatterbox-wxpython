import wx
import logging
import chatterbox_constants as c
import wx.dataview as dv
import forms as frm
from lists import states, ColumnSpec, ColumnType, ListSpec
from validators import FieldValidator, CheckboxValidator, ComboValidator, not_empty
import wx.py as py
from models import ViewState
from forms import FormSpec, FormDialog, FormLineSpec, edit_line, large, TextField

collection_name = c.COLLECTION_NAME_SUBJECT
name_column = 'name'

def create_data(db):
    records = db.all(collection_name)
    list = []
    for record in records:
        list.append(record)
    return list


def add_record():
    return {'id': None, 'name': ''}

class SubjectPanel(wx.Panel):
    """ shows a list of shelves and all the children """
    def __init__(self, parent=None):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.db = wx.GetApp().datastore
        self.db.create_entity(collection_name)

        # goes into base class
        main_sizer = frm.vsizer()
        self.SetSizer(main_sizer)

        shelf_header_panel = frm.panel_header(self, "pnlShelfHeader", "Shelf", self.add_shelf, self.delete_shelf, self.edit_shelf)
        main_sizer.Add(shelf_header_panel, 0, 0, 5)

        # this should be parameter of the class perhaps
        # create_data would be call to database
        self.listspec = ListSpec([
            ColumnSpec(name_column, ColumnType.str, 'Name', 100, True)
        ], create_data(self.db))

        # base class
        self.list = self.listspec.build(self, self.list_selection_change)
        wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
        wx.py.dispatcher.connect(receiver=self.add, signal=c.SIGNAL_ADD)
        wx.py.dispatcher.connect(receiver=self.delete, signal=c.SIGNAL_DELETE)

        main_sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
        py.dispatcher.send(signal=c.SIGNAL_VIEW_ACTIVATED, sender=self, command=c.COMMAND_VIEW_ACTIVATED, more=self)
