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

@auth.requires_membership("admin") #just making it private temporary
def school_enrolment():
    form = FORM(INPUT(_name='dni',_placeholder='Ingrese DNI',_class='form-control', requires=IS_NOT_EMPTY()),
        INPUT(_type='submit',_value='Buscar',_class='btn btn-primary btn-block'),_class='form-group', _id='search_form')
    if form.accepts(request, session):
        response.flash = 'busqueda terminada'
        candidate = db(db.auth_user.username == request.vars.dni).select().first()
        if (candidate == None):
            response.flash = 'El DNI no pertenece a ningun aspirante preinscripto.'
        else:
            redirect(URL('candidate','print_inscription_form', args = (request.vars.dni)))
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