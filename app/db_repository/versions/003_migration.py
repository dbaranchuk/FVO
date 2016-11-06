from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
student_info = Table('student_info', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('birth_date', Date),
    Column('last_name', String(length=20)),
    Column('first_name', String(length=20)),
    Column('middle_name', String(length=20)),
    Column('nationality', String(length=20)),
    Column('birth_place', String(length=64)),
    Column('education_middle', String(length=128)),
    Column('education_high', String(length=128)),
    Column('civil_profession', String(length=128)),
    Column('family_status', String(length=10)),
    Column('address_usual', String(length=128)),
    Column('address_registration', String(length=128)),
    Column('height', Integer),
    Column('head_size', Integer),
    Column('uniform_size', Integer),
    Column('shoes_size', Integer),
    Column('state_award', String(length=256)),
    Column('email', String(length=128)),
    Column('mobile_phone', String(length=30)),
    Column('home_phone', String(length=30)),
    Column('study_status', String(length=30)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['student_info'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['student_info'].drop()
