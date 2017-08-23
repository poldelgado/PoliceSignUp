def index():
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page = int(request.vars.page)
	start = (page-1)*5
	end = page*5
	latestpost = db(db.post).select(orderby=~db.post.date_of_post, limitby=(0,10))
	posts = db(db.post).select(orderby=~db.post.date_of_post, limitby=(start,end))
	categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
	return dict(posts=posts, latestpost=latestpost, categories = categories)

def show():
	post = db(db.post.id == request.args(0)).select().first() or redirect(URL('index'))
	categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
	return dict(post = post, categories = categories)

def show_by_category():
	# if not request.vars.page:
	# 	redirect(URL(vars={'page':1}))
	# else:
	# 	page = int(request.vars.page)
	# start = (page-1)*5
	# end = page*5
	posts = db(db.post.category == request.args(0)).select() or redirect(URL('index'))
	latestpost = db(db.post).select(orderby=~db.post.date_of_post, limitby=(0,10))
	categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
	return dict(posts=posts, categories = categories, latestpost = latestpost)