# -*- coding: utf-8 -*-

db.define_table('inscription',
                Field('auth_user', 'reference auth_user'),
                auth.signature,
                singular=T('Candidate Inscription'), plural=T('Candidate Inscriptions'),
                format = lambda r: '%s, %s %s' % (r.auth_user.username, r.auth_user.last_name, r.auth_user.first_name),
                )        



db.define_table('height',
                Field('inscription', 'reference inscription', label=T('inscription')),
                Field('height','double', label=T('height')),
                Field('aproved', 'boolean', label=T('aproved')),                
                Field('available','boolean', label=T('available')),
                auth.signature,
                singular=T('Height'), plural=T('Heights'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.username, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name)
                )


db.define_table('intellectual_exam',
                Field('inscription', 'reference inscription', label = T('Inscription')),
                Field('spanish_language','double', label=T('Spanish Language')),
                Field('history','double', label=T('History')),
                Field('geography','double', label=T('Geography')),
                Field('aproved', 'boolean', label=T('aproved')),                               
                Field('available','boolean', default=False, label=T('available')),
                auth.signature,
                singular=T('Intellectual Exam'), plural=T('Intellectual Exams'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.username, r.inscription.auth_user.first_name, r.inscription.auth_user.first_name),
                )


db.define_table('medical_exam',
                Field('inscription', 'reference inscription', label = T('inscription')),
                Field('exam_result','boolean', label = T('exam result')),
                Field('reason','string', label = T('reason')),
                Field('available','boolean', default=False, label=T('available')),
                auth.signature,
                singular=T('Medical Exam'), plural=T('Medical Exams'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.username, r.inscription.auth_user.fist_name, r.inscription.auth_user.first_name),
                )


db.define_table('physical_exam',
                Field('inscription', 'reference inscription', label = T('inscription')),
                Field('abs_test','integer', label=T('abs_test')),
                Field('arms','integer', label=T('arms')),
                Field('aerobics','integer', label=T('aerobics')),
                Field('aproved','boolean', label=T('aproved')),
                Field('available','boolean', default=False, label=T('available')),
                auth.signature,
                singular=T('Physical Exam'), plural=T('Physicals Exams'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.username, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),
                )


db.define_table('groupal_psychological_examination',
                Field('inscription', 'reference inscription', label = T('inscription')),
                Field('exam_result','boolean', label = T('reason')),
                Field('reason','string', label=T('reason')),
                Field('available','boolean', default=False, label=T('available')),
                auth.signature,
                singular=T('Groupal Psychological Examination'), plural=T('Groupal Psychological Examinations'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.username, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),
                )


db.define_table('psychological_interview',
                Field('inscription', 'reference inscription', label=T('inscription')),
                Field('exam_result','boolean',label=T('exam result')),
                Field('reason','string', label=T('reason')),
                Field('available','boolean', default=False, label=T('available')),
                auth.signature,
                singular=T('Psycological Interview'), plural=T('Psycological Interviews'),
                format = lambda r: '%s, %s %s' % (r.inscription.auth_user.username, r.inscription.auth_user.last_name, r.inscription.auth_user.first_name),
                )

db.define_table('notification',
                Field('auth_user', 'reference auth_user'),
                Field('date_of_notification', 'date', label=T('date')),
                Field('message', 'text', label=T('message')),
                auth.signature,
                singular=T('Notification'), plural=T('Notifications'),
                format = lambda r: '%s, %s %s' % (r.auth_user.username, r.auth_user.last_name, r.auth_user.first_name),

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

db.define_table('post',
                Field('title', 'string'),
                Field('date_of_post', 'date'),
                Field('picture','upload'),
                Field('resume', 'string'),
                Field('content', 'text'),
                
                auth.signature,
                singular= T('Post'), plural=T('Posts'),
                format = lambda r: '%s, %s' % (r.dateof_post, title),
                )