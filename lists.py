

class ListItem:

    def __init__(self, code: str, label: str):
        self.code = code
        self.label = label

    def __str__(self):
        return f"Code:{self.code} Label:{self.label}"

    def __repr__(self):
        return f"ListItem({self.code}, {self.label})"



states = [ListItem('VIC', 'Victoria'),  ListItem('TAS', 'Tasmania'),  ListItem('NSW', 'New South Wales'),  ListItem('SA', 'South Australia'),  ListItem('WA', 'West Australia')]

