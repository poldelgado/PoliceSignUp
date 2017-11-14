# -*- coding: utf-8 -*-

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
    auth.settings.register_onaccept = add_user_shift
    auth.settings.register_next = URL(c='candidate',f='profile')
    return dict(form = auth.register())

@auth.requires_login()
def forms():
    return dict()

@auth.requires_login()
def inscription_form():
    candidate = db(db.auth_user.id == auth.user_id).select().first()
    inscription = db(candidate.id == db.inscription.auth_user).select().last()
    shift = db(db.shift_candidate.auth_user == auth.user_id).select().last()
    return dict(inscription = inscription, shift = shift)

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

def print_inscription_form():
    candidate = db(db.auth_user.username == request.args(0)).select().first()
    inscription = db(db.inscription.auth_user == candidate.id).select().last()
    shift = db(db.shift_candidate.auth_user == candidate.id).select().last()
    return dict(inscription = inscription, shift = shift)
