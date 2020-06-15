"""
module for grinders view
a grinder is an exercise to practice something
this ui is for navigating the grinders for a particular subject
"""

from typing import Callable, Dict
from enum import Enum

import wx
import wx.dataview as dv
import datetime as dt

import chatterbox_constants as c
import data_functions as df
from lists import create_list, ListSpec, ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from panels import PanelSpec, BasePanel
import forms as frm
from validators import not_empty, FieldValidator
from models import ViewState, BaseEntityModel
import fn_format as fmt
import fn_widget as w

name_column = 'name'
description_column = 'description'
helpstr = "Grinders ..."
title = "Grinders"
form_name = "frmGrinder"
collection_name = c.COLLECTION_NAME_GRINDER


def create_data(subject_id, query_fn):
    records = query_fn(subject_id)
    list = []
    for record in records:
        list.append(record)
    return list


def make_new_record(subject_id: int):
    return {'id': None, 'subject_id': subject_id, 'name': '', 'description': ''}


def make_list_spec(fkey: int, selection_handler: Callable, edit_handler: Callable):
    return ListSpec(columns=[
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True, format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=True, browseable=True, format_fn=None)
    ], selection_handler=selection_handler,
        edit_handler=edit_handler,
        data=create_data(fkey, df.get_grinders_by_subject))


def make_panel_spec(parent, add_handler: Callable, edit_handler: Callable):
    return PanelSpec(parent=parent, name="pnlGrinder", title=title,
                     collection_name=collection_name, add_handler=add_handler, edit_handler=edit_handler)


def make_panel(spec: PanelSpec, list_spec: ListSpec):
    return BasePanel(spec=spec, listspec=list_spec)


def selection_change(event):
    pass


class Grinder:

    def __init__(self, parent, container):
        self.parent = parent
        self.container = container
        self.fkey = None
        self.__list_spec = make_list_spec(self.fkey, selection_change, self.__edit)
        self.__panel_spec = make_panel_spec(container, self.__add, self.__edit)
        self.panel = make_panel(self.__panel_spec, self.__list_spec)

    def parent_changed(self, fkey: int):
        self.fkey = fkey
        self.__list_spec.update_data(create_data(self.fkey, df.get_grinders_by_subject))


    def __make_form(self, dialog: frm.FormDialog, name: str, record, form_title: str, helpstr: str):
        form: frm.FormSpec = frm.FormSpec(parent=dialog, name=name, title=form_title, helpstr=helpstr, edit_lines=[
            frm.edit_line("Name", [frm.TextField(name_column, frm.large(),
                                         validator=FieldValidator(record, name_column, [not_empty]))]),
            frm.edit_line("Description", [frm.TextField(description_column, frm.large(),
                                                validator=FieldValidator(record, description_column, [not_empty]))])
        ])
        return form

    def __edit(self, event):
        # need to access the notebook and add a new page with a grindertask loaded as the child
        selected_item = get_selected_item(self.panel.list)
        record = get_record_from_item(self.__list_spec.model, selected_item)
        presenter = GrinderTaskPresenter(self, record, self.parent.frame)
        # task_panel = GrinderTask(self, record, self.parent.frame)
        self.parent.frame.add_page(key="grinder_task", title=c.NOTEBOOK_TITLE_GRINDER,
                                   window=presenter.view, page_data=None)

    def __add(self, event):
        if self.fkey is None:
            return
        record = make_new_record(self.fkey)

        dlg: frm.FormDialog = frm.make_dialog(parent=self.parent,
                                             record=record, title=title, collection_name=collection_name)
        form: frm.FormSpec = self.__make_form(dialog=dlg, name=form_name,
                                          record=record, form_title="Add " + title, helpstr=helpstr)
        dlg.build(form)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            df.add_record(collection_name, record)
            self.__list_spec.added_record(record)


class GrinderTaskModel(BaseEntityModel):

    collection_name = c.COLLECTION_NAME_GRINDERTASK
    task_column = 'task'
    solution_column = 'solution'
    created_column = 'created'

    def __init__(self, parent_key: int):
        super().__init__(parent_key)
        df.create_entity(GrinderTaskModel.collection_name)
        self.columns = [
                ColumnSpec(key=GrinderTaskModel.task_column, data_type=ColumnType.str, label='Task', width=400, sortable=True, browseable=True, format_fn=fmt.trunc),
                ColumnSpec(key=GrinderTaskModel.solution_column, data_type=ColumnType.str, label='Solution', width=100, sortable=False, browseable=False, format_fn=fmt.trunc),
                ColumnSpec(key=GrinderTaskModel.created_column, data_type=ColumnType.date, label='Created', width=300, sortable=True, browseable=True, format_fn=None)
            ]

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'grinder_id': self.parent_key, GrinderTask.task_column: '',
                GrinderTaskModel.solution_column: '', GrinderTaskModel.created_column: dt.datetime.today()}

    def create_data(self):
        records = df.get_grinder_tasks_by_grinder(self.parent_key)
        data_list = []
        for record in records:
            data_list.append(record)
        return data_list



class GrinderTaskPresenter:

    def __init__(self, grinder: Grinder, grinder_data, parent):
        self.Grinder = grinder
        self.parent = parent
        self.grinder_data = grinder_data
        self.model = GrinderTaskModel(grinder_data[c.FIELD_NAME_ID])
        self.view = GrinderTask(parent)
        self.view.set_list(create_list(parent, self.model.columns))
        self.view.list.AssociateModel(self.model)
        self.model.DecRef()

        # self.view.list.Bind... event handlers
        self.view.list.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.selection_handler)
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit_handler)
        # required for linux, otherwise double clicking or hitting enter
        # on selected list item results in text of column being edited
        # instead or running the ITEM_ACTIVATED event
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_START_EDITING, self.start_editing)
        self.view.set_form(None)

        # self.view.form = ....
        # self.view.layout(....)

        wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
        wx.py.dispatcher.connect(receiver=self.add, signal=c.SIGNAL_ADD)
        wx.py.dispatcher.connect(receiver=self.delete, signal=c.SIGNAL_DELETE)

    def selection_handler(self, event):
        pass


    # these may not be needed
    def edited_record(self, record):
        self.model.ItemChanged(self.model.ObjectToItem(record))

    def update_data(self, data):
        self.model.change_data(data)

    def added_record(self, record):
        self.model.data.append(record)
        self.model.ItemAdded(dv.NullDataViewItem, self.model.ObjectToItem(record))

    # handle the toolbar buttons
    def save(self, command, more):
        pass

    def add(self, command, more):
        pass

    def delete(self, command, more):
        pass

class GrinderTask(wx.Panel):
    """ has a list of grinder tasks - such as ;
    write an abstract base class etc etc
    each task needs to have a text solution
    hints?
    This class forms the View
    """
    collection_name = c.COLLECTION_NAME_GRINDERTASK
    task_column = 'task'
    solution_column = 'solution'
    created_column = 'created'
    help = 'Grinder Task'

    def __init__(self, parent):
        try:
            super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.parent = parent
            self.notebook: wx.aui.AuiNotebook = w.notebook(self)
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(main_sizer)

            # ListSpec needs to be replaced with something else
            # self.list_spec = ListSpec(columns=[
            #     ColumnSpec(key=GrinderTask.task_column, data_type=ColumnType.str, label='Task', width=400, sortable=True, browseable=True, format_fn=fmt.trunc),
            #     ColumnSpec(key=GrinderTask.solution_column, data_type=ColumnType.str, label='Solution', width=100, sortable=False, browseable=False, format_fn=fmt.trunc),
            #     ColumnSpec(key=GrinderTask.created_column, data_type=ColumnType.date, label='Created', width=300, sortable=True, browseable=True, format_fn=None)
            # ],
            #     selection_handler=self.list_selection_change,
            #     edit_handler=self.list_selection_edit,
            #     data=GrinderTask.create_data(self.grinder_data[c.FIELD_NAME_ID], df.get_grinder_tasks_by_grinder))
            # self.list = self.list_spec.make_list(self)
            # self.notebook.AddPage(self.list, "List", True)

            main_sizer.Add(self.notebook, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

            # figuring out how to seperate list and form into tabs
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEW_ACTIVATED, sender=self, command=c.COMMAND_VIEW_ACTIVATED, more=self)
        except BaseException as ex:
            print('Error in GrindTask __init__: ' + str(ex))

    def set_list(self, list):
        self.list = list
        self.view.notebook.AddPage(list, "List", True)

    def set_form(self, form):
        # to-do change this to use passed in form
        self.form_panel = w.panel(self, [])
        self.form_panel.SetSizer(w.sizer())
        self.form = frm.form(self.form_panel, "frmGrinder", "Grinder Tasks", GrinderTask.help, [
            frm.edit_line("Task", [frm.TextField(GrinderTask.task_column, frm.large(), style=wx.TE_MULTILINE,
                                                 validator=FieldValidator(None, GrinderTask.task_column, [not_empty]))]),
            frm.edit_line("Solution", [frm.CodeEditor(GrinderTask.solution_column, frm.large(),
                                                      validator=FieldValidator(None, GrinderTask.solution_column,
                                                                               [not_empty]))])
        ])
        self.form.build()
        self.notebook.AddPage(self.form_panel, "Task", False)
        self.form.set_viewstate(ViewState.empty)

    def save(self, command, more):
        if more is self:
            if self.form.view_state == ViewState.adding:
                record = GrinderTask.make_new_record(self.grinder_data[c.FIELD_NAME_ID])
                self.form.bind(record)
            if self.Validate():
                self.form_panel.TransferDataFromWindow()
                if self.form.view_state == ViewState.adding:
                    self.list_spec.added_record(record)
                    df.add_record(GrinderTask.collection_name, record)
                else:
                    selected_item = self.list.GetSelection()
                    record = self.list_spec.model.ItemToObject(selected_item)
                    df.update_record(GrinderTask.collection_name, record)
                    self.list_spec.edited_record(record)
                self.form.set_viewstate(ViewState.loaded)

    def add(self, command, more):
        if more is self:
            self.notebook.SetSelection(1)
            self.form.set_viewstate(ViewState.adding)


    def delete(self, command, more):
        pass

    def list_selection_change(self, event: dv.DataViewEvent):
        self.form.set_viewstate(ViewState.loading)
        selected_item = self.list.GetSelection()
        record = self.list_spec.model.ItemToObject(selected_item)
        self.form.bind(record)
        self.form_panel.TransferDataToWindow()
        self.form.set_viewstate(ViewState.loaded)

    def list_selection_edit(self, event: dv.DataViewEvent):
        self.notebook.SetSelection(1)