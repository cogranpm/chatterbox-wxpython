# classes etc that help define a form and related controls
from enum import Enum, auto

EditFieldType = Enum('EditFieldType', 'TEXT COMBO CHECK')
EditFieldWidth = Enum('EditFieldWidth', 'LARGE MEDIUM SMALL')


class FormSpec():
    """ for specifiying the contents of a form, a function will use this information to build up
    a 'form' and all it's contents
    a form consists of help text, title, and a bunch of labels/inputs
    once this spec is built up it can be passed into a function in order
    to render the corresponding controls
    formSpec has multipl FormLines
    FormLine has multiple EditFields
    """

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
    """ this is an edit field in a form, for example a combo box, or text box etc """

    def __init__(self, name: str, type: EditFieldType, width: EditFieldWidth):
        self.type = type
        self.name = name
        self.width = width
