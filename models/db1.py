# -*- coding: utf-8 -*-

DEBUG = True

from gluon import current
import datetime

# track changes for modules
from gluon.custom_import import track_changes
track_changes(DEBUG)

# set utc as standard time for app
request.now = request.utcnow

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.14.1 or newer")

#request.requires_https()

# application configuration using private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload=DEBUG)
current.myconf = myconf
myconf_env = myconf.get('environment.type')
current.myconf_env = myconf_env

# set db connection
if not request.env.web2py_runtime_gae:
    # if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.get(myconf_env + 'db.uri'),
             pool_size=myconf.get(myconf_env + 'db.pool_size'),
             migrate_enabled=myconf.get(myconf_env + 'db.migrate'),
             check_reserved=['mysql', 'postgres'],  # ['all'])
             lazy_tables=True)
else:
    # connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    # store sessions and tickets there
    session.connect(request, response, db=db)
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

# choose a style for forms
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# static assets folder versioning
# response.static_version = '0.0.0'

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db, host_names=myconf.get(myconf_env + 'host.name'))
service = Service()
plugins = PluginManager()

# define custom auth fields (before creating auth tables)
auth.settings.extra_fields['auth_user'] = [
    Field(
        'bookmarks', length=4096,
        # filter_in = lambda bm_obj: repr(bm_obj),  # could be str()
        # filter_out = lambda bm_str: eval(bm_str) if bm_str else {},  # could be ast.literal_eval
        represent=(lambda v, r: BEAUTIFY(eval(v)) if v else None),
        readable=False, writable=False,
        default={}
    ),
    Field('birth_date', 'date', label=T('Birth Date')),
    Field('gender', label=T('Gender') , requires = IS_IN_SET([T('Male'),T('Female')],
    zero=T('Choose one'))),
    Field('marital_status', label=T('Marital Status') , requires = IS_IN_SET([T('single'),T('married'),T('divorced'),T('widowed')],
    zero=T('Choose one'))),
    Field('nationality', label=T('Nationality')),
    Field('career', label=T('Career')),
    Field('high_school', label=T('High School')),
    Field('tertiary_title', label=T('Tertiary Title')),
    Field('phone', 'string', label=T('Phone')),
    Field('mobile_phone', 'string', label=T('Mobile Phone')),
    Field('address', 'string', label=T('Address')),
    Field('city', 'string', label=T('City')),
    Field('province', 'string', label=T('Province')),
    Field('police_station', 'string', label=T('Police Station')),
]


# create all tables needed by auth
auth.define_tables(username=True, signature=True)

# add auth formatting, validation, and representation
db.auth_user._format = '%(last_name)s %(first_name)s (%(id)s)'  # defaults to '%(username)'

# configure email
mail = auth.settings.mailer
mail.settings.server = myconf.get(myconf_env + 'smtp.server')
mail.settings.sender = myconf.get(myconf_env + 'smtp.sender')
mail.settings.login = myconf.get(myconf_env + 'smtp.login')
mail.settings.tls = myconf.get(myconf_env + 'smtp.tls') or False
mail.settings.ssl = myconf.get(myconf_env + 'smtp.ssl') or False

# configure auth policy
auth.settings.actions_disabled.append('register')
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = False  # defaults to True
auth.settings.expiration = 60 * 60 * 24  # seconds
auth.settings.logout_next = URL('index')
db.auth_user.username.requires = IS_MATCH('^\d{8,8}',error_message=T('please insert only numbers, minimum 8 numbers'))
db.auth_user.email.requires = IS_EMAIL()
db.auth_user.province.requires = IS_IN_SET(['Buenos Aires', 'Catamarca', 'Chaco', 'Chubut', 'Ciudad Autonoma de Buenos Aires', 'Córdoba', 'Corrientes', 'Entre Ríos', 'Formosa', 'Jujuy', 'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquén', 'Río Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero', 'Tierra del Fuego', 'Tucumán'])
db.auth_user.career.requires = IS_IN_SET([T('Aspirante a Cadete de la Policía de Tucumán'),T('Aspirante a Cadete del Servicio Penitenciario de Tucumán')],zero=T('Choose one'))
db.auth_user.city.requires = IS_NOT_EMPTY(error_message=T("Please complete the city field"))
#db.auth_user.phone.requires = IS_NOT_EMPTY(error_message=T("Please complete the phone field"))
db.auth_user.nationality.requires = IS_NOT_EMPTY(error_message=T("Please complete this information"))
db.auth_user.mobile_phone.requires = IS_NOT_EMPTY(error_message=T("Please complete the mobile phone field"))
db.auth_user.address.requires = IS_NOT_EMPTY(error_message=T("Please complete the address field"))
#db.auth_user.birth_date.requires = IS_DATE_IN_RANGE(format=T('%Y-%m-%d'), minimum=datetime.date(1993,2,3), maximum=datetime.date(2000,2,2),error_message='Ud. debe tener 18 años cumplidos y menos de 24 años al 01/02/2018')
db.auth_user.high_school.requires = IS_NOT_EMPTY(error_message=T("Please complete the high school field"))
db.auth_user.police_station.requires = IS_IN_SET(['Comisaría 1era', 'Comisaría 2da', 'Comisaría 3ra', 'Comisaría 4ta', 'Comisaría 5ta', 'Comisaría 6ta','Comisaría 7ma',
                                                'Comisaría 8va', 'Comisaría 9na', 'Comisaría 10ma', 'Comisaría 11va', 'Comisaría 12va', 'Comisaría 13va', 'Comisaría 14va',
                                                'Acheral', 'Agua Dulce', 'Aguilares', 'Alberdi', 'Alderete', 'Alpachiri', 'Amaicha del Valle', 'Amberes', 'Arcadia', 'Ataona',
                                                 'Banda del Río Sali', 'Bella Vista', 'Burruyacú', 'Campo el Químil', 'Cápitan Caceres', 'Chicligasta', 'Chilcas', 'Choromoro',
                                                 'Chusca', 'Colalao Del Valle', 'Colombres', 'Concepción', 'Delfín Gallo', 'El Bracho', 'El Cadillal', 'El Cajón', 'El Chañar',
                                                 'El Colmenar', 'El Corte', 'El Manantial', 'El Menor', 'El Mojon', 'El Naranjo', 'El Polear', 'El Puestito', 'El Timbo', 'Escaba',
                                                 'Esquina', 'Estación Aráoz', 'Famailla', 'Garmendia', 'Graneros', 'Huasa Pampa Sud', 'Ingenio Leales', 'La Cocha', 'La Florida',
                                                 'La Fronterita', 'La Invernada', 'La Ramada', 'La Reducción', 'La Trinidad', 'Lamadrid', 'Las Cejas', 'Las Talitas',
                                                 'Lastenia', 'León Rouges', 'Lomas de Tafí', 'Los Aguirre', 'Los Bulacio', 'Los Gomez', 'Los Herrera', 'Los Medinas', 'Los Nogales', 'Los Pocitos',
                                                 'Los Puestos', 'Los Ralos', 'Los Sarmientos', 'Los Sosa', 'Los Sueldos', 'Lules', 'Mancopa', 'Marti Coll', 'Mixta', 'Monteagudo',
                                                 'Monteros', 'Pozo del Alto', 'Quilmes', 'Raco', 'Ranchillos', 'Río Colorado', 'Río Seco', 'Río Tala', 'Romera Pozo', 'Rumi Punco',
                                                 'San Andres', 'San Ignacio', 'San Pablo', 'San Pedro del Colalao', 'Santa Ana', 'Santa Cruz', 'Santa Lucía', 'Santa Rosa de Leales',
                                                 'Sargento Moya', 'Simoca', 'Tacanas', 'Taco Ralo', 'Tafí del Valle', 'Tafí Viejo (centro)', 'Teniente Bernardina', 'Trancas',
                                                 'Villa Benjamín Aráoz', 'Villa de Leales', 'Villa Mariano Moreno', 'Villa Nougues', 'Villa Obrera', 'Vipos', 'Yerba Buena'   ], zero=T('Choose one'))

#auth.messages.label_username = T('SSN')
# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# add db, auth, mail to current for access from modules
current.db = db
current.auth = auth
current.mail = mail
