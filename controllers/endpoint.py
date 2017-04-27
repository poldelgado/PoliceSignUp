import gluon.contrib.simplejson as json


def call():
    session.forget()
    return service()


@service.json
def get_schedule():
	r = db(db.schedule).select().first()
	return dict(r=r)


@service.json
def post_schedule():
	db.schedule.insert(height_schedule=request.vars.height_schedule)
	return dict(status="ok")