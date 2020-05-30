import chatterbox_constants as c
from lists import ListSpec, ColumnType, ColumnSpec
from panels import PanelSpec, BasePanel
from forms import FormDialog, FormSpec, TextField, edit_line, large
from validators import not_empty, FieldValidator
from datastore import DataStore
import wx
import wx.dataview as dv
from fn_app import get_data_store
from shelve import Shelf
from pkgutil import get_data


name_column = 'name'
description_column = 'description'
shelf_id: int = None
panel: BasePanel = None
list_spec: ListSpec = None
panel_spec: PanelSpec = None
parent = None


def create_data():
    records = get_data_store().query(c.COLLECTION_NAME_SUBJECT, {'shelf_id': shelf_id})
    list = []
    for record in records:
        list.append(record)
    return list

def add_record(shelf_id: int):
    return {'id': None, 'shelf_id': shelf_id, 'name': '', 'description': ''}

def make_list_spec(datastore):
    return ListSpec([
        ColumnSpec(name_column, ColumnType.str, 'Name', 100, True),
        ColumnSpec(description_column, ColumnType.str, 'Description', 100, True)
    ], selection_change, edit, create_data())


def make_panel_spec(parent):
    return PanelSpec(parent, "pnlSubject", "Subject",
                     c.COLLECTION_NAME_SUBJECT, list_spec, add, edit)


def make_panel(spec: PanelSpec):
    return BasePanel(spec)


def selection_change(event: dv.DataViewEvent):
    selected_item = panel.list.GetSelection()
    record = list_spec.model.ItemToObject(selected_item)

def make_form(record):
    dlg: FormDialog = FormDialog(parent, "Add Subject", record, c.COLLECTION_NAME_SHELF)
    form: FormSpec = FormSpec(dlg, "frmDemo", "Subject", "Add Subject", [
        edit_line("Name", [TextField(name_column, large(),
                                     validator=FieldValidator(record, name_column, [not_empty]))]),
        edit_line("Description", [TextField(description_column, large(),
                                            validator=FieldValidator(record, description_column, [not_empty]))])
    ])
    dlg.build(form)
    return dlg

def parent_changed():
    list_spec.update_data(create_data())
    
    
    
def add(event):
    if shelf_id is None:
        return
    record = add_record(shelf_id)
    # redundance on Title and record
    dlg: FormDialog = make_form(record)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        get_data_store().add(c.COLLECTION_NAME_SUBJECT, record)

def delete(event):
    pass

def edit(event):
    selected_item = panel.list.GetSelection()
    record = list_spec.model.ItemToObject(selected_item)
    dlg: FormDialog = make_form(record)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        get_data_store().update(c.COLLECTION_NAME_SUBJECT, record)
