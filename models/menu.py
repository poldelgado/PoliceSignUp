# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('IES'),
                  _class="navbar-brand",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu += [
    (T('Insitution'), False, '#', [
        (T('Media'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('History'), False,
         URL(
             'admin', 'default'))
    ]),
    (T('Academic Activity'), False, '#', [
        (T('Career'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Career Program'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Courses'), False, URL('admin', 'default'))
    ]),
    (T('Student Orientation'), False, '#', [
        (T('Item #1'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Item #2'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Item #3'), False, URL('admin', 'default'))
    ]),
    (T('Academic Extension'), False, '#', [
        (T('Workshops'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Agreements'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Inter-institutional development'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Inter-institutional development'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Police and Judicial Education'), False, URL('admin', 'default')),
        LI(_class="divider"),
        (T('Cultural Education'), False, URL('admin', 'default'))
    ]),
    (T('News'), False, URL('admin', 'default', 'site')),
    (T('Campus Virtual'), False, URL('admin', 'default', 'site'))
]

DEVELOPMENT_MENU = False


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, '#', [
            (T('Design'), False, URL('admin', 'default')),
            LI(_class="divider"),
            (T('Controller'), False,
             URL(
                 'admin', 'default', 'edit'))
        ])
    ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
