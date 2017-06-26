def index():
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page = int(request.vars.page)
	start = (page-1)*10
	end = page*10
	latestposts = db(db.post).select(orderby=~db.post.date_of_post,limitby=(0,50))
	return dict(latestposts = latestposts)

def show():
	post = db(db.post.id == request.args(0)).select().first() or redirect(URL('index'))
	return dict(post = post)
