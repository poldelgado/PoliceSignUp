def index():
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page = int(request.vars.page)
	start = (page-1)*5
	end = page*5
	latestpost = db(db.post).select(orderby=~db.post.date_of_post, limitby=(0,10))
	posts = db(db.post).select(orderby=~db.post.date_of_post, limitby=(start,end))
	return dict(posts=posts, latestpost=latestpost)

def show():
	post = db(db.post.id == request.args(0)).select().first() or redirect(URL('index'))
	return dict(post = post)