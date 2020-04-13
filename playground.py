# a dialog for just about anything
import wx
import logging
import fn_widget as w
import wx.dataview as dv
import forms as frm
from lists import states
from models import PyTestModel
from validators import FieldValidator, not_empty


class PlaygroundForm(wx.Dialog):

    def __init__(self, parent=None):
        super().__init__(parent, id=wx.ID_ANY, title=u"Form Demo", pos=wx.DefaultPosition,
                           size=wx.Size(600, 800), style=wx.DEFAULT_DIALOG_STYLE | wx.WS_EX_VALIDATE_RECURSIVELY)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)
        self.list = self.create_list()
        main_sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
        btn_add = frm.tool_button(self, id=wx.ID_ANY, text="Add", handler=self.add_button_click)
        btn_delete = frm.tool_button(self, id=wx.ID_ANY, text="Del", handler=self.delete_button_click)
        tool_sizer = frm.hsizer([btn_add, btn_delete])
        main_sizer.Add(tool_sizer, wx.SizerFlags(0))
        self.name_validator = FieldValidator(self.data[0], None, 0, [not_empty])
        self.age_validator = FieldValidator(self.data[0], None, 1, [not_empty])
        self.edit_form()

        # frame stuff
        self.Layout()
        self.Centre(wx.BOTH)
        main_sizer.Fit(self)
        # Connect Events
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInitDialog)

    def OnInitDialog(self, event):
        logging.info('Playgound Dialog Initialized')

    def list_selection_change(self, event: dv.DataViewEvent):
        selected_item = self.list.GetSelection()
        record = self.model.ItemToObject(selected_item)
        name_edit: wx.Window = wx.Window.FindWindowByName("name", self)
        age_edit: wx.Window = wx.Window.FindWindowByName("age", self)

        name_edit.Validator.set_data(record)
        age_edit.Validator.set_data(record)

        self.TransferDataToWindow()
        #name_edit.SetValue(record[0])
        #age_edit.SetValue(record[1])

    # def OnOKButtonClick(self, event):
    #     print("ya clicked ok ya know")
    #     event.Skip()

    def add_button_click(self, event):
        new_person = ['Mike', '44', '55']
        self.data.append(new_person)
        self.model.ItemAdded(dv.NullDataViewItem, self.model.ObjectToItem(new_person))

    def delete_button_click(self, event):
        self.model.ItemDeleted(dv.NullDataViewItem, self.model.ObjectToItem(self.data[0]))
        del(self.data[0])

    def create_list(self):
        dvc = dv.DataViewCtrl(self, wx.ID_ANY, style=wx.BORDER_THEME)
        self.data = [['Peter', '33', '100'], ['Fred', '22', '98'], ['Malcolm', '43', '77']]
        self.model = PyTestModel(self.data)
        dvc.AssociateModel(self.model)
        self.model.DecRef()

        dvc.AppendTextColumn("Name", 0, width=260, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvc.AppendTextColumn("Age", 1, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvc.AppendTextColumn("Weight", 2, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
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
            frm.edit_line("Name", [frm.TextField("name", frm.large(), validator=self.name_validator)]),
            frm.edit_line("Age", [frm.TextField("age", frm.small(), validator=self.age_validator)]),
            frm.edit_line("Member", [frm.CheckboxField("member")]),
            frm.edit_line("Address", [frm.TextField("addr1", frm.large(), validator=self.name_validator)]),
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

