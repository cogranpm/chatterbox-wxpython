""" module for subject view
aim is to do as much in the functional style:
immutable values
pure functions
no side effects scattered, all should occur in single place """

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
shelf_id: int = None
panel: BasePanel = None
list_spec: ListSpec = None
panel_spec: PanelSpec = None
parent = None
helpstr = "Subject"
title = "Subject"
form_name = "frmSubject"
collection_name = c.COLLECTION_NAME_SUBJECT


def create_data(shelf_key, query_fn):
    records = query_fn(shelf_key)
    list = []
    for record in records:
        list.append(record)
    return list


def make_new_record(shelf_id: int):
    return {'id': None, 'shelf_id': shelf_id, 'name': '', 'description': ''}


def make_list_spec():
    return ListSpec(columns=[
        ColumnSpec(name_column, ColumnType.str, 'Name', 100, True),
        ColumnSpec(description_column, ColumnType.str, 'Description', 100, True)
    ], selection_handler=selection_change,
        edit_handler=edit,
        data=create_data(shelf_id, df.get_subjects_by_shelfid))


def make_panel_spec(parent):
    return PanelSpec(parent=parent, name="pnlSubject", title=title,
                     collection_name=collection_name, add_handler=add, edit_handler=edit)


def make_panel(spec: PanelSpec):
    return BasePanel(spec=spec, listspec=list_spec)


def selection_change(event: dv.DataViewEvent):
    selected_item = get_selected_item(panel.list)
    if selected_item is not None:
        record = get_record_from_item(list_spec.model, selected_item)
        # not sure yet what to do with this
        # probably pass on to grinders, publications, child subject(perhaps shelf) and so on


def make_dialog(record, title: str) -> FormDialog:
    dlg: FormDialog = FormDialog(parent, title, record, c.COLLECTION_NAME_SHELF)
    return dlg


def make_form(record, title: str, name: str, helpstr: str):
    dlg = make_dialog(record, title)
    form: FormSpec = FormSpec(parent=dlg, name=name, title=title, helpstr=helpstr, edit_lines=[
        edit_line("Name", [TextField(name_column, large(),
                                     validator=FieldValidator(record, name_column, [not_empty]))]),
        edit_line("Description", [TextField(description_column, large(),
                                            validator=FieldValidator(record, description_column, [not_empty]))])
    ])
    dlg.build(form)
    return dlg


def parent_changed():
    list_spec.update_data(create_data(shelf_id, df.get_subjects_by_shelfid))
    
    
def add(event):
    if shelf_id is None:
        return
    record = make_new_record(shelf_id)
    # redundance on Title and record
    dlg: FormDialog = make_form(record=record, title="Add " + title, name=form_name, helpstr=helpstr)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        df.add_record(collection_name, record)
        list_spec.added_record(record)


def edit(event):
    selected_item = get_selected_item(panel.list)
    record = get_record_from_item(list_spec.model, selected_item)
    dlg: FormDialog = make_form(record=record, title="Edit " + title, name=form_name, helpstr=helpstr)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        df.update_record(collection_name, record)
        list_spec.edited_record(record)
