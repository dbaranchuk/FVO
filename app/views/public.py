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
import json
import sys
from hidden import user_role
from app.models.easy import *

@app.route('/')
@app.route('/index')
@app.route('/ready')
@login_required
def ready():
    if user_role() < 1:
        return redirect(url_for('profile'))

    users = User.query.filter_by(role = 0)
    docs = Document.query.all()

    user_ids = map(lambda user: user.id, users) 
    
    # CAN OPTIMIZE HERE: JOIN TABLES INSTEAD OF DOING SERIES OF QUERIES
    students_info = {}
    for id in user_ids:
        students_info[id] = Student_info.query.filter_by( user_id=id )    

    return render_template('ready.html', title=u'Готовые', tab_active=1, users=users, 
        docs=docs, students_info=students_info)

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

    sections_arr = get_sections_data_by_id(user_id)
    section_statuses = get_section_statuses(user_id)
    comment = u""

    status = u'Имеются непроверенные секции | Анкета одобрена | Анкета отклонена'

    return render_template('user-admin.html', title=u'Одобрение аккаунта', sections=sections_arr, table_states=TABLE_STATES,
         comment=comment, quiz_status=status, section_statuses=section_statuses, user_id=user_id, navprivate=True)

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

    def copy(self):
        return InputValue( 
                           eng=self.eng, rus=self.rus, inp_type=self.inp_type, 
                           placeholder=self.placeholder, value=self.value, comment=self.comment
                         )

def fill_section_values(fields, user_info):
    for field in fields:
        if user_info[field.eng] is not None:
            field.value = user_info[field.eng]

def get_sections_data_by_id(user_id):
    user_tables = get_user_tables()
    student_info = User.query.get( user_id ).students_info

    sections_arr = []
    for table in user_tables:
        fields_table = get_fields( table )
        s = get_class_by_tablename( table )()

        fields_table = [InputValue(x[0], s.get_russian_name(x[0]), x[1], 
            s.placeholder(x[0])) for x in fields_table]
        fields_table = filter(lambda x: x.valid, fields_table)

        section_info = { 
                         'fields': fields_table, 'is_fixed': s.is_fixed(), 'table_name':table, 
                         'section_name': s.get_section_name(), 'section_number': len(sections_arr) 
                       }
        if s.is_fixed():
            table_record = student_info[table]
            if table_record:
                fill_section_values(section_info['fields'], table_record) 
        else:
            table_records = student_info[table]
            if table_records is not None:
                section_info['filled_fields'] = []
                for i in range(len(table_records)):
                    element = [x.copy() for x in section_info['fields']]
                    fill_section_values(element, table_records[i])
                    section_info['filled_fields'].append(element)
        sections_arr.append(section_info)

    return sections_arr

def get_section_statuses(user_id):
    student_info = User.query.get( user_id ).students_info
    return dict(map(lambda s: (s[0][len('table_'):], student_info[s[0]]), get_fields('student_info')))

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
    section_statuses = get_section_statuses(current_user.id)
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
    return render_template('user.html', title=u'Данные', sections=sections_arr, table_states=TABLE_STATES,
        vuses=vuses, comment=comment, approved=approved, section_statuses=section_statuses,
        curr_vus=curr_vus, user_id=current_user.id, navprivate=True)

