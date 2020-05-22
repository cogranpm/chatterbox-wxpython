import chatterbox_constants as c
from lists import ListSpec, ColumnType, ColumnSpec, create_data
from panels import PanelSpec, BasePanel
from forms import FormDialog, FormSpec, TextField, edit_line, large
from validators import not_empty, FieldValidator
from datastore import DataStore
import wx
import wx.dataview as dv

collection_name = c.COLLECTION_NAME_SUBJECT
name_column = 'name'

shelf_id: int = None
panel: BasePanel = None
list_spec: ListSpec = None
panel_spec: PanelSpec = None


def add_record(shelf_id: int):
    return {'id': None, 'shelf_id': shelf_id, 'name': ''}

def make_list_spec(datastore):
    return ListSpec([
        ColumnSpec(name_column, ColumnType.str, 'Name', 100, True)
    ], selection_change, create_data(datastore, c.COLLECTION_NAME_SUBJECT))


def make_panel_spec(parent):
    return PanelSpec(parent, "pnlSubject", "Subject",
                     c.COLLECTION_NAME_SUBJECT, list_spec, add, delete, edit)


def make_panel(spec: PanelSpec):
    return BasePanel(spec)


def selection_change(self, event: dv.DataViewEvent):
    global panel, list_spec
    selected_item = panel.list.GetSelection()
    record = list_spec.model.ItemToObject(selected_item)
    print(record)


def add(self, event):
    global shelf_id
    record = add_record(shelf_id)
    # redundance on Title and record
    dlg: FormDialog = FormDialog(self, "Add Subject", record, c.COLLECTION_NAME_SHELF)
    form: FormSpec = FormSpec(dlg, "frmDemo", "Subject", "Add Subject", [
        edit_line("Name", [TextField("name", large(), validator=FieldValidator(record, "name", [not_empty]))])
    ])
    dlg.build(form)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        db = wx.GetApp().datastore
        db.add(c.COLLECTION_NAME_SUBJECT, record)

def delete(self, event):
    pass

def edit(self, event):
    pass