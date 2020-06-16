"""
module for grinders view
a grinder is an exercise to practice something
this ui is for navigating the grinders for a particular subject
"""

from typing import Callable, Dict, List
from enum import IntEnum

import wx
import wx.dataview as dv
import datetime as dt

import chatterbox_constants as c
import data_functions as df
from lists import create_list, ListSpec, ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from panels import PanelSpec, BasePanel
import forms as frm
from validators import not_empty, FieldValidator
from models import ViewState, BaseEntityModel, BasePresenter, BindDirection
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

    task_column = 'task'
    solution_column = 'solution'
    created_column = 'created'
    help = 'Grinder Task'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=task_column, data_type=ColumnType.str, label='Task', width=400, sortable=True,
                   browseable=True, format_fn=fmt.trunc),
        ColumnSpec(key=solution_column, data_type=ColumnType.str, label='Solution', width=100,
                   sortable=False, browseable=False, format_fn=fmt.trunc),
        ColumnSpec(key=created_column, data_type=ColumnType.date, label='Created', width=300,
                   sortable=True, browseable=True, format_fn=None)
    ]

    def __init__(self, parent_key: int):
        super().__init__(parent_key, GrinderTaskModel.columns, c.COLLECTION_NAME_GRINDERTASK)


    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'grinder_id': self.parent_key, self.task_column: '',
                self.solution_column: '', self.created_column: dt.datetime.today()}

    def create_data(self):
        records = df.get_grinder_tasks_by_grinder(self.parent_key)
        data_list = []
        for record in records:
            data_list.append(record)
        return data_list


class GrinderTaskPresenter(BasePresenter):

    edit_tab_index = 1

    def __init__(self, grinder: Grinder, grinder_data, parent):
        super().__init__(parent, GrinderTaskModel(grinder_data[c.FIELD_NAME_ID]))
        self.Grinder = grinder
        self.grinder_data = grinder_data
        self.view = GrinderTask(parent)
        self.view.set_list(self.model.columns)
        self.view.list.AssociateModel(self.model)
        self.model.DecRef()

        # don't really need this
        self.view.list.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.selection_handler)
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit_handler)
        # required for linux, otherwise double clicking or hitting enter
        # on selected list item results in text of column being edited
        # instead or running the ITEM_ACTIVATED event
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_START_EDITING, self.start_editing)

        task_field_def: frm.EditFieldDef = frm.TextFieldDef(name=GrinderTaskModel.task_column, width=frm.large(),
                                                            validator=FieldValidator(None, GrinderTaskModel.task_column, [not_empty]),
                                                            multi_line=True)
        solution_field_def: frm.EditFieldDef = frm.CodeEditorDef(name=GrinderTaskModel.solution_column, width=frm.large(),
                                                                 validator=FieldValidator(None, GrinderTaskModel.solution_column, [not_empty]))
        edit_lines: List[frm.FormLineDef] = [frm.FormLineDef("Task", [task_field_def]),
                                             frm.FormLineDef("Solution", [solution_field_def])]

        self.form_def: frm.FormDef = frm.FormDef(title='Grinder Task',
                                            help=GrinderTaskModel.help,
                                            edit_lines=edit_lines,
                                            name='frmGrinderTask')
        self.view.set_form(self.form_def)
        self.model.change_data(self.model.create_data())

        wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
        wx.py.dispatcher.connect(receiver=self.add, signal=c.SIGNAL_ADD)
        wx.py.dispatcher.connect(receiver=self.delete, signal=c.SIGNAL_DELETE)

        wx.py.dispatcher.send(signal=c.SIGNAL_VIEW_ACTIVATED, sender=self, command=c.COMMAND_VIEW_ACTIVATED, more=self)

    def set_view_state(self, state: ViewState):
        # need to update the form
        if state == ViewState.adding:
            self.form_def.reset_fields()
            self.form_def.enable_fields(True)
            self.form_def.setfocusfirst()
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_ADDING, more=self)
        elif state == ViewState.empty:
            self.form_def.reset_fields()
            self.form_def.enable_fields(False)
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_EMPTY, more=self)
        elif state == ViewState.loaded:
            self.form_def.enable_fields(True)
            self.form_def.setfocusfirst()
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_LOADED, more=self)
            self.form_def.pause_dirty_events(False)
        elif state == ViewState.loading:
            self.form_def.pause_dirty_events(True)

        self.view_state = state

    def selection_handler(self, event):
        # not quite sure what to do, load the selection so it can be deleted?
        pass

    def edit_handler(self, event: dv.DataViewEvent):
        self.set_view_state(ViewState.loading)
        selected_item = self.view.list.GetSelection()
        record = self.model.ItemToObject(selected_item)
        # this sets the data property on all the validators that are defined for all the fields
        self.form_def.bind(record)
        # this tells view to push data from model to the controls
        self.view.bind(BindDirection.to_window)
        self.set_view_state(ViewState.loaded)
        self.view.set_current_tab(self.edit_tab_index)

    # handle the toolbar buttons
    def save(self, command, more):
        if more is self.view:
            if self.view_state == ViewState.adding:
                record = self.model.make_new_record()
                self.form_def.bind(record)
            if self.view.Validate():
                self.view.bind(BindDirection.from_window)
                if self.view_state == ViewState.adding:
                    self.added_record(record)
                    df.add_record(self.model.collection_name, record)
                else:
                    selected_item = self.view.list.GetSelection()
                    record = self.model.ItemToObject(selected_item)
                    df.update_record(self.model.collection_name, record)
                    self.edited_record(record)
                self.set_view_state(ViewState.loaded)

    def add(self, command, more):
        if more is self.view:
            self.set_view_state(ViewState.adding)
            self.view.set_current_tab(self.edit_tab_index)

    def delete(self, command, more):
        if more is self.view:
            selected_item = self.view.list.GetSelection()
            if selected_item is not None:
                if frm.confirm_delete(self.view):
                    self.model.ItemDeleted(dv.NullDataViewItem, selected_item)
                    record = self.model.ItemToObject(selected_item)
                    df.delete_record(self.model.collection_name, record)
                    self.model.data.remove(record)
                    self.set_view_state(ViewState.empty)



class GrinderTask(wx.Panel):
    """ has a list of grinder tasks - such as ;
    write an abstract base class etc etc
    each task needs to have a text solution
    hints?
    This class forms the View
    """

    def __init__(self, parent):
        try:
            super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.parent = parent
            self.notebook: wx.aui.AuiNotebook = w.notebook(self)
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(main_sizer)
            main_sizer.Add(self.notebook, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
        except BaseException as ex:
            print('Error in GrindTask __init__: ' + str(ex))

    def set_list(self, columns: List[ColumnSpec]):
        self.list = create_list(self.parent, columns)
        self.notebook.AddPage(self.list, "List", True)

    def set_form(self, form_def: frm.FormDef):
        # to-do change this to use passed in form
        self.form_panel = w.panel(self, [])
        self.form_panel.SetSizer(w.sizer())
        form_def.make_form(self.form_panel)
        self.notebook.AddPage(self.form_panel, "Task", False)

    def set_current_tab(self, index):
        self.notebook.SetSelection(index)

    def bind(self, direction: BindDirection):
        if direction == BindDirection.from_window:
            self.form_panel.TransferDataFromWindow()
        else:
            self.form_panel.TransferDataToWindow()


