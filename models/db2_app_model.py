# -*- coding: utf-8 -*-

db.define_table('inscription',
                Field('candidate', db.auth_user),
                auth.signature,
                singular='Candidate Inscription', plural='Candidate Inscriptions',
                format = '%(candidate)s',
                )


db.define_table('height',
                Field('inscription_id', db.inscription),
                Field('height','double'),
                Field('available','boolean'),
                auth.signature,
                singular='Height Examination', plural='Height Examinations',
                format = '%(height)s'
                )


db.define_table('intellectual_exam',
                Field('inscription_id', db.inscription),
                Field('spanish_language','double'),
                Field('history','double'),
                Field('geography','double'),
                Field('available','boolean', default=False),
                auth.signature,
                singular='Intellectual Exam', plural='Intellectual Exams',
                #format = '%(user_id)s'
                )


db.define_table('medical_exam',
                Field('inscription_id', db.inscription),
                Field('exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False),
                auth.signature,
                singular='Medical Exam', plural='Medical Exams',
                #format = '%(user_id)s'
                )


db.define_table('physical_exam',
                Field('inscription_id', db.inscription),
                Field('abs_test','integer'),
                Field('arms','integer'),
                Field('aerobics','double'),
                Field('available','boolean', default=False),
                auth.signature,
                singular='Physical Exam', plural='Physicals Exams',
                #format = '%(user_id)s'
                )


db.define_table('groupal_psychological_examination',
                Field('inscription_id', db.inscription),
                Field('exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False),
                auth.signature,
                singular='Groupal Psychological Examination', plural='Groupal Psychological Examinations',
                #format = '%(user_id)s'
                )


db.define_table('psycological_interview',
                Field('inscription_id', db.inscription),
                Field('exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False),
                auth.signature,
                singular='Psycological Interview', plural='Psycological Interviews',
                #format = '%(user_id)s'
                )

db.define_table('notification',
                Field('candidate', db.auth_user),
                Field('date_of_notification', 'date'),
                Field('message', 'text'),
                auth.signature,
                singular='Schedule', plural='Schedules',
                )
db.define_table('schedule',
                Field('height_schedule', 'text'),
                Field('intellectual_exam_schedule', 'text'),
                Field('medical_exam_schedule', 'text'),
                Field('physical_exam_schedule', 'text'),
                Field('intellectual_exam_schedule', 'text'),
                Field('groupal_psychological_examination_schedule', 'text'),
                Field('psycological_interview_schedule', 'text'),
                auth.signature,
                singular='Schedule', plural='Schedules',
                #format = '%(user_id)s'
                )