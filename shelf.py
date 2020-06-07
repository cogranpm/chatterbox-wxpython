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
from lists import states, ColumnSpec, ColumnType, ListSpec, create_data, get_selected_item, get_record_from_item
from validators import FieldValidator, CheckboxValidator, ComboValidator, not_empty
import wx.py as py
from models import ViewState
from forms import FormSpec, FormDialog, FormLineSpec, edit_line, large, TextField
from panels import BasePanel, PanelSpec
import subject as sb
import grinder as gr
import data_functions as df
import fn_widget as w

name_column = 'name'
collection_name = c.COLLECTION_NAME_SHELF
list_spec: ListSpec = None
panel: BasePanel = None
panel_spec: PanelSpec = None
parent = None
helpstr = "Shelf"
title = "Shelf"
form_name = "frmShelf"

def add_record():
    return {'id': None, 'name': ''}

class MainPanel(wx.Panel):
    """ shows a list of shelves and all the children """
    def __init__(self, parent=None):
        global list_spec, panel_spec, panel
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        df.create_entity(collection_name)
        df.create_entity(sb.collection_name)
        df.create_entity(gr.collection_name)
        main_sizer = frm.vsizer()
        self.SetSizer(main_sizer)
        splitter = frm.splitter(self)

        list_spec = ListSpec(columns=
            [ColumnSpec(name_column, ColumnType.str, 'Name', 100, True)], 
            selection_handler=selection_change,
            edit_handler=edit,
            data=create_data(df.get_all(collection_name)))

        panel_spec = PanelSpec(parent=splitter, name="pnlShelf", title=title, collection_name=collection_name,
                               add_handler=add,
                               edit_handler=edit)
        panel = BasePanel(spec=panel_spec, listspec=list_spec)


        # subject notebook
        # subject panel
        subject_container = w.panel(splitter, [])
        subject_sizer = frm.vsizer()
        subject_container.SetSizer(subject_sizer)
        subject_splitter = w.splitter(subject_container)

        # subject
        self.__subject = sb.Subject(self, subject_splitter)
        # sb.list_spec = sb.make_list_spec()
        # sb.panel_spec = sb.make_panel_spec(subject_splitter)
        # sb.panel = sb.make_panel(sb.panel_spec)
        # sb.parent = self

        # subject children
        subject_notebook = w.notebook(subject_splitter)

        # grinder
        gr.list_spec = gr.make_list_spec()
        gr.panel_spec = gr.make_panel_spec(subject_container)
        gr.panel = gr.make_panel(gr.panel_spec)
        gr.parent = subject_container

        # grinder = wx.TextCtrl(subject_notebook, -1, "Grinders", style=wx.TE_MULTILINE)
        publications = wx.TextCtrl(subject_notebook, -1, "Publications", style=wx.TE_MULTILINE)
        subject_notebook.AddPage(gr.panel, "Grinders", False)
        subject_notebook.AddPage(publications, "Publications")
        # subject_sizer.Add(sb.panel, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
        # subject_sizer.Add(subject_notebook, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
        subject_splitter.SplitHorizontally(self.__subject.panel, subject_notebook, 248)
        subject_sizer.Add(subject_splitter, wx.SizerFlags(1).Expand())


        splitter.SplitVertically(panel, subject_container, 248)

        #splitter.SplitVertically(panel, sb.panel, 248)
        # splitter.SetMinimumPaneSize(200)
        # splitter.SetSashGravity(0.5)
        main_sizer.Add(splitter, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

        # no save required
        # wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
        py.dispatcher.connect(receiver=handle_tool_add, signal=c.SIGNAL_ADD)
        py.dispatcher.connect(receiver=handle_tool_delete, signal=c.SIGNAL_DELETE)
        py.dispatcher.send(signal=c.SIGNAL_VIEW_ACTIVATED, sender=self, command=c.COMMAND_VIEW_ACTIVATED, more=self)


def selection_change(event: dv.DataViewEvent):
    selected_item = get_selected_item(panel.list)
    if selected_item is None:
        return
    record = get_record_from_item(list_spec.model, selected_item)
    sb.shelf_id = record['id']
    sb.parent_changed()


# can this be pulled out into the base class
# or some resusable function
def add(event):
    record = add_record()
    dlg: FormDialog = make_form(record, "Add " + title)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        df.add_record(collection_name, record)
        list_spec.added_record(record)


def edit(event):
    selected_item = get_selected_item(panel.list)
    record = get_record_from_item(list_spec.model, selected_item)
    dlg: FormDialog = make_form(record=record, title="Edit " + title)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        df.update_record(collection_name, record)
        list_spec.edited_record(record)


def make_dialog(record, title: str) -> FormDialog:
    dlg: FormDialog = FormDialog(parent=parent, title=title, record=record, collection_name=collection_name)
    return dlg

def make_form(record, title: str):
    dlg = make_dialog(record, title)
    form: FormSpec = FormSpec(parent=dlg, name=form_name, title=title, helpstr=helpstr, edit_lines=[
        edit_line("Name", [TextField(name_column, large(), validator=FieldValidator(record, name_column, [not_empty]))])
    ])
    dlg.build(form)
    return dlg

# just messing around to see if handling the toolbar commands make sense in this tab
# it probably doesn't as each sub panel has toolbars
# using the focused panel or control to figure on which sub panel to call the action
def handle_tool_add():
    focussed_item = wx.Window.FindFocus()
    match = frm.is_child_of([panel, sb.panel], focussed_item)
    if match is not None:
        if match is sb.panel:
            sb.add(None)
        elif match is panel:
            add(None)

def handle_tool_delete(self):
    logging.info("delete tool item clicked")

