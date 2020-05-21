""" all classes and functions pertaining to a shelf
shelf can have list of child subjects
subject can have child:
  shelves list - infinite recursion of subjects and shelves
  grinders - coding exercises with exercise and solution
    designed to be delivered randomly when user asks
  publications - topics, notes, exercises, audio recordings
  snippets - example code for anything
"""

import wx
import logging
import chatterbox_constants as c
import wx.dataview as dv
import forms as frm
from lists import states, ColumnSpec, ColumnType, ListSpec, create_data
from validators import FieldValidator, CheckboxValidator, ComboValidator, not_empty
import wx.py as py
from models import ViewState
from forms import FormSpec, FormDialog, FormLineSpec, edit_line, large, TextField
from panels import BasePanel, PanelSpec

name_column = 'name'

def add_record():
    return {'id': None, 'name': ''}


class ShelfPanel(wx.Panel):
    """ shows a list of shelves and all the children """
    def __init__(self, parent=None):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.db = wx.GetApp().datastore

        # goes into base class
        main_sizer = frm.vsizer()
        self.SetSizer(main_sizer)
        splitter = frm.splitter(self)

        self.shelf_list_spec = ListSpec([
            ColumnSpec(name_column, ColumnType.str, 'Name', 100, True)
        ], self.shelf_selection_change, create_data(self.db, c.COLLECTION_NAME_SHELF))

        shelf_spec = PanelSpec(splitter, "pnlShelf", "Shelf", c.COLLECTION_NAME_SHELF,
                               self.shelf_list_spec,
                               self.add_shelf,
                               self.delete_shelf,
                               self.edit_shelf)
        self.shelf_panel = BasePanel(shelf_spec)

        self.subject_list_spec = ListSpec([
            ColumnSpec(name_column, ColumnType.str, 'Name', 100, True)
        ], self.subject_selection_change, create_data(self.db, c.COLLECTION_NAME_SUBJECT))

        subject_spec = PanelSpec(splitter, "pnlSubject", "Subject", c.COLLECTION_NAME_SUBJECT,
                                 self.subject_list_spec,
                                 self.add_subject,
                                 self.delete_subject,
                                 self.edit_subject
                                 )
        self.subject_panel = BasePanel(subject_spec)

        splitter.SplitVertically(self.shelf_panel, self.subject_panel, 248)
        # splitter.SetMinimumPaneSize(200)
        # splitter.SetSashGravity(0.5)
        main_sizer.Add(splitter, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))


    def shelf_selection_change(self, event: dv.DataViewEvent):
        selected_item = self.shelf_panel.list.GetSelection()
        record = self.shelf_list_spec.model.ItemToObject(selected_item)
        print(record)

    def subject_selection_change(self, event: dv.DataViewEvent):
        selected_item = self.subject_panel.list.GetSelection()
        record = self.subject_list_spec.model.ItemToObject(selected_item)
        print(record)

    def add_shelf(self, event):
        record = dict(name='fred')
        dlg: FormDialog = FormDialog(self, "Add Shelf", record, c.COLLECTION_NAME_SHELF)
        form: FormSpec = FormSpec(dlg, "frmDemo", "Shelf", "Add Shelf", [
            edit_line("Name", [TextField("name", large(), validator=FieldValidator(record, "name", [not_empty]))])
        ])
        dlg.build(form)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            db = wx.GetApp().datastore
            db.add(c.COLLECTION_NAME_SHELF, record)

    def delete_shelf(self, event):
        pass

    def edit_shelf(self, event):
        pass

    def add_subject(self, event):
        record = dict(name='')
        dlg: FormDialog = FormDialog(self, "Add Subject", record, c.COLLECTION_NAME_SHELF)
        form: FormSpec = FormSpec(dlg, "frmDemo", "Subject", "Add Subject", [
            edit_line("Name", [TextField("name", large(), validator=FieldValidator(record, "name", [not_empty]))])
        ])
        dlg.build(form)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            db = wx.GetApp().datastore
            db.add(c.COLLECTION_NAME_SUBJECT, record)

    def delete_subject(self, event):
        pass

    def edit_subject(self, event):
        pass