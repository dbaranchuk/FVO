from app import db

# States of table
TABLE_STATES = {
    'NOT_EDITED' : 0,
    'EDITED'     : 1,
    'DECLINED'   : 2,
    'APPROVED'   : 3, 
}

# States of quiz
QUIZ_STATES = {
    'NOT_FILLED' : 0,
    'DECLINED'   : 1,
    'NOT_CHECKED': 2,
    'APPROVED'   : 3, 
}

# Mode of budgetary
NOT_BUDGET = 0
BUDGET     = 1


def get_user_tables():
    return [
            'basic_information',
            'certificates_change_name',
            'communications',
            'passports',
            'international_passports',
            'registration_certificates',
            'middle_education',
            'spec_middle_education',
            'high_education',
            'military_education',
            'languages',
            'mothers_fathers',
            'married_certificates',
            'brothers_sisters_children',
            'personal_data',
    ]

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