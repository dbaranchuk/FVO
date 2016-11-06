from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
family_member_info = Table('family_member_info', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('student_info_id', Integer),
    Column('last_name', String(length=20)),
    Column('first_name', String(length=20)),
    Column('middle_name', String(length=20)),
    Column('mobile_phone', String(length=30)),
    Column('address_usual', String(length=128)),
    Column('address_registration', String(length=128)),
    Column('membership_name', String(length=30)),
    Column('priority', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['family_member_info'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['family_member_info'].drop()
