#-.- coding: utf-8 -.-
from app import db
from app.models.simple import * 
from app.models.easy import *   

class User_info_table_interface(Class_with_attrs_access):
    def placeholder(self, eng):
        return self.placeholders[eng] if eng in self.placeholders else ''

    def get_russian_name(self, eng):
        return self.en2ru[eng] if eng in self.en2ru else unicode(eng[0].upper() + eng[1:])

    def get_section_name(self):
        return self.section_name

    def is_readonly(self, field):
        return field in self.readonly_fields


class Student_info(db.Model, Class_with_attrs_access):
    __tablename__ = 'student_info'
    id = db.Column(db.Integer, primary_key = True)
    user_id                         = db.Column( db.Integer, db.ForeignKey( 'user.id' ) )
    table_basic_information         = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] ) 
    table_certificates_change_name  = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_communications            = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_passports                 = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_international_passports   = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_registration_certificates = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_middle_education          = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_spec_middle_education     = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_high_education            = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_military_education        = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_languages                 = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_mothers_fathers           = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_brothers_sisters_children = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_married_certificates      = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_personal_data             = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )
    table_spec_data                 = db.Column( db.SmallInteger, default=TABLE_STATES['NOT_EDITED'] )

    user = db.relationship('User', 
        back_populates = 'students_info', uselist = False)
    comments = db.relationship('Comments', 
        back_populates = 'student_info', uselist = False)
    basic_information = db.relationship('Basic_information', 
        back_populates = 'student_info', uselist = False)
    certificates_change_name =  db.relationship('Certificates_change_name', 
        back_populates = 'student_info')
    communications =  db.relationship('Communications',
        back_populates = 'student_info', uselist = False)
    passports =  db.relationship('Passports', 
        back_populates = 'student_info', uselist = False)
    international_passports =  db.relationship('International_passports', 
        back_populates = 'student_info', uselist = False)
    registration_certificates =  db.relationship('Registration_certificates', 
        back_populates = 'student_info', uselist = False)
    middle_education =  db.relationship('Middle_education', 
        back_populates = 'student_info', uselist = False)
    spec_middle_education =  db.relationship('Spec_middle_education', 
        back_populates = 'student_info', uselist = False)
    high_education =  db.relationship('High_education', 
        back_populates = 'student_info')
    military_education =  db.relationship('Military_education', 
        back_populates = 'student_info', uselist = False)
    languages =  db.relationship('Languages', 
        back_populates = 'student_info')
    mothers_fathers =  db.relationship('Mothers_fathers', 
        back_populates = 'student_info')
    brothers_sisters_children =  db.relationship('Brothers_sisters_children', 
        back_populates = 'student_info')
    married_certificates =  db.relationship('Married_certificates', 
        back_populates = 'student_info')
    personal_data =  db.relationship('Personal_data', 
        back_populates = 'student_info', uselist = False)
    spec_data =  db.relationship('Spec_data', 
        back_populates = 'student_info', uselist = False)

class Comments(db.Model, Class_with_attrs_access):
    __tablename__ = 'comments'

    id              = db.Column(db.Integer, primary_key = True)
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))

    # поля с комментариями админа к секции
    basic_information_comment         = db.Column( db.String(300), default='' ) 
    certificates_change_name_comment  = db.Column( db.String(300), default='' )
    communications_comment            = db.Column( db.String(300), default='' )
    passports_comment                 = db.Column( db.String(300), default='' )
    international_passports_comment   = db.Column( db.String(300), default='' )
    registration_certificates_comment = db.Column( db.String(300), default='' )
    middle_education_comment          = db.Column( db.String(300), default='' )
    spec_middle_education_comment     = db.Column( db.String(300), default='' )
    high_education_comment            = db.Column( db.String(300), default='' )
    military_education_comment        = db.Column( db.String(300), default='' )
    languages_comment                 = db.Column( db.String(300), default='' )
    mothers_fathers_comment           = db.Column( db.String(300), default='' )
    brothers_sisters_children_comment = db.Column( db.String(300), default='' )
    married_certificates_comment      = db.Column( db.String(300), default='' )
    personal_data_comment             = db.Column( db.String(300), default='' )

    student_info = db.relationship( 'Student_info', back_populates = 'comments' )


class Basic_information(db.Model, User_info_table_interface):
    __tablename__ = 'basic_information'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))
    
    last_name             = db.Column( db.String(20), default='')
    first_name            = db.Column( db.String(20), default='')
    middle_name           = db.Column( db.String(20), default='')
    birth_date            = db.Column( db.String(10), default='')
    birth_place           = db.Column( db.String(64), default='')
    nationality           = db.Column( db.String(20), default='')
    family_status         = db.Column( db.String(10), default='')
    citizenship           = db.Column( db.String(50), default='')
    second_citizenship    = db.Column( db.String(50), default='')
    tin                   = db.Column( db.String(12), default='')
    insurance_certificate = db.Column( db.String(14), default='') 

    student_info =  db.relationship('Student_info', 
        back_populates = 'basic_information')

    def __init__(self, first_name='', middle_name='', last_name=''):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

        self.section_name = u'Основная информация'
        self.is_fixed     = True
        self.placeholders = {
            'last_name': u'Иванов',
            'first_name': u'Иван',
            'middle_name': u'Иванович',
            'birth_date': u'12.12.2012',
            'birth_place': u'гор. Нижние Пупки',
            'nationality': u'русский',
            'family_status': u'женат/холост',
            'citizenship': u'Российская Федерация',
            'second_citizenship': u'Залупия',
            'tin': u'123456789012',
            'insurance_certificate': u'123-456-789 01',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'last_name': u'Фамилия',
            'first_name': u'Имя',
            'middle_name': u'Отчество',
            'birth_date': u'Дата рождения',
            'birth_place': u'Место рождения',
            'nationality': u'Национальность',
            'family_status': u'Семейный положение',
            'citizenship': u'Гражданство',
            'second_citizenship': u'Второе гражданство, страна',
            'tin': u'ИНН',
            'insurance_certificate': u'Страховое свидетельство',
        }
        self.readonly_fields = set()


class Certificates_change_name(db.Model, User_info_table_interface):
    __tablename__ = 'certificates_change_name'
    
    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))
    
    serial     = db.Column( db.String(5),   default='' )
    number     = db.Column( db.String(10),  default='' )
    issuer     = db.Column( db.String(256), default='' )
    issue_date = db.Column( db.String(10),  default='' ) 
    changing   = db.Column( db.String(128), default='' )

    student_info = db.relationship('Student_info', 
        back_populates = 'certificates_change_name')

    def __init__(self):
        self.section_name = u'Свидетельство о перемене имени'
        self.is_fixed     = False
        self.placeholders = {
            'serial' : u'12345',
            'number' : u'1234567890',
            'issuer' : u'гор. Новосибирск, ЗАГС 61',
            'issue_date' : u'01.01.2000',
            'changing' : u'Поменял имя ПЕТР на имя ВАСИЛИЙ'
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'serial' : u'Серия',
            'number' : u'Номер',
            'issuer' : u'Кем выдан',
            'issue_date' : u'Когда выдан',
            'changing' : u'Что изменилось',
        }
        self.readonly_fields = set()

class Communications(db.Model, User_info_table_interface):
    __tablename__ = 'communications'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id') )

    mobile_phone_1 = db.Column( db.String(11), default='' )
    mobile_phone_2 = db.Column( db.String(11), default='' )
    home_phone     = db.Column( db.String(11), default='' )
    email          = db.Column( db.String(64), default='' )

    student_info =  db.relationship('Student_info', 
        back_populates = 'communications' )
    
    def __init__(self):
        self.section_name = u'Номера телефонов, электронная почта'
        self.is_fixed     = True
        self.placeholders = {
            'mobile_phone_1' : u'89012345678',
            'mobile_phone_2' : u'89012340567',
            'home_phone' : u'84953045678',
            'email' : u'vasya.pupkin@gmail.com'
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'mobile_phone_1' : u'Мобильный 1',
            'mobile_phone_2' : u'Мобильный 2',
            'home_phone' : u'Домашний',
            'email' : u'E-mail'
        }
        self.readonly_fields = set()

class Passports(db.Model, User_info_table_interface):
    __tablename__ = "passports"

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id') )
    
    serial               = db.Column( db.String(4),   default='' )
    number               = db.Column( db.String(6),   default='' )
    issuer               = db.Column( db.String(256), default='' )
    issue_date           = db.Column( db.String(10),  default='' ) 
    code                 = db.Column( db.String(7),   default='' )
    registration_index   = db.Column( db.String(6),   default='' )
    registration_address = db.Column( db.String(256), default='' )
    fact_index           = db.Column( db.String(6),   default='' )
    fact_address         = db.Column( db.String(256), default='' )

    student_info = db.relationship('Student_info', 
        back_populates = 'passports' )
    
    def __init__(self):
        self.section_name = u'Паспорт'
        self.is_fixed     = True
        self.placeholders = {
            'serial' : u'1234',
            'number' : u'123456',
            'issuer' : u'Отделом УФМС по гор. Москве по району Раменки',
            'issue_date' : u'01.01.2015',
            'code' : u'750-001',
            'registration_index' : u'192128',
            'registration_address' : u'гор. Новосибирск, ул. Пушкина, д. 56, кв. 17',
            'fact_index' : u'123456',
            'fact_address' : u'гор. Москва, Ленинские горы, д.1, корп. Б, комн. 123',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'serial' : u'Серия',
            'number' : u'Номер',
            'issuer' : u'Кем выдан',
            'issue_date' : u'Когда выдан',
            'code' : u'Код подразделения',
            'registration_index' : u'Индекс адреса регистрации',
            'registration_address' : u'Адрес регистрации',
            'fact_index' : u'Индекс фактического проживания',
            'fact_address' : u'Адрес фактического проживания',
        }
        self.readonly_fields = set()

class International_passports(db.Model, User_info_table_interface):
    __tablename__ = 'international_passports'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id') )
    
    serial     = db.Column( db.String(2),   default='' )
    number     = db.Column( db.String(7),   default='' )
    issuer     = db.Column( db.String(256), default='' )
    issue_date = db.Column( db.String(10),  default='' ) 
    validity   = db.Column( db.String(10),  default='' )

    student_info = db.relationship('Student_info', 
        back_populates = 'international_passports' )
    
    def __init__(self):
        self.section_name = u'Загранпаспорт'
        self.is_fixed     = True
        self.placeholders = {
            'serial' : u'12',
            'number' : u'1234567',
            'issuer' : u'Отделом УФМС по гор. Москве по району Раменки',
            'issue_date' : u'01.01.2015',
            'validity' : u'10 лет',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'serial' : u'Серия',
            'number' : u'Номер',
            'issuer' : u'Кем выдан',
            'issue_date' : u'Когда выдан',
            'validity' : u'Срок действия',
        }
        self.readonly_fields = set()

class Registration_certificates(db.Model, User_info_table_interface):
    __tablename__ = 'registration_certificates'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id') )

    serial              = db.Column( db.String(2),   default = '' ) 
    number              = db.Column( db.String(7),   default = '' )
    issuer              = db.Column( db.String(128), default = '' )
    date_issue          = db.Column( db.String(10),  default = '' )  
    military_department = db.Column( db.String(128), default = '' )
    shelf_category      = db.Column( db.String(32),  default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'registration_certificates' )

    def __init__(self):
        self.section_name = u'Приписное свидетельство'
        self.is_fixed     = True
        self.placeholders = {
            'serial' : u'АВ',
            'number' : u'1234567',
            'issuer' : u'Раменским комиссариатом',
            'date_issue' : u'01.01.2015',
            'military_department' : u'Раменский военный комиссариат',
            'shelf_category' : u'В+ годен с ограничениями'
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'serial' : u'Серия',
            'number' : u'Номер',
            'issuer' : u'Кем выдано',
            'date_issue' : u'Когда выдано',
            'military_department' : u'Военный комиссариат по месту воинского учета',
            'shelf_category' : u'Категория годности'
        }
        self.readonly_fields = set()

class Middle_education(db.Model, User_info_table_interface):
    __tablename__ = 'middle_education'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id') )
    
    school          = db.Column( db.String(128), default = '' )
    school_address  = db.Column( db.String(128), default = '' )
    entrance_year   = db.Column( db.String(4),   default = '' )
    graduation_year = db.Column( db.String(4),   default = '' )
    
    student_info = db.relationship('Student_info', 
        back_populates = 'middle_education' )

    def __init__(self):
        self.section_name = u'Образование среднее'
        self.is_fixed     = True
        self.placeholders = {
            'school' : u'МБОУ СОШ "Лицей № 5"',
            'school_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56',
            'entrance_year' : u'2005',
            'graduation_year' : u'2013',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'school' : u'Школа по аттестату',
            'school_address' : u'Адрес местонахождения',
            'entrance_year' : u'Год поступления',
            'graduation_year' : u'Год окончания',
        }
        self.readonly_fields = set()

class Spec_middle_education(db.Model, User_info_table_interface):
    __tablename__ = 'spec_middle_education'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id') )
    
    institution         = db.Column( db.String(128), default = '' )
    institution_address = db.Column( db.String(128), default = '' )
    speciality          = db.Column( db.String(128), default = '' )
    entrance_year       = db.Column( db.String(4), default = '' )
    graduation_year     = db.Column( db.String(4), default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'spec_middle_education' )
    
    def __init__(self):
        self.section_name = u'Образование среднеспециальное'
        self.is_fixed     = True
        self.placeholders = {
            'institution' : u'ПТУ № 43',
            'institution_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56',
            'speciality' : u'Сварщик',
            'entrance_year' : u'2005',
            'graduation_year' : u'2013',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'institution' : u'Учебное заведение',
            'institution_address' : u'Адрес местонахождения',
            'speciality' : u'Специальность по диплому',
            'entrance_year' : u'Год поступления',
            'graduation_year' : u'Год окончания',
        }
        self.readonly_fields = set()

class High_education(db.Model, User_info_table_interface):
    __tablename__ = 'high_education'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    
    institution        = db.Column( db.String(128), default = '' )
    budgetary          = db.Column( db.String(100), default = '' )
    full_faculty_name  = db.Column( db.String(128), default = '' )
    short_faculty_name = db.Column( db.String(16),  default = '' )
    spec_diploma       = db.Column( db.String(128), default = '' )
    study_group_2      = db.Column( db.String(10),  default = '' )
    study_group_3      = db.Column( db.String(10),  default = '' )
    study_group_4      = db.Column( db.String(10),  default = '' )
    form_study         = db.Column( db.String(20),  default = '' )
    quality            = db.Column( db.String(20),  default = '' )
    entrance_year      = db.Column( db.String(4),   default = '' )
    graduation_year    = db.Column( db.String(4),   default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'high_education' )
    
    def __init__(self):
        self.section_name = u'Образование высшее'
        self.is_fixed     = False
        self.placeholders = {
            'institution' : u'МГУ имени М. В. Ломоносова',
            'budgetary' : u'бюджет',
            'full_faculty_name' : u'Механико-математический факультет',
            'short_faculty_name' : u'МехМат',
            'spec_diploma' : u'Программист-математик',
            'study_group_2' : u'228',
            'study_group_3' : u'339',
            'study_group_4' : u'467М',
            'form_study' : u'очная',
            'quality' : u'Бакалавр',
            'entrance_year' : u'2005',
            'graduation_year' : u'2013',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'institution' : u'ВУЗ',
            'budgetary' : u'Бюджет',
            'full_faculty_name' : u'Факультет (полное название)',
            'short_faculty_name' : u'Факультет (сокращенное название)',
            'spec_diploma' : u'Специальность по диплому',
            'study_group_2' : u'Учебная группа 2 курс',
            'study_group_3' : u'Учебная группа 3 курс',
            'study_group_4' : u'Учебная группа 4 курс',
            'form_study' : u'Форма обучения',
            'quality' : u'Квалификация',
            'entrance_year' : u'Год поступления',
            'graduation_year' : u'Год окончания',
        }
        self.readonly_fields = { 'quality', }

class Military_education(db.Model, User_info_table_interface):
    __tablename__ = 'military_education'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    
    platoon_1 = db.Column( db.String(10), default = '' )
    platoon_2 = db.Column( db.String(10), default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'military_education' )
    
    def __init__(self):
        self.section_name = u'Военное образование в МГУ'
        self.is_fixed     = True
        self.placeholders = {
            'platoon_1' : u'117',
            'platoon_2' : u'127',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'platoon_1' : u'Взвод 1 года обучения',
            'platoon_2' : u'Взвод 2 года обучения',
        }
        self.readonly_fields = set()
    
class Languages(db.Model, User_info_table_interface):
    __tablename__ = 'languages'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    
    language     = db.Column( db.String(32),  default = '' )
    quality      = db.Column( db.String(32),  default = '' )
    certificates = db.Column( db.String(256), default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'languages' )

    def __init__(self):
        self.section_name = u'Иностранные языки'
        self.is_fixed     = False
        self.placeholders = {
            'language' : u'Английский',
            'quality' : u'Продвинутый',
            'certificates' : u'TOEFL, 101 балл; IELTS, 8 баллов'
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'language' : u'Язык',
            'quality' : u'Степень владения',
            'certificates' : u'Сертификаты'
        }
        self.readonly_fields = set()

class Mothers_fathers(db.Model, User_info_table_interface):
    __tablename__ = 'mothers_fathers'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    
    status              = db.Column( db.String(4),   default = '' ) # мать, отец
    last_name           = db.Column( db.String(20),  default = '' )
    first_name          = db.Column( db.String(20),  default = '' )
    middle_name         = db.Column( db.String(20),  default = '' )
    birth_date          = db.Column( db.String(10),  default = '' )
    birth_place         = db.Column( db.String(64),  default = '' )
    mobile_phone_1      = db.Column( db.String(11),  default = '' )
    mobile_phone_2      = db.Column( db.String(11),  default = '' )
    home_phone          = db.Column( db.String(11),  default = '' )
    job_place           = db.Column( db.String(128), default = '' )
    job_post            = db.Column( db.String(64),  default = '' )
    fact_index          = db.Column( db.String(9),   default = '' )
    fact_address        = db.Column( db.String(256), default = '' )
    foreign_citizenship = db.Column( db.String(256), default = '' )
    conviction          = db.Column( db.String(256), default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'mothers_fathers' )
    
    def __init__(self):
        self.section_name = u'Родители'
        self.is_fixed     = False
        self.placeholders = {
            'status' : u'мать',
            'last_name': u'Иванов',
            'first_name': u'Иван',
            'middle_name': u'Иванович',
            'birth_date': u'yyyy-mm-dd',
            'birth_place': u'гор. Нижние Пупки',
            'mobile_phone_1' : u'89012345678',
            'mobile_phone_2' : u'89012340567',
            'home_phone' : u'84953045678',
            'job_place' : u'ТЭЦ-5 гор. Караганда',
            'job_post' : u'Сварщик',
            'fact_index' : u'123456',
            'fact_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56',
            'foreign_citizenship' : u'Гражданство Белорусии',
            'conviction' : u'Не судим / судим в nnnn году, оправдан',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'status' : u'Статус',
            'last_name': u'Фамилия',
            'first_name': u'Имя',
            'middle_name': u'Отчество',
            'birth_date': u'Дата рождения',
            'birth_place': u'Место рождения',
            'mobile_phone_1' : u'Мобильный 1',
            'mobile_phone_2' : u'Мобильный 2',
            'home_phone' : u'Домашний',
            'job_place' : u'Место работы',
            'job_post' : u'Должность',
            'fact_index' : u'Индекс фактического проживания',
            'fact_address' : u'Адрес фактического проживания',
            'foreign_citizenship' : u'Иностранное гражданство или подданство',
            'conviction' : u'Судимость',
        }
        self.readonly_fields = {'status', }

class Brothers_sisters_children(db.Model, User_info_table_interface):
    __tablename__ = 'brothers_sisters_children'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    
    status              = db.Column( db.String(6),   default = '' ) # брат, сестра, сын, дочь
    last_name           = db.Column( db.String(20),  default = '' )
    first_name          = db.Column( db.String(20),  default = '' )
    middle_name         = db.Column( db.String(20),  default = '' )
    birth_date          = db.Column( db.String(10),  default = '' )
    birth_place         = db.Column( db.String(64),  default = '' )
    foreign_citizenship = db.Column( db.String(256), default = '' )
    conviction          = db.Column( db.String(256), default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'brothers_sisters_children' )

    def __init__(self):
        self.section_name = u'Родственники'
        self.is_fixed     = False
        self.placeholders = {
            'status' : u'брат',
            'last_name': u'Иванов',
            'first_name': u'Иван',
            'middle_name': u'Иванович',
            'birth_date': u'yyyy-mm-dd',
            'birth_place': u'гор. Нижние Пупки',
            'foreign_citizenship' : u'Гражданство Белорусии',
            'conviction' : u'Не судим / судим в nnnn году, оправдан',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'status' : u'Статус',
            'last_name': u'Фамилия',
            'first_name': u'Имя',
            'middle_name': u'Отчество',
            'birth_date': u'Дата рождения',
            'birth_place': u'Место рождения',
            'foreign_citizenship' : u'Иностранное гражданство или подданство',
            'conviction' : u'Судимость',
        }
        self.readonly_fields = {'status', }

class Married_certificates(db.Model, User_info_table_interface):
    __tablename__ = 'married_certificates'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    
    serial         = db.Column( db.String(20),  default = '' )
    number         = db.Column( db.String(20),  default = '' )
    issuer         = db.Column( db.String(128), default = '' )
    date_issue     = db.Column( db.String(10),  default = '' )
    last_name      = db.Column( db.String(20),  default = '' )
    first_name     = db.Column( db.String(20),  default = '' )
    middle_name    = db.Column( db.String(20),  default = '' )
    birth_date     = db.Column( db.String(10),  default = '' )
    birth_place    = db.Column( db.String(64),  default = '' )
    mobile_phone_1 = db.Column( db.String(11),  default = '' )
    mobile_phone_2 = db.Column( db.String(11),  default = '' )
    home_phone     = db.Column( db.String(11),  default = '' )
    job_place      = db.Column( db.String(128), default = '' )
    job_post       = db.Column( db.String(64),  default = '' )
    fact_index     = db.Column( db.String(9),   default = '' )
    fact_address   = db.Column( db.String(256), default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'married_certificates' )

    def __init__(self):
        self.section_name = u'Супруги'
        self.is_fixed     = False
        self.placeholders = {
            'serial' : u'EA12',
            'number' : u'1234567890',
            'issuer' : u'гор. Уфа, ЗАГС № 5',
            'date_issue' : u'12.12.2014',
            'last_name': u'Иванова',
            'first_name': u'Мария',
            'middle_name': u'Ивановна',
            'birth_date': u'yyyy-mm-dd',
            'birth_place': u'гор. Нижние Пупки',
            'mobile_phone_1' : u'89012345678',
            'mobile_phone_2' : u'89012340567',
            'home_phone' : u'84953045678',
            'job_place' : u'ТЭЦ-5 гор. Караганда',
            'job_post' : u'Сварщик',
            'fact_index' : u'123456',
            'fact_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56'
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'serial' : u'Серия',
            'number' : u'Номер',
            'issuer' : u'Кем выдано',
            'date_issue' : u'Когда выдано',
            'last_name': u'Фамилия',
            'first_name': u'Имя',
            'middle_name': u'Отчество',
            'birth_date': u'Дата рождения',
            'birth_place': u'Место рождения',
            'mobile_phone_1' : u'Мобильный 1',
            'mobile_phone_2' : u'Мобильный 2',
            'home_phone' : u'Домашний',
            'job_place' : u'Место работы',
            'job_post' : u'Должность',
            'fact_index' : u'Индекс фактического проживания',
            'fact_address' : u'Адрес фактического проживания'
        }
        self.readonly_fields = set()

class Personal_data(db.Model, User_info_table_interface):
    __tablename__ = 'personal_data'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    
    blood_group_resus    = db.Column( db.String(10),  default = '' )
    shoes_size           = db.Column( db.String(10),  default = '' )
    uniform_size         = db.Column( db.String(10),  default = '' )
    head_size            = db.Column( db.String(10),  default = '' )
    growth               = db.Column( db.String(10),  default = '' )
    protivogaz_size      = db.Column( db.String(10),  default = '' )
    OZK_size             = db.Column( db.String(10),  default = '' )
    government_prize     = db.Column( db.String(256), default = '' )
    injuries             = db.Column( db.String(256), default = '' )
    criminals            = db.Column( db.String(256), default = '' )
    civil_specialization = db.Column( db.String(256), default = '' )
    hobbies              = db.Column( db.String(256), default = '' )
    sports               = db.Column( db.String(256), default = '' )
    scientific_results   = db.Column( db.String(256), default = '' )
    work_experience      = db.Column( db.String(256), default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'personal_data' )
    
    def __init__(self):
        self.section_name = u'Личные данные'
        self.is_fixed     = True
        self.placeholders = {
            'blood_group_resus' : u'2+',
            'shoes_size' : u'46',
            'uniform_size' : u'48',
            'head_size' : u'64',
            'growth': u'165',
            'protivogaz_size': u'8',
            'OZK_size': u'34',
            'government_prize': u'медаль Жукова',
            'injuries': u'хронический бронхит',
            'criminals' : u'не судим',
            'civil_specialization' : u'Программист-математик',
            'hobbies' : u'Играю на гитаре, бегаю по утрам',
            'sports' : u'шахматы - КМС; вольная борьба - 1-й взрослый',
            'scientific_results' : u'Статья "Интерполяция экспоненты кривыми первого порядка" в Вестнике Томского университета',
            'work_experience' : u'ООО Компания, младший аналитик nnnn-nnnn г.',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'blood_group_resus' : u'Группа крови, резус фактор',
            'shoes_size' : u'Размер обуви',
            'uniform_size' : u'Размер одежды',
            'head_size' : u'Размер головного убора',
            'growth': u'Рост',
            'protivogaz_size': u'Размер противогаза',
            'OZK_size': u'Размер ОЗК',
            'government_prize': u'Государственные награды и знаки',
            'injuries': u'Полученные увечья (ранения, травмы, контузии), заболевания',
            'criminals' : u'Наличие судимости',
            'civil_specialization' : u'Гражданские специальности',
            'hobbies' : u'Хобби, увлечения',
            'sports' : u'Спортивные достижения, разряды',
            'scientific_results': u'Научные труды и изобретения',
            'work_experience': u'Трудовая деятельность (опыт работы)',
        }
        self.readonly_fields = set()

class Spec_data(db.Model, User_info_table_interface):
    __tablename__ = 'spec_data'

    id              = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    
    personal_number              = db.Column( db.String(16),  default = '' )
    military_department          = db.Column( db.String(128), default = '' )
    oath_date                    = db.Column( db.String(10),  default = '' )
    military_department_adr      = db.Column( db.String(300), default = '' )
    order_personal_number        = db.Column( db.String(300), default = '' )
    order_rank                   = db.Column( db.String(300), default = u'Пр. №           от «     »              20   г. военного комиссара г. Москвы' )
    military_charges_period_from = db.Column( db.String(10),  default = '' )
    military_charges_period_to   = db.Column( db.String(10),  default = '' )
    fvo_study_period_from        = db.Column( db.String(10),  default = '' )
    fvo_study_period_to          = db.Column( db.String(10),  default = '' )

    student_info = db.relationship('Student_info', 
        back_populates = 'spec_data' )
    
    def __init__(self):
        self.section_name = u'Служебные данные'
        self.is_fixed     = True
        self.placeholders = {
            'personal_number' : u'А-123456',
            'military_department': u'12102',
            'oath_date': u'22.07.2017', 
            'military_department_adr': u'606087, Нижегородская обл., р-н Володарский, пгт. Центральный, в/ч 12102',
            'order_personal_number': u'123456',
            'order_rank': u'123456',
            'military_charges_period_from': u'15.07.2017',
            'military_charges_period_to': u'16.08.2017',
            'fvo_study_period_from': u'01.09.2015',
            'fvo_study_period_to': u'30.08.2017',
        }
        self.en2ru = {
            'id': None, 
            'student_info_id' : None,
            'personal_number' : u'Личный номер',
            'military_department': u'Войсковая часть',
            'oath_date': u'Дата принятия присяги',
            'military_department_adr': u'Адрес войсковой части',
            'order_personal_number': u'Приказ о присвоении личного номера',
            'order_rank': u'Приказ о присвоении звания',
            'military_charges_period_from': u'Период сборов с',
            'military_charges_period_to': u'Период сборов по',
            'fvo_study_period_from': u'Период обучения на ФВО с',
            'fvo_study_period_to': u'Период обучения на ФВО по',
        }
        self.readonly_fields = set()
