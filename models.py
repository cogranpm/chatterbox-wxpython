# -------- python imports -------------
from typing import List, Dict, Callable
from dataclasses import dataclass
from enum import Enum
from abc import ABCMeta, ABC, abstractmethod

# ---------- lib imports --------------
import wx.dataview as dv
import wx

# ---------- project imports -----------
# import views as v
import data_functions as df
import chatterbox_constants as c
import forms as frm

ViewState = Enum('ViewState', 'adding dirty loaded loading empty')
BindDirection = Enum('BindDirection', 'from_window to_window')
ColumnType = Enum('ColumnType', 'str bool float int date')
column_type_map: Dict[ColumnType, str] = {ColumnType.str: 'string', ColumnType.bool: 'bool',
                                          ColumnType.float: 'double', ColumnType.int: 'string',
                                          ColumnType.date: 'datetime'}


@dataclass(frozen=True)
class ColumnSpec:
    key: str
    data_type: ColumnType
    label: str
    width: int
    format_fn: Callable = None
    browseable: bool = True
    sortable: bool = False


class BasePresenter(ABC):

    @staticmethod
    def start_editing(event):
        event.Veto()

    def __init__(self, parent: wx.Window, model: 'BaseEntityModel', view):
        self.parent = parent
        self.model = model
        self.view = view
        self.view.set_list(self.model.columns)
        self.view.list.AssociateModel(self.model)
        self.model.DecRef()
        # required for linux, veto the editing event
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_START_EDITING, self.start_editing)
        self.view.list.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.selection_handler)
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit_handler)
        wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
        wx.py.dispatcher.connect(receiver=self.add, signal=c.SIGNAL_ADD)
        wx.py.dispatcher.connect(receiver=self.delete, signal=c.SIGNAL_DELETE)

    # handle the toolbar buttons
    def save(self, command, more):
        if more is self.view:
            if self.view_state == ViewState.adding:
                record = self.model.make_new_record()
                self.form_def.bind(record)
            if self.view.Validate():
                self.view.bind(BindDirection.from_window)
                if self.view_state == ViewState.adding:
                    self.added_record(record)
                    df.add_record(self.model.collection_name, record)
                else:
                    selected_item = self.view.list.GetSelection()
                    record = self.model.ItemToObject(selected_item)
                    df.update_record(self.model.collection_name, record)
                    self.edited_record(record)
                self.set_view_state(ViewState.loaded)

    def add(self, command, more):
        if more is self.view:
            self.set_view_state(ViewState.adding)

    def delete(self, command, more):
        if more is self.view:
            selected_item = self.view.list.GetSelection()
            if selected_item is not None:
                if frm.confirm_delete(self.view):
                    self.model.ItemDeleted(dv.NullDataViewItem, selected_item)
                    record = self.model.ItemToObject(selected_item)
                    df.delete_record(self.model.collection_name, record)
                    self.model.data.remove(record)
                    self.set_view_state(ViewState.empty)

    def set_view_state(self, state: ViewState):
        # need to update the form
        if state == ViewState.adding:
            self.form_def.reset_fields()
            self.form_def.enable_fields(True)
            self.form_def.setfocusfirst()
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_ADDING, more=self)
        elif state == ViewState.empty:
            self.form_def.reset_fields()
            self.form_def.enable_fields(False)
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_EMPTY, more=self)
        elif state == ViewState.loaded:
            self.form_def.enable_fields(True)
            self.form_def.setfocusfirst()
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_LOADED, more=self)
            self.form_def.pause_dirty_events(False)
        elif state == ViewState.loading:
            self.form_def.pause_dirty_events(True)

        self.view_state = state


    def selection_handler(self, event):
        # not quite sure what to do, load the selection so it can be deleted?
        pass

    def edit_handler(self, event: dv.DataViewEvent):
        self.set_view_state(ViewState.loading)
        selected_item = self.view.list.GetSelection()
        record = self.model.ItemToObject(selected_item)
        # this sets the data property on all the validators that are defined for all the fields
        self.form_def.bind(record)
        # this tells view to push data from model to the controls
        self.view.bind(BindDirection.to_window)
        self.set_view_state(ViewState.loaded)



    def edited_record(self, record):
        self.model.ItemChanged(self.model.ObjectToItem(record))

    def update_data(self, data):
        self.model.change_data(data)

    def added_record(self, record):
        self.model.data.append(record)
        self.model.ItemAdded(dv.NullDataViewItem, self.model.ObjectToItem(record))


class BaseEntityModel(dv.PyDataViewModel):

    def __init__(self, parent_key: int, columns: List[ColumnSpec], collection_name: str):
        super().__init__()
        self.collection_name = collection_name
        self.parent_key = parent_key
        self.columns = columns
        self.data = dict()
        self.view_state = ViewState.empty
        df.create_entity(self.collection_name)

    @abstractmethod
    def get_records(self):
        pass

    @abstractmethod
    def make_new_record(self):
        pass

    def create_data(self):
        records = self.get_records()
        data_list = []
        for record in records:
            data_list.append(record)
        return data_list


    def change_data(self, records):
        self.data = records
        # cleared doesn't work on linux
        # so need to delete by item and
        # add by item

        if self.data is not None:
            for item in self.data:
                object = self.ObjectToItem(item)
                if object is not None:
                    self.ItemDeleted(dv.NullDataViewItem, self.ObjectToItem(item))

        for record in self.data:
            self.ItemAdded(dv.NullDataViewItem, self.ObjectToItem(record))


    def get_column_by_index(self, index):
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
        col_type = column_type_map[self.get_column_by_index(col).data_type]
        return col_type

    def GetColumnCount(self):
        return len(self.columns)

    def GetValue(self, item, col):
        try:
            row = self.ItemToObject(item)
        except Exception as ex:
            print(ex)
        column_spec: ColumnSpec = self.get_column_by_index(col)
        value = row[column_spec.key]
        if column_spec.format_fn is not None:
            return column_spec.format_fn(value)
        return value

    def GetAttr(self, item, col, attr):
        # if col == 1:
        #    attr.SetColour('blue')
        #    attr.SetBold(True)
        #    return True
        return False

    def SetValue(self, variant, item, col):
        try:
            row = self.ItemToObject(item)
            row[self.get_column_by_index(col).key] = variant
        except Exception as ex:
            print(ex)
        return True

    def Compare(self, item1, item2, col, ascending):
        try:
            if not ascending:  # swap sort order?
                item2, item1 = item1, item2

            row1 = self.ItemToObject(item1)
            row2 = self.ItemToObject(item2)

            # different sort depending on column
            if self.get_column_by_index(col).data_type == ColumnType.int:
                a = int(row1[self.get_column_by_index(col).key])
                b = int(row2[self.get_column_by_index(col).key])
                return (a > b) - (a < b)
            # elif self.get_column_by_index(col).data_type == ColumnType.date:
            #    return 0
            else:
                a = row1[self.get_column_by_index(col).key]
                b = row2[self.get_column_by_index(col).key]
                return (a > b) - (a < b)
        except Exception as ex:
            print(ex)
            return 0

# this is a wxPython xtra model based class
# has a ItemToObject mapper built in which makes
# selection processing easy
class EntityModel(dv.PyDataViewModel):
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
        
    def change_data(self, records):
        # cleared doesn't work on linux
        # so need to delete by item and 
        # add by item
        if self.data is not None:
            for item in self.data:
                object = self.ObjectToItem(item)
                if object is not None:
                    self.ItemDeleted(dv.NullDataViewItem, self.ObjectToItem(item))
        
        self.data = records        
        for record in self.data:
            self.ItemAdded(dv.NullDataViewItem, self.ObjectToItem(record))

    def get_column_by_index(self, index):
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
        col_type = column_type_map[self.get_column_by_index(col).data_type]
        return col_type

    def GetColumnCount(self):
        return len(self.columns)

    def GetValue(self, item, col):
        try:
            row = self.ItemToObject(item)
        except Exception as ex:
            print(ex)
        column_spec: ColumnSpec = self.get_column_by_index(col)
        value = row[column_spec.key]
        if column_spec.format_fn is not None:
            return column_spec.format_fn(value)
        return value

    def GetAttr(self, item, col, attr):
        #if col == 1:
        #    attr.SetColour('blue')
        #    attr.SetBold(True)
        #    return True
        return False

    def SetValue(self, variant, item, col):
        try:
            row = self.ItemToObject(item)
            row[self.get_column_by_index(col).key] = variant
        except Exception as ex:
            print(ex)
        return True

    def Compare(self, item1, item2, col, ascending):
        try:
            if not ascending: # swap sort order?
                item2, item1 = item1, item2

            row1 = self.ItemToObject(item1)
            row2 = self.ItemToObject(item2)

            # different sort depending on column
            if self.get_column_by_index(col).data_type == ColumnType.int:
                a = int(row1[self.get_column_by_index(col).key])
                b = int(row2[self.get_column_by_index(col).key])
                return (a > b) - (a < b)
            #elif self.get_column_by_index(col).data_type == ColumnType.date:
            #    return 0
            else:
                a = row1[self.get_column_by_index(col).key]
                b = row2[self.get_column_by_index(col).key]
                return (a > b) - (a < b)
        except Exception as ex:
            print(ex)
            return 0

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


