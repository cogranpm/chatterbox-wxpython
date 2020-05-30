import wx.dataview as dv
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum

ViewState = Enum('ViewState', 'adding dirty loaded loading empty')

# not sure how to do date time
ColumnType = Enum('ColumnType', 'str bool float int date')
column_type_map: Dict[ColumnType, str] = {ColumnType.str: 'string', ColumnType.bool: 'bool',
                                          ColumnType.float: 'double', ColumnType.int: 'string',
                                          ColumnType.date: 'string'}

@dataclass(frozen=True)
class ColumnSpec:
    key: str
    data_type: ColumnType
    label: str
    width: int
    browseable: bool = False
    sortable: bool = False


# this is a wxPython xtra model based class
# has a ItemToObject mapper built in which makes
# selection processing easy
class PyTestModel(dv.PyDataViewModel):
    """
    this class has a neat way to get the object that is stored
    inside the row of the table without resorting to storing pointers etc
    also supports sorting, adding, editing and deleting
    also supports attributes on cells etc
    """
    def __init__(self, data, columns: List[ColumnSpec]):
        super().__init__()
        self.data = data
        self.columns = columns

    def get_column_by_index(self, index):
        # return list(self.columns.values())[index]
        return self.columns[index]

    def GetChildren(self, item, children):
        if self.data is None:
            return
        for row in self.data:
            children.append(self.ObjectToItem(row))
        return len(self.data)

    def IsContainer(self, item):
        if not item:
            return True
        return False

    def GetParent(self, item):
        return dv.NullDataViewItem

    def GetColumnType(self, col):
        # global column_type_map
        return column_type_map[self.get_column_by_index(col).data_type]

    def GetColumnCount(self):
        return len(self.columns)
        #return len(self.columns.keys())


    def GetValue(self, item, col):
        row = self.ItemToObject(item)
        # change to map access
        # return row[col]
        return row[self.get_column_by_index(col).key]

    def GetAttr(self, item, col, attr):
        if col == 1:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def SetValue(self, variant, item, col):
        row = self.ItemToObject(item)
        # change to map access
        #row[col] = variant
        row[self.get_column_by_index(col).key] = variant
        return True

    def Compare(self, item1, item2, col, ascending):
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.ItemToObject(item1)
        row2 = self.ItemToObject(item2)

        # different sort depending on column
        if self.get_column_by_index(col).data_type == int:
            a = int(row1[self.get_column_by_index(col).key])
            b = int(row2[self.get_column_by_index(col).key])
            return (a > b) - (a < b)
        else:
            a = row1[self.get_column_by_index(col).key]
            b = row2[self.get_column_by_index(col).key]
            return (a > b) - (a < b)

        # if col == 1 or col == 2:
        #     a = int(row1[col])
        #     b = int(row2[col])
        #     return (a > b) - (a < b)
        # else:
        #     a = row1[col]
        #     b = row2[col]
        #     return (a > b) - (a < b)
#

# this is an example of a wxWidgets style DataView model for a table/list
# if using a list of lists style this could be generic for any domain model data
class TestModel(dv.DataViewIndexListModel):

    def __init__(self, data):
        super().__init__(len(data))
        self.data = data

    def GetColumnType(self, col):
        return 'string'

    def GetValueByRow(self, row, col):
        return self.data[row][col]

    def SetValueByRow(self, value, row, col):
        self.data[row][col] = value

    def GetColumnCount(self):
        return len(self.data[0])

    def GetCount(self):
        return len(self.data)

    def GetAttrByRow(self, row, col, attr):
        if col == 3:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def Compare(self, item1, item2, col, ascending):
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        if col == 1 or col == 2:
            a = int(self.data[row1][col])
            b = int(self.data[row2][col])
            return (a > b) - (a < b)
        else:
            a = self.data[row1][col]
            b = self.data[row2][col]
            return (a > b) - (a < b)

    def DeleteRows(self, rows):
        # make a copy since we'll be sorting(mutating) the list
        rows = list(rows)
        # use reverse order so the indexes don't change as we remove items
        rows.sort(reverse=True)

        for row in rows:
            # remove it from our data structure
            del self.data[row]
            # notify the view(s) using this model that it has been removed
            self.RowDeleted(row)

    def AddRow(self, value):
        # update data structure
        self.data.append(value)
        # notify views
        self.RowAppended()


