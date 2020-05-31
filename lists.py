import wx
import wx.dataview as dv
from enum import Enum
from typing import Dict, List, Callable, Any
from dataclasses import dataclass, InitVar
from models import PyTestModel, ColumnSpec, ColumnType


def create_list_column(index: int, dvc: dv.DataViewCtrl, column_spec: ColumnSpec):
    if column_spec.data_type == ColumnType.bool:
        list_column: dv.DataViewColumn = dvc.AppendToggleColumn(column_spec.label, index,
                                                                width=column_spec.width,
                                                                mode=dv.DATAVIEW_CELL_EDITABLE)
    else:
        list_column = dvc.AppendTextColumn(column_spec.label, index, width=column_spec.width,
                                           mode=dv.DATAVIEW_CELL_EDITABLE)
    return list_column


def create_data(db, collection_name):
    records = db.all(collection_name)
    list = []
    for record in records:
        list.append(record)
    return list

def get_record_from_item(model: PyTestModel, selected_item: dv.DataViewItem):
    if selected_item is None:
        return None
    return model.ItemToObject(selected_item)

def get_selected_item(list: dv.DataViewCtrl) -> dv.DataViewItem:
    if list is not None:
        return list.GetSelection()
    else:
        return None 
    

# would like to make this frozen, but model is a problem 
# as it is set in postinit
@dataclass()
class ListSpec:

    data: InitVar[Any] = None
    columns: InitVar[List[ColumnSpec]] = None
    model: PyTestModel = None
    selection_handler: Callable = None
    edit_handler: Callable = None
    
    def __post_init__(self, data, columns):
        if self.model is None:
            self.model = PyTestModel(data, columns)

    #===========================================================================
    # def __init__(self, columns: List[ColumnSpec], selection_handler, edit_handler, data = None):
    #     self.columns = columns
    #     # does this need to be stored in both this class AND the model instance
    #     self.model = PyTestModel(data, self.columns)
    #     self.selection_handler = selection_handler
    #     self.edit_handler = edit_handler
    #===========================================================================

    def make_list(self, parent) -> dv.DataViewCtrl:
        dvc = dv.DataViewCtrl(parent, wx.ID_ANY, style=wx.BORDER_THEME)
        dvc.AssociateModel(self.model)
        self.model.DecRef()

        for i, column in enumerate(self.model.columns):
            if column.browseable:
                list_column = create_list_column(i, dvc, column)

        for c in dvc.Columns:
            c.Sortable = True

        if self.selection_handler is not None:
            dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.selection_handler)
        
        if self.edit_handler is not None:
            dvc.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit_handler)
            
        return dvc
    
    def update_data(self, data):
        self.model.change_data(data)

        
    def added_record(self, record):
        self.model.data.append(record)
        self.model.ItemAdded(dv.NullDataViewItem, self.model.ObjectToItem(record))
        
    def edited_record(self, record):
        self.model.ItemChanged(self.model.ObjectToItem(record))


@dataclass(frozen=True)
class ListItem:
    code: str
    label: str

states = [ListItem('VIC', 'Victoria'),
          ListItem('TAS', 'Tasmania'),
          ListItem('NSW', 'New South Wales'),
          ListItem('SA', 'South Australia'),
          ListItem('WA', 'West Australia')]

