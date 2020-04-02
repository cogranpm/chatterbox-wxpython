# a dialog for just about anything
import wx
import logging
import fn_widget as w

class PlaygroundForm(wx.Dialog):

    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Settings", pos=wx.DefaultPosition,
                           size=wx.Size(604, 230), style=wx.DEFAULT_DIALOG_STYLE)


        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

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


        # stdButtonSizer = wx.StdDialogButtonSizer()
        # self.stdButtonSizerOK = wx.Button(self, wx.ID_OK)
        # stdButtonSizer.AddButton(self.stdButtonSizerOK)
        # self.stdButtonSizerCancel = wx.Button(self, wx.ID_CANCEL)
        # stdButtonSizer.AddButton(self.stdButtonSizerCancel)
        # stdButtonSizer.Realize()

        bSizer1.Add(std_buttons, 0, wx.EXPAND, 5)
        bSizer1.Add(test_sizer)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInitDialog)
        #self.stdButtonSizerOK.Bind(wx.EVT_BUTTON, self.OnOKButtonClick)


    def OnInitDialog(self, event):
        logging.info('Playgound Dialog Initialized')


    def OnOKButtonClick(self, event):
        print("ya clicked ok ya know")
        event.Skip()

    def go_button_click(self, event):
        print("clicked go on me did ya")

    def oh_button_click(self, event):
        print("clicked oh on me did ya")

