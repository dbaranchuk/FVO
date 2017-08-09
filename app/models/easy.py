#-.- coding: utf-8 -.-s
from app import db
import sys

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

# States of user
USER_STATES = {
    'ROLE_USER' : 0,
    'ROLE_ADMIN' : 1,
    'ROLE_SUPER_ADMIN' : 2,
    'ROLE_READONLY_ADMIN' : 3
}

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

class Students_info_lables_accessor():
    def __init__(self, student_info):
        
        self.student_info = student_info

        self.brother = [brother for brother in student_info.brothers_sisters_children if brother.status == u'Брат']
        self.sister = [sister for sister in student_info.brothers_sisters_children if sister.status == u'Сестра']
        self.child = [child for child in student_info.brothers_sisters_children if child.status == u'Сын' or child.status == u'Дочь']
        self.father = [father for father in student_info.mothers_fathers if father.status == u'Отец'][0]
        self.mother = [mother for mother in student_info.mothers_fathers if mother.status == u'Мать'][0]
        '''
        for br in self.brother:
            print >> sys.stderr, br.last_name
        for s in self.sister:
            print >> sys.stderr, s.last_name
        for c in self.child:
            print >> sys.stderr, c.last_name
        '''
        print >> sys.stderr, student_info.spec_middle_education.institution

        self.simple_fields = {
            'last_name' : ('basic_information', 'last_name'),
            'first_name' : ('basic_information', 'first_name'),
            'middle_name' : ('basic_information', 'middle_name'),
            'birth_date' : ('basic_information', 'birth_date'),
            'birth_place' : ('basic_information', 'birth_place'),
            'nationality' : ('basic_information', 'nationality'),
            'family_status' : ('basic_information', 'family_status'),
            'citizenship' : ('basic_information', 'citizenship'),
            'second_citizenship' : ('basic_information', 'second_citizenship'),
            'inn' : ('basic_information', 'tin'),
            'insurance_certificate' : ('basic_information', 'insurance_certificate'),

            'changename_serial' : ('certificates_change_name', 'serial'),
            'changename_number' : ('certificates_change_name', 'number'),
            'changename_issuer' : ('certificates_change_name', 'issuer'),
            'changename_issue_date' : ('certificates_change_name', 'issue_date'),
            'changename_changing' : ('certificates_change_name', 'changing'),

            'mobile_phone_1' : ('communications', 'mobile_phone_1'),
            'mobile_phone_2' : ('communications', 'mobile_phone_2'),
            'home_phone' : ('communications', 'home_phone'),
            'email' : ('communications', 'email'),

            'serial' : ('passports', 'serial'),
            'number' : ('passports', 'number'),
            'issuer' : ('passports', 'issuer'),
            'issue_date' : ('passports', 'issue_date'),
            'code' : ('passports', 'code'),
            'registration_index' : ('passports', 'registration_index'),
            'registration_address' : ('passports', 'registration_address'),
            'fact_index' : ('passports', 'fact_index'),
            'fact_address' : ('passports', 'fact_address'),

            'internation_serial' : ('international_passports', 'serial'),
            'international_number' : ('international_passports', 'number'),
            'international_issuer' : ('international_passports', 'issuer'),
            'international_issue_date' : ('international_passports', 'issue_date'),
            'international_validity' : ('international_passports', 'validity'),
            
            'registration_serial' : ('registration_certificates', 'serial'),
            'registration_number' : ('registration_certificates', 'number'),
            'registration_issuer' : ('registration_certificates', 'issuer'),
            'registration_date_issue' : ('registration_certificates', 'date_issue'),
            'registration_military_department' : ('registration_certificates', 'military_department'),
            'registration_shelf_category' : ('registration_certificates', 'shelf_category'),

            'school_name' : ('middle_education', 'school'),
            'school_address' : ('middle_education', 'school_address'),
            'school_entrance_year' : ('middle_education', 'entrance_year'),
            'school_graduation_year' : ('middle_education', 'graduation_year'),

            'ptu_name' : ('spec_middle_education', 'institution'),
            'ptu_address' : ('spec_middle_education', 'institution_address'),
            'ptu_speciality' : ('spec_middle_education', 'speciality'),
            'ptu_entrance_year' : ('spec_middle_education', 'entrance_year'),
            'ptu_graduation_year' : ('spec_middle_education', 'graduation_year'),

            'institution' : ('high_education', 'institution'),
            'budgetary' : ('high_education', 'budgetary'),
            'full_faculty_name' : ('high_education', 'full_faculty_name'),
            'short_faculty_name' : ('high_education', 'short_faculty_name'),
            'spec_diloma' : ('high_education', 'spec_diploma'),
            'study_group_2' : ('high_education', 'study_group_2'),
            'study_group_3' : ('high_education', 'study_group_3'),
            'study_group_4' : ('high_education', 'study_group_4'),
            'form_study' : ('high_education', 'form_study'),
            'qualification' : ('high_education', 'quality'),
            'vus_entrance_year' : ('high_education', 'entrance_year'),
            'vus_graduation_year' : ('high_education', 'graduation_year'),

            'vzvod_1' : ('military_education', 'platoon_1'),
            'vzvod_2' : ('military_education', 'platoon_2'),

            'language_name' : ('languages', 'language'),
            'language_quality' : ('languages', 'quality'),
            'language_certificates' : ('languages', 'certificates'),

            'married_serial' : ('married_certificates', 'serial'),
            'married_number' : ('married_certificates', 'number'),
            'married_issuer' : ('married_certificates', 'issuer'),
            'married_date_issue' : ('married_certificates', 'date_issue'),
            'married_last_name' : ('married_certificates', 'last_name'),
            'married_first_name' : ('married_certificates', 'first_name'),
            'married_middle_name' : ('married_certificates', 'middle_name'),
            'married_birth_date' : ('married_certificates', 'birth_date'),
            'married_birth_place' : ('married_certificates', 'birth_place'),
            'married_mobile_phone_1' : ('married_certificates', 'mobile_phone_1'),
            'married_mobile_phone_2' : ('married_certificates', 'mobile_phone_2'),
            'married_home_phone' : ('married_certificates', 'home_phone'),
            'married_job_place' : ('married_certificates', 'married_job_place'),
            'married_job_post' : ('married_certificates', 'married_job_post'),
            'married_fact_index' : ('married_certificates', 'fact_index'),
            'married_fact_address' : ('married_certificates', 'fact_address'),

            'resus' : ('personal_data', 'blood_group_resus'),
            'shoes_size' : ('personal_data', 'shoes_size'),
            'uniform_size' : ('personal_data', 'uniform_size'),
            'head_size' : ('personal_data', 'head_size'),
            'growth' : ('personal_data', 'growth'),
            'protivogaz_size' : ('personal_data', 'protivogaz_size'),
            'ozk_size' : ('personal_data', 'OZK_size'),
            'state_awards' : ('personal_data', 'government_prize'),
            'injuries' : ('personal_data', 'injuries'),
            'criminals' : ('personal_data', 'criminals'),
            'civil_specialization' : ('personal_data', 'civil_specialization'),
            'hobbies' : ('personal_data', 'hobbies'),
            'sports' : ('personal_data', 'sports'),
            'scientific_results' : ('personal_data', 'scientific_results'),
            'work_experience' : ('personal_data', 'work_experience'),
        }

    def __getitem__(self, item):
        item = item[1:-1].split('.')
        print >> sys.stderr, item

        res_record = ''
        if item[0] in self.simple_fields:

            path = self.simple_fields[item[0]]
            if len(item) > 1:
                try:
                    res_record = self.student_info[path[0]][int(item[1])-1][path[1]]
                except Exception:
                    return ''
            else:
                print >> sys.stderr, self.student_info[path[0]], self.student_info[path[0]][path[1]]
                res_record = self.student_info[path[0]][path[1]]

        else:
            
            try:
                (keyword, prop) = item[0].split('@')
            except Exception:
                return None
            #print >> sys.stderr, keyword, prop
            if hasattr(self, keyword):
                if len(item)>1:
                    try:
                        res_record = getattr(self, keyword)[int(item[1])-1][prop]
                    except Exception:
                        return ''
                else:
                    res_record = getattr(self, keyword)[prop]
            else:
                return None

        return res_record if res_record != None else ''
