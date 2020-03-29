"""Subclass of DlgSettings, which is generated by wxFormBuilder."""

import wx
import SettingsDialog
from ObjectListView import ObjectListView, ColumnDefn

# Implementing DlgSettings
class SettingsDialogImp( SettingsDialog.DlgSettings ):
	def __init__( self, parent, data_directory):
		SettingsDialog.DlgSettings.__init__( self, parent )
		self.data_directory = data_directory
		self.dirty = False
		# testing objectlistview
		test_data = [{"name": "fred", "author": "mehungry"},
					 {"name": "vargos", "author": "renounced"}]
		self.m_listView.SetColumns(
			[ColumnDefn("Name", "left", 220, "name"),
			 ColumnDefn("Author", "left", 200, "author")
			 ])
		self.m_listView.SetObjects(test_data)


	# Handlers for DlgSettings events.
	def OnInitDialog( self, event ):
		# TODO: Implement OnInitDialog
		self.dataDirPicker.SetPath(self.data_directory)

	def DataDirectoryOnDirChanged( self, event ):
		self.dirty = True


	def OnOKButtonClick( self, event ):
		self.data_directory = self.dataDirPicker.GetPath()
		event.Skip()




