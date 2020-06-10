from typing import Dict

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
from forms import label

class AppFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Chatterbox", pos=wx.DefaultPosition,
                         size=wx.Size(1133, 716),
                         style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE | wx.TAB_TRAVERSAL,
                         name="MainFrame")
        self.pages = dict()
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.setup()
        ico = wx.Icon('icons/disconnect2.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        wx.py.dispatcher.connect(receiver=self.on_viewstate, signal=c.SIGNAL_VIEWSTATE)
        wx.py.dispatcher.connect(receiver=self.on_view_activated, signal=c.SIGNAL_VIEW_ACTIVATED)
        self.Bind(wx.EVT_UPDATE_UI, self.on_updateui)

    def add_page(self, key: str, title: str, window, page_data):
        """ adds a notebook page and keeps track of it in the pages dict """
        self.notebook.AddPage(window, title, True)
        self.pages[key] = (window, page_data)

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
        active_page = self.notebook.GetCurrentPage()
        py.dispatcher.send(signal=c.SIGNAL_SAVE, sender=self, command=c.COMMAND_SAVE, more=active_page)
        self.menuFileSave.Enable(False)
        self.toolbar.EnableTool(wx.ID_SAVE, False)

    def on_add(self, event):
        active_page = self.notebook.GetCurrentPage()
        py.dispatcher.send(signal=c.SIGNAL_ADD, sender=self, command=c.COMMAND_ADD, more=active_page)

    def on_delete(self, event):
        active_page = self.notebook.GetCurrentPage()
        py.dispatcher.send(signal=c.SIGNAL_DELETE, sender=self, command=c.COMMAND_DELETE, more=active_page)

    def on_copyfiles(self, event):
        self.notebook.AddPage(copyfiles.CopyFilesPanel(self), "Copy Files", True)

    def handle_menu_export(self, event):
        event.Skip()

    def handle_menu_quit(self, event):
        self.Close()

    def handle_menu_settings(self, event):
        app = wx.App.Get()
        with SettingsDialogImp(self, app.data_directory) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                if dlg.dirty:
                    # more than this needs to happen
                    print(dlg.data_directory)
                    app.data_directory = dlg.data_directory


    def handle_menu_playground(self, event):
        self.notebook.AddPage(playground.PlaygroundPanel(self), "Playground", True)

    def handle_menu_shelf(self, event):
        self.notebook.AddPage(shelf.MainPanel(self), c.NOTEBOOK_TITLE_SHELF, True)


    def OnNotebookPageChanged(self, event):
        event.Skip()

    def OnNotebookPageClose(self, event):
        event.Skip()

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

        self.menubar = wx.MenuBar(0)
        self.menuFile = wx.Menu()
        self.menuFileExport = wx.MenuItem(self.menuFile, wx.ID_ANY, u"&Export", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.menuFileExport)

        self.menuFileNew = wx.MenuItem(self.menuFile, wx.ID_ADD, u"&New", wx.EmptyString,
                                        wx.ITEM_NORMAL)
        # not working on linux
        # self.menuFileNew.Enable(False)
        self.menuFileSave = wx.MenuItem(self.menuFile, wx.ID_SAVE, u"&Save", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFileQuit = wx.MenuItem(self.menuFile, wx.ID_EXIT, u"&Quit", wx.EmptyString,
                                        wx.ITEM_NORMAL)
        self.menuFile.Append(self.menuFileNew)
        self.menuFile.Append(self.menuFileSave)
        self.menuFile.Append(self.menuFileQuit)

        self.menubar.Append(self.menuFile, u"&File")

        self.menuEdit = wx.Menu()
        self.menuEdit.AppendSeparator()

        self.menuEditDelete = wx.MenuItem(self.menuEdit, wx.ID_DELETE, u"Delete", wx.EmptyString,
                                            wx.ITEM_NORMAL)
        # not working on linux
        # self.menuEditDelete.Enable(False)
        self.menuEdit.Append(self.menuEditDelete)

        self.menuEditSettings = wx.MenuItem(self.menuEdit, wx.ID_PREFERENCES, u"&Settings", wx.EmptyString,
                                            wx.ITEM_NORMAL)
        self.menuEdit.Append(self.menuEditSettings)


        self.menubar.Append(self.menuEdit, u"&Edit")

        menuView = wx.Menu()
        self.menubar.Append(menuView, "&View")

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
        self.SetMenuBar(self.menubar)

    def setup_statusbar(self):
        self.statusbar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)


    def setup_handlers(self):
        # Connect Events
        self.Bind(wx.EVT_MENU, self.handle_menu_export, id=self.menuFileExport.GetId())
        self.Bind(wx.EVT_MENU, self.on_save, id=self.menuFileSave.GetId())
        self.Bind(wx.EVT_MENU, self.handle_menu_quit, id=self.menuFileQuit.GetId())
        self.Bind(wx.EVT_MENU, self.handle_menu_settings, id=self.menuEditSettings.GetId())
        self.Bind(wx.EVT_MENU, self.handle_menu_playground, id=self.mnuEditPlayground.GetId())
        self.Bind(wx.EVT_MENU, self.on_delete, id=self.menuEditDelete.GetId())

        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged)
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose)

        #self.btnAddPublication.Bind(wx.EVT_UPDATE_UI, self.AddPublicationOnUpdateUI)
        #self.btnDeletePublication.Bind(wx.EVT_UPDATE_UI, self.DeletePublicationOnUpdateUI)
        #self.btnEditPublication.Bind(wx.EVT_UPDATE_UI, self.EditPublicationOnUpdateUI)


    def setup_contents(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.aui.AuiNotebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,  style=wx.aui.AUI_NB_CLOSE_BUTTON)
        dummy_contents = label(self.notebook, "Home", "lblHome")
        self.notebook.AddPage(dummy_contents, u"Home", False, wx.NullBitmap)
        sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(sizer, 1, wx.EXPAND, 5)
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)


    def setup(self):
        self.setup_menus()
        self.setup_toolbars()
        self.setup_statusbar()
        self.setup_contents()
        self.setup_handlers()





