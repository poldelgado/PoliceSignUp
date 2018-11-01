    # -*- coding: utf-8 -*-

'''This is a template controller with corresponding views
for list, create, view, and edit.
The list utilizes the datatables plugin.
The create and view views utilize the cascading field plugin.
'''
import datetime


table = db.shift_candidate
response.view_title = '%s %s' % (
    request.function.replace('_', ' ').title(),
    table._singular
)


def index():
    redirect(URL(request.controller, 'list'))

@auth.requires_membership('Admin')
def list():
    announcement = None  # XML(response.render('announcement.html'))
    query = (table)
    items = db(query).select(orderby=~table.created_on).render()

    actions = [
        {'is_item_action': lambda item: True, 'url': lambda item: URL('view.html', args=[item.id]), 'icon': 'search'},
        {'is_item_action': lambda item: True, 'url': lambda item: URL('edit.html', args=[item.id]), 'icon': 'pencil'},
    ]

    fields = [f for f in table]
    # fields = [
    #     table.id,
    #     table.created_on, table.created_by,
    # ]

    response.view = 'template/list.%s' % request.extension
    return dict(
        item_name=table._singular,
        row_list=items,
        actions=actions,
        field_list=fields,
        announcement=announcement
    )


@auth.requires_login()
def create():
    fields = [
        'id',
        'created_on', 'created_by',
    ]

    form = SQLFORM(table)  # , fields=fields)

    if form.process().accepted:
        session.flash = '%s created!' % table._singular
        redirect(URL(request.controller, 'create'))
    elif form.errors:
        response.flash = 'Please correct the errors'

    response.view = 'template/create.html'
    return dict(item_name=table._singular, form=form)


def view():
    item = table(table.id == request.args(0)) or redirect(URL('index'))
    form = SQLFORM(table, item, readonly=True, comments=False)

    response.view = 'template/view.%s' % request.extension
    return dict(item_name=table._singular, form=form, item=item)


@auth.requires_login()
def edit():
    # db.support_case.case_subcategory.requires = IS_IN_DB(
    #     # db, db.case_subcategory._id, db.case_category._format,
    #     db, db.case_subcategory._id, '%(case_category)s*%(title)s',
    #     # sort=True,  # orderby=db.case_subcategory.title,
    #     # cache=(cache.ram, 60)
    # )

    item = table(request.args(0)) or redirect(URL('index'))
    form = SQLFORM(table, item)

    if form.process().accepted:
        session.flash = '%s updated!' % table._singular
        redirect(URL(request.controller, 'list'))
    elif form.errors:
        response.flash = 'Please correct the errors'

    response.view = 'template/edit.html'
    return dict(item_name=table._singular, form=form)


@auth.requires_membership('Admin')
def populate():
    query = table
    set = db(query)
    # rows = set.select()
    set.delete()
    from gluon.contrib.populate import populate
    populate(table, 15)
    redirect(URL('list'))


@auth.requires_membership('Admin')
def update():
    query = table
    set = db(query)
    rows = set.select()

    for row in rows:
        # row.xxxx = 'yyyy'
        row.update_record()

    redirect(URL('list'))


@auth.requires_membership('Admin')
def list_to_xls():
    assigned_shift = db((db.shift.id == db.shift_candidate.shift) & (db.auth_user.id == db.shift_candidate.auth_user)).select(orderby=db.shift.shift_date|db.shift.shift_time)
    return dict(assigned_shift = assigned_shift)

@auth.requires_membership('Admin')
def listado_inscriptos():
    import os
    import xlwt
    from datetime import datetime
    inscriptions = db((db.shift.id == db.shift_candidate.shift) & (db.auth_user.id == db.shift_candidate.auth_user)).select(orderby=db.shift.shift_date|db.shift.shift_time)
    tmpfilename=os.path.join(request.folder,'private',str("tem.xls"))

    font0 = xlwt.Font()
    font0.name = 'Arial'
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0
    #Formato para fechas
    style1 = xlwt.XFStyle()
    style1.num_format_str = 'DD-MMMM-YYYY'
    #formato para datos en texto
    style2 = xlwt.XFStyle()
    style2.font.name = 'Arial'
    style2.font.bold = False
    #formato para datos de hora
    style3 = xlwt.XFStyle()
    style3.num_format_str = 'HH:MM'


    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sample report')
    #encabezado
    ws.write(0, 0, 'Formulario', style0)
    ws.write(0, 1, 'Fecha de Turno', style0)
    ws.write(0, 2, 'Hora de Turno', style0)
    ws.write(0, 3, 'DNI', style0)
    ws.write(0, 4, 'Apellido y Nombre/s', style0)
    ws.write(0, 5, 'F.Nac', style0)
    ws.write(0, 6, 'EDAD', style0)
    ws.write(0, 7, 'Genero', style0)
    ws.write(0, 8, 'Estado Civil', style0)
    ws.write(0, 9, 'Carrera', style0)
    ws.write(0, 10, 'Tel. Fijo', style0)
    ws.write(0, 11, 'Tel. Celular', style0)
    ws.write(0, 12, 'Direccion', style0)
    ws.write(0, 13, 'Provincia', style0)
    ws.write(0, 14, 'Comisaria Jur.', style0)
    ws.write(0, 15, 'Col. Secundario', style0)
    ws.write(0, 16, 'Titulo Terciario', style0)

    #completa filas con datos de inscriptos
    for i in xrange(0,len(inscriptions)):
        ws.write(i+1, 0, inscriptions[i].shift.id, style2)
        ws.write(i+1, 1, inscriptions[i].shift.shift_date, style1)
        ws.write(i+1, 2, inscriptions[i].shift.shift_time, style3)
        ws.write(i+1, 3, inscriptions[i].auth_user.username, style2)
        ws.write(i+1, 4, unicode(inscriptions[i].auth_user.last_name + ', ' + inscriptions[i].auth_user.first_name,'utf-8'), style2)
        ws.write(i+1, 5, inscriptions[i].auth_user.birth_date, style1)
        ws.write(i+1, 6, calculate_age(inscriptions[i].auth_user.birth_date), style1)
        ws.write(i+1, 7, inscriptions[i].auth_user.gender, style2)
        ws.write(i+1, 8, inscriptions[i].auth_user.marital_status, style2)
        ws.write(i+1, 9, unicode(inscriptions[i].auth_user.career,'utf-8'), style2)
        ws.write(i+1, 10, unicode(inscriptions[i].auth_user.phone,'utf-8'), style2)
        ws.write(i+1, 11, unicode(inscriptions[i].auth_user.mobile_phone,'utf-8'), style2)
        ws.write(i+1, 12, unicode(inscriptions[i].auth_user.address,'utf-8'), style2)
        ws.write(i+1, 13, unicode(inscriptions[i].auth_user.province,'utf-8'), style2)
        ws.write(i+1, 14, unicode(inscriptions[i].auth_user.police_station,'utf-8'), style2)
        ws.write(i+1, 15, unicode(inscriptions[i].auth_user.high_school,'utf-8'), style2)
        ws.write(i+1, 16, unicode(inscriptions[i].auth_user.tertiary_title,'utf-8'), style2)

    wb.save(tmpfilename)

    data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/vnd.ms-excel'

    return data

def calculate_age(dob):
    from datetime import date
    today = date.today()
    if today > dob:
        age = today.year - dob.year
        if dob.month > today.month:
            age -= 1
        if today.month == dob.month:
            if dob.day > dob.month:
                age -= 1        
        return age
    else:
        return 0
