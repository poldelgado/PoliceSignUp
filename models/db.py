# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()


auth.settings.extra_fields['auth_user'] = [
    Field('first_name', 'string'),
    Field('last_name', 'string'),
    Field('ssn', 'integer', label=T('ssn')),
    Field('birth_date', 'date'),
    Field('marital_status', requires = IS_IN_SET([T('single'),T('married'),T('divorced'),T('widowed')],
    zero=T('Choose one'))),
    Field('career', requires = IS_IN_SET([T('First Year Cadet Candidate'),T('Penitentiary Service Candidate')],zero=T('Choose one'))),
    Field('phone', 'string'),
    Field('address', 'string'),
    Field('city', 'string'),
    Field('province', 'string'),
    Field('grade', 'string')
]


auth.settings.login_userfield = 'ssn'        #the loginfield will be ssn instead of username


# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=True, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False


# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


db.define_table('inscription',
                Field('user_id',db.auth_user),
                Field('created_on', 'datetime', default=request.now)
                )


db.define_table('height',
                Field('inscription_id', db.inscription),
                Field('height','double'),
                Field('available','boolean')
                )


db.define_table('intellectual_exam',
                Field('inscription_id', db.inscription),
                Field('spanish_language','double'),
                Field('history','double'),
                Field('geography','double'),
                Field('available','boolean', default=False),
                )


db.define_table('medical_exam',
                Field('inscription_id', db.inscription),
                Field('exam_exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False),
                )


db.define_table('physical_exam',
                Field('inscription_id', db.inscription),
                Field('abs_test','integer'),
                Field('arms','integer'),
                Field('aerobics','double'),
                Field('available','boolean', default=False)
                )


db.define_table('groupal_psychological_examination',
                Field('inscription_id', db.inscription),
                Field('exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False)
                )


db.define_table('psycological_interview',
                Field('inscription_id', db.inscription),
                Field('exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False)
                )


db.define_table('schedule',
                Field('height_schedule', 'text'),
                Field('intellectual_exam_schedule', 'text'),
                Field('medical_exam_schedule', 'text'),
                Field('physical_exam_schedule', 'text'),
                Field('intellectual_exam_schedule', 'text'),
                Field('groupal_psychological_examination_schedule', 'text'),
                Field('psycological_interview_schedule', 'text')
                )

db.auth_user.username.readable = False
db.auth_user.username.writable = False
