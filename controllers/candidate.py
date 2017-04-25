@auth.requires_login()
def index():
    user_profile = db(db.auth_user.id == auth.user_id).select().first()
    inscription = db(user_profile.id == db.inscription.user_id).select().last()
    exams = db(((db.inscription.user_id == auth.user_id))
    & (((db.height.inscription_id == db.inscription.id) | (db.height.id == None))
    & ((db.intellectual_exam.inscription_id == db.inscription.id) | (db.intellectual_exam.id == None))
    & ((db.medical_exam.inscription_id == db.inscription.id) | (db.medical_exam.id == None))
    & ((db.physical_exam.inscription_id == db.inscription.id) | (db.physical_exam.id == None))
    & ((db.groupal_psychological_examination.inscription_id == db.inscription.id) | (db.groupal_psychological_examination.id == None))
    & ((db.psycological_interview.inscription_id == db.inscription.id) | (db.psycological_interview.id == None)))).select().first()
    auth.settings.login_next = URL(c='candidate',f='index')
    return dict(user = user_profile,inscription = inscription, exams = exams)


def candidate_registration():
    db.auth_user.username.readable = False
    db.auth_user.username.writable = False
    auth.settings.register_next = URL(c='candidate',f='index')
    return dict(form = auth.register())
