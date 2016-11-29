#-.- coding: utf-8 -.-
from app import app, db
from flask.ext.login import current_user
from docx import Document as Doc
from app.models import User, VUS, Document, Student_info, Family_member_info
from werkzeug.security import generate_password_hash
from flask import request, send_from_directory
import datetime
import json
from easy import *
from app.config import USER_PATH
import os
from keywords import *
from zipfile import ZipFile, ZIP_DEFLATED

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

@app.route('/generate_documents', methods=['POST'])
def generate_documents():
    data = json.loads(request.data)
    userIdxs = data['users']
    documentIdxs = data['documents']
    
    documents = Document.query.all()
    users = User.query.filter_by(role = 0)

    user_ids = []
    for user in users:
        user_ids.append(user.id);
    
    students_info = {};
    for id in user_ids:
        students_info[id] = Student_info.query.get(id)

    for doc_index, document in enumerate(documents, start=0):
        if doc_index in documentIdxs:
            docPath = os.path.join(USER_PATH, 'documents', document.filename)

            for usr_index, user in enumerate(users, start=0):
                if usr_index in userIdxs:
                    doc = Doc(docPath)
                    
                    #цикл по тексту
                    for p in doc.paragraphs:
                        #по ключевым слровам
                        for item in keywords_usrinfo:
                            if item['key'] in p.text:
                                to_paste = unicode(students_info[user.id].__dict__[item['name']])
                                text = p.text.replace(item['key'], to_paste)
                                style = p.style
                                p.text = text
                                p.style = style
                        for item in keywords_vusinfo:
                            if item['key'] in p.text:
                                to_paste = unicode(user.vus.__dict__[item['name']])
                                text = p.text.replace(item['key'], to_paste)
                                style = p.style
                                p.text = text
                                p.style = style
                        if '&fio' in p.text:
                                to_paste = unicode(students_info[user.id].last_name + ' ' + students_info[user.id].first_name + ' ' + students_info[user.id].middle_name)
                                text = p.text.replace('&fio', to_paste)
                                style = p.style
                                p.text = text
                                p.style = style

                    #по таблицам
                    for table in doc.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                for p in cell.paragraphs:
                                    for item in keywords_usrinfo:
                                        if item['key'] in p.text:
                                            to_paste = unicode(students_info[user.id].__dict__[item['name']])
                                            text = p.text.replace(item['key'], to_paste)
                                            style = p.style
                                            p.text = text
                                            p.style = style
                                    for item in keywords_vusinfo:
                                        if item['key'] in p.text:
                                            to_paste = unicode(user.vus.__dict__[item['name']])
                                            text = p.text.replace(item['key'], to_paste)
                                            style = p.style
                                            p.text = text
                                            p.style = style
                                    if '&fio' in p.text:
                                            to_paste = unicode(students_info[user.id].last_name + ' ' + students_info[user.id].first_name + ' ' + students_info[user.id].middle_name)
                                            text = p.text.replace('&fio', to_paste)
                                            style = p.style
                                            p.text = text
                                            p.style = style

                    doc_name = os.path.join(USER_PATH, 'documents', 'temp', document.filename[:-5] + students_info[user.id].last_name + '.docx')
                    doc.save(doc_name)

    zippath = os.path.join(USER_PATH, 'Documents.zip')
    zipf = ZipFile(zippath, 'w', ZIP_DEFLATED)

    basedir = os.path.join(USER_PATH, 'documents', 'temp')
    for root, dirs, files in os.walk(basedir):
        for fn in files:
            absfn = os.path.join(root, fn)
            zfn = absfn[len(basedir)+len(os.sep):]
            zipf.write(absfn, zfn)
            os.remove(absfn)
    zipf.close()

    return gen_success(url = '/static/user_data/Documents.zip')
    #return send_from_directory(directory = USER_PATH, filename = 'Documents.zip')

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


    count_relatives = int(unicode(data['count_relatives']));

    for i in range(count_relatives):
        member = Family_member_info.query.filter_by(student_info_id = current_user.id, 
                                                    membership_name = unicode(data['who-' + str(i)])).first()
        if(member):
            member.last_name = unicode(data['last-name-' + str(i)])
            member.first_name = unicode(data['first-name-' + str(i)])
            member.middle_name = unicode(data['middle-name-' + str(i)])
            member.mobile_phone = unicode(data['phones-' + str(i)])
            member.address_usual = unicode(data['address-usual-' + str(i)])
            member.address_registration = unicode(data['address-registration-' + str(i)])
        else:
            member = Family_member_info(
                    id = Family_member_info.query.count(),
                    student_info_id = current_user.id,
                    last_name = unicode(data['last-name-' + str(i)]),
                    first_name = unicode(data['first-name-' + str(i)]),
                    middle_name = unicode(data['middle-name-' + str(i)]),
                    mobile_phone = unicode(data['phones-' + str(i)]),
                    address_usual = unicode(data['address-usual-' + str(i)]),
                    address_registration = unicode(data['address-registration-' + str(i)]),
                    membership_name = unicode(data['who-' + str(i)])
                )
        db.session.add(member)
        
    db.session.commit()
    return gen_success()
