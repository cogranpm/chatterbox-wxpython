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
from lists import states, ColumnSpec, ColumnType, ListSpec
from validators import FieldValidator, CheckboxValidator, ComboValidator, not_empty
import wx.py as py
from models import ViewState
from forms import FormSpec, FormDialog, FormLineSpec, edit_line, large, TextField



collection_name = c.COLLECTION_NAME_SHELF
name_column = 'name'


def create_data(db):
    records = db.all(collection_name)
    list = []
    for record in records:
        list.append(record)
    return list


def add_record():
    return {'id': None, 'name': ''}




class ShelfPanel(wx.Panel):
    """ shows a list of shelves and all the children """
    def __init__(self, parent=None):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.db = wx.GetApp().datastore
        self.db.create_entity(collection_name)

        # goes into base class
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        shelf_header_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        shelf_caption = wx.StaticText(shelf_header_panel, wx.ID_ANY, u"Shelves", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        shelf_caption.Wrap(-1)
        btn_add_shelf = frm.panel_tool_button(shelf_header_panel, c.ID_ADD_SHELF, wx.EmptyString,
                                              self.add_shelf, c.ICON_ADD)

        btn_add_shelf.SetMaxSize(wx.Size(25, -1))
        btn_delete_shelf = wx.Button(shelf_header_panel, c.ID_DELETE_SHELF, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(20, 20), 0)
        btn_delete_shelf.Enable(False)
        btn_delete_shelf.SetMaxSize(wx.Size(25, -1))
        btn_edit_shelf = wx.Button(shelf_header_panel, c.ID_EDIT_SHELF, wx.EmptyString, wx.DefaultPosition,
                                        wx.Size(20, 20), 0)
        btn_edit_shelf.Enable(False)
        btn_edit_shelf.SetMaxSize(wx.Size(60, -1))



        header_sizer = frm.hsizer([shelf_caption, btn_add_shelf, btn_delete_shelf, btn_edit_shelf])
        shelf_header_panel.SetSizer(header_sizer)
        shelf_header_panel.Layout()
        header_sizer.Fit(shelf_header_panel)
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

    def save(self, command, more):
        pass

    def add(self, command, more):
        """ prepares for an add by asking to save changes if dirty, then cleaning out the controls for new entry """
        if more is self:
            self.form.set_viewstate(ViewState.adding)

    def delete(self, command, more):
        if more is self:
            selected_item = self.list.GetSelection()
            if selected_item is not None:
                if frm.confirm_delete(self):
                    self.listspec.model.ItemDeleted(dv.NullDataViewItem, selected_item)
                    record = self.listspec.model.ItemToObject(selected_item)
                    self.db.remove(collection_name, record)
                    # del (self.listspec.data[0])
                    self.listspec.data.remove(record)


    def list_selection_change(self, event: dv.DataViewEvent):
        # testing dispatcher stuff
        selected_item = self.list.GetSelection()
        record = self.listspec.model.ItemToObject(selected_item)
        print(record)
        #self.form.bind(record)
        #self.TransferDataToWindow()

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
