def index():
    form = SQLFORM.smartgrid(db.auth_user)
    return dict(form = form)

def schedule():
    form = SQLFORM(db.schedule)
    return dict(form = form)
