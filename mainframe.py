# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
from ObjectListView import ObjectListView, ColumnDefn

wx.ID_QUIT = 1000
wx.ID_ADD_SHELF = 1001
wx.ID_DELETE_SHELF = 1002
wx.ID_EDIT_SHELF = 1003
wx.ID_ADDPUBLICATION = 1004

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Chatterbox", pos = wx.DefaultPosition, size = wx.Size( 1133,716 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL, name = u"MainFrame" )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.menuFile = wx.Menu()
		self.menuFileExport = wx.MenuItem( self.menuFile, wx.ID_ANY, u"&Export", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.Append( self.menuFileExport )

		self.menuFileQuit = wx.MenuItem( self.menuFile, wx.ID_QUIT, u"&Quit"+ u"\t" + u"CTRL+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.Append( self.menuFileQuit )

		self.m_menubar1.Append( self.menuFile, u"&File" )

		self.menuEdit = wx.Menu()
		self.menuEdit.AppendSeparator()

		self.menuEditSettings = wx.MenuItem( self.menuEdit, wx.ID_PREFERENCES, u"&Settings", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuEdit.Append( self.menuEditSettings )

		self.m_menubar1.Append( self.menuEdit, u"&Edit" )

		self.SetMenuBar( self.m_menubar1 )

		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		bSizerNotebookMain = wx.BoxSizer( wx.VERTICAL )

		self.m_auiShelf = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelNotes = wx.Panel( self.m_auiShelf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelNotes.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		splitterSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter1 = wx.SplitterWindow( self.m_panelNotes, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

		self.pnlShelf = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.pnlShelfHeader = wx.Panel( self.pnlShelf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self.pnlShelfHeader, wx.ID_ANY, u"Shelves", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer6.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_btnAddShelf = wx.Button( self.pnlShelfHeader, wx.ID_ADD_SHELF, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.m_btnAddShelf.SetMaxSize( wx.Size( 25,-1 ) )

		bSizer6.Add( self.m_btnAddShelf, 0, wx.ALIGN_LEFT, 5 )

		self.m_btnDeleteShelf = wx.Button( self.pnlShelfHeader, wx.ID_DELETE_SHELF, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.m_btnDeleteShelf.Enable( False )
		self.m_btnDeleteShelf.SetMaxSize( wx.Size( 25,-1 ) )

		bSizer6.Add( self.m_btnDeleteShelf, 0, 0, 5 )

		self.m_btnEditShelf = wx.Button( self.pnlShelfHeader, wx.ID_EDIT_SHELF, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.m_btnEditShelf.Enable( False )
		self.m_btnEditShelf.SetMaxSize( wx.Size( 60,-1 ) )

		bSizer6.Add( self.m_btnEditShelf, 0, 0, 5 )


		self.pnlShelfHeader.SetSizer( bSizer6 )
		self.pnlShelfHeader.Layout()
		bSizer6.Fit( self.pnlShelfHeader )
		bSizer5.Add( self.pnlShelfHeader, 0, 0, 5 )

		self.pnlShelfList = wx.Panel( self.pnlShelf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.shelf_list = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
		bSizer7.Add( self.shelf_list, 1, wx.EXPAND, 5 )


		self.pnlShelfList.SetSizer( bSizer7 )
		self.pnlShelfList.Layout()
		bSizer7.Fit( self.pnlShelfList )
		bSizer5.Add( self.pnlShelfList, 1, wx.EXPAND, 5 )


		self.pnlShelf.SetSizer( bSizer5 )
		self.pnlShelf.Layout()
		bSizer5.Fit( self.pnlShelf )
		self.pnlShelfChildren = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter2 = wx.SplitterWindow( self.pnlShelfChildren, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )

		self.pnlSubject = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.pnlSubjectHeader = wx.Panel( self.pnlSubject, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.pnlSubjectHeader, wx.ID_ANY, u"Subjects", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer13.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.btnAddSubject = wx.Button( self.pnlSubjectHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.btnAddSubject.Enable( False )
		self.btnAddSubject.SetMaxSize( wx.Size( 25,-1 ) )

		bSizer13.Add( self.btnAddSubject, 0, 0, 5 )

		self.btnDeleteSubject = wx.Button( self.pnlSubjectHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.btnDeleteSubject.Enable( False )
		self.btnDeleteSubject.SetMaxSize( wx.Size( 25,-1 ) )

		bSizer13.Add( self.btnDeleteSubject, 0, 0, 5 )

		self.btnEditSubject = wx.Button( self.pnlSubjectHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.btnEditSubject.Enable( False )
		self.btnEditSubject.SetMaxSize( wx.Size( 60,-1 ) )

		bSizer13.Add( self.btnEditSubject, 0, 0, 5 )


		self.pnlSubjectHeader.SetSizer( bSizer13 )
		self.pnlSubjectHeader.Layout()
		bSizer13.Fit( self.pnlSubjectHeader )
		bSizer12.Add( self.pnlSubjectHeader, 0, wx.EXPAND, 5 )

		self.pnlSubjectList = wx.Panel( self.pnlSubject, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.subject_list = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
		bSizer14.Add( self.subject_list, 1, wx.EXPAND, 5 )


		self.pnlSubjectList.SetSizer( bSizer14 )
		self.pnlSubjectList.Layout()
		bSizer14.Fit( self.pnlSubjectList )
		bSizer12.Add( self.pnlSubjectList, 1, wx.EXPAND, 5 )


		self.pnlSubject.SetSizer( bSizer12 )
		self.pnlSubject.Layout()
		bSizer12.Fit( self.pnlSubject )
		self.pnlPublication = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.pnlPublicationHeader = wx.Panel( self.pnlPublication, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self.pnlPublicationHeader, wx.ID_ANY, u"Publications", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer10.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.btnAddPublication = wx.Button( self.pnlPublicationHeader, wx.ID_ADDPUBLICATION, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.btnAddPublication.Enable( False )
		self.btnAddPublication.SetMaxSize( wx.Size( 25,-1 ) )

		bSizer10.Add( self.btnAddPublication, 0, 0, 5 )

		self.btnDeletePublication = wx.Button( self.pnlPublicationHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.btnDeletePublication.Enable( False )
		self.btnDeletePublication.SetMaxSize( wx.Size( 25,-1 ) )

		bSizer10.Add( self.btnDeletePublication, 0, 0, 5 )

		self.btnEditPublication = wx.Button( self.pnlPublicationHeader, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,20 ), 0 )
		self.btnEditPublication.Enable( False )
		self.btnEditPublication.SetMaxSize( wx.Size( 60,-1 ) )

		bSizer10.Add( self.btnEditPublication, 0, 0, 5 )


		self.pnlPublicationHeader.SetSizer( bSizer10 )
		self.pnlPublicationHeader.Layout()
		bSizer10.Fit( self.pnlPublicationHeader )
		bSizer9.Add( self.pnlPublicationHeader, 0, wx.EXPAND, 5 )

		self.pnlPublicationList = wx.Panel( self.pnlPublication, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.publication_list = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
		bSizer11.Add( self.publication_list, 1, wx.EXPAND, 5 )


		self.pnlPublicationList.SetSizer( bSizer11 )
		self.pnlPublicationList.Layout()
		bSizer11.Fit( self.pnlPublicationList )
		bSizer9.Add( self.pnlPublicationList, 5, wx.EXPAND, 5 )


		self.pnlPublication.SetSizer( bSizer9 )
		self.pnlPublication.Layout()
		bSizer9.Fit( self.pnlPublication )
		self.m_splitter2.SplitHorizontally( self.pnlSubject, self.pnlPublication, 0 )
		bSizer8.Add( self.m_splitter2, 1, wx.EXPAND, 5 )


		self.pnlShelfChildren.SetSizer( bSizer8 )
		self.pnlShelfChildren.Layout()
		bSizer8.Fit( self.pnlShelfChildren )
		self.m_splitter1.SplitVertically( self.pnlShelf, self.pnlShelfChildren, 248 )
		splitterSizer.Add( self.m_splitter1, 1, wx.EXPAND, 5 )


		self.m_panelNotes.SetSizer( splitterSizer )
		self.m_panelNotes.Layout()
		splitterSizer.Fit( self.m_panelNotes )
		self.m_auiShelf.AddPage( self.m_panelNotes, u"Home", False, wx.NullBitmap )

		bSizerNotebookMain.Add( self.m_auiShelf, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( bSizerNotebookMain, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.FileExportOnMenuSelection, id = self.menuFileExport.GetId() )
		self.Bind( wx.EVT_MENU, self.menuFileQuitOnMenuSelection, id = self.menuFileQuit.GetId() )
		self.Bind( wx.EVT_MENU, self.menuEditSettingsOnMenuSelection, id = self.menuEditSettings.GetId() )
		self.m_auiShelf.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged )
		self.m_auiShelf.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose )
		self.m_btnAddShelf.Bind( wx.EVT_BUTTON, self.AddShelfOnButtonClick )
		self.m_btnDeleteShelf.Bind( wx.EVT_BUTTON, self.DeleteShelfOnButtonClick )
		self.m_btnEditShelf.Bind( wx.EVT_BUTTON, self.EditShelfOnButtonClick )
		self.btnAddSubject.Bind( wx.EVT_BUTTON, self.AddSubjectOnButtonClick )
		self.btnDeleteSubject.Bind( wx.EVT_BUTTON, self.DeleteSubjectOnButtonClick )
		self.btnEditSubject.Bind( wx.EVT_BUTTON, self.EditSubjectOnButtonClick )
		self.btnAddPublication.Bind( wx.EVT_BUTTON, self.AddPublicationOnButtonClick )
		self.btnAddPublication.Bind( wx.EVT_UPDATE_UI, self.AddPublicationOnUpdateUI )
		self.btnDeletePublication.Bind( wx.EVT_BUTTON, self.DeletePublicationOnButtonClick )
		self.btnDeletePublication.Bind( wx.EVT_UPDATE_UI, self.DeletePublicationOnUpdateUI )
		self.btnEditPublication.Bind( wx.EVT_BUTTON, self.EditPublicationOnButtonClick )
		self.btnEditPublication.Bind( wx.EVT_UPDATE_UI, self.EditPublicationOnUpdateUI )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def FileExportOnMenuSelection( self, event ):
		event.Skip()

	def menuFileQuitOnMenuSelection( self, event ):
		event.Skip()

	def menuEditSettingsOnMenuSelection( self, event ):
		event.Skip()

	def OnNotebookPageChanged( self, event ):
		event.Skip()

	def OnNotebookPageClose( self, event ):
		event.Skip()

	def AddShelfOnButtonClick( self, event ):
		event.Skip()

	def DeleteShelfOnButtonClick( self, event ):
		event.Skip()

	def EditShelfOnButtonClick( self, event ):
		event.Skip()

	def AddSubjectOnButtonClick( self, event ):
		event.Skip()

	def DeleteSubjectOnButtonClick( self, event ):
		event.Skip()

	def EditSubjectOnButtonClick( self, event ):
		event.Skip()

	def AddPublicationOnButtonClick( self, event ):
		event.Skip()

	def AddPublicationOnUpdateUI( self, event ):
		event.Skip()

	def DeletePublicationOnButtonClick( self, event ):
		event.Skip()

	def DeletePublicationOnUpdateUI( self, event ):
		event.Skip()

	def EditPublicationOnButtonClick( self, event ):
		event.Skip()

	def EditPublicationOnUpdateUI( self, event ):
		event.Skip()

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 248 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )

	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 0 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )


