import wx
import os
import logging
import chatterbox_constants as c
import wx.py as py
from models import ViewState
import forms as frm


class CopyFilesPanel(wx.Panel):

    def __init__(self, parent=None):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        self.source_path = ''
        self.dest_path = ''
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        btn_source = frm.command_button(self, wx.ID_ANY, "Source Dir", self.on_source)
        self.txt_source = frm.single_edit(self)

        btn_dest = frm.command_button(self, wx.ID_ANY, "Dest Dir", self.on_dest)
        self.txt_dest = frm.single_edit(self)
        btn_copy = frm.command_button(self, wx.ID_ANY, "Copy", self.on_copy)
        self.txt_feedback = frm.multi_edit(self)
        self.txt_source.SetValue(c.read_config(c.COPY_FILE_SOURCE_DIR))
        self.txt_dest.SetValue(c.read_config(c.COPY_FILE_DEST_DIR))

        source_sizer = frm.hsizer([btn_source, self.txt_source])
        dest_sizer = frm.hsizer([btn_dest, self.txt_dest])
        feedback_sizer = frm.vsizer()
        feedback_sizer.Add(btn_copy, wx.SizerFlags())
        feedback_sizer.Add(self.txt_feedback, wx.SizerFlags(1).Expand())
        source_flags = wx.SizerFlags().Expand()

        main_sizer.Add(source_sizer, source_flags)
        main_sizer.Add(dest_sizer, source_flags)
        main_sizer.Add(feedback_sizer, wx.SizerFlags().Expand().Proportion(1))
        self.SetSizer(main_sizer)

    def on_copy(self, event):
        self.txt_feedback.AppendText("I clicked copy\n")
        self.txt_feedback.AppendText("Source %s \n" % self.txt_source.Value)
        source_path = self.txt_source.Value.strip()
        if not os.path.isdir(self.txt_source.Value):
            self.txt_feedback.AppendText("Path %s does not exist: " % source_path)

        for path, files, dirs in os.walk(source_path):
            pass
            #self.txt_feedback.AppendText("%s\n" % path)
            #for name in files:



    def on_source(self, event):
        path, modal_result = self.select_folder("Choose Source Directory:", self.txt_source.Value)
        if modal_result == wx.ID_OK:
            self.txt_source.SetValue(path)
            c.set_config(c.COPY_FILE_SOURCE_DIR, path)

    def on_dest(self, event):
        path, modal_result = self.select_folder("Choose Destination Directory:", self.txt_dest.Value)
        if modal_result == wx.ID_OK:
            self.txt_dest.SetValue(path)
            c.set_config(c.COPY_FILE_DEST_DIR, path)

    def select_folder(self, label: str, default: str = None):
        if default is None:
            default = os.getcwd()
        path = ""
        dlg = wx.DirDialog(self, label, defaultPath=default,
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        modal_result = dlg.ShowModal()
        if modal_result == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        return (path, modal_result)

