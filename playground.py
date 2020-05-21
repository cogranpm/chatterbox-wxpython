# a dialog for just about anything
import wx
import logging
import chatterbox_constants as c
import fn_widget as w
import wx.dataview as dv
import forms as frm
from lists import states, ColumnSpec, ColumnType, ListSpec, create_data
from validators import FieldValidator, CheckboxValidator, ComboValidator, not_empty
import wx.py as py
from models import ViewState

from typing import List, Dict

collection_name = 'playground'
name_column = 'name'
age_column = 'age'
member_column = 'member'
address1_column = 'address1'
address2_column = 'address2'
city_column = 'city'
state_column = 'state'
zip_column = 'zip'
phone_column = 'phone'
email_column = 'email'


def add_record():
    return {'id': None, 'name': '', 'age': None, 'member': False, 'address1': "", 'address2': "",
             'city': '', 'zip': '', 'state': '', 'phone': '', 'email': ''}

class PlaygroundPanel(wx.Panel):

    def __init__(self, parent=None):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.db = wx.GetApp().datastore
        #py.dispatcher.send(signal=c.SIGNAL_CREATE_ENTITY, sender=self,
        #                   command=None, more=collection_name)
        self.db.create_entity(collection_name)

        # goes into base class
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        # this should be parameter of the class perhaps
        # create_data would be call to database
        self.listspec = ListSpec([
            ColumnSpec(name_column, ColumnType.str, 'Name', 100, True),
            ColumnSpec(age_column, ColumnType.int, 'Age', 40, True),
            ColumnSpec(member_column, ColumnType.bool, 'Member', 40, True),
            ColumnSpec(address1_column, ColumnType.str, 'Address', 120, True),
            ColumnSpec(address2_column, ColumnType.str, 'Address 2', 120, True),
            ColumnSpec(city_column, ColumnType.str, 'City', 80, True),
            ColumnSpec(zip_column, ColumnType.str, 'Zip', 45, True),
            ColumnSpec(state_column, ColumnType.str, 'State', 45, True),
            ColumnSpec(phone_column, ColumnType.str, 'Phone', 145, True),
            ColumnSpec(email_column, ColumnType.str, 'Email', 145, True)
        ], self.list_selection_change, create_data(self.db))

        # base class
        self.list = self.listspec.build(self)
        wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
        wx.py.dispatcher.connect(receiver=self.add, signal=c.SIGNAL_ADD)
        wx.py.dispatcher.connect(receiver=self.delete, signal=c.SIGNAL_DELETE)

        # declare the validators
        # make as declarative as possible
        # these really do not need to be named
        self.name_validator = FieldValidator(None, name_column, [not_empty])
        self.age_validator = FieldValidator(None, age_column, [not_empty])
        self.address1_validator = FieldValidator(None, address1_column, [])
        self.address2_validator = FieldValidator(None, address2_column, [])
        self.member_validator = CheckboxValidator(None, member_column, [])
        self.email_validator = FieldValidator(None, email_column, [])
        self.phone_validator = FieldValidator(None, phone_column, [])
        self.city_validator = FieldValidator(None, city_column, [])
        self.state_validator = ComboValidator(None, state_column, [])
        self.zip_validator = FieldValidator(None, zip_column, [])

        main_sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

        # parameterize this somehow maybe in derived class an an override
        self.edit_form()
        self.form.set_viewstate(ViewState.empty)
        py.dispatcher.send(signal=c.SIGNAL_VIEW_ACTIVATED, sender=self, command=c.COMMAND_VIEW_ACTIVATED, more=self)

    def save(self, command, more):
        if more is self:
            if self.form.view_state == ViewState.adding:
                record = add_record()
                self.form.bind(record)
            #else:
            #    selected_item = self.list.GetSelection()
            #    record = self.listspec.model.ItemToObject(selected_item)
            is_valid = self.Validate()
            if is_valid:
                # save to backend
                self.TransferDataFromWindow()

                if self.form.view_state == ViewState.adding:
                    self.listspec.data.append(record)
                    self.listspec.model.ItemAdded(dv.NullDataViewItem, self.listspec.model.ObjectToItem(record))
                    self.db.add(collection_name, record)
                    #py.dispatcher.send(signal=c.SIGNAL_STORE, sender=self, command=c.COMMAND_ADD,
                    #                   more=record)
                else:
                    selected_item = self.list.GetSelection()
                    record = self.listspec.model.ItemToObject(selected_item)
                    self.db.update(collection_name, record)
                    #py.dispatcher.send(signal=c.SIGNAL_STORE, sender=self, command=c.COMMAND_SAVE,
                    #                   more=record)

                self.form.set_viewstate(ViewState.loaded)


    def add(self, command, more):
        """ prepares for an add by asking to save changes if dirty, then cleaning out the controls for new entry """
        if more is self:
            self.form.set_viewstate(ViewState.adding)

    def delete(self, command, more):
        if more is self:
            selected_item = self.list.GetSelection()
            if selected_item is not None:
                if frm.confirm_delete(self):
                    self.listspec.model.ItemDeleted(dv.NullDataViewItem, selected_item)
                    record = self.listspec.model.ItemToObject(selected_item)
                    self.db.remove(collection_name, record)
                    # del (self.listspec.data[0])
                    self.listspec.data.remove(record)
                    self.form.set_viewstate(ViewState.empty)

    def list_selection_change(self, event: dv.DataViewEvent):
        # testing dispatcher stuff
        self.form.set_viewstate(ViewState.loading)
        selected_item = self.list.GetSelection()
        record = self.listspec.model.ItemToObject(selected_item)
        self.form.bind(record)
        self.TransferDataToWindow()
        self.form.set_viewstate(ViewState.loaded)

    def edit_form(self):
        helpstr = """
        This is the FlexGrid Sizer demo 
        specify  which columns or rows should grow
        grow flexibly in either direction meaning,
        you can specify proportional amounts for child elements
        and specify behaviour in the non flexible direction
        growable row means in the vertical direction
        growable col means in the horizontal direction
        use the proportion argument in the Add method to make cell grow at different amount """

        self.form = frm.form(self, "frmDemo", "Form Demo", helpstr, [
            frm.edit_line("Name", [frm.TextField(name_column, frm.large(), validator=self.name_validator)]),
            frm.edit_line("Age", [frm.TextField(age_column, frm.small(), validator=self.age_validator)]),
            frm.edit_line("Member", [frm.CheckboxField(member_column, validator=self.member_validator)]),
            frm.edit_line("Address", [frm.TextField(address1_column, frm.large(), validator=self.address1_validator)]),
            frm.edit_line(None, [frm.TextField(address2_column, frm.large(), validator=self.address2_validator)]),
            frm.edit_line("City, State, Zip", [
                frm.TextField(city_column, frm.large(), validator=self.city_validator),
                frm.ComboField(state_column, frm.medium(), states, validator=self.state_validator),
                frm.TextField(zip_column, frm.small(), validator=self.zip_validator)
            ]),
            frm.edit_line("Phone", [frm.TextField(phone_column, frm.small(), validator=self.phone_validator)]),
            frm.edit_line("Email", [frm.TextField(email_column, frm.medium(), validator=self.email_validator)])
        ])

        self.form.build()


class PlaygroundForm(wx.Dialog):

    def __init__(self, parent=None):
        super().__init__(parent, id=wx.ID_ANY, title=u"Form Demo", pos=wx.DefaultPosition,
                           size=wx.Size(600, 800), style=wx.DEFAULT_DIALOG_STYLE | wx.WS_EX_VALIDATE_RECURSIVELY)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        # self.data = create_data()
        # self.model = PyTestModel(self.data, self.columns)
        # self.list = self.create_list()
        self.listspec = ListSpec([
            ColumnSpec(name_column, ColumnType.str, 'Name', 100, True),
            ColumnSpec(age_column, ColumnType.int, 'Age', 40, True),
            ColumnSpec(member_column, ColumnType.bool, 'Member', 40, True),
            ColumnSpec(address1_column, ColumnType.str, 'Address', 120, True),
            ColumnSpec(address2_column, ColumnType.str, 'Address 2', 120, True),
            ColumnSpec(city_column, ColumnType.str, 'City', 80, True),
            ColumnSpec(zip_column, ColumnType.str, 'Zip', 45, True),
            ColumnSpec(state_column, ColumnType.str, 'State', 45, True),
            ColumnSpec(phone_column, ColumnType.str, 'Phone', 145, True),
            ColumnSpec(email_column, ColumnType.str, 'Email', 145, True)
        ], self.list_selection_change, create_data())
        self.list = self.listspec.build(self)

        # self.columns = {self.name_column.key: self.name_column, self.age_column.key: self.age_column, self.member_column.key: self.member_column,
        #                self.address1_column.key: self.address1_column, self.address2_column.key: self.address2_column}


        # dispatcher.connect
        # just showing an example
        wx.py.dispatcher.connect(receiver=self.push, signal='Interpreter.push')

        # declare the validators
        # make as declarative as possible
        self.name_validator = FieldValidator(None, name_column, [not_empty])
        self.age_validator = FieldValidator(None, age_column, [not_empty])
        self.address1_validator = FieldValidator(None, address1_column, [])
        self.address2_validator = FieldValidator(None, address2_column, [])
        self.member_validator = CheckboxValidator(None, member_column, [])
        self.email_validator = FieldValidator(None, email_column, [])
        self.phone_validator = FieldValidator(None, phone_column, [])
        self.city_validator = FieldValidator(None, city_column, [])
        self.state_validator = ComboValidator(None, state_column, [])
        self.zip_validator = FieldValidator(None, zip_column, [])

        main_sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
        btn_add = frm.tool_button(self, id=wx.ID_ANY, text="Add", handler=self.add_button_click)
        btn_delete = frm.tool_button(self, id=wx.ID_ANY, text="Del", handler=self.delete_button_click)
        tool_sizer = frm.hsizer([btn_add, btn_delete])
        main_sizer.Add(tool_sizer, wx.SizerFlags(0))

        self.edit_form()

        # frame stuff
        self.Layout()
        self.Centre(wx.BOTH)
        main_sizer.Fit(self)
        # Connect Events
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInitDialog)

    def OnInitDialog(self, event):
        logging.info('Playgound Dialog Initialized')

    def on_ok(self, event):
        # pass
        # self.EndModal()
        event.Skip()

    def on_cancel(self, event):
        event.Skip()

    def push(self, command, more):
        """ just an example of dispatcher in action """
        print('got a push')

    # this could possibly be moved to the listspec class
    # after all it knows the parent which is the only variant needed
    def list_selection_change(self, event: dv.DataViewEvent):
        # testing dispatcher stuff
        py.dispatcher.send(signal='Interpreter.push', sender=self, command='listchange', more=event)
        selected_item = self.list.GetSelection()
        record = self.listspec.model.ItemToObject(selected_item)
        for column in self.listspec.columns:
            control: wx.Window = wx.Window.FindWindowByName(column.key, self)
            if control is not None and control.Validator is not None:
                control.Validator.set_data(record)

        self.TransferDataToWindow()

    def add_button_click(self, event):
        new_person = {'name': 'Peter', 'age': 33, 'address1': '14 Angel Terrace'}
        self.listspec.data.append(new_person)
        self.listspec.model.ItemAdded(dv.NullDataViewItem, self.listspec.model.ObjectToItem(new_person))

    def delete_button_click(self, event):
        self.model.ItemDeleted(dv.NullDataViewItem, self.listspec.model.ObjectToItem(self.listspec.data[0]))
        del(self.listspec.data[0])

    def edit_form(self):
        helpstr = """
        This is the FlexGrid Sizer demo 
        specify  which columns or rows should grow
        grow flexibly in either direction meaning,
        you can specify proportional amounts for child elements
        and specify behaviour in the non flexible direction
        growable row means in the vertical direction
        growable col means in the horizontal direction
        use the proportion argument in the Add method to make cell grow at different amount """

        person_form = frm.form(self, "frmDemo", "Form Demo", helpstr, [
            frm.edit_line("Name", [frm.TextField(name_column, frm.large(), validator=self.name_validator)]),
            frm.edit_line("Age", [frm.TextField(age_column, frm.small(), validator=self.age_validator)]),
            frm.edit_line("Member", [frm.CheckboxField(member_column, validator=self.member_validator)]),
            frm.edit_line("Address", [frm.TextField(address1_column, frm.large(), validator=self.address1_validator)]),
            frm.edit_line(None, [frm.TextField(address2_column, frm.large(), validator=self.address2_validator)]),
            frm.edit_line("City, State, Zip", [
                frm.TextField(city_column, frm.large(), validator=self.city_validator),
                frm.ComboField(state_column, frm.medium(), states, validator=self.state_validator),
                frm.TextField(zip_column, frm.small(), validator=self.zip_validator)
            ]),
            frm.edit_line("Phone", [frm.TextField(phone_column, frm.small(), validator=self.phone_validator)]),
            frm.edit_line("Email", [frm.TextField(email_column, frm.medium(), validator=self.email_validator)])
        ])

        panel = person_form.build(display_type=frm.DisplayType.DIALOG, ok_handler=self.on_ok, cancel_handler=self.on_cancel)
        return panel

    def seesaw_style_test(self):
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
        return test_sizer

