from gluon.contrib.populate import populate


def test_candidate_register():
	for i in xrange(500):
		populate(db.auth_user,1)
		user = db(db.auth_user).select().last()
		shift = search_shift()
		db.shift_candidate.insert(auth_user = user.id, shift = shift)
    	db.inscription.insert(auth_user = user.id)


def search_shift():
    shifts = db(db.shift).select(orderby = db.shift.shift_date|db.shift.shift_time)
    flag = True
    shift_candidate1 = db(db.shift_candidate.shift == shifts[0].id).select()
    first_id = shifts.first().id
    if shift_candidate1 is None:
        flag = False
        return first_id
    else:
        for i in xrange(1, len(shifts)):
            shift_candidate2 = db(db.shift_candidate.shift == shifts[i].id).select()
            if shift_candidate2 is None:
                flag = False
                return shifts[i].id
            else:
                if len(shift_candidate1) > len(shift_candidate2):
                    flag = False
                    return shifts[i].id
    if flag:
        return first_id
