# -*- coding: utf-8 -*-

table = db.intellectual_exam
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


@auth.requires_membership('Super Admin')
def launch():
    form = FORM.confirm('Are you sure?')
    if form.accepted:
        launch_intellectual_exam()
    
    return(dict(form = form))

@auth.requires_membership('Super Admin')#Launch massive intellectuall exams to candidates which pass the height exam
def launch_intellectual_exam():
    inscriptions_heights = db((db.auth_user.id == db.inscription.auth_user) & (db.height.inscription == db.inscription.id)).select()
    for ih in inscriptions_heights:
        if (ih.height.height >= 1.70 and ih.inscription.auth_user.gender == T('Male')) or (ih.height.height >= 1.65 and ih.inscription.auth_user.gender == T('Female')):
            table.insert(inscription = ih.inscription.id)
    redirect(URL('admin','index'))


@auth.requires_login()
def intellectual_form():
    import os
    from gluon.contrib.pyfpdf import FPDF

    candidate = db(db.auth_user.id == auth.user_id).select().first()
    inscription = db(db.shift_candidate.auth_user == auth.user_id).select().last()
    logoIES = os.path.join(request.folder, "static", "images", "logo_ies.png")
    logoMinSeg = os.path.join(request.folder, "static", "images", "logoMinisterio.png")

    #creo el objeto PDF
    pdf = FPDF('P', 'mm', 'A4')

    #FORMULARIO NOTAS EXAMEN INTELECTUAL
    pdf.add_page()
    #LOGOS
    pdf.image(logoIES,165,10,23,26)
    pdf.image(logoMinSeg,45,13,80,20)
    #VARIABLES
    enc_intelectual = unicode('FORMULARIO DE EXÁMENES DE CONOCIMIENTOS INTELECTUALES PARA ASPIRANTES A CADETES DE PRIMER AÑO DEL INSTITUTO DE ENSEÑANZA SUPERIOR DE POLICÍA "GRAL. JOSÉ FRANCISCO DE SAN MARTÍN"','utf-8')
    presentado = unicode('(El presente formulario deberá ser presentado por el Aspirante al momento de rendir los Exámenes de Conocimientos Intelectuales)','utf-8')
    aprobacion = unicode('La aprobación del EXAMEN DE CONOCIMIENTOS INTELECTUALES requerirá la obtención de un puntaje mínimo de sesenta (60) sobre cien (100) puntos por materia o de doscientos cuarenta (240) puntos en la sumatoria de las tres asignaturas, siempre y cuando no se obtenga menos de cuarenta (40) puntos en ninguna materia.','utf-8')
    sin_recuperatorio = unicode('LOS EXAMENES INTELECTUALES NO TIENEN RECUPERATORIO.','utf-8')
    pdf.rect(30,37,170,250)
    pdf.set_xy(33,40)
    pdf.set_font('Arial','BU',12)
    pdf.multi_cell(165,5,enc_intelectual,0,'C',False)
    pdf.set_xy(31,56)
    pdf.set_font('Times','',9)
    pdf.multi_cell(172,3,presentado,0,'',False)
    pdf.set_font('Times','',12)
    pdf.text(33,70,'APELIDO/S:  '+unicode(inscription.auth_user.last_name,'utf-8').upper())
    pdf.text(33,75,'NOMBRE/S:  '+unicode(inscription.auth_user.first_name,'utf-8').upper())
    pdf.text(33,80,'D.N.I.:  '+unicode(inscription.auth_user.username,'utf-8').upper())
    pdf.text(33,85,'FECHA DE NACIMIENTO:  ' + inscription.auth_user.birth_date.strftime("%d/%m/%Y"))
    pdf.text(33,90,'NACIONALIDAD:  ' + unicode(inscription.auth_user.nationality,'utf-8').upper())
    pdf.rect(140,60,60,30)
    pdf.text(153,68,unicode('FORMULARIO N°','utf-8'))
    pdf.set_xy(140,75)
    pdf.set_font('Arial','B',40)
    pdf.multi_cell(60,5,str(inscription.id),0,'C',False)
    pdf.set_xy(33,98)
    pdf.set_font('Times','',10)
    pdf.multi_cell(165,5,aprobacion,0,'J',False)
    pdf.text(125,125,unicode('SAN MIGUEL DE TUCUMÁN,......./......./..............','utf-8'))
    pdf.text(125,242,unicode('SAN MIGUEL DE TUCUMÁN,......./......./..............','utf-8'))
    pdf.text(33,135,unicode('FIRMA DEL ASPIRANTE.........................................................................................................................................','utf-8'))
    pdf.text(33,142,unicode('ACLARACIÓN...........................................................................................................................................................','utf-8'))
    pdf.text(33,256,unicode('FIRMA DEL ASPIRANTE.........................................................................................................................................','utf-8'))
    pdf.text(33,264,unicode('ACLARACIÓN...........................................................................................................................................................','utf-8'))
    

    pdf.set_xy(33,112)
    pdf.set_font('Times','B',10)
    pdf.multi_cell(165,5,sin_recuperatorio,0,'',False)

    #CUADRO NOTAS EXAMENES
    pdf.rect(33,152,164,40)
    pdf.line(33,162,197,162)
    pdf.line(74,162,74,192)
    pdf.line(115,162,115,192)
    pdf.line(156,162,156,192)
    pdf.dashed_line(36,188,71,188)
    pdf.dashed_line(77,188,112,188)
    pdf.dashed_line(118,188,153,188)
    pdf.dashed_line(159,188,194,188)
    pdf.rect(84,200,62,30)
    pdf.line(84,210,146,210)
    pdf.dashed_line(87,227,143,227)

    pdf.text(87,158,unicode('RESULTADO DE LOS EXÁMENES','utf-8'))
    pdf.text(46,168,'LENGUA')
    pdf.text(86,168,'HISTORIA')
    pdf.text(125,168,unicode('GEOGRAFÍA','utf-8'))
    pdf.text(104,206,'PROMEDIO')
    pdf.set_xy(156,165)
    pdf.multi_cell(41,4,unicode('EDUCACIÓN ÉTICA Y CIUDADANA','utf-8'),0,'C',False)

    return pdf.output(dest='S')





