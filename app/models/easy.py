from app import db

# Mode of table
NOT_EDIT    = 0
EDIT        = 1
CHANGING    = 2
ABSENT      = 3 

# Mode of budgetary
NOT_BUDGET  = 0
BUDGET      = 1

def get_form_type(table_type):
    table2form = {
        'INTEGER': 'number',
        'DATE': 'date',
        'VARCHAR': 'text'
    }
    if '(' in table_type:
        table_type = table_type[:table_type.index('(')]
    if table_type in table2form:
        return table2form[table_type]
    return 'text'

def get_tables():
    return db.metadata.tables

def get_fields(table):
    columns = db.metadata.tables[table].get_children()
    return [(x.name, get_form_type(str(x.type))) for x in columns]