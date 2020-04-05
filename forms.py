# classes etc that help define a form and related controls
from enum import Enum, auto

EditFieldType = Enum('EditFieldType', 'TEXT COMBO CHECK')



class FormSpec():

    def __init__(self, parent, title: str, helpstr: str):
        self.parent = parent
        self.title = title
        self.helpstr = helpstr

class FormLineSpec():

    def __init__(self, labelstr: str, edit_fields):
        self.labelstr = labelstr
        self.edit_fields = edit_fields

class EditFieldSpec():

    def __init__(self, type: EditFieldType):
        self.type = type
    