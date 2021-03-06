def index():
	graduation = db(db.graduation.title == "police").select(db.graduation.ALL, orderby=db.graduation.number|db.graduation.last_name|db.graduation.first_name)
	categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
	return dict(categories = categories, graduation = graduation)

def penitentiary():
	graduation = db(db.graduation.title == "penitentiary").select(db.graduation.ALL, orderby=db.graduation.number|db.graduation.last_name|db.graduation.first_name)
	categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
	return dict(categories = categories, graduation = graduation)