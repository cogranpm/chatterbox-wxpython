# a dialog for just about anything
import wx
import logging
import fn_widget as w

class PlaygroundForm(wx.Dialog):

    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Settings", pos=wx.DefaultPosition,
                           size=wx.Size(604, 230), style=wx.DEFAULT_DIALOG_STYLE)


        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # declarative ui style begin
        widget_list = \
            [[w.sizer, [],
            [w.std_buttons, [self, self.OnOKButtonClick]]
            ]]


        bSizer1 = widget_list[0][0]
        #std_button_container = widget_list

        stdButtonSizer = wx.StdDialogButtonSizer()
        self.stdButtonSizerOK = wx.Button(self, wx.ID_OK)
        stdButtonSizer.AddButton(self.stdButtonSizerOK)
        self.stdButtonSizerCancel = wx.Button(self, wx.ID_CANCEL)
        stdButtonSizer.AddButton(self.stdButtonSizerCancel)
        stdButtonSizer.Realize()

        bSizer1.Add(stdButtonSizer, 0, wx.EXPAND, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInitDialog)
        self.stdButtonSizerOK.Bind(wx.EVT_BUTTON, self.OnOKButtonClick)


    def OnInitDialog(self, event):
        logging.info('Playgound Dialog Initialized')


    def OnOKButtonClick(self, event):
        event.Skip()
