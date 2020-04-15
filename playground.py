# a dialog for just about anything
import wx
import logging
import fn_widget as w
import wx.dataview as dv
import forms as frm
from lists import states
from models import PyTestModel, ColumnSpec, ColumnType
from validators import FieldValidator, not_empty
from typing import List, Dict


def create_data():
    return [{'name': 'Fred', 'age': 22, 'member': False, 'address1': "44 Jones lane"},
            {'name': 'Peter', 'age': 76, 'member': True, 'address1': "22 Honeysuckle Avenue"},
            {'name': 'Beltran', 'age': 22, 'member': True, 'address1': "223 Brigard Stree"},
            {'name': 'Anne', 'age': 4, 'member': False, 'address1': "4 The Alter Place"}]


class PlaygroundForm(wx.Dialog):

    def __init__(self, parent=None):
        super().__init__(parent, id=wx.ID_ANY, title=u"Form Demo", pos=wx.DefaultPosition,
                           size=wx.Size(600, 800), style=wx.DEFAULT_DIALOG_STYLE | wx.WS_EX_VALIDATE_RECURSIVELY)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)
        self.create_columns()
        self.data = create_data()
        self.model = PyTestModel(self.data, self.columns)
        self.list = self.create_list()
        self.name_validator = FieldValidator(self.data[0], self.name_column.key, [not_empty])
        self.age_validator = FieldValidator(self.data[0], self.age_column.key, [not_empty])
        self.address1_validator = FieldValidator(self.data[0], self.address1_column.key, [])

        main_sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
        btn_add = frm.tool_button(self, id=wx.ID_ANY, text="Add", handler=self.add_button_click)
        btn_delete = frm.tool_button(self, id=wx.ID_ANY, text="Del", handler=self.delete_button_click)
        tool_sizer = frm.hsizer([btn_add, btn_delete])
        main_sizer.Add(tool_sizer, wx.SizerFlags(0))

        self.edit_form()

        # frame stuff
        self.Layout()
        self.Centre(wx.BOTH)
        main_sizer.Fit(self)
        # Connect Events
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInitDialog)

    def OnInitDialog(self, event):
        logging.info('Playgound Dialog Initialized')

    def create_columns(self):
        self.name_column = ColumnSpec('name', ColumnType.str, 'Name', 100, True)
        self.age_column = ColumnSpec('age', ColumnType.int, 'Age', 40, True)
        self.member_column = ColumnSpec('member', ColumnType.bool, 'Member', 40, True)
        self.address1_column = ColumnSpec('address1', ColumnType.str, 'Address', 120, True)
        self.columns = {self.name_column.key: self.name_column, self.age_column.key: self.age_column, self.member_column.key: self.member_column,
                        self.address1_column.key: self.address1_column}

    def list_selection_change(self, event: dv.DataViewEvent):
        selected_item = self.list.GetSelection()
        record = self.model.ItemToObject(selected_item)
        for key in self.columns:
            print(key)
            control: wx.Window = wx.Window.FindWindowByName(key, self)
            if control is not None and control.Validator is not None:
                control.Validator.set_data(record)

        self.TransferDataToWindow()

    # def OnOKButtonClick(self, event):
    #     print("ya clicked ok ya know")
    #     event.Skip()

    def add_button_click(self, event):
        new_person = {'name': 'Peter', 'age': 33, 'address1': '14 Angel Terrace'}
        self.data.append(new_person)
        self.model.ItemAdded(dv.NullDataViewItem, self.model.ObjectToItem(new_person))

    def delete_button_click(self, event):
        self.model.ItemDeleted(dv.NullDataViewItem, self.model.ObjectToItem(self.data[0]))
        del(self.data[0])

    def create_list_column(self, index: int, dvc: dv.DataViewCtrl, column_spec: ColumnSpec):
        if column_spec.data_type == ColumnType.bool:
            list_column: dv.DataViewColumn = dvc.AppendToggleColumn(column_spec.label, index,
                                                                    width=column_spec.width,
                                                                    mode=dv.DATAVIEW_CELL_EDITABLE)
        else:
            list_column = dvc.AppendTextColumn(column_spec.label, index, width=column_spec.width,
                                               mode=dv.DATAVIEW_CELL_EDITABLE)
        return list_column

    def create_list(self):
        dvc = dv.DataViewCtrl(self, wx.ID_ANY, style=wx.BORDER_THEME)
        dvc.AssociateModel(self.model)
        self.model.DecRef()

        for i, key in enumerate(self.columns):
            column_spec = self.columns[key]
            if column_spec.browseable:
                column = self.create_list_column(i, dvc, column_spec)

        for c in dvc.Columns:
            c.Sortable = True

        dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.list_selection_change)
        return dvc

    def edit_form(self):
        helpstr = """
        This is the FlexGrid Sizer demo 
        specify  which columns or rows should grow
        grow flexibly in either direction meaning,
        you can specify proportional amounts for child elements
        and specify behaviour in the non flexible direction
        growable row means in the vertical direction
        growable col means in the horizontal direction
        use the proportion argument in the Add method to make cell grow at different amount """

        person_form = frm.form(self, "frmDemo", "Form Demo", helpstr,[
            frm.edit_line("Name", [frm.TextField(self.name_column.key, frm.large(), validator=self.name_validator)]),
            frm.edit_line("Age", [frm.TextField(self.age_column.key, frm.small(), validator=self.age_validator)]),
            frm.edit_line("Member", [frm.CheckboxField("member")]),
            frm.edit_line("Address", [frm.TextField(self.address1_column.key, frm.large(), validator=self.address1_validator)]),
            frm.edit_line(None, [frm.TextField("addr2", frm.large(), validator=self.name_validator)]),
            frm.edit_line("City, State, Zip", [
                frm.TextField("city", frm.large(), validator=self.name_validator),
                frm.ComboField("state", frm.medium(), states),
                frm.TextField("zip", frm.small(), validator=self.name_validator)
            ]),
            frm.edit_line("Phone", [frm.TextField("phone", frm.small(), validator=self.name_validator)]),
            frm.edit_line("Email", [frm.TextField("email", frm.medium(), validator=self.name_validator)])
        ])

        panel = person_form.build()
        return panel

    def seesaw_style_test(self):
        # seesaw is a immediate function with keyword arguments style
        # big on first class functions so function takes a list, some of the arguments are functions themselves
        # the functions would be called before being passed to the called function
        test_sizer = w.hsizer(
            items=[
                w.tool_button(parent=self, id=wx.ID_ANY, text="Add", handler=self.add_button_click),
                w.tool_button(parent=self, id=wx.ID_ANY, text="Del", handler=self.delete_button_click),
                w.hsizer(
                    items=[
                        w.tool_button(parent=self, id=wx.ID_ANY, text="IN", handler=self.add_button_click),
                    ]
                )
            ]
        )

        # declarative ui style begin
        # not sure, this is more groovy builder style using function vars
        # seesaw style is more direct using named arguments and function calls
        widget_list = \
            [
                [w.sizer, [],
                 [
                     [w.std_buttons, [self, self.OnOKButtonClick]]
                 ]
                 ]
            ]

        # first child is the wiget function
        # second position is list of arguments
        # third position is list containing children
        # this is a test, in reality the whole list of lists structure would be recursed etc
        sizer_dec = widget_list[0][0]
        bSizer1 = sizer_dec()
        child_list = widget_list[0][2]
        std_buttons_list = child_list[0]
        std_buttons_dec = std_buttons_list[0]
        std_buttons_arg = std_buttons_list[1]
        # call the widget functions with arguments contained in list
        # first should be parent instance, second  should be click handler
        std_buttons = std_buttons_dec(std_buttons_arg)
        return test_sizer

