# -*- coding: utf-8 -*-

db.define_table('inscription',
                Field('auth_user', 'reference auth_user'),
                auth.signature,
                singular=T('Candidate Inscription'), plural=T('Candidate Inscriptions'),
                format = lambda r: '%s, %s %s' % (r.auth_user.ssn, r.auth_user.last_name, r.auth_user.first_name),
                )        



db.define_table('height',
                Field('inscription', 'reference inscription'),
                Field('height','double'),
                Field('available','boolean'),
                auth.signature,
                singular=T('Height'), plural=T('Heights'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.ssn, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),

                )


db.define_table('intellectual_exam',
                Field('inscription', 'reference inscription'),
                Field('spanish_language','double'),
                Field('history','double'),
                Field('geography','double'),
                Field('available','boolean', default=False),
                auth.signature,
                singular=T('Intellectual Exam'), plural=T('Intellectual Exams'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.ssn, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),
                )


db.define_table('medical_exam',
                Field('inscription', 'reference inscription'),
                Field('exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False),
                auth.signature,
                singular=T('Medical Exam'), plural=T('Medical Exams'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.ssn, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),
                )


db.define_table('physical_exam',
                Field('inscription', 'reference inscription'),
                Field('abs_test','integer'),
                Field('arms','integer'),
                Field('aerobics','integer'),
                Field('available','boolean', default=False),
                auth.signature,
                singular=T('Physical Exam'), plural=T('Physicals Exams'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.ssn, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),
                )


db.define_table('groupal_psychological_examination',
                Field('inscription', 'reference inscription'),
                Field('exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False),
                auth.signature,
                singular=T('Groupal Psychological Examination'), plural=T('Groupal Psychological Examinations'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.ssn, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),
                )


db.define_table('psychological_interview',
                Field('inscription', 'reference inscription'),
                Field('exam_result','boolean'),
                Field('reason','string'),
                Field('available','boolean', default=False),
                auth.signature,
                singular=T('Psycological Interview'), plural=T('Psycological Interviews'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.ssn, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),
                )

db.define_table('notification',
                Field('auth_user', 'reference auth_user'),
                Field('date_of_notification', 'date'),
                Field('message', 'text'),
                auth.signature,
                singular=T('Notification'), plural=T('Notifications'),
                format = lambda r: '%s, %s %s' % (r.auth_user.ssn, r.auth_user.last_name, r.auth_user.first_name),

                )
db.define_table('schedule',
                Field('height_schedule', 'text'),
                Field('intellectual_exam_schedule', 'text'),
                Field('medical_exam_schedule', 'text'),
                Field('physical_exam_schedule', 'text'),
                Field('intellectual_exam_schedule', 'text'),
                Field('groupal_psychological_examination_schedule', 'text'),
                Field('psychological_interview_schedule', 'text'),
                auth.signature,
                singular=T('Schedule'), plural=T('Schedules'),
                #format = '%(user_id)s'
                )