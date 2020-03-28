# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DlgSettings
###########################################################################

class DlgSettings ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Settings", pos = wx.DefaultPosition, size = wx.Size( 604,230 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Data Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.dataDirPicker = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
		bSizer2.Add( self.dataDirPicker, 5, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )

		stdButtonSizer = wx.StdDialogButtonSizer()
		self.stdButtonSizerOK = wx.Button( self, wx.ID_OK )
		stdButtonSizer.AddButton( self.stdButtonSizerOK )
		self.stdButtonSizerCancel = wx.Button( self, wx.ID_CANCEL )
		stdButtonSizer.AddButton( self.stdButtonSizerCancel )
		stdButtonSizer.Realize();

		bSizer1.Add( stdButtonSizer, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDialog )
		self.dataDirPicker.Bind( wx.EVT_DIRPICKER_CHANGED, self.DataDirectoryOnDirChanged )
		self.stdButtonSizerOK.Bind( wx.EVT_BUTTON, self.OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnInitDialog( self, event ):
		event.Skip()

	def DataDirectoryOnDirChanged( self, event ):
		event.Skip()

	def OnOKButtonClick( self, event ):
		event.Skip()


