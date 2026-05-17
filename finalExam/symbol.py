# symbol.py

class Entry:
    def __init__(self, string, token):
        self.string = string
        self.token = token

symbol_table = []

# تجميع كلمات جميع نماذج الامتحانات في مصفوفة البداية
keywords_init = [
    Entry('div', 'DIV'), Entry('mod', 'MOD'),
    Entry('if', 'IF'), Entry('then', 'THEN'),
    Entry('while', 'WHILE'), Entry('do', 'DO'), # تدعم النموذج 442 و 432
    Entry('begin', 'BEGIN'), Entry('end', 'END'),
    Entry('void', 'VOID'), # تدعم النموذج 421 لتعريف الدالات
    Entry('repeat', 'REPEAT'), # تدعم النموذج 461 و 432
    Entry('until', 'UNTIL') # تدعم جميع نماذج الحلقات المتأخرة الفحص
]

def initialize():
    global symbol_table
    symbol_table = []
    for entry in keywords_init:
        insert(entry.string, entry.token)

def lookup(string):
    for index, entry in enumerate(symbol_table):
        if entry.string == string: return index
    return None

def insert(string, token):
    symbol_table.append(Entry(string, token))
    return len(symbol_table) - 1