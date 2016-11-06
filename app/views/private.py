#-.- coding: utf-8 -.-
from app import app, db
from flask.ext.login import current_user
from app.models import User, VUS, Document, Student_info
from werkzeug.security import generate_password_hash
from flask import request
import datetime
import json
from easy import *
from app.config import USER_PATH
import os

def create_account(login, password):
    hash = generate_password_hash(password)
    new_user = User(login = login, password = hash)
    db.session.add(new_user)
    db.session.commit()


@app.route('/make_account', methods=['POST'])
def make_account():
    data = json.loads(request.data)
    if 'login' not in data or 'password' not in data:
        return gen_error('Wrong data sent to server (must be [login, password]).')
    create_account(data['login'], data['password'])
    return gen_success()


@app.route('/add_document', methods=['POST'])
def add_document():
    if 'file' not in request.files:
        return gen_error('No file sent')
    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '' or not file:
        return gen_error('No file selected')

    if 'name' not in request.form:
        return gen_error('No name document could not be created')
    if 'vus' not in request.form:
        return gen_error('No vus document could not be created')

    vus = map(int, request.form['vus'].split())
    vus = VUS.query.filter_by(number=vus[0], code=vus[1]).first()
    if vus is None:
        return gen_error('Such vus not yet exists in this system')

    docs = os.listdir(os.path.join(USER_PATH, 'documents'))
    filename = file.filename
    if filename in docs:
        i = 1
        while filename + str(i) in docs:
            i += 1
        filename += str(i)

    file.save(os.path.join(USER_PATH, 'documents', filename))
    d = Document(name=request.form['name'], vus_id=vus.id, filename=filename)
    db.session.add(d)
    db.session.commit()

    return gen_success(filename=filename, message='Success!')

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.form;
    
    si = Student_info.query.get(current_user.id)

    if(si):
        birth_date              = data["birth_date"].split("-")
        if(birth_date):
            birth_date[0]           = int(unicode(birth_date[0]))
            birth_date[1]           = int(unicode(birth_date[1]))
            birth_date[2]           = int(unicode(birth_date[2]))
            si.birth_date           = datetime.date(*birth_date)

        si.last_name            = unicode(data["last_name"])
        si.first_name           = unicode(data["first_name"])
        si.middle_name          = unicode(data["middle_name"])
        si.nationality          = unicode(data["nationality"])
        si.birth_place          = unicode(data["birth_place"])
        si.education_middle     = unicode(data["education_middle"])
        si.education_high       = unicode(data["education_high"])
        si.civil_profession     = unicode(data["civil_profession"])
        si.family_status        = unicode(data["family_status"])
        si.address_usual        = unicode(data["address_usual"])
        si.address_registration = unicode(data["address_registration"])
        if(unicode(data["height"])):
            si.height               = int(unicode(data["height"]))
        if(unicode(data["head_size"])):
            si.head_size            = int(unicode(data["head_size"]))
        if(unicode(data["uniform_size"])):
            si.uniform_size         = int(unicode(data["uniform_size"]))
        if(unicode(data["shoes_size"])):
            si.shoes_size           = int(unicode(data["shoes_size"]))
        
        si.state_award          = unicode(data["state_award"])
        si.email                = unicode(data["email"])
        si.mobile_phone         = unicode(data["mobile_phone"])
        si.home_phone           = unicode(data["home_phone"])
        si.study_status         = unicode(data["study_status"])
    else:
        birth_date      = data["birth_date"].split("-")
        height          = None;
        head_size       = None;
        uniform_size    = None;
        shoes_size      = None;
        if(birth_date):
            birth_date[0] = int(unicode(birth_date[0]))
            birth_date[1] = int(unicode(birth_date[1]))
            birth_date[2] = int(unicode(birth_date[2]))

        if(unicode(data["height"])):
            height          = int(unicode(data["height"]))
        if(unicode(data["head_size"])):
            head_size       = int(unicode(data["head_size"]))
        if(unicode(data["uniform_size"])):
            uniform_size    = int(unicode(data["uniform_size"]))
        if(unicode(data["shoes_size"])):
            shoes_size      = int(unicode(data["shoes_size"]))

        si = Student_info(
                id                   = current_user.id,
                birth_date           = datetime.date(*birth_date) if birth_date else None,
                last_name            = unicode(data["last_name"]),
                first_name           = unicode(data["first_name"]),
                middle_name          = unicode(data["middle_name"]),
                nationality          = unicode(data["nationality"]),
                birth_place          = unicode(data["birth_place"]),
                education_middle     = unicode(data["education_middle"]),
                education_high       = unicode(data["education_high"]),
                civil_profession     = unicode(data["civil_profession"]),
                family_status        = unicode(data["family_status"]),
                address_usual        = unicode(data["address_usual"]),
                address_registration = unicode(data["address_registration"]),

                height               = height,
                head_size            = head_size,
                uniform_size         = uniform_size,
                shoes_size           = shoes_size,
                
                state_award          = unicode(data["state_award"]),
                email                = unicode(data["email"]),
                mobile_phone         = unicode(data["mobile_phone"]),
                home_phone           = unicode(data["home_phone"]),
                study_status         = unicode(data["study_status"])
        )
        db.session.add(si)
    
    user = User.query.get(current_user.id)
    spec = unicode(data["vus"]).split(' ');
    if(spec):
        spec[0] = int(spec[0]);
        spec[1] = int(spec[1]);
        vus_id = VUS.query.filter_by(number = spec[0], code = spec[1]).first().id
        if(vus_id):
            user.vus_id = vus_id
    db.session.commit()
    return gen_success()