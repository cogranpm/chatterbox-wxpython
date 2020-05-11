import wx
import wx.xrc
import wx.aui
import wx.py as py

import chatterbox_constants as c
from SettingsDialogImp import SettingsDialogImp
from fn_app import make_icon
import logging
import playground
import shelf
import copyfiles




class AppFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Chatterbox", pos = wx.DefaultPosition,
                         size = wx.Size(1133,716 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL, name = u"MainFrame")
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.setup()
        ico = wx.Icon('icons/disconnect2.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        # self.m_btnEditShelf.SetBitmap(wx.Bitmap('icons/Edit.png', wx.BITMAP_TYPE_PNG))
        self.m_btnEditShelf.SetBitmap(make_icon('Edit.png'))
        self.m_btnAddShelf.SetBitmap(make_icon('Add.png'))
        self.m_btnDeleteShelf.SetBitmap(make_icon('Cancel.png'))
        wx.py.dispatcher.connect(receiver=self.on_viewstate, signal=c.SIGNAL_VIEWSTATE)
        wx.py.dispatcher.connect(receiver=self.on_view_activated, signal=c.SIGNAL_VIEW_ACTIVATED)
        self.Bind(wx.EVT_UPDATE_UI, self.on_updateui)

    def on_updateui(self, event):
        """ this gets called at regular intervals, can be useful for polling type logic """
        pass

    def on_view_activated(self, command, more):
        self.menuFileNew.Enable(True)
        self.toolbar.EnableTool(wx.ID_NEW, True)

    def on_viewstate(self, command, more):
        if command == c.COMMAND_ADDING:
            self.menuFileSave.Enable(True)
            self.toolbar.EnableTool(wx.ID_SAVE, True)
        elif command == c.COMMAND_EMPTY:
            self.menuEditDelete.Enable(False)
            self.toolbar.EnableTool(wx.ID_DELETE, False)
            self.menuFileSave.Enable(False)
            self.toolbar.EnableTool(wx.ID_SAVE, False)
        elif command == c.COMMAND_LOADED:
            self.menuEditDelete.Enable(True)
            self.toolbar.EnableTool(wx.ID_DELETE, True)
        elif command == c.COMMAND_DIRTY:
            # this does not quite work, also fires
            # when selection of item in list is made
            self.menuFileSave.Enable(True)
            self.toolbar.EnableTool(wx.ID_SAVE, True)


    def on_save(self, event):
        active_page = self.m_auiShelf.GetCurrentPage()
        py.dispatcher.send(signal=c.SIGNAL_SAVE, sender=self, command=c.COMMAND_SAVE, more=active_page)
        self.menuFileSave.Enable(False)
        self.toolbar.EnableTool(wx.ID_SAVE, False)

    def on_add(self, event):
        active_page = self.m_auiShelf.GetCurrentPage()
        py.dispatcher.send(signal=c.SIGNAL_ADD, sender=self, command=c.COMMAND_ADD, more=active_page)

    def on_delete(self, event):
        active_page = self.m_auiShelf.GetCurrentPage()
        py.dispatcher.send(signal=c.SIGNAL_DELETE, sender=self, command=c.COMMAND_DELETE, more=active_page)

    def on_copyfiles(self, event):
        self.m_auiShelf.AddPage(copyfiles.CopyFilesPanel(self), "Copy Files", True)

    def FileExportOnMenuSelection(self, event):
        event.Skip()

    def menuFileQuitOnMenuSelection(self, event):
        self.Close()

    def menuEditSettingsOnMenuSelection(self, event):
        app = wx.App.Get()
        with SettingsDialogImp(self, app.data_directory) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                if dlg.dirty:
                    # more than this needs to happen
                    app.data_directory = dlg.data_directory


    def handle_menu_playground(self, event):
        self.m_auiShelf.AddPage(playground.PlaygroundPanel(self), "Playground", True)

    def handle_menu_shelf(self, event):
        self.m_auiShelf.AddPage(shelf.ShelfPanel(self), "Shelf", True)


    def OnNotebookPageChanged(self, event):
        event.Skip()

    def OnNotebookPageClose(self, event):
        event.Skip()

    def AddShelfOnButtonClick(self, event):
        event.Skip()

    def DeleteShelfOnButtonClick(self, event):
        event.Skip()

    def EditShelfOnButtonClick(self, event):
        event.Skip()

    def AddSubjectOnButtonClick(self, event):
        event.Skip()

    def DeleteSubjectOnButtonClick(self, event):
        event.Skip()

    def EditSubjectOnButtonClick(self, event):
        event.Skip()

    def AddPublicationOnButtonClick(self, event):
        event.Skip()

    def AddPublicationOnUpdateUI(self, event):
        event.Skip()

    def DeletePublicationOnButtonClick(self, event):
        event.Skip()

    def DeletePublicationOnUpdateUI(self, event):
        event.Skip()

    def EditPublicationOnButtonClick(self, event):
        event.Skip()

    def EditPublicationOnUpdateUI(self, event):
        event.Skip()

    def m_splitter1OnIdle(self, event):
        self.m_splitter1.SetSashPosition(248)
        self.m_splitter1.Unbind(wx.EVT_IDLE)

    def m_splitter2OnIdle(self, event):
        self.m_splitter2.SetSashPosition(0)
        self.m_splitter2.Unbind(wx.EVT_IDLE)

    def setup_toolbars(self):
        self.toolbar = self.CreateToolBar()
        tsize = (24, 24)
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        delete_bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, tsize)
        self.toolbar.SetToolBitmapSize(tsize)
        self.toolbar.AddTool(wx.ID_ADD, "New", new_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "New",
                             "Long help for 'New'", None)
        self.toolbar.EnableTool(wx.ID_NEW, False)
        self.toolbar.AddTool(wx.ID_SAVE, "Save", save_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Save",
                             "Long help for 'Save'", None)
        self.toolbar.EnableTool(wx.ID_SAVE, False)
        self.toolbar.AddTool(wx.ID_DELETE, "Delete", delete_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Delete",
                             "Long help for 'Delete'", None)
        self.toolbar.EnableTool(wx.ID_DELETE, False)
        self.Bind(wx.EVT_TOOL, self.on_add, id=wx.ID_ADD)
        self.Bind(wx.EVT_TOOL, self.on_save, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.on_delete, id=wx.ID_DELETE)

        #tool_save = self.toolbar.AddTool(wx.NewId(), 'Save', make_icon('SaveHS.png'), 'Save current item')
        #tool_add = self.toolbar.AddTool(wx.NewId(), 'New', make_icon('Add.png'), 'Add a new item')

        self.toolbar.Realize()

    def setup_menus(self):

        self.m_menubar1 = wx.MenuBar(0)
        self.menuFile = wx.Menu()
        self.menuFileExport = wx.MenuItem(self.menuFile, wx.ID_ANY, u"&Export", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.menuFileExport)

        self.menuFileNew = wx.MenuItem(self.menuFile, wx.ID_ADD, u"&New", wx.EmptyString,
                                        wx.ITEM_NORMAL)
        self.menuFileNew.Enable(False)
        self.menuFileSave = wx.MenuItem(self.menuFile, wx.ID_SAVE, u"&Save", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFileQuit = wx.MenuItem(self.menuFile, wx.ID_EXIT, u"&Quit", wx.EmptyString,
                                        wx.ITEM_NORMAL)
        self.menuFile.Append(self.menuFileNew)
        self.menuFile.Append(self.menuFileSave)
        self.menuFile.Append(self.menuFileQuit)

        self.m_menubar1.Append(self.menuFile, u"&File")

        self.menuEdit = wx.Menu()
        self.menuEdit.AppendSeparator()

        self.menuEditDelete = wx.MenuItem(self.menuEdit, wx.ID_DELETE, u"Delete", wx.EmptyString,
                                            wx.ITEM_NORMAL)
        self.menuEditDelete.Enable(False)
        self.menuEdit.Append(self.menuEditDelete)

        self.menuEditSettings = wx.MenuItem(self.menuEdit, wx.ID_PREFERENCES, u"&Settings", wx.EmptyString,
                                            wx.ITEM_NORMAL)
        self.menuEdit.Append(self.menuEditSettings)


        self.m_menubar1.Append(self.menuEdit, u"&Edit")

        menuView = wx.Menu()
        self.m_menubar1.Append(menuView, "&View")

        menuViewCopyFiles = wx.MenuItem(menuView, c.ID_VIEW_COPYFILES, '&Copy Files')
        self.Bind(wx.EVT_MENU, self.on_copyfiles, id=menuViewCopyFiles.GetId())

        self.mnuEditPlayground = wx.MenuItem(menuView, wx.ID_ANY, u"Playground",
                                             wx.EmptyString, wx.ITEM_NORMAL)

        menuViewShelf = wx.MenuItem(menuView, c.ID_VIEW_SHELF, '&Shelf')
        self.Bind(wx.EVT_MENU, self.handle_menu_shelf, id=menuViewShelf.GetId())

        menuView.Append(self.mnuEditPlayground)
        menuView.Append(menuViewCopyFiles)
        menuView.Append(menuViewShelf)

        accelerator_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('Q'), self.menuFileQuit.GetId()),
            (wx.ACCEL_CTRL, ord('S'), self.menuFileSave.GetId()),
            (wx.ACCEL_CTRL, ord('N'), self.menuFileNew.GetId()),
            (wx.ACCEL_CTRL, ord('P'), self.mnuEditPlayground.GetId()),
            (wx.ACCEL_CTRL, ord('V'), menuViewShelf.GetId()),
            (wx.ACCEL_CTRL, ord('C'), menuViewCopyFiles.GetId()),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, self.menuEditDelete.GetId())
        ])
        self.AcceleratorTable = accelerator_tbl
        self.SetMenuBar(self.m_menubar1)

    def setup_statusbar(self):
        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)


    def setup_handlers(self):
        # Connect Events
        self.Bind(wx.EVT_MENU, self.FileExportOnMenuSelection, id=self.menuFileExport.GetId())
        self.Bind(wx.EVT_MENU, self.on_save, id=self.menuFileSave.GetId())
        self.Bind(wx.EVT_MENU, self.menuFileQuitOnMenuSelection, id=self.menuFileQuit.GetId())
        self.Bind(wx.EVT_MENU, self.menuEditSettingsOnMenuSelection, id=self.menuEditSettings.GetId())
        self.Bind(wx.EVT_MENU, self.handle_menu_playground, id=self.mnuEditPlayground.GetId())
        self.Bind(wx.EVT_MENU, self.on_delete, id=self.menuEditDelete.GetId())

        self.m_auiShelf.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged)
        self.m_auiShelf.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose)
        self.m_btnAddShelf.Bind(wx.EVT_BUTTON, self.AddShelfOnButtonClick)
        self.m_btnDeleteShelf.Bind(wx.EVT_BUTTON, self.DeleteShelfOnButtonClick)
        self.m_btnEditShelf.Bind(wx.EVT_BUTTON, self.EditShelfOnButtonClick)
        self.btnAddSubject.Bind(wx.EVT_BUTTON, self.AddSubjectOnButtonClick)
        self.btnDeleteSubject.Bind(wx.EVT_BUTTON, self.DeleteSubjectOnButtonClick)
        self.btnEditSubject.Bind(wx.EVT_BUTTON, self.EditSubjectOnButtonClick)
        self.btnAddPublication.Bind(wx.EVT_BUTTON, self.AddPublicationOnButtonClick)
        self.btnAddPublication.Bind(wx.EVT_UPDATE_UI, self.AddPublicationOnUpdateUI)
        self.btnDeletePublication.Bind(wx.EVT_BUTTON, self.DeletePublicationOnButtonClick)
        self.btnDeletePublication.Bind(wx.EVT_UPDATE_UI, self.DeletePublicationOnUpdateUI)
        self.btnEditPublication.Bind(wx.EVT_BUTTON, self.EditPublicationOnButtonClick)
        self.btnEditPublication.Bind(wx.EVT_UPDATE_UI, self.EditPublicationOnUpdateUI)


    def setup_shelf(self):
        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        bSizerNotebookMain = wx.BoxSizer(wx.VERTICAL)

        self.m_auiShelf = wx.aui.AuiNotebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,  style=wx.aui.AUI_NB_CLOSE_BUTTON)
        self.m_panelNotes = wx.Panel(self.m_auiShelf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panelNotes.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        splitterSizer = wx.BoxSizer(wx.VERTICAL)

        self.m_splitter1 = wx.SplitterWindow(self.m_panelNotes, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D)
        self.m_splitter1.Bind(wx.EVT_IDLE, self.m_splitter1OnIdle)

        self.pnlShelf = wx.Panel(self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.pnlShelfHeader = wx.Panel(self.pnlShelf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText5 = wx.StaticText(self.pnlShelfHeader, wx.ID_ANY, u"Shelves", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)

        bSizer6.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.m_btnAddShelf = wx.Button(self.pnlShelfHeader, c.ID_ADD_SHELF, wx.EmptyString, wx.DefaultPosition,
                                       wx.Size(20, 20), 0)
        self.m_btnAddShelf.SetMaxSize(wx.Size(25, -1))

        bSizer6.Add(self.m_btnAddShelf, 0, wx.ALIGN_LEFT, 5)

        self.m_btnDeleteShelf = wx.Button(self.pnlShelfHeader, c.ID_DELETE_SHELF, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(20, 20), 0)
        self.m_btnDeleteShelf.Enable(False)
        self.m_btnDeleteShelf.SetMaxSize(wx.Size(25, -1))

        bSizer6.Add(self.m_btnDeleteShelf, 0, 0, 5)

        self.m_btnEditShelf = wx.Button(self.pnlShelfHeader, c.ID_EDIT_SHELF, wx.EmptyString, wx.DefaultPosition,
                                        wx.Size(20, 20), 0)
        self.m_btnEditShelf.Enable(False)
        self.m_btnEditShelf.SetMaxSize(wx.Size(60, -1))

        bSizer6.Add(self.m_btnEditShelf, 0, 0, 5)

        self.pnlShelfHeader.SetSizer(bSizer6)
        self.pnlShelfHeader.Layout()
        bSizer6.Fit(self.pnlShelfHeader)
        bSizer5.Add(self.pnlShelfHeader, 0, 0, 5)

        self.pnlShelfList = wx.Panel(self.pnlShelf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer7 = wx.BoxSizer(wx.VERTICAL)


        self.m_textCtrl1 = wx.TextCtrl(self.pnlShelfList, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        self.pnlShelfList.SetSizer(bSizer7)
        self.pnlShelfList.Layout()
        bSizer7.Fit(self.pnlShelfList)
        bSizer5.Add(self.pnlShelfList, 1, wx.EXPAND, 5)

        self.pnlShelf.SetSizer(bSizer5)
        self.pnlShelf.Layout()
        bSizer5.Fit(self.pnlShelf)
        self.pnlShelfChildren = wx.Panel(self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TAB_TRAVERSAL)
        bSizer8 = wx.BoxSizer(wx.VERTICAL)
        self.m_splitter2 = wx.SplitterWindow(self.pnlShelfChildren, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                             wx.SP_3D)
        self.m_splitter2.Bind(wx.EVT_IDLE, self.m_splitter2OnIdle)

        self.setup_subject()
        self.setup_publication()

        bSizer8.Add(self.m_splitter2, 1, wx.EXPAND, 5)

        self.pnlShelfChildren.SetSizer(bSizer8)
        self.pnlShelfChildren.Layout()
        bSizer8.Fit(self.pnlShelfChildren)
        self.m_splitter1.SplitVertically(self.pnlShelf, self.pnlShelfChildren, 248)
        splitterSizer.Add(self.m_splitter1, 1, wx.EXPAND, 5)

        self.m_panelNotes.SetSizer(splitterSizer)
        self.m_panelNotes.Layout()
        splitterSizer.Fit(self.m_panelNotes)
        self.m_auiShelf.AddPage(self.m_panelNotes, u"Home", False, wx.NullBitmap)

        bSizerNotebookMain.Add(self.m_auiShelf, 1, wx.EXPAND | wx.ALL, 5)

        bSizer1.Add(bSizerNotebookMain, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)


    def setup_subject(self):
        self.pnlSubject = wx.Panel(self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        self.pnlSubjectHeader = wx.Panel(self.pnlSubject, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TAB_TRAVERSAL)
        bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText7 = wx.StaticText(self.pnlSubjectHeader, wx.ID_ANY, u"Subjects", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)

        bSizer13.Add(self.m_staticText7, 0, wx.ALL, 5)

        self.btnAddSubject = wx.Button(self.pnlSubjectHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.Size(20, 20), 0)
        self.btnAddSubject.Enable(False)
        self.btnAddSubject.SetMaxSize(wx.Size(25, -1))

        bSizer13.Add(self.btnAddSubject, 0, 0, 5)

        self.btnDeleteSubject = wx.Button(self.pnlSubjectHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(20, 20), 0)
        self.btnDeleteSubject.Enable(False)
        self.btnDeleteSubject.SetMaxSize(wx.Size(25, -1))

        bSizer13.Add(self.btnDeleteSubject, 0, 0, 5)

        self.btnEditSubject = wx.Button(self.pnlSubjectHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.Size(20, 20), 0)
        self.btnEditSubject.Enable(False)
        self.btnEditSubject.SetMaxSize(wx.Size(60, -1))

        bSizer13.Add(self.btnEditSubject, 0, 0, 5)

        self.pnlSubjectHeader.SetSizer(bSizer13)
        self.pnlSubjectHeader.Layout()
        bSizer13.Fit(self.pnlSubjectHeader)
        bSizer12.Add(self.pnlSubjectHeader, 0, wx.EXPAND, 5)

        self.pnlSubjectList = wx.Panel(self.pnlSubject, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        self.m_textCtrl2 = wx.TextCtrl(self.pnlSubjectList, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        bSizer14.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.pnlSubjectList.SetSizer(bSizer14)
        self.pnlSubjectList.Layout()
        bSizer14.Fit(self.pnlSubjectList)
        bSizer12.Add(self.pnlSubjectList, 1, wx.EXPAND, 5)

        self.pnlSubject.SetSizer(bSizer12)
        self.pnlSubject.Layout()
        bSizer12.Fit(self.pnlSubject)

    def setup_publication(self):
        self.pnlPublication = wx.Panel(self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TAB_TRAVERSAL)
        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.pnlPublicationHeader = wx.Panel(self.pnlPublication, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                             wx.TAB_TRAVERSAL)
        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText6 = wx.StaticText(self.pnlPublicationHeader, wx.ID_ANY, u"Publications", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)

        bSizer10.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.btnAddPublication = wx.Button(self.pnlPublicationHeader, c.ID_ADDPUBLICATION, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(20, 20), 0)
        self.btnAddPublication.Enable(False)
        self.btnAddPublication.SetMaxSize(wx.Size(25, -1))

        bSizer10.Add(self.btnAddPublication, 0, 0, 5)

        self.btnDeletePublication = wx.Button(self.pnlPublicationHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.Size(20, 20), 0)
        self.btnDeletePublication.Enable(False)
        self.btnDeletePublication.SetMaxSize(wx.Size(25, -1))

        bSizer10.Add(self.btnDeletePublication, 0, 0, 5)

        self.btnEditPublication = wx.Button(self.pnlPublicationHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.Size(20, 20), 0)
        self.btnEditPublication.Enable(False)
        self.btnEditPublication.SetMaxSize(wx.Size(60, -1))

        bSizer10.Add(self.btnEditPublication, 0, 0, 5)

        self.pnlPublicationHeader.SetSizer(bSizer10)
        self.pnlPublicationHeader.Layout()
        bSizer10.Fit(self.pnlPublicationHeader)
        bSizer9.Add(self.pnlPublicationHeader, 0, wx.EXPAND, 5)

        self.pnlPublicationList = wx.Panel(self.pnlPublication, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.TAB_TRAVERSAL)
        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.pnlPublicationList.SetSizer(bSizer11)
        self.pnlPublicationList.Layout()
        bSizer11.Fit(self.pnlPublicationList)
        bSizer9.Add(self.pnlPublicationList, 5, wx.EXPAND, 5)

        self.pnlPublication.SetSizer(bSizer9)
        self.pnlPublication.Layout()
        bSizer9.Fit(self.pnlPublication)
        self.m_splitter2.SplitHorizontally(self.pnlSubject, self.pnlPublication, 0)


    def setup(self):
        self.setup_menus()
        self.setup_toolbars()
        self.setup_statusbar()
        self.setup_shelf()
        self.setup_handlers()





