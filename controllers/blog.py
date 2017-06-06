def index():
	latestposts = db(db.post).select(orderby=~db.post.date_of_post,limitby=(0,5))
	return dict(latestposts = latestposts)

def show():
	post = db(db.post.id == request.args(0)).select().first() or redirect(URL('index'))
	return dict(post = post)
