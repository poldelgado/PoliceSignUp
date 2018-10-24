# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations


def index():
    latestposts = db(db.post).select(orderby=~db.post.date_of_post,limitby=(0,4))
    categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
    return dict(latestposts = latestposts, categories = categories)

    
def about():
    response.view_title = 'About'
    return dict()


def tou():
    response.view_title = 'Terms of Use'
    return dict()


def privacy():
    response.view_title = 'Privacy Policy'
    return dict()


def changelog():
    response.view_title = 'Changelog and 3rd Party Services'

    import os
    changelog_markmin = MARKMIN('')
    infile = open(os.path.join(request.folder, 'CHANGELOG'))
    for line in infile:
        changelog_markmin += MARKMIN(line)

    return dict(changelog_markmin=changelog_markmin)


# def search():
#     tables = [db.dog, db.person]

    items = []
    for t in tables:
        fields = [
            t.id, t.title,
            t.created_on, t.created_by,
        ]
        query = (t.title.contains(request.vars['q']))
        rows = db(query).select(*fields).render()
        for r in rows:
            items += [[t._singular, r.id, r.title, r.created_on, r.created_by]]

    response.view_title = T('Search Results')
    return dict(
        items=items
    )


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    response.view_title = ''

    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def login_candidate():
    auth.settings.login_next = URL(c='candidate',f='profile')
    return dict(loginform = auth())

def logout():
    auth.settings.logout_next = URL('index')
    return dict()

def entry_program():
    categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
    return dict(categories = categories)

#@auth.requires_membership("admin") #just making it private temporary
def school_enrolment():
    form = FORM(INPUT(_name='dni',_placeholder='Ingrese DNI',_class='form-control', requires=IS_NOT_EMPTY()),
        INPUT(_type='submit',_value='Buscar',_class='btn btn-primary btn-block'),_class='form-group', _id='search_form')
    if form.accepts(request, session):
        response.flash = 'busqueda terminada'
        candidate = db(db.auth_user.username == request.vars.dni).select().first()
        if (candidate == None):
            response.flash = 'El DNI no pertenece a ningun aspirante preinscripto.'
        else:
            redirect(URL('candidate','print_inscription_form.pdf', vars = dict(dni = request.vars.dni)))
    elif form.errors:
        response.flash = 'el formulario tiene errores'

    categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
    return dict(form = form, categories = categories)

def entry_requirements():
        categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
        return dict(categories = categories)

def inscription_instructions():
        categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
        return dict(categories = categories)


def report():
    import os
    response.title = "web2py sample report"

    from gluon.contrib.pyfpdf import FPDF, HTMLMixin
    
    class PDF(FPDF):
        def header(self):
            #LOGOS
            logoIES = os.path.join(request.folder, "static", "images", "logo_ies.png")
            logoMinSeg = os.path.join(request.folder, "static", "images", "logoMinisterio.png")

            self.image(logoIES,165,10,23,26)
            self.set_font('Arial', 'B', 15)

            self.image(logoMinSeg,45,13,80,20)
            # Move to the right
            #self.cell(80)
            # Title
            #self.cell(30, 10, 'Title', 1, 0, 'C')
            # Line break
            #self.ln(20)
    titulo_form = unicode('FORMULARIO UNICO DE INSCRIPCION PARA ASPIRANTES A CADETES DE PRIMER AÑO DEL INSTITUTO DE ENSEÑANZA SUPERIOR DE POLICIA "GRAL. JOSE FRANCISCO DE SAN MARTIN" - CICLO LECTIVO 2019',"utf-8")
    aclaracion = unicode('Los datos consignados en este formulario tienen carácter de "Declaración Jurada". La presentación del presente formulario implica conocer y aceptar los términos de la convocatoria y proceso de selección. La presentación de este formulario es de carácter GRATUITO','utf-8')
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    #pdf.cell(40, 10, 'Hello World!')
    pdf.line(30,37,200,37)
    pdf.line(30,37,30,290)
    pdf.line(200,37,200,290)
    pdf.line(30,290,200,290)
    pdf.line(30,75,200,75)
    pdf.line(120,37,120,75)
    pdf.line(30,240,200,240)
    pdf.dashed_line(35,65,115,65) #FIRMA CONTROLADOR FORMULARIO
    pdf.dashed_line(141,280,195,280) #FIRMA CONTROLADOR FISICO

    pdf.text(40,43,'DOCUMENTACION CONTROLADA')
    pdf.text(138,43,'FORMULARIO NRO:')
    pdf.text(33,50,'FECHA:         /         /    ')
    pdf.text(37,70,'FIRMA Y SELLO DEL CONTROLADOR')
    pdf.text(150,63,'TURNO:')
    pdf.text(125,69,'DIA: 20/12/2018')
    pdf.text(125,74,'HORA: 08:00')
    pdf.set_xy(38,85)
    pdf.multi_cell(157,5, titulo_form,0,'C',False)
    #DATOS DEL POSTULANTE
    pdf.set_font('Arial','',11)
    pdf.text(34,112,'APELLIDO/S: VILLOLDO')
    pdf.text(34,120,'NOMBRE/S: JULIANA ANTONELLA')
    pdf.text(34,128,'FECHA DE NACIMIENTO: 07/08/1994')
    pdf.text(34,136,'EDAD: 21')
    pdf.text(34,144,'NACIONALIDAD: ARGENTINO/A')
    pdf.text(34,152,'COMISARIA JURISDICCIONAL: COMISARIA 9NA')
    pdf.text(34,160,'TEL. FIJO: 4555555')
    pdf.text(34,168,'TEL. FIJO: 3815183732')
    pdf.text(34,176,'CORREO ELECTRONICO: julianavilloldo@live.com')
    pdf.text(34,184,unicode('TITULO SECUNDARIO EXPEDIDO POR: ESC. CONGRESO DE TUCUMÁN','utf-8'))
    pdf.text(38,248, unicode('ESTOS DATOS SERÁN COMPLETADOS POR PERSONAL DEL I.E.S.P "G.J.F.S.M"','utf-8'))
    pdf.text(34,260, 'ESTATURA:..........')
    pdf.text(34,268, 'PESO:..............')
    pdf.text(34,276, 'I.M.C.:............')

    pdf.set_font('Arial','',9)
    pdf.text(34,200,unicode('FIRMA DEL ASPIRANTE AL MOMENTO DE PRESENTAR LA DOCUMENTACIÓN: ...............................................','utf-8'))
    pdf.text(34,208,unicode('ACLARACIÓN...............................................................................................................................................................','utf-8'))
    pdf.set_xy(34,220)
    pdf.multi_cell(160,5, aclaracion,0,'J',False)
    pdf.text(140,285, 'FIRMA Y SELLO DEL CONTROLADOR')


    #NRO DE FORMULARIO
    pdf.set_font('Arial','B',40)
    pdf.text(145,57,'4957')

    #SEGUNDA

    return pdf.output(dest='S')

def excel_report():
    import os
    import xlwt
    from datetime import datetime
    tmpfilename=os.path.join(request.folder,'private',str("tem.xls"))

    font0 = xlwt.Font()
    font0.name = 'Arial'
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.num_format_str = 'DD-MMMM-YYYY'

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sample report')

    ws.write(0, 0, 'Text here', style0)
    ws.write(0, 6, 'More text here', style0)
    ws.write(0, 7, datetime.now(), style1)

    wb.save(tmpfilename)

    data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/vnd.ms-excel'
    return data
    