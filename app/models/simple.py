from app import db

ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_SUPER_ADMIN = 2


class VUS(db.Model):
    __tablename__ = 'VUS'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    code = db.Column(db.Integer)
    name1 = db.Column(db.String(120))
    name2 = db.Column(db.String(120))

    users = db.relationship('User', backref = 'vus', lazy = 'dynamic')
    documents = db.relationship('Document', backref = 'vus', lazy = 'dynamic')

    def to_string(self):
        return '%03d %03d' % (self.number, self.code)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120), unique = False)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    active = db.Column(db.Boolean, default = True)
    vus_id = db.Column(db.Integer, db.ForeignKey('VUS.id'), default = -1)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r, %r>' % (self.login, self.password)



class Document(db.Model):
    __tablename__ = 'Document'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    vus_id = db.Column(db.Integer, db.ForeignKey('VUS.id'), default = -1)
    filename = db.Column(db.String(120))
    

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(8096))