#-.- coding: utf-8 -.-
from app import db
from app.models.easy import USER_STATES


class VUS(db.Model):
    __tablename__ = 'VUS'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    code = db.Column(db.Integer)
    name1 = db.Column(db.String(120))
    name2 = db.Column(db.String(120))

    users = db.relationship('User', backref = 'VUS', lazy = 'dynamic' )
    documents = db.relationship('Document', backref = 'VUS', lazy = 'dynamic' )

    def to_string(self):
        return '%03d %03d' % (self.number, self.code)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120), unique = False)
    role = db.Column(db.SmallInteger, default = USER_STATES['ROLE_USER'])
    active = db.Column(db.Boolean, default = True)
    vus_id = db.Column(db.Integer, db.ForeignKey('VUS.id'), default = -1)

    approved = db.Column(db.Boolean, default = False)

    students_info = db.relationship( 'Student_info', backref = 'user', uselist = False )

    def __repr__(self):
        return '<User %r, %r>' % (self.login, self.password)

class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    vus_id = db.Column(db.Integer, db.ForeignKey('VUS.id'), default = -1)
    filename = db.Column(db.String(120))
    

