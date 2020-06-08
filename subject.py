""" module for subject view
 """

import chatterbox_constants as c
import data_functions as df
from lists import ListSpec, ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from panels import PanelSpec, BasePanel
from forms import FormDialog, FormSpec, TextField, edit_line, large
from validators import not_empty, FieldValidator
import wx
import wx.dataview as dv
import grinder as gr

name_column = 'name'
description_column = 'description'
helpstr = "Subject"
title = "Subject"
form_name = "frmSubject"
collection_name = c.COLLECTION_NAME_SUBJECT


class Subject:

    def __init__(self, parent, parent_container):
        self.parent = parent
        self.shelf_id = None
        self.list_spec = make_list_spec(fkey=self.shelf_id, selection_handler=self.__selection_change, edit_handler=self.__edit)
        self.panel_spec = self.__make_panel_spec(parent_container)
        self.panel = self.__make_panel(self.panel_spec)

    # called from event on panel
    def __add(self, event):
        if self.shelf_id is None:
            return
        record = make_new_record(self.shelf_id)
        dlg: FormDialog = self.__make_form(record=record, form_title="Add " + title)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            df.add_record(collection_name, record)
            self.list_spec.added_record(record)

    def __edit(self, event):
        selected_item = get_selected_item(self.panel.list)
        record = get_record_from_item(self.list_spec.model, selected_item)
        dlg: FormDialog = self.__make_form(record=record, form_title="Edit " + title)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            df.update_record(collection_name, record)
            self.list_spec.edited_record(record)


    def __make_panel_spec(self, parent):
        return PanelSpec(parent=parent, name="pnlSubject", title=title,
                         collection_name=collection_name, add_handler=self.__add, edit_handler=self.__edit)

    def __make_panel(self, spec: PanelSpec):
        return BasePanel(spec=spec, listspec=self.list_spec)

    def __selection_change(self, event: dv.DataViewEvent):
        selected_item = get_selected_item(self.panel.list)
        if selected_item is not None:
            record = get_record_from_item(self.list_spec.model, selected_item)
            gr.fkey = record['id']
            gr.parent_changed()

    def __make_dialog(self, record, dialog_title) -> FormDialog:
        return FormDialog(parent=self.parent, title=dialog_title, record=record, collection_name=collection_name)

    def __make_form(self, record, form_title):
        dlg = self.__make_dialog(record, form_title)
        form: FormSpec = FormSpec(parent=dlg, name=form_name, title=form_title, helpstr=helpstr, edit_lines=[
            edit_line("Name", [TextField(name_column, large(),
                                         validator=FieldValidator(record, name_column, [not_empty]))]),
            edit_line("Description", [TextField(description_column, large(),
                                                validator=FieldValidator(record, description_column, [not_empty]))])
        ])
        dlg.build(form)
        return dlg

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


    
