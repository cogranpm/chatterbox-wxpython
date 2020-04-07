# classes etc that help define a form and related controls
from enum import Enum, auto

EditFieldType = Enum('EditFieldType', 'TEXT COMBO CHECK')
EditFieldWidth = Enum('EditFieldWidth', 'LARGE MEDIUM SMALL')



class FormSpec():

    def __init__(self, parent, title: str, helpstr: str):
        self.parent = parent
        self.title = title
        self.helpstr = helpstr

class FormLineSpec():
    """ can be made up of multiple edit fields or a single, such as zip, state, city on a single line """

    def __init__(self, labelstr: str, edit_fields):
        self.labelstr = labelstr
        self.edit_fields = edit_fields

class EditFieldSpec():

    def __init__(self, name: str, caption: str, type: EditFieldType, width: EditFieldWidth):
        self.type = type
        self.name = name
        self.caption = caption
        self.width = width
