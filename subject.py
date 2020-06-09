""" module for subject view
 """

from typing import Callable

import wx
import wx.dataview as dv

import chatterbox_constants as c
import data_functions as df
from lists import ListSpec, ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from panels import make_panel, make_panel_spec
from forms import FormDialog, make_dialog, FormSpec, TextField, edit_line, large
from validators import not_empty, FieldValidator
import grinder as gr

name_column = 'name'
description_column = 'description'
helpstr = "Subject"
title = "Subject"
form_name = "frmSubject"
collection_name = c.COLLECTION_NAME_SUBJECT


class Subject:

    def __init__(self, parent, parent_container, grinder: gr.Grinder):
        self.parent = parent
        self.grinder = grinder
        self.shelf_id = None
        self.list_spec = make_list_spec(fkey=self.shelf_id, selection_handler=self.__selection_change, edit_handler=self.__edit)
        self.panel_spec = make_panel_spec(parent=parent_container, name='frmPanel', title=title,
                                          collection_name=collection_name,
                                          add_handler=self.__add, edit_handler=self.__edit)
        self.panel = make_panel(self.panel_spec, self.list_spec)

    # called from event on panel
    def __add(self, event):
        if self.shelf_id is None:
            return
        record = make_new_record(self.shelf_id)

        dlg: FormDialog = make_dialog(parent=self.parent,
                                             record=record, title=title, collection_name=collection_name)
        form: FormSpec = self.__make_form(dialog=dlg, name=form_name,
                                          record=record, form_title="Add " + title, helpstr=helpstr)
        dlg.build(form)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            df.add_record(collection_name, record)
            self.list_spec.added_record(record)

    def __edit(self, event):
        selected_item = get_selected_item(self.panel.list)
        record = get_record_from_item(self.list_spec.model, selected_item)
        dlg: FormDialog = make_dialog(parent=self.parent,
                                      record=record, title=title, collection_name=collection_name)
        form: FormSpec = self.__make_form(dialog=dlg, name=form_name,
                                          record=record, form_title="Edit " + title, helpstr=helpstr)
        dlg.build(form)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            df.update_record(collection_name, record)
            self.list_spec.edited_record(record)

    def __selection_change(self, event: dv.DataViewEvent):
        selected_item = get_selected_item(self.panel.list)
        if selected_item is not None:
            record = get_record_from_item(self.list_spec.model, selected_item)
            self.grinder.parent_changed(record[c.FIELD_NAME_ID])

    def __make_form(self, dialog: FormDialog, name: str, record, form_title: str, helpstr: str):
        form: FormSpec = FormSpec(parent=dialog, name=name, title=form_title, helpstr=helpstr, edit_lines=[
            edit_line("Name", [TextField(name_column, large(),
                                         validator=FieldValidator(record, name_column, [not_empty]))]),
            edit_line("Description", [TextField(description_column, large(),
                                                validator=FieldValidator(record, description_column, [not_empty]))])
        ])
        return form

    # comes from a list event
    def parent_changed(self, fkey: int):
        self.shelf_id = fkey
        self.list_spec.update_data(create_data(fkey, df.get_subjects_by_shelf))


def create_data(shelf_key, query_fn):
    records = query_fn(shelf_key)
    list = []
    for record in records:
        list.append(record)
    return list


def make_new_record(shelf_id: int):
    return {'id': None, 'shelf_id': shelf_id, 'name': '', 'description': ''}


def make_list_spec(fkey, selection_handler, edit_handler):
    return ListSpec(columns=[
        ColumnSpec(name_column, ColumnType.str, 'Name', 100, True),
        ColumnSpec(description_column, ColumnType.str, 'Description', 100, True)
    ], selection_handler=selection_handler,
        edit_handler=edit_handler,
        data=create_data(fkey, df.get_subjects_by_shelf))


    
