#-.- coding: utf-8 -.-
from app import db
from simple import *

# Mode of table
NOT_EDIT    = 0
EDIT        = 1
CHANGING    = 2
ABSENT      = 3 

# Mode of budgetary
NOT_BUDGET  = 0
BUDGET      = 1

class Student_info(db.Model):
    __tablename__ = 'student_info'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column( db.Integer, db.ForeignKey( 'user.id' ) )
    table_basic_information = db.Column( db.SmallInteger, default = NOT_EDIT ) 
    table_certificates_change_name = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_communications = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_passports = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_international_passports = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_registration_certificates = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_middle_education = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_spec_middle_education = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_high_education = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_military_education = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_languages = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_mothers_fathers = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_brothers_sisters_children = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_married_certificates = db.Column( db.SmallInteger, default = NOT_EDIT )
    table_personal_data = db.Column( db.SmallInteger, default = NOT_EDIT )

    basic_information =  db.relationship('Basic_information', 
        backref = 'student_info', lazy = 'dynamic' )
    certificates_change_name =  db.relationship('Certificates_change_name', 
        backref = 'student_info', lazy = 'dynamic' )
    communications =  db.relationship('Communications', 
        backref = 'student_info', lazy = 'dynamic' )
    passport =  db.relationship('Passports', 
        backref = 'student_info', lazy = 'dynamic' )
    international_passport =  db.relationship('International_passports', 
        backref = 'student_info', lazy = 'dynamic' )
    registration_certificate =  db.relationship('Registration_certificates', 
        backref = 'student_info', lazy = 'dynamic' )
    middle_education =  db.relationship('Middle_education', 
        backref = 'student_info', lazy = 'dynamic' )
    spec_middle_education =  db.relationship('Spec_middle_education', 
        backref = 'student_info', lazy = 'dynamic' )
    high_education =  db.relationship('High_education', 
        backref = 'student_info', lazy = 'dynamic' )
    military_education =  db.relationship('Military_education', 
        backref = 'student_info', lazy = 'dynamic' )
    languages =  db.relationship('Languages', 
        backref = 'student_info', lazy = 'dynamic' )
    mother_father =  db.relationship('Mothers_fathers', 
        backref = 'student_info', lazy = 'dynamic' )
    brothers_sisters_children =  db.relationship('Brothers_sisters_children', 
        backref = 'student_info', lazy = 'dynamic' )
    married_certificates =  db.relationship('Married_certificates', 
        backref = 'student_info', lazy = 'dynamic' )
    personal_data =  db.relationship('Personal_data', 
        backref = 'student_info', lazy = 'dynamic' )


class Basic_information(db.Model):
    __tablename__ = 'basic_information'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    middle_name = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(64))
    nationality = db.Column(db.String(20))
    family_status = db.Column( db.String( 10 ) )
    citizenship = db.Column( db.String( 50 ) )
    second_citizenship = db.Column( db.String( 50 ) )
    tin = db.Column( db.String( 12 ) )
    insurance_certificate = db.Column( db.String( 14 ) ) 

    def placeholder(self, eng):
        placeholders = {
            'last_name': u'Иванов',
            'first_name': u'Иван',
            'middle_name': u'Иванович',
            'birth_date': u'yyyy-mm-dd',
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

    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'birth_date': self.birth_date,
            'birth_place': self.birth_place,
            'nationality': self.nationality,
            'family_status': self.family_status,
            'citizenship': self.citizenship,
            'second_citizenship': self.second_citizenship,
            'tin': self.tin,
            'insurance_certificate': self.insurance_certificate,
        }
        return item2obj[item];

class Certificates_change_name(db.Model):
    __tablename__ = 'certificates_change_name'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))
    serial = db.Column( db.String( 5 ) )
    number = db.Column( db.String( 10 ) )
    issuer = db.Column( db.String( 256 ) )
    issue_date = db.Column( db.Date )
    changing = db.Column( db.String( 128 ) )

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

    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'serial' : self.serial,
            'number' : self.number,
            'issuer' : self.issuer,
            'issue_date' : self.issue_date,
            'changing' : self.changing,
        }
        return item2obj[item];

class Communications( db.Model ):
    __tablename__ = 'communications'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    mobile_phone_1 = db.Column( db.String( 11 ) )
    mobile_phone_2 = db.Column( db.String( 11 ) )
    home_phone = db.Column( db.String( 11 ) )
    email = db.Column( db.String( 64 ) )

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
            'mobile_phone_1' : u'Мобильный 1',
            'mobile_phone_2' : u'Мобильный 2',
            'home_phone' : u'Домашний',
            'email' : u'E-mail'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'mobile_phone_1' : self.mobile_phone_1,
            'mobile_phone_2' : self.mobile_phone_2,
            'home_phone' : self.home_phone,
            'email' : self.email
        }
        return item2obj[item];

class Passports( db.Model ):
    __tablename__ = "passports"
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 4 ) )
    number = db.Column( db.String( 6 ) )
    issuer = db.Column( db.String( 256 ) )
    issue_date = db.Column( db.Date )
    code = db.Column( db.String( 7 ) )
    registration_index = db.Column( db.String( 6 ) )
    registration_address = db.Column( db.String( 256 ) )
    fact_index = db.Column( db.String( 6 ) )
    fact_address = db.Column( db.String( 256 ) )
    
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
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'serial' : self.serial,
            'number' : self.number,
            'issuer' : self.issuer,
            'issue_date' : self.issue_date,
            'code' : self.code,
            'registration_index' : self.registration_index,
            'registration_address' : self.registration_address,
            'fact_index' : self.fact_index,
            'fact_address' : self.fact_addresss,
        }
        return item2obj[item];

class International_passports( db.Model ):
    __tablename__ = 'international_passports'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 2 ) )
    number = db.Column( db.String( 7 ) )
    issuer = db.Column( db.String( 256 ) )
    issue_date = db.Column( db.Date )
    validity = db.Column( db.String( 10 ) )
    
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
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'serial' : self.serial,
            'number' : self.number,
            'issuer' : self.issuer,
            'issue_date' : self.issue_date,
            'validity' : self.validity,
        }
        return item2obj[item];

class Registration_certificates( db.Model ):
    __tablename__ = 'registration_certificates'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 2 ) ) 
    number = db.Column( db.String( 7 ) )
    issuer = db.Column( db.String( 128 ) )
    date_issue = db.Column( db.Date )
    military_department = db.Column( db.String( 128 ) )
    shelf_category = db.Column( db.String( 32 ) )
    
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
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'serial' : self.serial,
            'number' : self.number,
            'issuer' : self.issuer,
            'date_issue' : self.date_issue,
            'military_department' : self.military_department,
            'shelf_category' : self.shelf_category
        }
        return item2obj[item];

class Middle_education( db.Model ):
    __tablename__ = 'middle_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    school = db.Column( db.String( 128 ) )
    school_address = db.Column( db.String( 128 ) )
    
    def placeholder(self, eng):
        placeholders = {
            'school' : u'МБОУ СОШ "Лицей № 5"',
            'school_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56'
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None,
            'school' : u'Школа по аттестату',
            'school_address' : u'Адрес местонахождения'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'school' : self.school,
            'school_address' : self.school_address
        }
        return item2obj[item];

class Spec_middle_education( db.Model ):
    __tablename__ = 'spec_middle_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    institution = db.Column( db.String( 128 ) )
    institution_address = db.Column( db.String( 128 ) )
    speciality = db.Column( db.String( 128 ) )
    
    def placeholder(self, eng):
        placeholders = {
            'institution' : u'ПТУ № 43',
            'institution_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56',
            'speciality' : u'Сварщик'
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None,
            'institution' : u'Учебное заведение',
            'institution_address' : u'Адрес местонахождения',
            'speciality' : u'Специальность по диплому'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'institution' : self.institution,
            'institution_address' : self.institution_address,
            'speciality' : self.speciality
        }
        return item2obj[item];

class High_education(db.Model):
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
            'quality' : 'Бакалавр'
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None,
            'institution' : u'ВУЗ',
            'budgetary' : u'Бюджет',
            'full_faculty_name' : u'Факультет (полное название)',
            'short_faculty_name' : u'Факультет (сокращенное название)',
            'spec_diploma' : u'Специальность по диплому',
            'study_group_2' : u'Учебная группа 2 курс',
            'study_group_3' : u'Учебная группа 3 курс',
            'study_group_4' : u'Учебная группа 4 курс',
            'form_study' : u'Форма обучения',
            'quality' : 'Квалификация'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'institution' : self.institution,
            'budgetary' : self.budgetary,
            'full_faculty_name' : self.full_faculty_name,
            'short_faculty_name' : self.short_faculty_name,
            'spec_diploma' : self.spec_diploma,
            'study_group_2' : self.study_group_2,
            'study_group_3' : self.study_group_3,
            'study_group_4' : self.study_group_4,
            'form_study' : self.form_study,
            'quality' : self.quality
        }
        return item2obj[item];

class Military_education( db.Model ):
    __tablename__ = 'military_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    platoon_1 = db.Column( db.String( 10 ) )
    platoon_2 = db.Column( db.String( 10 ) )
    
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
            'platoon_1' : u'Взвод 1 года обучения',
            'platoon_2' : u'Взвод 2 года обучения',
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'platoon_1' : self.platoon_1,
            'platoon_2' : self.platoon_2,
        }
        return item2obj[item];

class Languages( db.Model ):
    __tablename__ = 'languages'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    language = db.Column( db.String( 32 ) )
    quality = db.Column( db.String( 32 ) )
    certificates = db.Column( db.String( 256 ) )
    
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
            'language' : u'Язык',
            'quality' : u'Степень владения',
            'certificates' : u'Сертификаты'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'language' : self.language,
            'quality' : self.quality,
            'certificates' : self.certificates
        }
        return item2obj[item];

class Mothers_fathers( db.Model ):
    __tablename__ = 'mothers_fathers'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    status = db.Column( db.String( 4 ) ) # мать, отец
    last_name = db.Column( db.String( 20 ) )
    first_name = db.Column( db.String( 20 ) )
    middle_name = db.Column( db.String( 20 ) )
    birth_date = db.Column( db.Date )
    birth_place = db.Column( db.String( 64 ) )
    mobile_phone_1 = db.Column( db.String( 11 ) )
    mobile_phone_2 = db.Column( db.String( 11 ) )
    home_phone = db.Column( db.String( 11 ) )
    job_place = db.Column( db.String( 128 ) )
    job_post = db.Column( db.String( 64 ) )
    fact_index = db.Column( db.String( 9 ) )
    fact_address = db.Column( db.String( 256 ) )
    
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
            'fact_address' : u'гор. Нижневартовск, ул. Пушкина, д. 56'
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None,
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
            'fact_address' : u'Адрес фактического проживания'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'status' : self.status,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'birth_date': self.birth_date,
            'birth_place': self.birth_place,
            'mobile_phone_1' : self.mobile_phone_1,
            'mobile_phone_2' : self.mobile_phone_2,
            'home_phone' : self.home_phone,
            'job_place' : self.job_place,
            'job_post' : self.job_post,
            'fact_index' : self.fact_index,
            'fact_address' : self.fact_address
        }
        return item2obj[item];

class Brothers_sisters_children( db.Model ):
    __tablename__ = 'brothers_sisters_children'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    status = db.Column( db.String( 6 ) ) # брат, сестра, сын, дочь
    last_name = db.Column( db.String( 20 ) )
    first_name = db.Column( db.String( 20 ) )
    middle_name = db.Column( db.String( 20 ) )
    birth_date = db.Column( db.Date )
    birth_place = db.Column( db.String( 64 ) )
    
    def placeholder(self, eng):
        placeholders = {
            'status' : u'брат',
            'last_name': u'Иванов',
            'first_name': u'Иван',
            'middle_name': u'Иванович',
            'birth_date': u'yyyy-mm-dd',
            'birth_place': u'гор. Нижние Пупки',
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None,
            'status' : u'Статус',
            'last_name': u'Фамилия',
            'first_name': u'Имя',
            'middle_name': u'Отчество',
            'birth_date': u'Дата рождения',
            'birth_place': u'Место рождения',
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'status' : self.status,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'birth_date': self.birth_date,
            'birth_place': self.birth_place,
        }
        return item2obj[item];

class Married_certificates( db.Model ):
    __tablename__ = 'married_certificates'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 20 ) )
    number = db.Column( db.String( 20 ) )
    issuer = db.Column( db.String( 128 ) )
    date_issue = db.Column( db.Date )
    last_name = db.Column( db.String( 20 ) )
    first_name = db.Column( db.String( 20 ) )
    middle_name = db.Column( db.String( 20 ) )
    birth_date = db.Column( db.Date )
    birth_place = db.Column( db.String( 64 ) )
    mobile_phone_1 = db.Column( db.String( 11 ) )
    mobile_phone_2 = db.Column( db.String( 11 ) )
    home_phone = db.Column( db.String( 11 ) )
    job_place = db.Column( db.String( 128 ) )
    job_post = db.Column( db.String( 64 ) )
    fact_index = db.Column( db.String( 9 ) )
    fact_address = db.Column( db.String( 256 ) )
    
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
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'serial' : self.serial,
            'number' : self.number,
            'issuer' : self.issuer,
            'date_issue' : self.date_issue,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'birth_date': self.birth_date,
            'birth_place': self.birth_place,
            'mobile_phone_1' : self.mobile_phone_1,
            'mobile_phone_2' : self.mobile_phone_2,
            'home_phone' : self.home_phone,
            'job_place' : self.job_place,
            'job_post' : self.job_post,
            'fact_index' : self.fact_index,
            'fact_address' : self.fact_address
        }
        return item2obj[item];

class Personal_data( db.Model ):
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
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]
    
    def get_russian_name(self, eng):
        en2ru = {
            'id': None,
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
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])
    
    def __getitem__(self,item):
        item2obj = {
            'id': self.id,
            'blood_group_resus' : self.blood_group_resus,
            'shoes_size' : self.shoes_size,
            'uniform_size' : self.uniform_size,
            'head_size' : self.head_size,
            'growth': self.growth,
            'protivogaz_size': self.protivogaz_size,
            'OZK_size': self.OZK_size,
            'government_prize': self.government_prize,
            'injuries' : self.injuries,
            'criminals' : self.criminals,
            'civil_specialization' : self.civil_specialization,
            'hobbies' : self.hobbies,
            'sports' : self.sports,
        }
        return item2obj[item];