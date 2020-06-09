"""
module for grinders view
a grinder is an exercise to practice something
this ui is for navigating the grinders for a particular subject
"""

import chatterbox_constants as c
import data_functions as df
from lists import ListSpec, ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from panels import PanelSpec, BasePanel
from forms import FormDialog, FormSpec, TextField, edit_line, large
from validators import not_empty, FieldValidator
import wx
import wx.dataview as dv

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


def make_list_spec(fkey: int):
    return ListSpec(columns=[
        ColumnSpec(name_column, ColumnType.str, 'Name', 100, True),
        ColumnSpec(description_column, ColumnType.str, 'Description', 100, True)
    ], selection_handler=selection_change,
        edit_handler=edit,
        data=create_data(fkey, df.get_grinders_by_subject))


def make_panel_spec(parent):
    return PanelSpec(parent=parent, name="pnlGrinder", title=title,
                     collection_name=collection_name, add_handler=add, edit_handler=edit)


def make_panel(spec: PanelSpec, list_spec: ListSpec):
    return BasePanel(spec=spec, listspec=list_spec)


def selection_change(event):
    pass

def edit(event):
    pass

def add(event):
    pass


class Grinder:

    def __init__(self, parent, container):
        self.parent = parent
        self.container = container
        self.fkey = None
        self.__list_spec = make_list_spec(self.fkey)
        self.__panel_spec = make_panel_spec(container)
        self.panel = make_panel(self.__panel_spec, self.__list_spec)

    def parent_changed(self, fkey: int):
        self.fkey = fkey
        self.__list_spec.update_data(create_data(self.fkey, df.get_grinders_by_subject))



