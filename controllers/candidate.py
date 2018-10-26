# -*- coding: utf-8 -*-
from datetime import datetime


table = db.auth_user
inscription = db.inscription
height = db.height
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


@auth.requires_membership('Admin')
def create():
    fields = [
        'id',
        'created_on', 'created_by',
    ]

    form = SQLFORM(table)  # , fields=fields)

    if form.process().accepted:
        session.flash = '%s created!' % table._singular
        redirect(URL(request.controller, 'list'))
    elif form.errors:
        response.flash = 'Please correct the errors'

    response.view = 'template/create.html'
    return dict(item_name=table._singular, form=form)


def view():
    item = table(table.id == request.args(0)) or redirect(URL('index'))
    form = SQLFORM(table, item, readonly=True, comments=False)

    response.view = 'template/view.%s' % request.extension
    return dict(item_name=table._singular, form=form, item=item)


@auth.requires_membership('Admin')
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

def gestion():
    form = SQLFORM.smartgrid(db.person, csv=False)
    return dict(form = form)

@auth.requires_login()
def profile():
    user_profile = db(db.auth_user.id == auth.user_id).select().first()
    shift = db(db.shift_candidate.auth_user == auth.user_id).select().first()
    inscription = db(user_profile.id == db.inscription.auth_user).select().last()
    height_exam = db(db.height.inscription == inscription.id).select().first()
    intellectual_exam = db(db.intellectual_exam.inscription == inscription.id).select().first()
    medical_exam = db(db.medical_exam.inscription == inscription.id).select().first()
    physical_exam = db(db.physical_exam.inscription == inscription.id).select().first()
    groupal_psychological_examination = db(db.groupal_psychological_examination.inscription == inscription.id).select().first()
    psychological_interview = db(db.psychological_interview.inscription == inscription.id).select().first()


    if not(height_exam == None):
        if ((height_exam.height >= 1.7) and (user_profile.gender == T('Male'))) or ((height_exam.height >= 1.65) and (user_profile.gender == T('Female'))):
            height_exam.update_record(aproved=True)
        else:
            height_exam.update_record(aproved=False)


    if not(intellectual_exam  == None):
        if (intellectual_exam.spanish_language >=6) and (intellectual_exam.history >= 6) and (intellectual_exam.geography >=6):
            intellectual_exam.update_record(aproved=True)
        else:
            intellectual_exam.update_record(aproved=False)


    if not(physical_exam == None):
        if physical_exam.abs_test >= 6 and physical_exam.arms >=6 and physical_exam.aerobics >= 6:
            physical_exam.update_record(aproved=True)
        else:
            physical_exam.update_record(aproved=False)


    return dict(user = user_profile, shift = shift, inscription = inscription, height_exam = height_exam, intellectual_exam = intellectual_exam, medical_exam = medical_exam, physical_exam = physical_exam,
        groupal_psychological_examination = groupal_psychological_examination, psychological_interview = psychological_interview)

def register():
    control_time = False 
    limitI = datetime(2018,11,1,3,0,0)
    limitF = datetime(2018,11,12,2,55,0)
    actual_time = datetime.now()
    if actual_time<limitF and actual_time>limitI:
        control_time = True
    auth.settings.register_onaccept = add_user_shift
    auth.settings.register_next = URL(c='candidate',f='profile')
    return dict(form = auth.register(), control_time = control_time)

@auth.requires_login()
def forms():
    return dict()

# @auth.requires_login()
# def inscription_form():
#     candidate = db(db.auth_user.id == auth.user_id).select().first()
#     inscription = db(db.shift_candidate.auth_user == auth.user_id).select().last()
#     return dict(inscription = inscription)

@auth.requires_login()
def inscription_form():
    import os
    from gluon.contrib.pyfpdf import FPDF

    candidate = db(db.auth_user.id == auth.user_id).select().first()
    inscription = db(db.shift_candidate.auth_user == auth.user_id).select().last()
    age = calculate_age(candidate.birth_date)
    
    class PDF(FPDF):
        def header(self):
            #LOGOS
            logoIES = os.path.join(request.folder, "static", "images", "logo_ies.png")
            logoMinSeg = os.path.join(request.folder, "static", "images", "logoMinisterio.png")
            self.image(logoIES,165,10,23,26)
            self.image(logoMinSeg,45,13,80,20)
         
    titulo_form = unicode('FORMULARIO UNICO DE INSCRIPCIÓN PARA ASPIRANTES A CADETES DE PRIMER AÑO DEL INSTITUTO DE ENSEÑANZA SUPERIOR DE POLICÍA "GRAL. JOSE FRANCISCO DE SAN MARTÍN" - CICLO LECTIVO 2019',"utf-8")
    #aclaracion = unicode('Los datos consignados en este formulario tienen carácter de "Declaración Jurada". La presentación del presente formulario implica conocer y aceptar los términos de la convocatoria y proceso de selección. La presentación de este formulario es de carácter GRATUITO','utf-8')
    declaracion_jurada = unicode('Declaro bajo juramento de ley: 1°) Que los datos consignados son verdaderos; 2°) Que he tomado conocimiento y acepto los términos de la presente convocatoria y proceso de selección, conforme el Decreto respectivo, como así tambien las pautas establecidas por el I.E.S. de Policía "GJFSM"; 3°) Que no registro antecedentes judiciales ni penales de carácter doloso ni contravencionales policiales, ni me encuentro procesado por la justicia provincial o nacional. En consecuencia, quedo sujeto a las normas que rigen administrativa y jurídicamente en la materia (Art. 172, 292 y c.c. Código Penal Argentino), y además obligado a comunicar toda variante dentro de los 15 (quince) días corridos a partir de la fecha en que éstas se hayan producido.','utf-8')
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Times', 'B', 12)
    pdf.line(30,37,200,37)
    pdf.line(30,37,30,290)
    pdf.line(200,37,200,290)
    pdf.line(30,290,200,290)
    pdf.line(30,75,200,75)
    pdf.line(120,37,120,75)
    pdf.line(30,245,200,245)
    pdf.dashed_line(35,65,115,65) #FIRMA CONTROLADOR FORMULARIO
    pdf.dashed_line(138,278,198,278) #FIRMA CONTROLADOR FISICO

    pdf.text(40,43,unicode('DOCUMENTACIÓN CONTROLADA','utf-8'))
    pdf.text(138,43,'FORMULARIO NRO:')
    pdf.text(33,50,'FECHA:         /         /    ')
    pdf.text(37,70,'FIRMA Y SELLO DEL CONTROLADOR')
    pdf.text(150,63,'TURNO:')
    pdf.text(125,69,unicode('DÍA: ','utf-8') + inscription.shift.shift_date.strftime("%d/%m/%Y"))
    pdf.text(125,74,'HORA: ' + inscription.shift.shift_time.strftime("%H:%M"))
    pdf.set_xy(38,77)
    pdf.multi_cell(157,5, titulo_form,0,'C',False)
    #DATOS DEL POSTULANTE
    pdf.set_font('Times','',12)
    pdf.text(34,100,'APELLIDO/S: ' + unicode(inscription.auth_user.last_name,'utf-8').upper())
    pdf.text(34,105,'NOMBRE/S: ' + unicode(inscription.auth_user.first_name,'utf-8').upper())
    pdf.text(34,110,'FECHA DE NACIMIENTO: ' + inscription.auth_user.birth_date.strftime("%d/%m/%Y"))
    pdf.text(34,115,'EDAD: ' + str(age))
    pdf.text(34,120,'GENERO: ' + unicode(inscription.auth_user.gender,'utf-8').upper())
    pdf.text(34,125,'ESTADO CIVIL: ' + unicode(inscription.auth_user.marital_status, 'utf-8').upper())
    pdf.text(34,130,'NACIONALIDAD: ' + unicode(inscription.auth_user.nationality, 'utf-8').upper())
    pdf.text(34,135, 'DOMICILIO: ' + unicode(inscription.auth_user.address, 'utf-8').upper())
    pdf.text(34,140, 'CIUDAD / LOCALIDAD: ' + unicode(inscription.auth_user.city,'utf-8').upper())
    pdf.text(34,145,'PROVINCIA: ' + unicode(inscription.auth_user.province,'utf-8').upper())
    pdf.text(34,150, unicode('COMISARIA JURISDICCIONAL: ' + inscription.auth_user.police_station, 'utf-8').upper())
    pdf.text(34,155,'TEL. FIJO: ' + inscription.auth_user.phone)
    pdf.text(34,160,'TEL. FIJO: ' + inscription.auth_user.mobile_phone)
    pdf.text(34,165,unicode('CORREO ELECTRÓNICO: ','utf-8') + unicode(inscription.auth_user.email,'utf-8').upper())
    pdf.text(34,170, unicode('TÍTULO SECUNDARIO EXPEDIDO POR: ' + inscription.auth_user.high_school,'utf-8').upper())
    pdf.text(34,175, unicode('TÍTULO TERCIARIO: ' + inscription.auth_user.tertiary_title,'utf-8').upper())
    pdf.text(44,310, unicode('ESTOS DATOS SERÁN COMPLETADOS POR PERSONAL DEL I.E.S.P "G.J.F.S.M"','utf-8'))
    pdf.text(34,255, 'ESTATURA:..................')
    pdf.text(34,265, 'PESO:.............................')
    pdf.text(34,275, 'I.M.C.:............................')
    pdf.set_xy(34,180)
    pdf.set_font('Times','',12)
    pdf.multi_cell(160,4, declaracion_jurada,0,'J',False)
    pdf.set_font('Times','',9)
    pdf.text(34,225,unicode('FIRMA DEL ASPIRANTE AL MOMENTO DE PRESENTAR LA DOCUMENTACIÓN: ..........................................................','utf-8'))
    pdf.text(34,232,unicode('ACLARACIÓN: .................................................................................................................................................................................','utf-8'))
    #pdf.set_xy(34,320)
    #pdf.multi_cell(160,5, aclaracion,0,'J',False)
    pdf.text(140,282, 'FIRMA Y SELLO DEL CONTROLADOR')


    #NRO DE FORMULARIO
    pdf.set_font('Arial','B',40)
    pdf.set_xy(120,47)
    pdf.cell(75,10,str(inscription.id),0,0,'C')

    #SEGUNDA PAGINA
    pdf.add_page()
    pdf.set_font('Times', 'B', 12)
    pdf.line(30,37,200,37)
    pdf.line(30,37,30,290)
    pdf.line(200,37,200,290)
    pdf.line(30,290,200,290)
    pdf.line(30,75,200,75)
    pdf.line(120,37,120,75)
    pdf.line(30,245,200,245)
    pdf.dashed_line(35,65,115,65) #FIRMA CONTROLADOR FORMULARIO
    pdf.dashed_line(138,278,198,278) #FIRMA CONTROLADOR FISICO

    pdf.text(40,43,unicode('DOCUMENTACIÓN CONTROLADA','utf-8'))
    pdf.text(138,43,'FORMULARIO NRO:')
    pdf.text(33,50,'FECHA:         /         /    ')
    pdf.text(37,70,'FIRMA Y SELLO DEL CONTROLADOR')
    pdf.text(150,63,'TURNO:')
    pdf.text(125,69,unicode('DÍA: ','utf-8') + inscription.shift.shift_date.strftime("%d/%m/%Y"))
    pdf.text(125,74,'HORA: ' + inscription.shift.shift_time.strftime("%H:%M"))
    pdf.set_xy(38,77)
    pdf.multi_cell(157,5, titulo_form,0,'C',False)
    #DATOS DEL POSTULANTE
    pdf.set_font('Times','',12)
    pdf.text(34,100,'APELLIDO/S: ' + unicode(inscription.auth_user.last_name,'utf-8').upper())
    pdf.text(34,105,'NOMBRE/S: ' + unicode(inscription.auth_user.first_name,'utf-8').upper())
    pdf.text(34,110,'FECHA DE NACIMIENTO: ' + inscription.auth_user.birth_date.strftime("%d/%m/%Y"))
    pdf.text(34,115,'EDAD: ' + str(age))
    pdf.text(34,120,'GENERO: ' + unicode(inscription.auth_user.gender,'utf-8').upper())
    pdf.text(34,125,'ESTADO CIVIL: ' + unicode(inscription.auth_user.marital_status, 'utf-8').upper())
    pdf.text(34,130,'NACIONALIDAD: ' + unicode(inscription.auth_user.nationality, 'utf-8').upper())
    pdf.text(34,135, 'DOMICILIO: ' + unicode(inscription.auth_user.address, 'utf-8').upper())
    pdf.text(34,140, 'CIUDAD / LOCALIDAD: ' + unicode(inscription.auth_user.city,'utf-8').upper())
    pdf.text(34,145,'PROVINCIA: ' + unicode(inscription.auth_user.province,'utf-8').upper())
    pdf.text(34,150, unicode('COMISARIA JURISDICCIONAL: ' + inscription.auth_user.police_station, 'utf-8').upper())
    pdf.text(34,155,'TEL. FIJO: ' + inscription.auth_user.phone)
    pdf.text(34,160,'TEL. FIJO: ' + inscription.auth_user.mobile_phone)
    pdf.text(34,165,unicode('CORREO ELECTRÓNICO: ','utf-8') + unicode(inscription.auth_user.email,'utf-8').upper())
    pdf.text(34,170, unicode('TÍTULO SECUNDARIO EXPEDIDO POR: ' + inscription.auth_user.high_school,'utf-8').upper())
    pdf.text(34,175, unicode('TÍTULO TERCIARIO: ' + inscription.auth_user.tertiary_title,'utf-8').upper())
    pdf.text(44,310, unicode('ESTOS DATOS SERÁN COMPLETADOS POR PERSONAL DEL I.E.S.P "G.J.F.S.M"','utf-8'))
    pdf.text(34,255, 'ESTATURA:..................')
    pdf.text(34,265, 'PESO:.............................')
    pdf.text(34,275, 'I.M.C.:............................')
    pdf.set_xy(34,180)
    pdf.set_font('Times','',12)
    pdf.multi_cell(160,4, declaracion_jurada,0,'J',False)
    pdf.set_font('Times','',9)
    pdf.text(34,225,unicode('FIRMA DEL ASPIRANTE AL MOMENTO DE PRESENTAR LA DOCUMENTACIÓN: ..........................................................','utf-8'))
    pdf.text(34,232,unicode('ACLARACIÓN: .................................................................................................................................................................................','utf-8'))
    #pdf.set_xy(34,320)
    #pdf.multi_cell(160,5, aclaracion,0,'J',False)
    pdf.text(140,282, 'FIRMA Y SELLO DEL CONTROLADOR')


    #NRO DE FORMULARIO
    pdf.set_font('Arial','B',40)
    pdf.set_xy(120,47)
    pdf.cell(75,10,str(inscription.id),0,0,'C')

    return pdf.output(dest='S')


@auth.requires_login()
def medical_exam_form():
    candidate = db(db.auth_user.id == auth.user_id).select().first()
    inscription = db(candidate.id == db.inscription.auth_user).select().last()
    return dict(inscription = inscription)

@auth.requires_login()
def physical_exam_form():
    candidate = db(db.auth_user.id == auth.user_id).select().first()
    inscription = db(candidate.id == db.inscription.auth_user).select().last()
    return dict(inscription = inscription)

@auth.requires_login()
def intellectual_exam_form():
    candidate = db(db.auth_user.id == auth.user_id).select().first()
    inscription = db(candidate.id == db.inscription.auth_user).select().last()
    return dict(inscription = inscription)


def add_user_shift(form):
    user_id=form.vars.id
    shift = search_shift()
    db.shift_candidate.insert(auth_user = user_id, shift = shift)
    inscription.insert(auth_user = user_id)


#function that search the shift with less cadets
def search_shift():
    shifts = db(db.shift).select(orderby = db.shift.shift_date|db.shift.shift_time)
    flag = True
    shift_candidate1 = db(db.shift_candidate.shift == shifts[0].id).select()
    first_id = shifts.first().id
    if shift_candidate1 is None:
        flag = False
        return first_id
    else:
        for i in range(1, len(shifts)):
            shift_candidate2 = db(db.shift_candidate.shift == shifts[i].id).select()
            if shift_candidate2 is None:
                flag = False
                return shifts[i].id
            else:
                if len(shift_candidate1) > len(shift_candidate2):
                    flag = False
                    return shifts[i].id
    if flag:
        return first_id

def show_shift_assigned():
    form = FORM(DIV(DIV(INPUT(_name='dni',_placeholder='Ingrese DNI',_class='form-control', requires=IS_NOT_EMPTY()),_class='input-group'),_class='form-group'),
        INPUT(_type='submit',_value='Buscar',_class='btn btn-primary'),_class='form-inline')
    if form.accepts(request, session):
        response.flash = 'busqueda terminada'
        redirect(URL('candidate','print_inscription_form', args = (request.vars.dni)))
    elif form.errors:
        response.flash = 'el formulario tiene errores'
    else:
        response.flash = 'por favor complete el formulario'
    return dict(form = form)

# def print_inscription_form():
#     candidate = db(db.auth_user.username == request.vars['dni']).select().first()
#     # inscription = db(db.inscription.auth_user == candidate.id).select().last()
#     inscription = db(db.shift_candidate.auth_user == candidate.id).select().last()
#     return dict(inscription = inscription)

def print_inscription_form():
    import os
    from gluon.contrib.pyfpdf import FPDF

    candidate = db(db.auth_user.username == request.vars['dni']).select().first()
    inscription = db(db.shift_candidate.auth_user == candidate.id).select().last()
    age = calculate_age(candidate.birth_date)
    logoIES = os.path.join(request.folder, "static", "images", "logo_ies.png")
    logoMinSeg = os.path.join(request.folder, "static", "images", "logoMinisterio.png")
    
    # class PDF(FPDF):
        # def header(self):
        #     #LOGOS
        #     logoIES = os.path.join(request.folder, "static", "images", "logo_ies.png")
        #     logoMinSeg = os.path.join(request.folder, "static", "images", "logoMinisterio.png")
        #     self.image(logoIES,165,10,23,26)
        #     self.image(logoMinSeg,45,13,80,20)  

    titulo_form = unicode('FORMULARIO UNICO DE INSCRIPCIÓN PARA ASPIRANTES A CADETES DE PRIMER AÑO DEL INSTITUTO DE ENSEÑANZA SUPERIOR DE POLICÍA "GRAL. JOSE FRANCISCO DE SAN MARTÍN" - CICLO LECTIVO 2019',"utf-8")
    #aclaracion = unicode('Los datos consignados en este formulario tienen carácter de "Declaración Jurada". La presentación del presente formulario implica conocer y aceptar los términos de la convocatoria y proceso de selección. La presentación de este formulario es de carácter GRATUITO','utf-8')
    declaracion_jurada = unicode('Declaro bajo juramento de ley: 1°) Que los datos consignados son verdaderos; 2°) Que he tomado conocimiento y acepto los términos de la presente convocatoria y proceso de selección, conforme el Decreto respectivo, como así tambien las pautas establecidas por el I.E.S. de Policía "GJFSM"; 3°) Que no registro antecedentes judiciales ni penales de carácter doloso ni contravencionales policiales, ni me encuentro procesado por la justicia provincial o nacional. En consecuencia, quedo sujeto a las normas que rigen administrativa y jurídicamente en la materia (Art. 172, 292 y c.c. Código Penal Argentino), y además obligado a comunicar toda variante dentro de los 15 (quince) días corridos a partir de la fecha en que éstas se hayan producido.','utf-8')
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    #LOGOS
    pdf.image(logoIES,165,10,23,26)
    pdf.image(logoMinSeg,45,13,80,20)
    pdf.set_font('Times', 'B', 12)
    pdf.line(30,37,200,37)
    pdf.line(30,37,30,290)
    pdf.line(200,37,200,290)
    pdf.line(30,290,200,290)
    pdf.line(30,75,200,75)
    pdf.line(120,37,120,75)
    pdf.line(30,245,200,245)
    pdf.dashed_line(35,65,115,65) #FIRMA CONTROLADOR FORMULARIO
    pdf.dashed_line(138,278,198,278) #FIRMA CONTROLADOR FISICO

    pdf.text(40,43,unicode('DOCUMENTACIÓN CONTROLADA','utf-8'))
    pdf.text(138,43,'FORMULARIO NRO:')
    pdf.text(33,50,'FECHA:         /         /')
    pdf.text(37,70,'FIRMA Y SELLO DEL CONTROLADOR')
    pdf.text(150,63,'TURNO:')
    pdf.text(125,69,unicode('DÍA: ','utf-8') + inscription.shift.shift_date.strftime("%d/%m/%Y"))
    pdf.text(125,74,'HORA: ' + inscription.shift.shift_time.strftime("%H:%M"))
    pdf.set_xy(38,77)
    pdf.multi_cell(157,5, titulo_form,0,'C',False)
    #DATOS DEL POSTULANTE
    pdf.set_font('Times','',12)
    pdf.text(34,100,'APELLIDO/S: ' + unicode(inscription.auth_user.last_name,'utf-8').upper())
    pdf.text(34,105,'NOMBRE/S: ' + unicode(inscription.auth_user.first_name,'utf-8').upper())
    pdf.text(34,110, 'D.N.I.:' + unicode(inscription.auth_user.username, 'utf-8'))
    pdf.text(34,115,'FECHA DE NACIMIENTO: ' + inscription.auth_user.birth_date.strftime("%d/%m/%Y"))
    pdf.text(34,120,'EDAD: ' + str(age))
    pdf.text(34,125,'GENERO: ' + unicode(inscription.auth_user.gender,'utf-8').upper())
    pdf.text(34,130,'ESTADO CIVIL: ' + unicode(inscription.auth_user.marital_status, 'utf-8').upper())
    pdf.text(34,135,'NACIONALIDAD: ' + unicode(inscription.auth_user.nationality, 'utf-8').upper())
    pdf.text(34,140, 'DOMICILIO: ' + unicode(inscription.auth_user.address, 'utf-8').upper())
    pdf.text(34,145, 'CIUDAD / LOCALIDAD: ' + unicode(inscription.auth_user.city,'utf-8').upper())
    pdf.text(34,150,'PROVINCIA: ' + unicode(inscription.auth_user.province,'utf-8').upper())
    pdf.text(34,155, unicode('COMISARIA JURISDICCIONAL: ' + inscription.auth_user.police_station, 'utf-8').upper())
    pdf.text(34,160,'TEL. FIJO: ' + inscription.auth_user.phone)
    pdf.text(34,165,'TEL. FIJO: ' + inscription.auth_user.mobile_phone)
    pdf.text(34,170,unicode('CORREO ELECTRÓNICO: ','utf-8') + unicode(inscription.auth_user.email,'utf-8').upper())
    pdf.text(34,175, unicode('TÍTULO SECUNDARIO EXPEDIDO POR: ' + inscription.auth_user.high_school,'utf-8').upper())
    pdf.text(34,180, unicode('TÍTULO TERCIARIO: ' + inscription.auth_user.tertiary_title,'utf-8').upper())
    pdf.text(44,310, unicode('ESTOS DATOS SERÁN COMPLETADOS POR PERSONAL DEL I.E.S.P "G.J.F.S.M"','utf-8'))
    pdf.text(34,255, 'ESTATURA:..................')
    pdf.text(34,265, 'PESO:.............................')
    pdf.text(34,275, 'I.M.C.:............................')
    pdf.set_xy(34,184)
    pdf.set_font('Times','',12)
    pdf.multi_cell(160,4, declaracion_jurada,0,'J',False)
    pdf.set_font('Times','',9)
    pdf.text(34,230,unicode('FIRMA DEL ASPIRANTE AL MOMENTO DE PRESENTAR LA DOCUMENTACIÓN: ..........................................................','utf-8'))
    pdf.text(34,237,unicode('ACLARACIÓN: .................................................................................................................................................................................','utf-8'))
    #pdf.set_xy(34,320)
    #pdf.multi_cell(160,5, aclaracion,0,'J',False)
    pdf.text(140,282, 'FIRMA Y SELLO DEL CONTROLADOR')


    #NRO DE FORMULARIO
    pdf.set_font('Arial','B',40)
    pdf.set_xy(120,47)
    pdf.cell(75,10,str(inscription.id),0,0,'C')

    #SEGUNDA PAGINA
    pdf.add_page()
    #LOGOS
    pdf.image(logoIES,165,10,23,26)
    pdf.image(logoMinSeg,45,13,80,20)
    pdf.set_font('Times', 'B', 12)
    pdf.line(30,37,200,37)
    pdf.line(30,37,30,290)
    pdf.line(200,37,200,290)
    pdf.line(30,290,200,290)
    pdf.line(30,75,200,75)
    pdf.line(120,37,120,75)
    pdf.line(30,245,200,245)
    pdf.dashed_line(35,65,115,65) #FIRMA CONTROLADOR FORMULARIO
    pdf.dashed_line(138,278,198,278) #FIRMA CONTROLADOR FISICO

    pdf.text(40,43,unicode('DOCUMENTACIÓN CONTROLADA','utf-8'))
    pdf.text(138,43,'FORMULARIO NRO:')
    pdf.text(33,50,'FECHA:         /         /')
    pdf.text(37,70,'FIRMA Y SELLO DEL CONTROLADOR')
    pdf.text(150,63,'TURNO:')
    pdf.text(125,69,unicode('DÍA: ','utf-8') + inscription.shift.shift_date.strftime("%d/%m/%Y"))
    pdf.text(125,74,'HORA: ' + inscription.shift.shift_time.strftime("%H:%M"))
    pdf.set_xy(38,77)
    pdf.multi_cell(157,5, titulo_form,0,'C',False)
    #DATOS DEL POSTULANTE
    pdf.set_font('Times','',12)
    pdf.text(34,100,'APELLIDO/S: ' + unicode(inscription.auth_user.last_name,'utf-8').upper())
    pdf.text(34,105,'NOMBRE/S: ' + unicode(inscription.auth_user.first_name,'utf-8').upper())
    pdf.text(34,110, 'D.N.I.:' + unicode(inscription.auth_user.username, 'utf-8'))
    pdf.text(34,115,'FECHA DE NACIMIENTO: ' + inscription.auth_user.birth_date.strftime("%d/%m/%Y"))
    pdf.text(34,120,'EDAD: ' + str(age))
    pdf.text(34,125,'GENERO: ' + unicode(inscription.auth_user.gender,'utf-8').upper())
    pdf.text(34,130,'ESTADO CIVIL: ' + unicode(inscription.auth_user.marital_status, 'utf-8').upper())
    pdf.text(34,135,'NACIONALIDAD: ' + unicode(inscription.auth_user.nationality, 'utf-8').upper())
    pdf.text(34,140, 'DOMICILIO: ' + unicode(inscription.auth_user.address, 'utf-8').upper())
    pdf.text(34,145, 'CIUDAD / LOCALIDAD: ' + unicode(inscription.auth_user.city,'utf-8').upper())
    pdf.text(34,150,'PROVINCIA: ' + unicode(inscription.auth_user.province,'utf-8').upper())
    pdf.text(34,155, unicode('COMISARIA JURISDICCIONAL: ' + inscription.auth_user.police_station, 'utf-8').upper())
    pdf.text(34,160,'TEL. FIJO: ' + inscription.auth_user.phone)
    pdf.text(34,165,'TEL. FIJO: ' + inscription.auth_user.mobile_phone)
    pdf.text(34,170,unicode('CORREO ELECTRÓNICO: ','utf-8') + unicode(inscription.auth_user.email,'utf-8').upper())
    pdf.text(34,175, unicode('TÍTULO SECUNDARIO EXPEDIDO POR: ' + inscription.auth_user.high_school,'utf-8').upper())
    pdf.text(34,180, unicode('TÍTULO TERCIARIO: ' + inscription.auth_user.tertiary_title,'utf-8').upper())
    pdf.text(44,310, unicode('ESTOS DATOS SERÁN COMPLETADOS POR PERSONAL DEL I.E.S.P "G.J.F.S.M"','utf-8'))
    pdf.text(34,255, 'ESTATURA:..................')
    pdf.text(34,265, 'PESO:.............................')
    pdf.text(34,275, 'I.M.C.:............................')
    pdf.set_xy(34,184)
    pdf.set_font('Times','',12)
    pdf.multi_cell(160,4, declaracion_jurada,0,'J',False)
    pdf.set_font('Times','',9)
    pdf.text(34,230,unicode('FIRMA DEL ASPIRANTE AL MOMENTO DE PRESENTAR LA DOCUMENTACIÓN: ..........................................................','utf-8'))
    pdf.text(34,237,unicode('ACLARACIÓN: .................................................................................................................................................................................','utf-8'))
    #pdf.set_xy(34,320)
    #pdf.multi_cell(160,5, aclaracion,0,'J',False)
    pdf.text(140,282, 'FIRMA Y SELLO DEL CONTROLADOR')


    #NRO DE FORMULARIO
    pdf.set_font('Arial','B',40)
    pdf.set_xy(120,47)
    pdf.cell(75,10,str(inscription.id),0,0,'C')

    #FORMULARIO DE AUTORIZACION MENOR DE EDAD
    if age < 18:
        instituto = unicode('INSTITUTO DE ENSEÑANZA SUPERIOR DE POLICÍA "GRAL. JOSÉ FRANCISCO DE SAN MARTÍN"','utf-8')
        direccion = unicode('Calle Muñecas N°1.025 - San Miguel de Tucumán','utf-8')
        telefono = unicode('Telefono N°(0381) 4305141 - Republica Argentina','utf-8')
        porintermedio = unicode('Por intermedio de la presente, manifiesto/amos expreso consentimiento AUTORIZANDO a mí/nuestro....................................................................................., nacido el ......./......./....... a inscribirse  y participar en todas las etapas del proceso de selección (Exámenes Intelectuales, Psicológicos, Médicos y de Aptitud Física), para ingresar como Aspirante a Cadete de Primer Año del Instituto de Enseñanza Superior de Policía "Gral. José Francisco de San Martín"  Ciclo Lectivo 2019, bajo los términos y condiciones del Decreto respectivo y las pautas establecidas por el I.E.S.P. "G.J.F.S.M."','utf-8')
        consentimiento = unicode('(El consentimiento expreso para la presente autorización debe ser otorgada por ambos progenitores de conformidad a lo dispuesto por el Art. 645 y ccs del Código Civil y Comercial de la nación).','utf-8')
        enesteacto = unicode('En este acto presta conformidad expresa el menor de edad para realizar  los actos enunciados precedentemente.','utf-8')
        certificacion = unicode('CERTIFICACIÓN DE FIRMAS POR ESCRIBANO PÚBLICO O JUEZ DE PAZ (DE PROGENITORES)','utf-8')
        pdf.add_page()
        pdf.rect(30,10,155,28)
        pdf.image(logoIES,32,11,23,26)
        pdf.set_xy(52,11)
        pdf.set_font('Times','B',14)
        pdf.multi_cell(135,5, instituto,0,'C',False)
        pdf.set_font('Times','',12)
        pdf.text(77,30,direccion)
        pdf.text(76,35,telefono)
        pdf.set_font('Arial','BU',14)
        pdf.set_xy(30,40)
        pdf.multi_cell(150,6,unicode('INGRESO 2019\nAUTORIZACION PARA ASPIRANTES MENORES DE 19 AÑOS','utf-8'),0,'C',False)
        pdf.set_xy(30,55)
        pdf.set_font('Times','',10)
        pdf.multi_cell(150,4,consentimiento,0,'J',False)
        pdf.set_font('Times','',12)
        pdf.set_xy(30,70)
        pdf.multi_cell(150,5,porintermedio,0,'J',False)
        pdf.rect(30,115,155,60)
        pdf.line(30,125,185,125)
        pdf.line(30,145,185,145)
        pdf.line(30,155,185,155)
        pdf.line(80,115,80,175)
        pdf.line(135,125,135,145)
        pdf.line(135,155,135,175)
        pdf.line(135,130,185,130)
        pdf.line(135,160,185,160)
        pdf.set_xy(30,116)
        pdf.set_font('Arial','B',10)
        pdf.multi_cell(48,4,'APELLIDO Y NOMBRE DEL PROGENITOR',0,'C',False)
        pdf.set_xy(30,146)
        pdf.multi_cell(48,4,'APELLIDO Y NOMBRE DEL PROGENITOR',0,'C',False)
        pdf.text(67,135,'FIRMA')
        pdf.text(67,165,'FIRMA')
        pdf.text(150,129, unicode('D.N.I N°','utf-8'))
        pdf.text(150,159, unicode('D.N.I N°','utf-8'))
        pdf.set_font('Arial','', 9)
        pdf.text(90,209,'(Lugar y Fecha)')
        pdf.text(31,226,unicode('*Espacio reservado para certificación de firmas','utf-8'))
        pdf.set_xy(30,176)
        pdf.multi_cell(150,3,enesteacto,0,'C',False)
        pdf.rect(30,182,155,15)
        pdf.line(30,187,185,187)
        pdf.line(120,182,120,197)
        pdf.line(132,182,132,197)
        pdf.line(30,205,185,205)
        pdf.set_font('Arial','B',10)
        pdf.text(45,186,'APELLIDO Y NOMBRE DEL MENOR')
        pdf.text(121,186,'EDAD')
        pdf.text(151,186,unicode('DNI N°','utf-8'))
        pdf.set_xy(30,213)
        pdf.set_font('Arial','B',12)
        pdf.multi_cell(155,5,certificacion,0,'C',False)
        pdf.rect(30,223,155,68)

        #2da Pagina Menor
        pdf.add_page()

        pdf.set_font('Arial','BU',14)
        pdf.set_xy(30,20)
        pdf.multi_cell(150,6,unicode('INGRESO 2019\nAUTORIZACION PARA ASPIRANTES MENORES DE 19 AÑOS','utf-8'),0,'C',False)
        pdf.set_xy(30,35)
        pdf.set_font('Times','',10)
        pdf.multi_cell(150,4,consentimiento,0,'J',False)
        pdf.set_font('Times','',12)
        pdf.set_xy(30,50)
        pdf.multi_cell(150,5,porintermedio,0,'J',False)
        pdf.rect(30,95,155,90)
        pdf.line(30,100,185,100)
        pdf.line(30,125,185,125)
        pdf.line(30,130,185,130)
        pdf.line(30,150,185,150)
        pdf.line(30,155,185,155)
        pdf.line(78,95,78,185)
        pdf.line(150,95,150,185)
        pdf.dashed_line(32,120,76,120)
        pdf.dashed_line(32,145,76,145)
        pdf.dashed_line(32,180,76,180)
        pdf.dashed_line(80,120,148,120)
        pdf.dashed_line(152,120,182,120)
        pdf.dashed_line(80,145,148,145)
        pdf.dashed_line(152,145,182,145)
        pdf.dashed_line(80,180,148,180)
        pdf.dashed_line(152,180,182,180)
        
        pdf.set_font('Times','B',10)
        pdf.text(45,99,'FIRMA')
        pdf.text(100,99,unicode('ACLARACIÓN','utf-8'))
        pdf.text(160,99,unicode('D.N.I. N°','utf-8'))
        pdf.text(45,124,'PADRE')
        pdf.text(45,149,'MADRE')
        pdf.text(31,184,'REPRESENTANTE LEGAL')









    return pdf.output(dest='S')


def hidden_candidate_register():
    auth.settings.register_onaccept = add_user_shift
    auth.settings.register_next = URL(c='candidate',f='profile')
    return dict(form = auth.register())

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



# IMPRESION EN A4
# def inscription_form():
#     import os
#     from gluon.contrib.pyfpdf import FPDF

#     candidate = db(db.auth_user.id == auth.user_id).select().first()
#     inscription = db(db.shift_candidate.auth_user == auth.user_id).select().last()
#     age = calculate_age(candidate.birth_date)
    
#     class PDF(FPDF):
#         def header(self):
#             #LOGOS
#             logoIES = os.path.join(request.folder, "static", "images", "logo_ies.png")
#             logoMinSeg = os.path.join(request.folder, "static", "images", "logoMinisterio.png")
#             self.image(logoIES,165,10,23,26)
#             self.image(logoMinSeg,45,13,80,20)
         
#     titulo_form = unicode('FORMULARIO UNICO DE INSCRIPCION PARA ASPIRANTES A CADETES DE PRIMER AÑO DEL INSTITUTO DE ENSEÑANZA SUPERIOR DE POLICIA "GRAL. JOSE FRANCISCO DE SAN MARTIN" - CICLO LECTIVO 2019',"utf-8")
#     aclaracion = unicode('Los datos consignados en este formulario tienen carácter de "Declaración Jurada". La presentación del presente formulario implica conocer y aceptar los términos de la convocatoria y proceso de selección. La presentación de este formulario es de carácter GRATUITO','utf-8')
#     pdf = PDF('P', 'mm', 'A4')
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 12)
#     #pdf.cell(40, 10, 'Hello World!')
#     pdf.line(30,37,200,37)
#     pdf.line(30,37,30,290)
#     pdf.line(200,37,200,290)
#     pdf.line(30,290,200,290)
#     pdf.line(30,75,200,75)
#     pdf.line(120,37,120,75)
#     pdf.line(30,240,200,240)
#     pdf.dashed_line(35,65,115,65) #FIRMA CONTROLADOR FORMULARIO
#     pdf.dashed_line(141,280,195,280) #FIRMA CONTROLADOR FISICO

#     pdf.text(40,43,'DOCUMENTACION CONTROLADA')
#     pdf.text(138,43,'FORMULARIO NRO:')
#     pdf.text(33,50,'FECHA:         /         /    ')
#     pdf.text(37,70,'FIRMA Y SELLO DEL CONTROLADOR')
#     pdf.text(150,63,'TURNO:')
#     pdf.text(125,69,'DIA: ' + inscription.shift.shift_date.strftime("%d/%m/%Y"))
#     pdf.text(125,74,'HORA: ' + inscription.shift.shift_time.strftime("%H:%M"))
#     pdf.set_xy(38,85)
#     pdf.multi_cell(157,5, titulo_form,0,'C',False)
#     #DATOS DEL POSTULANTE
#     pdf.set_font('Arial','',11)
#     pdf.text(34,110,'APELLIDO/S: ' + unicode(inscription.auth_user.last_name,'utf-8'))
#     pdf.text(34,115,'NOMBRE/S: ' + unicode(inscription.auth_user.first_name,'utf-8'))
#     pdf.text(34,120,'FECHA DE NACIMIENTO: ' + inscription.auth_user.birth_date.strftime("%d/%m/%Y"))
#     pdf.text(34,125,'EDAD: ' + str(age))
#     pdf.text(34,130,'GENERO: ' + unicode(inscription.auth_user.gender,'utf-8'))
#     pdf.text(34,135,'ESTADO CIVIL: ' + unicode(inscription.auth_user.marital_status, 'utf-8'))
#     pdf.text(34,140,'NACIONALIDAD: ' + unicode(inscription.auth_user.nationality, 'utf-8'))
#     pdf.text(34,145, 'DOMICILIO: ' + unicode(inscription.auth_user.address, 'utf-8'))
#     pdf.text(34,150, 'CIUDAD / LOCALIDAD: ' + unicode(inscription.auth_user.city,'utf-8'))
#     pdf.text(34,155,'PROVINCIA: ' + unicode(inscription.auth_user.province,'utf-8'))
#     pdf.text(34,160, unicode('COMISARIA JURISDICCIONAL: ' + inscription.auth_user.police_station, 'utf-8'))
#     pdf.text(34,165,'TEL. FIJO: ' + inscription.auth_user.phone)
#     pdf.text(34,170,'TEL. FIJO: ' + inscription.auth_user.mobile_phone)
#     pdf.text(34,175,'CORREO ELECTRONICO: ' + unicode(inscription.auth_user.email,'utf-8'))
#     pdf.text(34,180, unicode('TITULO SECUNDARIO EXPEDIDO POR: ' + inscription.auth_user.high_school,'utf-8'))
#     pdf.text(34,185, unicode('TITULO TERCIARIO: ' + inscription.auth_user.tertiary_title,'utf-8'))   
#     pdf.text(38,248, unicode('ESTOS DATOS SERÁN COMPLETADOS POR PERSONAL DEL I.E.S.P "G.J.F.S.M"','utf-8'))
#     pdf.text(34,260, 'ESTATURA:..........')
#     pdf.text(34,268, 'PESO:..............')
#     pdf.text(34,276, 'I.M.C.:............')

#     pdf.set_font('Arial','',9)
#     pdf.text(34,200,unicode('FIRMA DEL ASPIRANTE AL MOMENTO DE PRESENTAR LA DOCUMENTACIÓN: ...............................................','utf-8'))
#     pdf.text(34,208,unicode('ACLARACIÓN...............................................................................................................................................................','utf-8'))
#     pdf.set_xy(34,220)
#     pdf.multi_cell(160,5, aclaracion,0,'J',False)
#     pdf.text(140,285, 'FIRMA Y SELLO DEL CONTROLADOR')


#     #NRO DE FORMULARIO
#     pdf.set_font('Arial','B',40)
#     pdf.text(145,57, str(inscription.id))

#     #SEGUNDA PAGINA

#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 12)
#     #pdf.cell(40, 10, 'Hello World!')
#     pdf.line(30,37,200,37)
#     pdf.line(30,37,30,290)
#     pdf.line(200,37,200,290)
#     pdf.line(30,290,200,290)
#     pdf.line(30,75,200,75)
#     pdf.line(120,37,120,75)
#     pdf.line(30,240,200,240)
#     pdf.dashed_line(35,65,115,65) #FIRMA CONTROLADOR FORMULARIO
#     pdf.dashed_line(141,280,195,280) #FIRMA CONTROLADOR FISICO

#     pdf.text(40,43,'DOCUMENTACION CONTROLADA')
#     pdf.text(138,43,'FORMULARIO NRO:')
#     pdf.text(33,50,'FECHA:         /         /    ')
#     pdf.text(37,70,'FIRMA Y SELLO DEL CONTROLADOR')
#     pdf.text(150,63,'TURNO:')
#     pdf.text(125,69,'DIA: ' + inscription.shift.shift_date.strftime("%d/%m/%Y"))
#     pdf.text(125,74,'HORA: ' + inscription.shift.shift_time.strftime("%H:%M"))
#     pdf.set_xy(38,85)
#     pdf.multi_cell(157,5, titulo_form,0,'C',False)
#     #DATOS DEL POSTULANTE
#     pdf.set_font('Arial','',11)
#     pdf.text(34,110,'APELLIDO/S: ' + unicode(inscription.auth_user.last_name,'utf-8'))
#     pdf.text(34,115,'NOMBRE/S: ' + unicode(inscription.auth_user.first_name,'utf-8'))
#     pdf.text(34,120,'FECHA DE NACIMIENTO: ' + inscription.auth_user.birth_date.strftime("%d/%m/%Y"))
#     pdf.text(34,125,'EDAD: ' + str(age))
#     pdf.text(34,130,'GENERO: ' + unicode(inscription.auth_user.gender,'utf-8'))
#     pdf.text(34,135,'ESTADO CIVIL: ' + unicode(inscription.auth_user.marital_status, 'utf-8'))
#     pdf.text(34,140,'NACIONALIDAD: ' + unicode(inscription.auth_user.nationality, 'utf-8'))
#     pdf.text(34,145, 'DOMICILIO: ' + unicode(inscription.auth_user.address, 'utf-8'))
#     pdf.text(34,150, 'CIUDAD / LOCALIDAD: ' + unicode(inscription.auth_user.city,'utf-8'))
#     pdf.text(34,155,'PROVINCIA: ' + unicode(inscription.auth_user.province,'utf-8'))
#     pdf.text(34,160, unicode('COMISARIA JURISDICCIONAL: ' + inscription.auth_user.police_station, 'utf-8'))
#     pdf.text(34,165,'TEL. FIJO: ' + inscription.auth_user.phone)
#     pdf.text(34,170,'TEL. FIJO: ' + inscription.auth_user.mobile_phone)
#     pdf.text(34,175,'CORREO ELECTRONICO: ' + unicode(inscription.auth_user.email,'utf-8'))
#     pdf.text(34,180, unicode('TITULO SECUNDARIO EXPEDIDO POR: ' + inscription.auth_user.high_school,'utf-8'))
#     pdf.text(34,185, unicode('TITULO TERCIARIO: ' + inscription.auth_user.tertiary_title,'utf-8'))
#     pdf.text(38,248, unicode('ESTOS DATOS SERÁN COMPLETADOS POR PERSONAL DEL I.E.S.P "G.J.F.S.M"','utf-8'))
#     pdf.text(34,260, 'ESTATURA:..........')
#     pdf.text(34,268, 'PESO:..............')
#     pdf.text(34,276, 'I.M.C.:............')

#     pdf.set_font('Arial','',9)
#     pdf.text(34,200,unicode('FIRMA DEL ASPIRANTE AL MOMENTO DE PRESENTAR LA DOCUMENTACIÓN: ...............................................','utf-8'))
#     pdf.text(34,208,unicode('ACLARACIÓN...............................................................................................................................................................','utf-8'))
#     pdf.set_xy(34,220)
#     pdf.multi_cell(160,5, aclaracion,0,'J',False)
#     pdf.text(140,285, 'FIRMA Y SELLO DEL CONTROLADOR')


#     #NRO DE FORMULARIO
#     pdf.set_font('Arial','B',40)
#     pdf.text(145,57, str(inscription.id))
#     return pdf.output(dest='S')
