# a dialog for just about anything
import wx
import logging
import fn_widget as w
import wx.dataview as dv
import forms as frm
from lists import states
from models import PyTestModel


class PlaygroundForm(wx.Dialog):

    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Settings", pos=wx.DefaultPosition,
                           size=wx.Size(1200, 1200), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # testing out the list control
        self.dvc = dv.DataViewCtrl(self, wx.ID_ANY, style = wx.BORDER_THEME)
        self.data = [['Peter', '33', '100'], ['Fred', '22', '98'], ['Malcolm', '43', '77']]
        self.model = PyTestModel(self.data)
        self.dvc.AssociateModel(self.model)
        self.model.DecRef()

        self.dvc.AppendTextColumn("Name",  0, width=260, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Age",   1, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Weight", 2, width=80,  mode=dv.DATAVIEW_CELL_EDITABLE)
        for c in self.dvc.Columns:
            c.Sortable = True
        self.dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.list_selection_change)

        btn_add = frm.tool_button(parent=self, id=wx.ID_ANY, text="Add", handler=self.add_button_click)
        btn_delete = frm.tool_button(parent=self, id=wx.ID_ANY, text="Del", handler=self.delete_button_click)
        tool_sizer = frm.hsizer([btn_add, btn_delete])

        edit_panel = self.edit_form(self)

        # not sure if needed
        # stdButtonSizer = wx.StdDialogButtonSizer()
        # self.stdButtonSizerOK = wx.Button(self, wx.ID_OK)
        # stdButtonSizer.AddButton(self.stdButtonSizerOK)
        # self.stdButtonSizerCancel = wx.Button(self, wx.ID_CANCEL)
        # stdButtonSizer.AddButton(self.stdButtonSizerCancel)
        # stdButtonSizer.Realize()

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        list_sizer = frm.vsizer()
        list_sizer.Add(self.dvc, wx.SizerFlags(1).Expand())
        list_sizer.Add(tool_sizer, wx.SizerFlags().Expand().Border(wx.ALL, 5))
        main_sizer.Add(list_sizer, wx.SizerFlags(1).Expand())
        main_sizer.Add(edit_panel, 1, wx.EXPAND, 5)
        # not sure if this is needed for a tabbed ui
        # main_sizer.Add(stdButtonSizer, 0, wx.EXPAND, 5)
        main_sizer.Fit(self)
        # frame stuff
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)
        # Connect Events
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInitDialog)
        # self.stdButtonSizerOK.Bind(wx.EVT_BUTTON, self.OnOKButtonClick)


    def OnInitDialog(self, event):
        logging.info('Playgound Dialog Initialized')

    def list_selection_change(self, event: dv.DataViewEvent):
        selected_item = self.dvc.GetSelection()
        record = self.model.ItemToObject(selected_item)
        name_edit: wx.Window = wx.Window.FindWindowByName("name", self)
        age_edit: wx.Window = wx.Window.FindWindowByName("age", self)
        name_edit.SetValue(record[0])
        age_edit.SetValue(record[1])

    def OnOKButtonClick(self, event):
        print("ya clicked ok ya know")
        event.Skip()

    def add_button_click(self, event):
        new_person = ['Mike', '44', '55']
        self.data.append(new_person)
        self.model.ItemAdded(dv.NullDataViewItem, self.model.ObjectToItem(new_person))

    def delete_button_click(self, event):
        self.model.ItemDeleted(dv.NullDataViewItem, self.model.ObjectToItem(self.data[0]))
        del(self.data[0])

    def edit_form(self, parent):
        helpstr = """
        This is the FlexGrid Sizer demo 
        specify  which columns or rows should grow
        grow flexibly in either direction meaning,
        you can specify proportional amounts for child elements
        and specify behaviour in the non flexible direction
        growable row means in the vertical direction
        growable col means in the horizontal direction
        use the proportion argument in the Add method to make cell grow at different amount """

        person_form = frm.form(parent, "frmDemo", "Form Demo", helpstr,[
            frm.edit_line("Name", [frm.TextField("name", frm.large())]),
            frm.edit_line("Age", [frm.TextField("age", frm.small())]),
            frm.edit_line("Member", [frm.CheckboxField("member")]),
            frm.edit_line("Address", [frm.TextField("addr1", frm.large())]),
            frm.edit_line(None, [frm.TextField("addr2", frm.large())]),
            frm.edit_line("City, State, Zip", [
                frm.TextField("city", frm.large()),
                frm.ComboField("state", frm.medium(), states),
                frm.TextField("zip", frm.small())
            ]),
            frm.edit_line("Phone", [frm.TextField("phone", frm.small())]),
            frm.edit_line("Email", [frm.TextField("email", frm.medium())])
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

