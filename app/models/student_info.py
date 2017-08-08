#-.- coding: utf-8 -.-
from app import db
from app.models.simple import * 
from app.models.easy import *

class Class_with_attrs_access():

    def __setitem__(self, item, value):
        try:
            return setattr(self, item, value)
        except all:
            return '' 

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except all:
            return ''    


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

    comments = db.relationship('Comments', 
        back_populates = 'student_info', uselist = False )
    basic_information =  db.relationship('Basic_information', 
        back_populates = 'student_info', uselist = False )
    certificates_change_name =  db.relationship('Certificates_change_name', 
        back_populates = 'student_info' )
    communications =  db.relationship('Communications', 
        back_populates = 'student_info' )
    passports =  db.relationship('Passports', 
        back_populates = 'student_info' )
    international_passports =  db.relationship('International_passports', 
        back_populates = 'student_info' )
    registration_certificates =  db.relationship('Registration_certificates', 
        back_populates = 'student_info' )
    middle_education =  db.relationship('Middle_education', 
        back_populates = 'student_info' )
    spec_middle_education =  db.relationship('Spec_middle_education', 
        back_populates = 'student_info' )
    high_education =  db.relationship('High_education', 
        back_populates = 'student_info' )
    military_education =  db.relationship('Military_education', 
        back_populates = 'student_info' )
    languages =  db.relationship('Languages', 
        back_populates = 'student_info' )
    mothers_fathers =  db.relationship('Mothers_fathers', 
        back_populates = 'student_info' )
    brothers_sisters_children =  db.relationship('Brothers_sisters_children', 
        back_populates = 'student_info' )
    married_certificates =  db.relationship('Married_certificates', 
        back_populates = 'student_info' )
    personal_data =  db.relationship('Personal_data', 
        back_populates = 'student_info' )

class Comments(db.Model, Class_with_attrs_access):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))

    # поля с комментариями админа к секции
    basic_information_comment         = db.Column( db.String( 512 ), default='' ) 
    certificates_change_name_comment  = db.Column( db.String( 512 ), default='' )
    communications_comment            = db.Column( db.String( 512 ), default='' )
    passports_comment                 = db.Column( db.String( 512 ), default='' )
    international_passports_comment   = db.Column( db.String( 512 ), default='' )
    registration_certificates_comment = db.Column( db.String( 512 ), default='' )
    middle_education_comment          = db.Column( db.String( 512 ), default='' )
    spec_middle_education_comment     = db.Column( db.String( 512 ), default='' )
    high_education_comment            = db.Column( db.String( 512 ), default='' )
    military_education_comment        = db.Column( db.String( 512 ), default='' )
    languages_comment                 = db.Column( db.String( 512 ), default='' )
    mothers_fathers_comment           = db.Column( db.String( 512 ), default='' )
    brothers_sisters_children_comment = db.Column( db.String( 512 ), default='' )
    married_certificates_comment      = db.Column( db.String( 512 ), default='' )
    personal_data_comment             = db.Column( db.String( 512 ), default='' )

    student_info = db.relationship( 'Student_info', back_populates = 'comments' )


class Basic_information(db.Model, Class_with_attrs_access):
    __tablename__ = 'basic_information'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    middle_name = db.Column(db.String(20))
    birth_date = db.Column(db.String(10))
    birth_place = db.Column(db.String(64))
    nationality = db.Column(db.String(20))
    family_status = db.Column( db.String( 10 ) )
    citizenship = db.Column( db.String( 50 ) )
    second_citizenship = db.Column( db.String( 50 ) )
    tin = db.Column( db.String( 12 ) )
    insurance_certificate = db.Column( db.String( 14 ) ) 

    student_info =  db.relationship('Student_info', 
        back_populates = 'basic_information' )

    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Основная информация'

    def placeholder(self, eng):
        placeholders = {
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
        if eng not in placeholders:
            return ''
        return placeholders[eng]

    def get_russian_name(self, eng):
        en2ru = {
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
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Certificates_change_name(db.Model, Class_with_attrs_access):
    __tablename__ = 'certificates_change_name'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))
    serial = db.Column( db.String( 5 ) )
    number = db.Column( db.String( 10 ) )
    issuer = db.Column( db.String( 256 ) )
    issue_date = db.Column(db.String(10)) 
    changing = db.Column( db.String( 128 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'certificates_change_name')

    def is_fixed(self):
        return False

    def get_section_name(self):
        return u'Свидетельство о перемене имени'

    def placeholder(self, eng):
        placeholders = {
            'serial' : u'12345',
            'number' : u'1234567890',
            'issuer' : u'гор. Новосибирск, ЗАГС 61',
            'issue_date' : u'01.01.2000',
            'changing' : u'Поменял имя ПЕТР на имя ВАСИЛИЙ'
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]

    def get_russian_name(self, eng):
        en2ru = {
            'id': None, 
            'student_info_id' : None,
            'serial' : u'Серия',
            'number' : u'Номер',
            'issuer' : u'Кем выдан',
            'issue_date' : u'Когда выдан',
            'changing' : u'Что изменилось',
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Communications( db.Model, Class_with_attrs_access ):
    __tablename__ = 'communications'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    mobile_phone_1 = db.Column( db.String( 11 ) )
    mobile_phone_2 = db.Column( db.String( 11 ) )
    home_phone = db.Column( db.String( 11 ) )
    email = db.Column( db.String( 64 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'communications' )

    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Номера телефонов, электронная почта'

    def placeholder(self, eng):
        placeholders = {
            'mobile_phone_1' : u'89012345678',
            'mobile_phone_2' : u'89012340567',
            'home_phone' : u'84953045678',
            'email' : u'vasya.pupkin@gmail.com'
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None, 
            'student_info_id' : None,
            'mobile_phone_1' : u'Мобильный 1',
            'mobile_phone_2' : u'Мобильный 2',
            'home_phone' : u'Домашний',
            'email' : u'E-mail'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Passports( db.Model, Class_with_attrs_access ):
    __tablename__ = "passports"
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 4 ) )
    number = db.Column( db.String( 6 ) )
    issuer = db.Column( db.String( 256 ) )
    issue_date = db.Column(db.String(10)) 
    code = db.Column( db.String( 7 ) )
    registration_index = db.Column( db.String( 6 ) )
    registration_address = db.Column( db.String( 256 ) )
    fact_index = db.Column( db.String( 6 ) )
    fact_address = db.Column( db.String( 256 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'passports' )
    
    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Паспорт'

    def placeholder(self, eng):
        placeholders = {
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
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
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
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class International_passports( db.Model, Class_with_attrs_access ):
    __tablename__ = 'international_passports'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 2 ) )
    number = db.Column( db.String( 7 ) )
    issuer = db.Column( db.String( 256 ) )
    issue_date = db.Column(db.String(10)) 
    validity = db.Column( db.String( 10 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'international_passports' )
    
    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Загранпаспорт'

    def placeholder(self, eng):
        placeholders = {
            'serial' : u'12',
            'number' : u'1234567',
            'issuer' : u'Отделом УФМС по гор. Москве по району Раменки',
            'issue_date' : u'01.01.2015',
            'validity' : u'10 лет',
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None, 
            'student_info_id' : None,
            'serial' : u'Серия',
            'number' : u'Номер',
            'issuer' : u'Кем выдан',
            'issue_date' : u'Когда выдан',
            'validity' : u'Срок действия',
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Registration_certificates( db.Model, Class_with_attrs_access ):
    __tablename__ = 'registration_certificates'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 2 ) ) 
    number = db.Column( db.String( 7 ) )
    issuer = db.Column( db.String( 128 ) )
    date_issue = db.Column(db.String(10))  
    military_department = db.Column( db.String( 128 ) )
    shelf_category = db.Column( db.String( 32 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'registration_certificates' )
    
    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Приписное свидетельство'

    def placeholder(self, eng):
        placeholders = {
            'serial' : u'АВ',
            'number' : u'1234567',
            'issuer' : u'Раменским комиссариатом',
            'date_issue' : u'01.01.2015',
            'military_department' : u'Раменский военный комиссариат',
            'shelf_category' : u'В+ годен с ограничениями'
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None, 
            'student_info_id' : None,
            'serial' : u'Серия',
            'number' : u'Номер',
            'issuer' : u'Кем выдано',
            'date_issue' : u'Когда выдано',
            'military_department' : u'Военный комиссариат по месту воинского учета',
            'shelf_category' : u'Категория годности'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Middle_education( db.Model, Class_with_attrs_access ):
    __tablename__ = 'middle_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    school = db.Column( db.String( 128 ) )
    school_address = db.Column( db.String( 128 ) )
    entrance_year = db.Column( db.String( 4 ) )
    graduation_year = db.Column( db.String( 4 ) )
    
    student_info =  db.relationship('Student_info', 
        back_populates = 'middle_education' )

    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Образование среднее'

    def placeholder(self, eng):
        placeholders = {
            'school' : u'МБОУ СОШ "Лицей № 5"',
            'school_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56',
            'entrance_year' : u'2005',
            'graduation_year' : u'2013',
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None, 
            'student_info_id' : None,
            'school' : u'Школа по аттестату',
            'school_address' : u'Адрес местонахождения',
            'entrance_year' : u'Год поступления',
            'graduation_year' : u'Год окончания',
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Spec_middle_education( db.Model, Class_with_attrs_access ):
    __tablename__ = 'spec_middle_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    institution = db.Column( db.String( 128 ) )
    institution_address = db.Column( db.String( 128 ) )
    speciality = db.Column( db.String( 128 ) )
    entrance_year = db.Column( db.String( 4 ) )
    graduation_year = db.Column( db.String( 4 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'spec_middle_education' )
    
    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Образование среднеспециальное'

    def placeholder(self, eng):
        placeholders = {
            'institution' : u'ПТУ № 43',
            'institution_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56',
            'speciality' : u'Сварщик',
            'entrance_year' : u'2005',
            'graduation_year' : u'2013',
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None, 
            'student_info_id' : None,
            'institution' : u'Учебное заведение',
            'institution_address' : u'Адрес местонахождения',
            'speciality' : u'Специальность по диплому',
            'entrance_year' : u'Год поступления',
            'graduation_year' : u'Год окончания',
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class High_education(db.Model, Class_with_attrs_access):
    __tablename__ = 'high_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    institution = db.Column( db.String( 128 ) )
    budgetary = db.Column( db.Boolean, default=NOT_BUDGET )
    full_faculty_name = db.Column( db.String( 128 ) )
    short_faculty_name = db.Column( db.String( 16 ) )
    spec_diploma = db.Column( db.String( 128 ) )
    study_group_2 = db.Column( db.String( 10 ) )
    study_group_3 = db.Column( db.String( 10 ) )
    study_group_4 = db.Column( db.String( 10 ) )
    form_study = db.Column( db.String( 20 ) )
    quality = db.Column( db.String( 20 ) )
    entrance_year = db.Column( db.String( 4 ) )
    graduation_year = db.Column( db.String( 4 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'high_education' )
    
    def is_fixed(self):
        return False

    def get_section_name(self):
        return u'Образование высшее'

    def placeholder(self, eng):
        placeholders = {
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
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
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
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Military_education( db.Model, Class_with_attrs_access ):
    __tablename__ = 'military_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    platoon_1 = db.Column( db.String( 10 ) )
    platoon_2 = db.Column( db.String( 10 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'military_education' )
    
    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Военное образование в МГУ'

    def placeholder(self, eng):
        placeholders = {
            'platoon_1' : u'117',
            'platoon_2' : u'127',
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None, 
            'student_info_id' : None,
            'platoon_1' : u'Взвод 1 года обучения',
            'platoon_2' : u'Взвод 2 года обучения',
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
class Languages( db.Model, Class_with_attrs_access ):
    __tablename__ = 'languages'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    language = db.Column( db.String( 32 ) )
    quality = db.Column( db.String( 32 ) )
    certificates = db.Column( db.String( 256 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'languages' )

    def is_fixed(self):
        return False
 
    def get_section_name(self):
        return u'Иностранные языки'

    def placeholder(self, eng):
        placeholders = {
            'language' : u'Английский',
            'quality' : u'Продвинутый',
            'certificates' : u'TOEFL, 101 балл; IELTS, 8 баллов'
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None, 
            'student_info_id' : None,
            'language' : u'Язык',
            'quality' : u'Степень владения',
            'certificates' : u'Сертификаты'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Mothers_fathers( db.Model, Class_with_attrs_access ):
    __tablename__ = 'mothers_fathers'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    status = db.Column( db.String( 4 ) ) # мать, отец
    last_name = db.Column( db.String( 20 ) )
    first_name = db.Column( db.String( 20 ) )
    middle_name = db.Column( db.String( 20 ) )
    birth_date = db.Column(db.String(10))
    birth_place = db.Column( db.String( 64 ) )
    mobile_phone_1 = db.Column( db.String( 11 ) )
    mobile_phone_2 = db.Column( db.String( 11 ) )
    home_phone = db.Column( db.String( 11 ) )
    job_place = db.Column( db.String( 128 ) )
    job_post = db.Column( db.String( 64 ) )
    fact_index = db.Column( db.String( 9 ) )
    fact_address = db.Column( db.String( 256 ) )
    foreign_citizenship = db.Column( db.String( 256 ) )
    conviction = db.Column( db.String( 256 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'mothers_fathers' )
    
    def is_fixed(self):
        return False

    def get_section_name(self):
        return u'Родители'

    def placeholder(self, eng):
        placeholders = {
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
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
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
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Brothers_sisters_children( db.Model, Class_with_attrs_access ):
    __tablename__ = 'brothers_sisters_children'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    status = db.Column( db.String( 6 ) ) # брат, сестра, сын, дочь
    last_name = db.Column( db.String( 20 ) )
    first_name = db.Column( db.String( 20 ) )
    middle_name = db.Column( db.String( 20 ) )
    birth_date = db.Column(db.String(10))
    birth_place = db.Column( db.String( 64 ) )
    foreign_citizenship = db.Column( db.String( 256 ) )
    conviction = db.Column( db.String( 256 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'brothers_sisters_children' )

    def is_fixed(self):
        return False
    
    def get_section_name(self):
        return u'Родственники'

    def placeholder(self, eng):
        placeholders = {
            'status' : u'брат',
            'last_name': u'Иванов',
            'first_name': u'Иван',
            'middle_name': u'Иванович',
            'birth_date': u'yyyy-mm-dd',
            'birth_place': u'гор. Нижние Пупки',
            'foreign_citizenship' : u'Гражданство Белорусии',
            'conviction' : u'Не судим / судим в nnnn году, оправдан',
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
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
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Married_certificates( db.Model, Class_with_attrs_access ):
    __tablename__ = 'married_certificates'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 20 ) )
    number = db.Column( db.String( 20 ) )
    issuer = db.Column( db.String( 128 ) )
    date_issue = db.Column(db.String(10))
    last_name = db.Column( db.String( 20 ) )
    first_name = db.Column( db.String( 20 ) )
    middle_name = db.Column( db.String( 20 ) )
    birth_date = db.Column(db.String(10))
    birth_place = db.Column( db.String( 64 ) )
    mobile_phone_1 = db.Column( db.String( 11 ) )
    mobile_phone_2 = db.Column( db.String( 11 ) )
    home_phone = db.Column( db.String( 11 ) )
    job_place = db.Column( db.String( 128 ) )
    job_post = db.Column( db.String( 64 ) )
    fact_index = db.Column( db.String( 9 ) )
    fact_address = db.Column( db.String( 256 ) )

    def is_fixed(self):
        return False

    def get_section_name(self):
        return u'Супруги'

    student_info =  db.relationship('Student_info', 
        back_populates = 'married_certificates' )
    
    def placeholder(self, eng):
        placeholders = {
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
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
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
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

class Personal_data( db.Model, Class_with_attrs_access ):
    __tablename__ = 'personal_data'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    blood_group_resus = db.Column( db.String( 5 ) )
    shoes_size = db.Column( db.SmallInteger )
    uniform_size = db.Column( db.SmallInteger )
    head_size = db.Column( db.SmallInteger )
    growth = db.Column( db.Integer )
    protivogaz_size = db.Column( db.SmallInteger )
    OZK_size = db.Column( db.SmallInteger )
    government_prize = db.Column( db.String( 256 ) )
    injuries = db.Column( db.String( 256 ) )
    criminals = db.Column( db.String( 256 ) )
    civil_specialization = db.Column( db.String( 256 ) )
    hobbies = db.Column( db.String( 256 ) )
    sports = db.Column( db.String( 256 ) )
    scientific_results = db.Column( db.String( 256 ) )
    work_experience = db.Column( db.String( 256 ) )

    student_info =  db.relationship('Student_info', 
        back_populates = 'personal_data' )
    
    def is_fixed(self):
        return True

    def get_section_name(self):
        return u'Личные данные'

    def placeholder(self, eng):
        placeholders = {
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
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
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
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
