def index():
	categories = db(db.post_category).select().sort(lambda post_category: len(post_category.name)) #post category sorted by name size
	return dict(categories = categories)

