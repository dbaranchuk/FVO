#-.- coding: utf-8 -.-
from app import db


class Student_info(db.Model):
    __tablename__ = 'student_info'
    id = db.Column(db.Integer, primary_key = True)
    birth_date = db.Column(db.Date)
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    middle_name = db.Column(db.String(20))
    nationality = db.Column(db.String(20))
    birth_place = db.Column(db.String(64))
    education_middle = db.Column(db.String(128))
    education_high = db.Column(db.String(128))
    civil_profession = db.Column(db.String(128))
    family_status = db.Column(db.String(10))
    address_usual = db.Column(db.String(128))
    address_registration = db.Column(db.String(128))
    height = db.Column(db.Integer)
    head_size = db.Column(db.Integer)
    uniform_size = db.Column(db.Integer)
    shoes_size = db.Column(db.Integer)
    state_award = db.Column(db.String(256))
    email = db.Column(db.String(128))
    mobile_phone = db.Column(db.String(30))
    home_phone = db.Column(db.String(30))
    study_status = db.Column(db.String(30))

    def placeholder(self, eng):
        placeholders = {
            'first_name': u'Иван',
            'last_name': u'Иванов',
            'middle_name': u'Иванович',
            'address_registration': u"100000 , г. Москва, ул. Пушкина, д. 1, корп. 1, кв. 1",
            'address_usual': u'100000 , г. Москва, ул. Пушкина, д. 1, корп. 1, кв. 1',
            'birth_date': u'yyyy-mm-dd',
            'birth_place': u'гор. Нижние Пупки',
            'civil_profession': u'',
            'education_high': u'МГУ им. Ломоносова',
            'education_middle': u'МБОУ "ПТУ № 1"',
            'family_status': u'женат/холост',
            'head_size': u'56',
            'height': u'176',
            'home_phone': u'84950123456',
            'metadata': None,
            'mobile_phone': u'89260481011',
            'nationality': u'русский',
            'query': None,
            'query_class': None,
            'shoes_size': u'52',
            'state_award': u'не имею',
            'study_status': u'очная',
            'uniform_size': u'48',
            'email': u'alexey.dukhovich@gmail.com' 
        }
        if eng not in placeholders:
            return ''
        return placeholders[eng]

    def get_russian_name(self, eng):
        en2ru = {
            'id': None,
            'address_registration': u'Адрес по прописке',
            'address_usual': u'Фактический адрес',
            'birth_date': u'Дата рождения',
            'birth_place': u'Место рождения',
            'civil_profession': u'Гражданские специальности',
            'education_high': u'Высшее образование',
            'education_middle': u'Среднее образование',
            'family_status': u'Семейный статус',
            'first_name': u'Имя',
            'head_size': u'Размер головы',
            'height': u'Рост',
            'home_phone': u'Домашний телефон',
            'last_name': u'Фамилия',
            'metadata': None,
            'middle_name': u'Отчество',
            'mobile_phone': u'Мобильный телефон',
            'nationality': u'Национальность',
            'query': None,
            'query_class': None,
            'shoes_size': u'Размер обуви',
            'state_award': u'Государственные награды',
            'study_status': u'Форма обучения',
            'uniform_size': u'Размер обмундирования'
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
            'address_registration': self.address_registration,
            'address_usual': self.address_usual,
            'birth_date': self.birth_date,
            'birth_place': self.birth_place,
            'civil_profession': self.civil_profession,
            'education_high': self.education_high,
            'education_middle': self.education_middle,
            'family_status': self.family_status,
            'first_name': self.first_name,
            'head_size': self.head_size,
            'height': self.height,
            'home_phone': self.home_phone,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'mobile_phone': self.mobile_phone,
            'nationality': self.nationality,
            'shoes_size': self.shoes_size,
            'state_award': self.state_award,
            'study_status': self.study_status,
            'uniform_size': self.uniform_size,
            'email': self.email
        }
        return item2obj[item];


class Family_member_info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_info_id = db.Column(db.Integer, db.ForeignKey('student_info.id'))
    last_name = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    middle_name = db.Column(db.String(20))
    mobile_phone = db.Column(db.String(30))
    address_usual = db.Column(db.String(128))
    address_registration = db.Column(db.String(128))
    membership_name = db.Column(db.String(30))
    priority = db.Column(db.Integer)
