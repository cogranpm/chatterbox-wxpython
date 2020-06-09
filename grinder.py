"""
module for grinders view
a grinder is an exercise to practice something
this ui is for navigating the grinders for a particular subject
"""

from typing import Callable

import wx
import wx.dataview as dv

import chatterbox_constants as c
import data_functions as df
from lists import ListSpec, ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from panels import PanelSpec, BasePanel
from forms import FormDialog, FormSpec, TextField, edit_line, large, make_dialog
from validators import not_empty, FieldValidator

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
        ColumnSpec(name_column, ColumnType.str, 'Name', 100, True),
        ColumnSpec(description_column, ColumnType.str, 'Description', 100, True)
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


    def __make_form(self, dialog: FormDialog, name: str, record, form_title: str, helpstr: str):
        form: FormSpec = FormSpec(parent=dialog, name=name, title=form_title, helpstr=helpstr, edit_lines=[
            edit_line("Name", [TextField(name_column, large(),
                                         validator=FieldValidator(record, name_column, [not_empty]))]),
            edit_line("Description", [TextField(description_column, large(),
                                                validator=FieldValidator(record, description_column, [not_empty]))])
        ])
        return form

    def __edit(self, event):
        selected_item = get_selected_item(self.panel.list)
        record = get_record_from_item(self.__list_spec.model, selected_item)
        dlg: FormDialog = make_dialog(parent=self.parent,
                                      record=record, title=title, collection_name=collection_name)
        form: FormSpec = self.__make_form(dialog=dlg, name=form_name,
                                          record=record, form_title="Edit " + title, helpstr=helpstr)
        dlg.build(form)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            df.update_record(collection_name, record)
            self.__list_spec.edited_record(record)

    def __add(self, event):
        if self.fkey is None:
            return
        record = make_new_record(self.fkey)

        dlg: FormDialog = make_dialog(parent=self.parent,
                                             record=record, title=title, collection_name=collection_name)
        form: FormSpec = self.__make_form(dialog=dlg, name=form_name,
                                          record=record, form_title="Add " + title, helpstr=helpstr)
        dlg.build(form)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            df.add_record(collection_name, record)
            self.__list_spec.added_record(record)


class GrinderTask(wx.Panel):
    """ has a list of grinder tasks - such as ;
    write an abstract base class etc etc
    each task needs to have a text solution
    hints?
    """
    collection_name = c.COLLECTION_NAME_GRINDERTASK
    task_column = 'task'
    solution_column = 'solution'
    created_column = 'created'

    def create_data(grinder_id: int, query_fn):
        records = query_fn(grinder_id)
        list = []
        for record in records:
            list.append(record)
        return list

    def __init__(self, grinder: Grinder, parent):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        df.create_entity(GrinderTask.collection_name)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)
        self.list_spec = ListSpec(columns=[
            ColumnSpec(GrinderTask.task_column, ColumnType.str, 'Task', 100, True),
            ColumnSpec(GrinderTask.solution_column, ColumnType.str, 'Solution', 100, True),
            ColumnSpec(GrinderTask.created_column, ColumnType.date, 'Created', 100, True)
        ],
        selection_handler=None,
        data=GrinderTask.create_data(0, df.get_grinder_tasks_by_grinder))


