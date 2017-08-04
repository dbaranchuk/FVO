#-.- coding: utf-8 -.-
from app import app, db
from flask import render_template, request, flash, redirect, url_for, abort
from flask.ext.login import login_required, login_user, current_user, logout_user
from app.models import User, VUS, Document, Student_info, Comments
from werkzeug.security import check_password_hash
from easy import *
import json
from hidden import user_role
from app.models.easy import get_fields, get_tables

@app.route('/')
@app.route('/index')
@app.route('/ready')
@login_required
def ready():
    if user_role() < 1:
        return redirect(url_for('profile'))

    users = User.query.filter_by(role = 0)
    docs = Document.query.all()

    user_ids = []
    for user in users:
        user_ids.append(user.id);
    
    students_info = {};
    for id in user_ids:
        students_info[id] = Student_info.query.get(id)    

    return render_template('ready.html', title=u'Готовые', tab_active=1, users = users, 
        docs = docs, students_info =students_info)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        role = user_role()
        if role < 0:
            return render_template('login.html', navprivate=True, title=u'Вход')
        elif role == 0:
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('ready'))

    data = json.loads(request.data)
    login = data['login']
    password = data['password']
    registered_user = User.query.filter_by(login=login).first()

    if registered_user is None or not check_password_hash(registered_user.password, password):
        return gen_error(u'Неправильная пара ЛОГИН-ПАРОЛЬ')
    login_user(registered_user)
    return gen_success()

@app.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/inprocess')
@login_required
def inprocess():
    if user_role() < 1:
        abort(404)
    users = User.query.filter_by(role = 0, active = True)
    ids = []
    for user in users:
        ids.append(user.vus_id)
    vuses = {};
    for id in ids:
        vuses[id] = VUS.query.get(id)

    user_ids = []
    for user in users:
        user_ids.append(user.id);
    
    students_info = {};
    for id in user_ids:
        students_info[id] = Student_info.query.get(id)  

    relatives = {};
    for id in students_info:
        relatives[id] = Family_member_info.query.filter_by(student_info_id=id)  

    return render_template('inprocess.html', title=u'В процессе', tab_active=2, users = users, 
        vuses = vuses, students_info =students_info, relatives = relatives)


@app.route('/inprocess/<user_id>')
@login_required
def to_page_approve_user(user_id):
    if user_role() < 1:
        abort(404)
    s = Student_info()
    fields = get_fields('student_info')
    fields = [InputValue(x[0], s.get_russian_name(x[0]), x[1], 
        s.placeholder(x[0])) for x in fields]
    fields = filter(lambda x: x.valid is not None, fields)

    user_info = Student_info.query.get(user_id)
    if user_info is not None:
        fill_values(fields, user_info)

    relatives = Family_member_info.query.filter_by(student_info_id = user_id)
    vuses = VUS.query.all()
    return render_template('user-admin.html', title=u'Одобрение аккаунта', 
        fields = fields, vuses = vuses, relatives = relatives, user_id = user_id,
         navprivate=True)

'''
@app.route('/approve_user/<user_id>')
@login_required
def approve_user(user_id):
    print(user_id);
    if user_role() < 1:
        abort(404)
    user = User.query.get(user_id)
    user.active = False;
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('inprocess'))
'''

@app.route('/send_comments')
@login_required
def send_comments(user_id):
    if user_role() < 1:
        abort(404)
    return redirect(url_for('inprocess'))

@app.route('/documents')
@login_required
def documents():
    if user_role() < 1:
        abort(404)
    vuses = VUS.query.all()
    docs = Document.query.all()
    return render_template('documents.html', title=u'Документы', tab_active=3, vuses=vuses, 
        docs=docs)


@app.route('/account_creator')
@login_required
def account_creator():
    if user_role() < 1:
        abort(404)
    vuses = VUS.query.all()

    return render_template('account_creator.html', title=u'Создание аккаунтов', tab_active=4, vuses=vuses)


class InputValue:
    def __init__(self, eng, rus, inp_type, placeholder, value='', comment=''):
        self.eng = eng
        self.rus = rus
        self.inp_type = inp_type
        self.placeholder = placeholder
        self.value = value
        self.comment = comment
        self.valid = self.eng is not None

def fill_values(fields, user_info):
    for field in fields:
        field.value = user_info[field.eng];

@app.route('/profile')
@login_required
def profile():
    if user_role() > 0:
        return redirect('ready')
    fields = {}
    vuses = {}
    comment = ''
    approved = 0
    curr_vus = ''
    tables = get_tables()
    for table in tables:
        if( table != 'student_info' ):
            print table
            #fields_table = get_fields( table )
            #fields_table = [InputValue(x[0], s.get_russian_name(x[0]), x[1], 
            #    s.placeholder(x[0])) for x in fields_table]
            #fields = filter(lambda x: x.valid is not None, fields)
            #fields.update( { table : get } )
    #fields = get_fields('student_info')
    #fields = [InputValue(x[0], s.get_russian_name(x[0]), x[1], 
    #    s.placeholder(x[0])) for x in fields]
    #fields = filter(lambda x: x.valid is not None, fields)

    #user_info = Student_info.query.get(current_user.id)
    #if user_info is not None:
    #    fill_values(fields, user_info)

    #vuses = VUS.query.all()
    #comment = ""
    #if(Comments.query.get(current_user.id)):
    #    comment = Comments.query.get(current_user.id).comment
    #approved = User.query.get(current_user.id).active

    #curr_vus = VUS.query.get(User.query.get(current_user.id).vus_id)

    return render_template('user.html', title=u'Данные', fields = fields, vuses = vuses, 
        comment = comment, approved = approved, curr_vus = curr_vus,  navprivate=True)





