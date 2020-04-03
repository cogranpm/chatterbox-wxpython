# a dialog for just about anything
import wx
import logging
import fn_widget as w
import wx.dataview as dv

# if using a list of lists style this could be generic for any domain model data
class TestModel(dv.DataViewIndexListModel):
#class TestModel(dv.PyDataViewModel):

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



class PlaygroundForm(wx.Dialog):

    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Settings", pos=wx.DefaultPosition,
                           size=wx.Size(604, 230), style=wx.DEFAULT_DIALOG_STYLE)


        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # testing out the list control
        self.dvc = dv.DataViewCtrl(self, wx.ID_ANY, style = wx.BORDER_THEME)
        data = [['Peter', '33', '100'], ['Fred', '22', '98']]
        self.model = TestModel(data)
        self.dvc.AssociateModel(self.model)
        self.dvc.AppendTextColumn("Name",  0, width=260, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Age",   1, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Weight", 2, width=80,  mode=dv.DATAVIEW_CELL_EDITABLE)
        for c in self.dvc.Columns:
            c.Sortable = True
        self.dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.list_selection_change)

        # seesaw is a immediate function with keyword arguments style
        # big on first class functions so function takes a list, some of the arguments are functions themselves
        # the functions would be called before being passed to the called function
        test_sizer = w.hsizer(
            items=[
                w.tool_button(parent=self, id=wx.ID_ANY, text="GO", handler=self.go_button_click),
                w.tool_button(parent=self, id=wx.ID_ANY, text="OH", handler=self.oh_button_click),
                w.hsizer(
                    items=[
                        w.tool_button(parent=self, id=wx.ID_ANY, text="IN", handler=self.go_button_click),
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

        # dataview list control sample
        # wxPython demo shows direct use of model



        # stdButtonSizer = wx.StdDialogButtonSizer()
        # self.stdButtonSizerOK = wx.Button(self, wx.ID_OK)
        # stdButtonSizer.AddButton(self.stdButtonSizerOK)
        # self.stdButtonSizerCancel = wx.Button(self, wx.ID_CANCEL)
        # stdButtonSizer.AddButton(self.stdButtonSizerCancel)
        # stdButtonSizer.Realize()

        bSizer1.Add(self.dvc, 1, wx.EXPAND)
        bSizer1.Add(test_sizer)
        bSizer1.Add(std_buttons, 0, wx.EXPAND, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInitDialog)
        #self.stdButtonSizerOK.Bind(wx.EVT_BUTTON, self.OnOKButtonClick)


    def OnInitDialog(self, event):
        logging.info('Playgound Dialog Initialized')

    def list_selection_change(self, event: dv.DataViewEvent):
        print('selection made', event)
        print(event.GetModel().data)
        selected_item =self.dvc.GetSelection()
        # need to use the DataViewItemObjectMapper for this or the PyDataViewModel as the model baseclass
        #print(self.model.ItemToObject(selected_item))

    def OnOKButtonClick(self, event):
        print("ya clicked ok ya know")
        event.Skip()

    def go_button_click(self, event):
        print("clicked go on me did ya")

    def oh_button_click(self, event):
        print("clicked oh on me did ya")

