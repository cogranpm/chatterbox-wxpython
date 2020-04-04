# a dialog for just about anything
import wx
import logging
import fn_widget as w
import wx.dataview as dv


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


class PyTestModel(dv.PyDataViewModel):
    """
    this class has a neat way to get the object that is stored
    inside the row of the table without resorting to storing pointers etc
    also supports sorting, adding, editing and deleting
    also supports attributes on cells etc
    """
    def __init__(self, data):
        super().__init__()
        self.data = data

    def GetChildren(self, item, children):
        for row in self.data:
            children.append(self.ObjectToItem(row))
        print("Hi this should update:", self.data)
        return len(self.data)

    def IsContainer(self, item):
        if not item:
            return True
        return False

    def GetParent(self, item):
        return dv.NullDataViewItem

    def GetColumnType(self, col):
        return 'string'

    def GetColumnCount(self):
        return len(self.data[0])

    def GetValue(self, item, col):
        row = self.ItemToObject(item)
        return row[col]

    def GetAttr(self, item, col, attr):
        if col == 1:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def SetValue(self, variant, item, col):
        row = self.ItemToObject(item)
        row[col] = variant
        return True

    def Compare(self, item1, item2, col, ascending):
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.ItemToObject(item1)
        row2 = self.ItemToObject(item2)

        # different sort depending on column
        if col == 1 or col == 2:
            a = int(row1[col])
            b = int(row2[col])
            return (a > b) - (a < b)
        else:
            a = row1[col]
            b = row2[col]
            return (a > b) - (a < b)


class PlaygroundForm(wx.Dialog):

    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Settings", pos=wx.DefaultPosition,
                           size=wx.Size(604, 230), style=wx.DEFAULT_DIALOG_STYLE)

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
        selected_item = self.dvc.GetSelection()
        print(self.model.ItemToObject(selected_item))

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

    def OnFlexGridSizer(self, parent):
        panel = w.panel(parent)
        # vertical sizer to split screen
        box = wx.BoxSizer(wx.VERTICAL)
        # sizer to display help text
        # textbox = wx.BoxSizer(wx.HORIZONTAL)
        helpstr = """
This is the FlexGrid Sizer demo 
specify which columns or rows should grow
grow flexibly in either direction meaning,
you can specify proportional amounts for child elements
and specify behaviour in the non flexible direction
growable row means in the vertical direction
growable col means in the horizontal direction
use the proportion argument in the Add method to make cell grow at different amount """
        sizerheader = wx.StaticText(panel, 0, "Flex Grid Sizer")
        sizerlabel = wx.StaticText(panel, 0, helpstr.lstrip())
        sizerheader.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizerlabel.SetFont(wx.Font(14, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        box.Add(sizerheader, 0, wx.ALL, 5)
        # add a static line
        box.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        box.Add(sizerlabel, 0, wx.ALL, 5)
        box.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        # grid bag sizer demo
        demolabel = wx.StaticText(panel, -1, "Name:")
        demotext = wx.TextCtrl(panel, -1, "Emmett")

        agelabel = wx.StaticText(panel, -1, "Date of Birth:")
        agetext = wx.TextCtrl(panel, -1, "06/19/2015")

        lbladdress = wx.StaticText(panel, -1, "Address:")
        addr1 = wx.TextCtrl(panel, -1, "Flat 1")
        addr2 = wx.TextCtrl(panel, -1, "18890 Edgewood Ln")

        lblcity = wx.StaticText(panel, -1, "City, State, Zip:")
        city = wx.TextCtrl(panel, -1, "Prior Lake", size=(150, -1))
        state = wx.TextCtrl(panel, -1, "MN", size=(50, -1))
        zip = wx.TextCtrl(panel, -1, "55370", size=(70, -1))

        lblphone = wx.StaticText(panel, -1, "Phone:")
        phone = wx.TextCtrl(panel, -1, "612 562 4433")

        lblemail = wx.StaticText(panel, -1, "Email:")
        email = wx.TextCtrl(panel, -1, "mussym@live.com")

        gridsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        gridsizer.AddGrowableCol(1)

        gridsizer.Add(demolabel, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        # make the name expand
        gridsizer.Add(demotext, proportion=0, flag=wx.EXPAND)

        # age
        gridsizer.Add(agelabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        # keep the age a fixed size
        gridsizer.Add(agetext, 0, 0)

        # address
        gridsizer.Add(lbladdress, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(addr1, 0, wx.EXPAND)
        # empty space in between, address 2 has no label, just space
        # gridsizer.Add((10, 10))
        gridsizer.AddSpacer(10)
        gridsizer.Add(addr2, 0, wx.EXPAND)

        # city state zip
        gridsizer.Add(lblcity, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        # an inline box sizer for the single line city, state, zip
        cstsizer = wx.BoxSizer(wx.HORIZONTAL)
        cstsizer.Add(city, 1)  # city expands, state and zip do not
        cstsizer.Add(state, 0, wx.LEFT | wx.RIGHT, 5)  # border on each side of state
        cstsizer.Add(zip)
        gridsizer.Add(cstsizer, 0, wx.EXPAND)

        # phone
        gridsizer.Add(lblphone, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(phone, 0, wx.EXPAND)

        # email
        gridsizer.Add(lblemail, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(email, 0, wx.EXPAND)

        # can add a sizer to a sizer, not just add widget to sizer, creates a nested sizer
        box.Add(gridsizer, 0, wx.EXPAND | wx.ALL, 10)

        # some buttons on the bottom
        savebtn = wx.Button(panel, -1, "Save")
        cancelbtn = wx.Button(panel, -1, "Cancel")
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        # this spacer pushes the buttons to the right
        # btnSizer.Add((20, 20), 1)
        btnSizer.AddStretchSpacer(20)
        btnSizer.Add(savebtn)
        btnSizer.AddSpacer(20)
        btnSizer.Add(cancelbtn)
        btnSizer.AddSpacer(20)
        box.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM | wx.ALIGN_RIGHT, 10)

        panel.SetSizer(box)
        box.Fit(parent)  # this call triggers the layout alorithm to fire
        box.SetSizeHints(parent)
        panel.SetBackgroundColour("orange")
        panel.Refresh()
