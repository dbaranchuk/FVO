#-.- coding: utf-8 -.-
from app import app, db
from flask import render_template, request, flash, redirect, url_for, abort
from flask.ext.login import login_required, login_user, current_user, logout_user
from app.models import User, VUS, Document, Comments, Student_info, Basic_information 
from app.models import Certificates_change_name, Communications, Passports,International_passports
from app.models import Registration_certificates, Middle_education, Spec_middle_education 
from app.models import High_education, Military_education, Languages, Mothers_fathers 
from app.models import Brothers_sisters_children, Married_certificates, Personal_data
from werkzeug.security import check_password_hash
from easy import *
import json
import sys
from hidden import user_role
from app.models.easy import get_fields, get_tables, get_class_by_tablename

@app.route('/')
@app.route('/index')
@app.route('/ready')
@login_required
def ready():
    if user_role() < 1:
        return redirect(url_for('profile'))

    users = User.query.filter_by(role = 0, active = False)
    documents = Document.query.all()

    userInfo = []
    for user in users:
        userInfo.append({
            'id' : user.id,
            'lastName' : user.students_info.basic_information.last_name,
            'firstName' : user.students_info.basic_information.first_name,
            'middleName' : user.students_info.basic_information.middle_name,
            'year' : user.login[-4:]
        })

    docs = []
    for document in documents:
        docs.append({
            'id' : document.id,
            'name' : document.name
        })

    return render_template('ready.html', title=u'Готовые', tab_active=1, users=userInfo, 
        docs=docs)

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

@app.route('/search')
@login_required
def search():
    if user_role() < 1:
        abort(404)

    vuses = VUS.query.all()
    users = User.query.filter_by(role=0)

    return render_template('search.html', title=u'Поиск', tab_active=5, vuses=vuses, users=users)


class InputValue:
    def __init__(self, eng, rus, inp_type, placeholder, value='', comment=''):
        self.eng = eng
        self.rus = rus
        self.inp_type = inp_type
        self.placeholder = placeholder
        self.value = value
        self.comment = comment
        self.valid = ( self.eng is not None and self.rus is not None )

def fill_values(fields, user_info):
    for field in fields:
        if( user_info[field.eng] is not None):
            field.value = user_info[field.eng]

def get_sections_data_by_id(user_id):
    fixed_sections = {}
    not_fixed_sections = {}
    tables = get_tables()
    section_number = 0
    for table in tables:
        fields_table = get_fields( table )
        s = get_class_by_tablename( table )
        if not s:
            continue
        s = s() 
        fields_table = [InputValue(x[0], s.get_russian_name(x[0]), x[1], 
            s.placeholder(x[0])) for x in fields_table]
        fields_table = filter(lambda x: x.valid, fields_table)
        section_info = { 
                         'fields': fields_table, 'is_fixed': s.is_fixed(), 'table_name':table, 
                         'section_name': s.get_section_name(), 'section_number': section_number 
                       }
        if s.is_fixed():
            fixed_sections.update({ table : section_info })
        else:
            not_fixed_sections.update({ table : section_info })
        section_number += 1

    student_info = User.query.get( user_id ).students_info

    if student_info==None:
        return False

    for table in fixed_sections:
        fields_table = get_fields( table )
        s = get_class_by_tablename( table )
        if not s:
            continue
        user_info = s.query.filter_by( student_info_id=student_info.id ).first()
        if user_info is not None:
            fill_values(fixed_sections[table]['fields'], user_info) 

    for table in not_fixed_sections:
        fields_table = get_fields( table )
        s = get_class_by_tablename( table )
        if not s:
            continue
        user_infos = s.query.filter_by( student_info_id=student_info.id ).all()
        if user_infos is not None:
            not_fixed_sections[table]['filled_fields'] = [not_fixed_sections[table]['fields'] for _ in range(len(user_infos))]
            for i in range(len(user_infos)):
                fill_values(not_fixed_sections[table]['filled_fields'][i], user_infos[i])

    sections_arr = [fixed_sections[t] if t in fixed_sections else not_fixed_sections[t] for t in get_tables()]
    return sections_arr

@app.route('/profile')
@login_required
def profile():
    if user_role() > 0:
        return redirect('ready')
    vuses = {}
    comment = ''
    approved = 0
    curr_vus = ''

    sections_arr = get_sections_data_by_id(current_user.id)
    if not sections_arr:
        comment = u'ОБРАТИТЕСЬ К АДМИНИСТРАТОРУ'
        return render_template('user.html', title=u'Данные', fixed_sections=fixed_sections, not_fixed_sections=not_fixed_sections, 
            vuses=vuses, comment=comment, approved=approved, curr_vus=curr_vus, navprivate=True)

    vuses = VUS.query.all()
    comment = u""
    if(Comments.query.get(current_user.id)):
        comment = Comments.query.get(current_user.id).comment
    approved = User.query.get(current_user.id).active
    curr_vus = VUS.query.get(User.query.get(current_user.id).vus_id)
    return render_template('user.html', title=u'Данные', sections=sections_arr, 
        vuses=vuses, comment=comment, approved=approved, curr_vus=curr_vus, user_id=current_user.id, navprivate=True)






