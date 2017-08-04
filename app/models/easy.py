from app import db

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

def get_class_by_tablename( tablename ):
    for c in db.Model._decl_class_registry.values():
        if ( 
            hasattr( c, 'placeholder' ) 
            and hasattr( c, '__tablename__' ) 
            and hasattr( c, 'get_russian_name' ) 
            and c.__tablename__ == tablename 
        ):
          return c
    return None