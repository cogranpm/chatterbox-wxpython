import wx
import os
from pathlib import Path, PurePath
import shutil
import threading, _thread
import time
import logging
import chatterbox_constants as c
import wx.py as py
from models import ViewState
import forms as frm


def cancel(parent):
    wx.CallAfter(parent.post_feedback, "Cancelled by user")
    _thread.exit()

def get_dest_folder(foldername, subfolder, num_parts_in_sourcepath
                    , source_folder, dest_path):
    full_source = os.path.join(foldername, subfolder)
    full_source_pure = PurePath(full_source)
    seperated_source = os.sep.join(
        full_source_pure.parts[num_parts_in_sourcepath: len(full_source_pure.parts)])
    last_part_prefixed = os.path.join(dest_path, source_folder, seperated_source)
    return last_part_prefixed

def copy(parent, source_path, dest_path):
    all_files = []
    all_dirs = []
    source_path_pure = PurePath(source_path)

    last_part = source_path_pure.parts[-1]
    num_parts = len(source_path_pure.parts)
    if parent.is_cancelled:
        cancel(parent)

    for foldername, subfolders, filenames in os.walk(source_path):
        # self.txt_feedback.AppendText("%s\n" % path)

        if parent.is_cancelled:
            cancel(parent)

        for name in filenames:
            if parent.is_cancelled:
                cancel(parent)
            dest_file = get_dest_folder(foldername, name
                                             , num_parts, last_part, dest_path)
            source_file = os.path.join(foldername, name)
            all_files.append((source_file, dest_file))

        for subfolder in subfolders:
            if parent.is_cancelled:
                cancel(parent)
            target_folder_name = get_dest_folder(foldername, subfolder, num_parts, last_part, dest_path)
            if not os.path.exists(target_folder_name):
                all_dirs.append(target_folder_name)

    # make all the directories first
    wx.CallAfter(parent.post_feedback, "Creating Directories %i of %i" % (1, len(all_dirs)))
    for dir in all_dirs:
        try:
            Path(dir).mkdir(parents=True, exist_ok=True)
        except Exception as err :
            wx.CallAfter(parent.post_feedback, "Error creating directory: " + dir
                         + " Error: " + err)


    # _thread.start_new_thread(copy_files, (all_files[:2],))
    # or
    #first_thread = threading.Thread(target=copy_files, args=(all_files[:3], parent))
    #first_thread.start()
    # could split up among multiple threads, makes it slower though
    # _thread.start_new_thread(copy_files, (all_files[2:5],))

    wx.CallAfter(parent.post_feedback, "Copying Files: %i of %i" % (1, len(all_files)))
    copy_files(all_files[:700], parent)
    wx.CallAfter(parent.post_feedback, "Finished")


def copy_file(parent, source, target):
    if not os.path.exists(target):
        wx.CallAfter(parent.post_feedback, "copied " + source)
        shutil.copy2(source, target)

def copy_files(files, parent):
    for file_def in files:
        if parent.is_cancelled:
            cancel(parent)
        src, dest = file_def
        copy_file(parent, src, dest)
        time.sleep(0.01)


class CopyFilesPanel(wx.Panel):

    def __init__(self, parent=None):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.is_cancelled = False
        self.source_path = ''
        self.dest_path = ''
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        btn_source = frm.command_button(self, wx.ID_ANY, "&Source Dir", self.on_source)
        self.txt_source = frm.single_edit(self)

        btn_dest = frm.command_button(self, wx.ID_ANY, "&Dest Dir", self.on_dest)
        self.txt_dest = frm.single_edit(self)
        btn_copy = frm.command_button(self, wx.ID_ANY, "&Copy", self.on_copy)
        btn_cancel = frm.command_button(self, wx.ID_ANY, "Cance&l", self.on_cancel)
        self.txt_feedback = frm.multi_edit(self)
        self.txt_source.SetValue(c.read_config(c.COPY_FILE_SOURCE_DIR))
        self.txt_dest.SetValue(c.read_config(c.COPY_FILE_DEST_DIR))

        source_sizer = frm.hsizer([btn_source, self.txt_source])
        dest_sizer = frm.hsizer([btn_dest, self.txt_dest])
        feedback_sizer = frm.vsizer()
        feedback_sizer.Add(btn_copy, wx.SizerFlags())
        feedback_sizer.Add(btn_cancel, wx.SizerFlags())
        feedback_sizer.Add(self.txt_feedback, wx.SizerFlags(1).Expand())
        source_flags = wx.SizerFlags().Expand()

        main_sizer.Add(source_sizer, source_flags)
        main_sizer.Add(dest_sizer, source_flags)
        main_sizer.Add(feedback_sizer, wx.SizerFlags().Expand().Proportion(1))
        self.SetSizer(main_sizer)




    def post_feedback(self, message: str):
        self.txt_feedback.AppendText(message + '\n')

    def on_cancel(self, event):
        self.is_cancelled = True

    def on_copy(self, event):
        self.txt_feedback.Clear()

        source_path = self.txt_source.Value.strip()
        if not os.path.isdir(source_path):
            self.post_feedback("Path %s does not exist: " % source_path)
            return

        dest_path = self.txt_dest.Value.strip()
        if not os.path.isdir(dest_path):
            self.post_feedback("Path %s does not exist: " % dest_path)
            return

        self.txt_feedback.AppendText("Locating files in %s \n" % self.txt_source.Value)
        first_thread = threading.Thread(target=copy, args=(self, source_path, dest_path))
        first_thread.start()


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

