#-.- coding: utf-8 -.-
from app import app, db
from flask.ext.login import current_user
from docx import Document as Doc
from openpyxl import load_workbook
from app.models import User, VUS, Document, Student_info, Basic_information, Comments
from werkzeug.security import generate_password_hash
from flask import request, send_from_directory
import datetime
import json
from easy import *
from app.models.easy import *
from app.config import USER_PATH
import os
import random, string
from keywords import *
from transliteration import *
from zipfile import ZipFile, ZIP_DEFLATED
import sys

def create_account(login, password, userData):
    hash = generate_password_hash(password)

    new_user = User(login = login, password = hash)
    info = Student_info()
    basicInfo = Basic_information(last_name = userData['lastName'], first_name = userData['firstName'], middle_name = userData['middleName'])

    new_user.students_info = info
    new_user.VUS = userData['vus']
    new_user.basic_information = basicInfo

    info.table_basic_information = CHANGING

    print >> sys.stderr, new_user.VUS, new_user.VUS.to_string()

    db.session.add(new_user)
    db.session.add(info)
    db.session.add(basicInfo)
    db.session.commit()

@app.route('/approve_user', methods=['POST'])
def approve_user():
    data = request.form
    user_id = data['id']
    user = User.query.get(user_id)
    user.active = False;
    db.session.add(user)
    db.session.commit()
    return gen_success()

@app.route('/comment_user', methods=['POST'])
def comment_user():
    data = request.form
    user_id = data['id'];
    comment = data['comment']
    comment_user = Comments.query.get(user_id);
    if(comment_user):
        comment_user.comment = unicode(comment);
    else:
        comment_user = Comments(
            id = user_id,
            comment = unicode(comment)
        )
    db.session.add(comment_user)
    db.session.commit()
    return gen_success()

@app.route('/make_account', methods=['POST'])
def make_account():
    data = json.loads(request.data)
    if 'login' not in data or 'password' not in data:
        return gen_error('Wrong data sent to server (must be [login, password]).')
    create_account(data['login'], data['password'])
    return gen_success()


@app.route('/create_accounts', methods=['POST'])
def create_accounts():
    if 'file' not in request.files:
        return gen_error('Файл не выбран')
    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '' or not file:
        return gen_error(u'Файл не выбран')
    if file.filename[-4:] != 'xlsx':
        return gen_error(u'Файл должен быть формата .xlsx')

    if 'vus' not in request.form:
        return gen_error('Выберите ВУС')
    if 'completionYear' not in request.form:
        return gen_error('Введите год поступления')

    completionYear = request.form['completionYear']
    if completionYear == '':
        return gen_error('Введите год поступления')

    vus = map(int, request.form['vus'].split())
    vus = VUS.query.filter_by(number=vus[0], code=vus[1]).first()
    if vus is None:
        return gen_error('Such vus not yet exists in this system')

    wb = load_workbook(file)
    active = wb.active
    userNames = User.query.with_entities(User.login)

    for idx, row in enumerate(active.rows, start = 1):
        login = ''

        #фамилия
        for char in row[0].value:
            login += vocabulary[char.lower()]
        login += u'.'

        #инициалы имени и отчества
        firstNameShort = row[1].value[0].lower()
        middleNameShort = row[2].value[0].lower()
        login += vocabulary[firstNameShort] + u'.'
        login += vocabulary[middleNameShort] + u'.'
        
        login += completionYear
        password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        #print >> sys.stderr, login, password

        for name in userNames:
            if login == name.login:
                return gen_error(u'В системе уже существует аккаунт: ' + login)

        info = {
            'lastName': row[0].value,
            'firstName': row[1].value,
            'middleName': row[2].value,
            'vus': vus
        }

        create_account(login, password, info)

        active.cell(row = idx, column = 4, value = login)
        active.cell(row = idx, column = 5, value = password)
        #print >> sys.stderr, password

    path = os.path.join(USER_PATH, 'logins.xlsx')
    wb.save(path)

    return gen_success(url = '/static/user_data/logins.xlsx')


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

@app.route('/delete_document', methods=['POST'])
def delete_document():
    data = json.loads(request.data)
    docId = data['docId']

    document = Document.query.filter_by(id = docId).first()
    filePath = os.path.join(USER_PATH, 'documents', document.filename)


    if document is None:
        return gen_error('No document with such id')

    #print >> sys.stderr, document.name, filePath

    os.remove(filePath)

    Document.query.filter_by(id = docId).delete()
    db.session.commit()

    return gen_success(message='Success!')



@app.route('/generate_documents', methods=['POST'])
def generate_documents():
    data = json.loads(request.data)
    userIds = data['users']
    documentIdxs = data['documents']
    
    documents = Document.query.all()
    users = User.query.filter_by(role = 0)

    #user_ids = []
    #for user in users:
    #    user_ids.append(user.id);
    
    students_info = {};
    for id in userIds:
        students_info[id] = Student_info.query.get(id)

    for doc_index, document in enumerate(documents, start=0):
        if doc_index in documentIdxs:
            docPath = os.path.join(USER_PATH, 'documents', document.filename)

            for usr_index, user in enumerate(users, start=0):
                if user.id in userIds:
                    doc = Doc(docPath)
                    family_info = Family_member_info.query.filter_by(student_info_id = user.id)
                    father = [member for member in family_info if unicode(member.membership_name) == unicode('Отец', 'utf-8') ]
                    mother = [member for member in family_info if unicode(member.membership_name) == unicode('Мать', 'utf-8') ]
                    wife = [member for member in family_info if unicode(member.membership_name) == unicode('Жена', 'utf-8') ]
                    brister = [member for member in family_info if unicode(member.membership_name) == unicode('Брат', 'utf-8') or unicode(member.membership_name) == unicode('Сестра', 'utf-8') ]
                    children = [member for member in family_info if unicode(member.membership_name) == unicode('Сын', 'utf-8') or unicode(member.membership_name) == unicode('Дочь', 'utf-8') ]

                    #print >> sys.stderr, father, mother, wife, brister, children
                    #for member in children:
                    #    print >> sys.stderr, member.last_name

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

                        """brister_count = 0
                        children_count = 0
                        for member in family_info:

                            #print >> sys.stderr, member.last_name

                            for item in keywords_familyinfo:
                                if ((unicode(member.membership_name) == unicode('Брат', 'utf-8')) and ('brister' in item['key'])
                                    or (unicode(member.membership_name) == unicode('Сестра', 'utf-8')) and ('brister' in item['key'])):
                                    brister_count += 1
                                if ((unicode(member.membership_name) == unicode('Сын', 'utf-8')) and ('child' in item['key'])
                                    or (unicode(member.membership_name) == unicode('Дочь', 'utf-8')) and ('child' in item['key'])):
                                    children_count += 1
                                if ((unicode(member.membership_name) == unicode('Отец', 'utf-8')) and ('father' in item['key'])
                                    or (unicode(member.membership_name) == unicode('Мать', 'utf-8')) and ('mother' in item['key'])
                                    or (unicode(member.membership_name) == unicode('Жена', 'utf-8')) and ('wife' in item['key'])
                                    or (unicode(member.membership_name) == unicode('Брат', 'utf-8')) and ('brister'+`brister_count` in item['key'])
                                    or (unicode(member.membership_name) == unicode('Сестра', 'utf-8')) and ('brister'+`brister_count` in item['key'])
                                    or (unicode(member.membership_name) == unicode('Сын', 'utf-8')) and ('child'+`children_count` in item['key'])
                                    or (unicode(member.membership_name) == unicode('Дочь', 'utf-8')) and ('child'+`children_count` in item['key'])):
                                    
                                    to_paste = unicode(member.__dict__[item['name']])
                                    text = p.text.replace(item['key'], to_paste)
                                    style = p.style
                                    p.text = text
                                    p.style = style  """

                        for item in keywords_familyinfo:
                            if item['key'] in p.text:
                                if 'father' in item['key']:
                                    for member in father:
                                        to_paste = unicode(member.__dict__[item['name']])
                                        text = p.text.replace(item['key'], to_paste)
                                        style = p.style
                                        p.text = text
                                        p.style = style
                                        break
                                if 'mother' in item['key']:
                                    for member in mother:
                                        to_paste = unicode(member.__dict__[item['name']])
                                        text = p.text.replace(item['key'], to_paste)
                                        style = p.style
                                        p.text = text
                                        p.style = style
                                        break
                                if 'wife' in item['key']:
                                    for member in wife:
                                        to_paste = unicode(member.__dict__[item['name']])
                                        text = p.text.replace(item['key'], to_paste)
                                        style = p.style
                                        p.text = text
                                        p.style = style
                                        break
                                if 'brister' in item['key']:
                                    number = int(item['key'][8:9])   
                                    if number < len(brister):
                                        to_paste = unicode(brister[number].__dict__[item['name']])
                                        text = p.text.replace(item['key'], to_paste)
                                        style = p.style
                                        p.text = text
                                        p.style = style
                                    else:
                                        to_paste = ''
                                        text = p.text.replace(item['key'], to_paste)
                                        style = p.style
                                        p.text = text
                                        p.style = style
                                if 'child' in item['key']:
                                    number = int(item['key'][6:7])
                                    if number < len(children):
                                        to_paste = unicode(children[number].__dict__[item['name']])
                                        text = p.text.replace(item['key'], to_paste)
                                        style = p.style
                                        p.text = text
                                        p.style = style
                                    else:
                                        to_paste = ''
                                        text = p.text.replace(item['key'], to_paste)
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

                                    for item in keywords_familyinfo:
                                        if item['key'] in p.text:
                                            if 'father' in item['key']:
                                                for member in father:
                                                    to_paste = unicode(member.__dict__[item['name']])
                                                    text = p.text.replace(item['key'], to_paste)
                                                    style = p.style
                                                    p.text = text
                                                    p.style = style
                                                    break
                                            if 'mother' in item['key']:
                                                for member in mother:
                                                    to_paste = unicode(member.__dict__[item['name']])
                                                    text = p.text.replace(item['key'], to_paste)
                                                    style = p.style
                                                    p.text = text
                                                    p.style = style
                                                    break
                                            if 'wife' in item['key']:
                                                for member in wife:
                                                    to_paste = unicode(member.__dict__[item['name']])
                                                    text = p.text.replace(item['key'], to_paste)
                                                    style = p.style
                                                    p.text = text
                                                    p.style = style
                                                    break
                                            if 'brister' in item['key']:
                                                number = int(item['key'][8:9])   
                                                if number < len(brister):
                                                    to_paste = unicode(brister[number].__dict__[item['name']])
                                                    text = p.text.replace(item['key'], to_paste)
                                                    style = p.style
                                                    p.text = text
                                                    p.style = style
                                                else:
                                                    to_paste = ''
                                                    text = p.text.replace(item['key'], to_paste)
                                                    style = p.style
                                                    p.text = text
                                                    p.style = style
                                            if 'child' in item['key']:
                                                number = int(item['key'][6:7])
                                                if number < len(children):
                                                    to_paste = unicode(children[number].__dict__[item['name']])
                                                    text = p.text.replace(item['key'], to_paste)
                                                    style = p.style
                                                    p.text = text
                                                    p.style = style
                                                else:
                                                    to_paste = ''
                                                    text = p.text.replace(item['key'], to_paste)
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

    comment = Comments.query.get(current_user.id);
    if(comment):
        comment.comment = ""
        db.session.add(comment)



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
    user.active = True;
    spec = unicode(data["vus"]).split(' ');
    if(spec):
        spec[0] = int(spec[0]);
        spec[1] = int(spec[1]);
        vus_id = VUS.query.filter_by(number = spec[0], code = spec[1]).first().id
        if(vus_id):
            user.vus_id = vus_id
    db.session.add(user)


    count_relatives = int(unicode(data['count_relatives']));
    count_curr_rel = Family_member_info.query.count();
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
                    id = count_curr_rel,
                    student_info_id = current_user.id,
                    last_name = unicode(data['last-name-' + str(i)]),
                    first_name = unicode(data['first-name-' + str(i)]),
                    middle_name = unicode(data['middle-name-' + str(i)]),
                    mobile_phone = unicode(data['phones-' + str(i)]),
                    address_usual = unicode(data['address-usual-' + str(i)]),
                    address_registration = unicode(data['address-registration-' + str(i)]),
                    membership_name = unicode(data['who-' + str(i)])
                )
            count_curr_rel = count_curr_rel + 1
        db.session.add(member)
        
    db.session.commit()
    return gen_success()

### POSTs

def test_method(data):
    return gen_success(message = data['DATA'] + '_SERVER' )


@app.route('/post_query', methods=['POST'])
def post_query():
    data = request.form
    try:
        if 'do' in data and data['do'] in POST_METHODS:
            return POST_METHODS[data['do']](data)
        else:
            return gen_error(u'post method not defined!')
    except Exception:
        return gen_error(u'error in post method')


POST_METHODS = {
                'test_method': test_method,

                }


