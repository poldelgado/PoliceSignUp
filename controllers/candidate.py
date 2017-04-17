@auth.requires_login()
def index():        
    return dict()


def candidate_registration():
    db.auth_user.username.readable = False
    db.auth_user.username.writable = False
    return dict(form = auth.register())
