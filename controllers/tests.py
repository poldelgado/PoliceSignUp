from gluon.contrib.populate import populate
from fpdf import FPDF



def test_candidate_register():
	for i in range(5000):
		populate(db.auth_user,1)
		user = db(db.auth_user).select().last()
		shift = search_shift()
		db.shift_candidate.insert(auth_user = user.id, shift = shift)
    	inscription.insert(auth_user = user.id)



def search_shift():
    shifts = db(db.shift).select(orderby = db.shift.shift_date|db.shift.shift_time)
    flag = True
    shift_candidate1 = db(db.shift_candidate.shift == shifts[0].id).select()
    first_id = shifts.first().id
    if shift_candidate1 is None:
        flag = False
        return first_id
    else:
        for i in range(1, len(shifts)):
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


def print_pdf_sample():
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Arial', 'B', 16)
	pdf.cell(40, 10, 'Hola Mundo!')
	pdf.output('tuto1.pdf', 'F')