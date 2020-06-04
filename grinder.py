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
fkey: int = None
panel: BasePanel = None
list_spec: ListSpec = None
panel_spec: PanelSpec = None
parent = None
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


def make_list_spec():
    return ListSpec(columns=[
        ColumnSpec(name_column, ColumnType.str, 'Name', 100, True),
        ColumnSpec(description_column, ColumnType.str, 'Description', 100, True)
    ], selection_handler=selection_change,
        edit_handler=edit,
        data=create_data(fkey, df.get_grinders_by_subject))


def make_panel_spec(parent):
    return PanelSpec(parent=parent, name="pnlGrinder", title=title,
                     collection_name=collection_name, add_handler=add, edit_handler=edit)


def make_panel(spec: PanelSpec):
    return BasePanel(spec=spec, listspec=list_spec)


def selection_change(event: dv.DataViewEvent):
    selected_item = get_selected_item(panel.list)
    if selected_item is not None:
        record = get_record_from_item(list_spec.model, selected_item)
        # not sure yet what to do with this
        # probably pass on to grinders, publications, child subject(perhaps shelf) and so on


def make_dialog(record, dialog_title) -> FormDialog:
    return FormDialog(parent=parent, title=dialog_title, record=record, collection_name=collection_name)


def make_form(record, form_title):
    dlg = make_dialog(record, form_title)
    form: FormSpec = FormSpec(parent=dlg, name=form_name, title=form_title, helpstr=helpstr, edit_lines=[
        edit_line("Name", [TextField(name_column, large(),
                                     validator=FieldValidator(record, name_column, [not_empty]))]),
        edit_line("Description", [TextField(description_column, large(),
                                            validator=FieldValidator(record, description_column, [not_empty]))])
    ])
    dlg.build(form)
    return dlg


def parent_changed():
    list_spec.update_data(create_data(fkey, df.get_grinders_by_subject))


def add(event):
    if fkey is None:
        return
    record = make_new_record(fkey)
    # redundance on Title and record
    dlg: FormDialog = make_form(record=record, form_title="Add " + title)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        df.add_record(collection_name, record)
        list_spec.added_record(record)


def edit(event):
    selected_item = get_selected_item(panel.list)
    record = get_record_from_item(list_spec.model, selected_item)
    dlg: FormDialog = make_form(record=record, form_title="Edit " + title)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        df.update_record(collection_name, record)
        list_spec.edited_record(record)
