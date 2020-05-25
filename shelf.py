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
from fn_app import get_data_store
import forms as frm
from lists import states, ColumnSpec, ColumnType, ListSpec, create_data
from validators import FieldValidator, CheckboxValidator, ComboValidator, not_empty
import wx.py as py
from models import ViewState
from forms import FormSpec, FormDialog, FormLineSpec, edit_line, large, TextField
from panels import BasePanel, PanelSpec
import subject as sb

name_column = 'name'

def add_record():
    return {'id': None, 'name': ''}


class MainPanel(wx.Panel):
    """ shows a list of shelves and all the children """
    def __init__(self, parent=None):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.db = get_data_store()
        self.db.create_entity(c.COLLECTION_NAME_SHELF)
        self.db.create_entity(c.COLLECTION_NAME_SUBJECT)
        main_sizer = frm.vsizer()
        self.SetSizer(main_sizer)
        splitter = frm.splitter(self)

        self.list_spec = ListSpec([
            ColumnSpec(name_column, ColumnType.str, 'Name', 100, True)
        ], self.selection_change, create_data(self.db, c.COLLECTION_NAME_SHELF))

        panel_spec = PanelSpec(splitter, "pnlShelf", "Shelf", c.COLLECTION_NAME_SHELF,
                               self.list_spec,
                               self.add,
                               self.delete,
                               self.edit)
        self.panel = BasePanel(panel_spec)

        # subject
        sb.list_spec = sb.make_list_spec(self.db)
        sb.panel_spec = sb.make_panel_spec(splitter)
        sb.panel = sb.make_panel(sb.panel_spec)
        sb.parent = self


        splitter.SplitVertically(self.panel, sb.panel, 248)
        # splitter.SetMinimumPaneSize(200)
        # splitter.SetSashGravity(0.5)
        main_sizer.Add(splitter, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

        # no save required
        # wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
        wx.py.dispatcher.connect(receiver=self.handle_tool_add, signal=c.SIGNAL_ADD)
        wx.py.dispatcher.connect(receiver=self.handle_tool_delete, signal=c.SIGNAL_DELETE)
        py.dispatcher.send(signal=c.SIGNAL_VIEW_ACTIVATED, sender=self, command=c.COMMAND_VIEW_ACTIVATED, more=self)


    def selection_change(self, event: dv.DataViewEvent):
        selected_item = self.panel.list.GetSelection()
        record = self.list_spec.model.ItemToObject(selected_item)
        sb.shelf_id = record['id']

    def handle_tool_add(self):
        focussed_item = wx.Window.FindFocus()
        match = frm.is_child_of([self.panel, sb.panel], focussed_item)
        if match is not None:
            if match is sb.panel:
                sb.add(None)
            elif match is self.panel:
                self.add(None)

    def handle_tool_delete(self):
        logging.info("delete tool item clicked")

    def add(self, event):
        record = add_record()
        dlg: FormDialog = self.make_form(record)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            db = wx.GetApp().datastore
            db.add(c.COLLECTION_NAME_SHELF, record)
            self.list_spec.data.append(record)
            self.list_spec.model.ItemAdded(dv.NullDataViewItem, self.list_spec.model.ObjectToItem(record))

    def delete(self, event):
        selected_item = self.panel.list.GetSelection()

    def edit(self, event):
        pass

    def make_form(self, record):
        dlg: FormDialog = FormDialog(self, "Add Shelf", record, c.COLLECTION_NAME_SHELF)
        form: FormSpec = FormSpec(dlg, "frmDemo", "Shelf", "Add Shelf", [
            edit_line("Name", [TextField(name_column, large(), validator=FieldValidator(record, name_column, [not_empty]))])
        ])
        dlg.build(form)
        return dlg

