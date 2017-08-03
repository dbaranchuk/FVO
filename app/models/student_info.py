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
            #'address_registration': u"100000 , г. Москва, ул. Пушкина, д. 1, корп. 1, кв. 1",
            #'address_usual': u'100000 , г. Москва, ул. Пушкина, д. 1, корп. 1, кв. 1',
            #'civil_profession': u'',
            #'education_high': u'МГУ им. Ломоносова',
            #'education_middle': u'МБОУ "ПТУ № 1"',
            #'head_size': u'56',
            #'height': u'176',
            #'home_phone': u'84950123456',
            #'metadata': None,
            #'mobile_phone': u'89260481011',
            #'query': None,
            #'query_class': None,
            #'shoes_size': u'52',
            #'state_award': u'не имею',
            #'study_status': u'очная',
            #'uniform_size': u'48',
            #'email': u'alexey.dukhovich@gmail.com' 
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
            #'address_registration': u'Адрес по прописке',
            #'address_usual': u'Фактический адрес',
            #'civil_profession': u'Гражданские специальности',
            #'education_high': u'Высшее образование',
            #'education_middle': u'Среднее образование',
            #'head_size': u'Размер головы',
            #'height': u'Рост',
            #'home_phone': u'Домашний телефон',
            #'metadata': None,
            #'mobile_phone': u'Мобильный телефон',
            #'query': None,
            #'query_class': None,
            #'shoes_size': u'Размер обуви',
            #'state_award': u'Государственные награды',
            #'study_status': u'Форма обучения',
            #'uniform_size': u'Размер обмундирования'
        }
        if eng in en2ru:
            return en2ru[eng]
        else:
            return unicode(eng[0].upper() + eng[1:])

    def __repr__(self):
        return '<Student %r>' % (self.first_name)

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
            #'address_registration': self.address_registration,
            #'address_usual': self.address_usual,
            #'birth_date': self.birth_date,
            #'birth_place': self.birth_place,
            #'civil_profession': self.civil_profession,
            #'education_high': self.education_high,
            #'education_middle': self.education_middle,
            #'head_size': self.head_size,
            #'height': self.height,
            #'home_phone': self.home_phone,
            #'mobile_phone': self.mobile_phone,
            #'shoes_size': self.shoes_size,
            #'state_award': self.state_award,
            #'study_status': self.study_status,
            #'uniform_size': self.uniform_size,
            #'email': self.email
        }
        return item2obj[item];


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

class Certificates_change_name(db.Model):
    __tablename__ = 'certificates_change_name'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey('student_info.id'))
    serial = db.Column( db.String( 5 ) )
    number = db.Column( db.String( 10 ) )
    issuer = db.Column( db.String( 256 ) )
    issue_date = db.Column( db.Date )
    changing = db.Column( db.String( 128 ) )

class Communications( db.Model ):
    __tablename__ = 'communications'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    mobile_phone_1 = db.Column( db.String( 11 ) )
    mobile_phone_2 = db.Column( db.String( 11 ) )
    home_phone = db.Column( db.String( 11 ) )
    email = db.Column( db.String( 64 ) )

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

class International_passports( db.Model ):
    __tablename__ = 'international_passports'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    serial = db.Column( db.String( 2 ) )
    number = db.Column( db.String( 7 ) )
    issuer = db.Column( db.String( 256 ) )
    issue_date = db.Column( db.Date )
    validity = db.Column( db.SmallInteger )

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

class Middle_education( db.Model ):
    __tablename__ = 'middle_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    school = db.Column( db.String( 128 ) )
    school_address = db.Column( db.String( 128 ) )

class Spec_middle_education( db.Model ):
    __tablename__ = 'spec_middle_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    institution = db.Column( db.String( 128 ) )
    institution_address = db.Column( db.String( 128 ) )
    speciality = db.Column( db.String( 128 ) )

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

class Military_education( db.Model ):
    __tablename__ = 'military_education'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    platoon_1 = db.Column( db.String( 10 ) )
    platoon_2 = db.Column( db.String( 10 ) )

class Languages( db.Model ):
    __tablename__ = 'languages'
    id = db.Column( db.Integer, primary_key = True )
    student_info_id = db.Column( db.Integer, db.ForeignKey( 'student_info.id' ) )
    language = db.Column( db.String( 32 ) )
    quality = db.Column( db.String( 32 ) )
    certificates = db.Column( db.String( 256 ) )

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