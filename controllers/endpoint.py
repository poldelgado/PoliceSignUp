import gluon.contrib.simplejson as json


def call():
    session.forget()
    return service()


@service.json
def save_document():
    data = json.loads(request.body.read())
    try:
        insert = db.notification.insert(date_of_notification=request.now,
                                    message=data['message'])
        return dict(status="ok", data=data)
    except Exception as e:
        return dict(status="error")

@auth.requires_membership('Admin')
@service.json
def save_post():
	data = json.loads(request.body.read())
	try:
		insert = db.post.insert(title=data['title'],
								date_of_post=data['date_of_post'],
								content=data['content'])
		return dict(status="ok", data=data)
	except Exception as e:
		return dict(status="error")