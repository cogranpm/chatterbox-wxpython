import wx
import wx.dataview as dv
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass
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


class ListSpec:

    def __init__(self, columns: List[ColumnSpec], data):
        self.columns = columns
        self.data = data
        self.model = PyTestModel(self.data, self.columns)

    def build(self, parent, handler):
        dvc = dv.DataViewCtrl(parent, wx.ID_ANY, style=wx.BORDER_THEME)
        dvc.AssociateModel(self.model)
        self.model.DecRef()

        for i, column in enumerate(self.columns):
            if column.browseable:
                list_column = create_list_column(i, dvc, column)

        for c in dvc.Columns:
            c.Sortable = True

        dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, handler)
        return dvc


@dataclass(frozen=True)
class ListItem:
    code: str
    label: str

states = [ListItem('VIC', 'Victoria'),
          ListItem('TAS', 'Tasmania'),
          ListItem('NSW', 'New South Wales'),
          ListItem('SA', 'South Australia'),
          ListItem('WA', 'West Australia')]

