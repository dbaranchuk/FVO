#-.- coding: utf-8 -.-
from app import db


class Student_info(db.Model):
    __tablename__ = 'student_info'
    id = db.Column(db.Integer, primary_key = True)
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
    #education_middle = db.Column(db.String(128))
    #education_high = db.Column(db.String(128))
    #civil_profession = db.Column(db.String(128))
    #address_usual = db.Column(db.String(128))
    #address_registration = db.Column(db.String(128))
    #height = db.Column(db.Integer)
    #head_size = db.Column(db.Integer)
    #uniform_size = db.Column(db.Integer)
    #shoes_size = db.Column(db.Integer)
    #state_award = db.Column(db.String(256))
    #email = db.Column(db.String(128))
    #mobile_phone = db.Column(db.String(30))
    #home_phone = db.Column(db.String(30))
    #study_status = db.Column(db.String(30))

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


class Family_member_info(db.Model):
    __tablename__ = 'family_member_info'
    id = db.Column(db.Integer, primary_key = True)
    student_info_id = db.Column(db.Integer, db.ForeignKey('student_info.id'))
    membership_name = db.Column( db.String( 30 ) )
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    middle_name = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(64))
    mobile_phone_1 = db.Column( db.String( 11 ) )
    mobile_phone_2 = db.Column( db.String( 11 ) )
    home_phone = db.Column( db.String( 11 ) )
    job_place = db.Column( db.String( 128 ) )
    job_post  = db.Column( db.String( 64 ) )
    index_usual = db.Column( db.String( 10 ) )
    address_usual = db.Column( db.String( 256 ) )
