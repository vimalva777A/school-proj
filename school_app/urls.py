from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    # path('run-migrations/', views.run_migrations), # https://school-proj.onrender.com/run-migrations/
    path('list-migrations/', views.list_migrations), #https://school-proj.onrender.com/list-migrations/


    path('enroll_student/', views.enroll_student, name='enroll_student'),
    path('enroll-teacher/', views.enroll_teacher, name='enroll_teacher'),
    path('delete-class-subj-tr/',views. delete_class_subj_Tr, name='delete_class_subj_Tr'),
    path('create_class/', views.create_class, name='create_class'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path("create-sub-subject/", views.create_sub_subject, name="create_sub_subject"),
    path('media/delete/<int:media_id>/', views.delete_media, name='delete_media'),

    # timetable loading 
    path('get_teachers_by_class/<int:class_id>/', views.get_teachers_by_class, name='get_teachers_by_class'),
    path('get_subjects_by_teacher_and_class/<int:teacher_id>/<int:class_id>/', views.get_subjects_by_teacher_and_class, name='get_subjects_by_teacher_and_class'),
    path('get_saved_timetable/<str:day>/', views.get_saved_timetable, name='get_saved_timetable'),

    # URL to load the dedicated Add Sub-Subject page with proper dropdown

        # Sub subject handling urls
        # AJAX URL to get subjects for a selected class
        path('ajax/get-subjects-by-class/<int:class_id>/', views.get_subjects_by_class, name='get_subjects_by_class'),
        
        # AJAX URL to get sub-subjects for a selected subject (to list below)
        path('ajax/get-subsubjects-by-subject/<int:subject_id>/', views.get_subsubjects_by_subject, name='get_subsubjects_by_subject'),

        # URL to create a new sub-subject
        path('ajax/create-sub-subject/', views.create_sub_subject, name='create_sub_subject'),
        path('class_subject_subsubject_list/', views.list_class_subjects_subsubjects, name='class_subject_subsubject_list'),
        path('ajax/delete-subsubject/<int:subsubject_id>/', views.delete_subsubject, name='delete_subsubject'),
        path('update-internal-marks/', views.update_internal_marks, name='update_internal_marks'),

        
    # URL to list subjects (and sub‑subjects) for a specific class
    path("get_yearly_events/", views.get_yearly_events, name="get_yearly_events"),
    path('get_teachers_subjects/', views.get_teachers_subjects, name='get_teachers_subjects'),
    path('get_teacher_mappings/', views.get_teacher_mappings, name='get_teacher_mappings'),
    path('save_timetable/', views.save_timetable, name='save_timetable'),
    path("get_events/", views.get_events, name="get_events"),
    path("add_event/", views.add_event, name="add_event"),
    path("update_event/", views.update_event, name="update_event"),

    path('check_teacher_exists/', views.check_teacher_exists, name='check_teacher_exists'),
    path("assign_subjects_to_class/", views.assign_subjects_to_class, name="assign_subjects_to_class"),
    path("get_assigned_subjects/<int:class_id>/", views.get_assigned_subjects, name="get_assigned_subjects"),
    path("enroll_teacher/", views.enroll_teacher, name="enroll_teacher"),
    path('get_teacher_availability/', views.get_teacher_availability, name='get_teacher_availability'),

    path('save_timetable/', views.save_timetable, name='save_timetable'),
    path('daywise_timetable_entry/', views.daywise_timetable_entry_view, name='daywise_timetable_entry'),
    path('entities/<str:timetable_type>/', views.get_entities, name='get_entities'),
    path('get_teachers_subjects_sorted/<int:class_id>/', views.get_teachers_subjects_sorted, name='get_teachers_subjects_sorted'),
    path('check_timetable_conflicts/', views.check_timetable_conflicts, name='check_timetable_conflicts'),

    path("get_classes/", views.get_classes, name="get_classes"),
    path("get_timetable/<int:class_id>/", views.get_timetable, name="get_timetable"),
    path("update_timetable/", views.update_timetable, name="update_timetable"),
    path("get_classes", views.get_classes, name="get_classes"),

    path("delete_subject", views.delete_subject, name="delete_subject"),

    path("get_teachers/", views.get_teachers, name="get_teachers"),
    path("get_subjects/",views. get_subjects, name="get_subjects"),
    path("get_teachers_by_class/<int:class_id>/", views.get_teachers_by_class, name="get_teachers_by_class"),
    path("get_subjects_by_teacher/<int:teacher_id>/", views.get_subjects_by_teacher, name="get_subjects_by_teacher"),
    path("get_available_teachers/<int:period>/", views.get_available_teachers, name="get_available_teachers"),
    #  path("save_timetable", views.save_timetable, name="save_timetable"),
    path('save_timetable/', views.save_timetable, name='save_timetable'),
    path("create_exam/", views.create_exam, name="create_exam"),
    path("delete_exam/<int:exam_id>/", views.delete_exam, name="delete_exam"),
    path("export_exam_schedule/", views.export_exam_schedule, name="export_exam_schedule"),
    path("class_detail/<int:class_id>/", views.class_detail_view, name="class_detail"),  # ✅ Fix this!
 path('update_marks/', views.update_marks, name='update_marks'), #saving marks from teachers dashboard
    path("get_exam_schedule/<int:exam_id>/", views.get_exam_schedule, name="get_exam_schedule"),
    path("create_class", views.create_class, name="create_class"),

    path("save-internal-marks/", views.save_internal_marks_by_class, name="save_internal_marks_by_class"),
    path('attendance/save/', views.save_attendance, name='save_attendance'),
    path('media/delete/<int:media_id>/', views.delete_media, name='delete_media'),  # Delete media URL

    # Pages urls are in down
    path('index_view', views.index_view, name='index'),
    path('media_upload', views.media_upload, name='media_upload'),
    path('media_gallery', views.media_gallery, name='media_gallery'),
    path("class_creation_pg", views.class_creation_pg, name="class_creation_pg"),
    path("class_subject_management_pg", views.class_subject_management_pg, name="class_subject_management_pg"),
    path("teacher_enrollment_pg", views.teacher_enrollment_pg, name="teacher_enrollment_pg"),
    path('student_enrollment', views.student_enrollment, name='student_enrollment'),
    path("exam_department", views.exam_department, name="exam_department"),

    path('subsubject_management_pg', views.subsubject_management_pg, name='subsubject_management_pg'),
    path('internal_assessment_view', views.internal_assessment_view, name='internal_assessment_view'),
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('assessment_table', views.assessment_table, name='assessment_table'),

    path('principal_dashboard', views.principal_dashboard, name='principal_dashboard'),
    path("year_planner/", views.year_planner_view, name="year_planner"),

    # Time tables
    path("timetable_view", views.timetable_view, name="timetable_view"),
    path("teacher_timetable_pg", views.teacher_timetable_pg, name="teacher_timetable_pg"),
    path("class_timetable_page", views.class_timetable_page, name="class_timetable_page"),  # Renders HTML page
    path("free_teachers_view",  views.free_teachers_view, name="free_teachers"),
    path("classroom_overview", views.classroom_overview, name="classroom_overview"),
    path('teacher_subject_class_table', views.teacher_subject_class_table, name='teacher_subject_class_table'),
    path("get_free_teachers_timetable/", views.get_free_teachers_timetable, name="get_free_teachers_timetable"),
    path("get_teacher_timetable/<int:teacher_id>/", views.get_teacher_timetable, name="get_teacher_timetable"),
    path("class_timetable/", views.class_timetable_page, name="class_timetable_page"),
    path("get_class_timetable/<int:class_id>/", views.get_class_timetable, name="get_class_timetable"),  # Fetches timetable data
    path("parent_dashboard", views.parent_dashboard, name="parent_dashboard"),
    # path("logout/", views.parent_logout, name="logout"),
    path("parent_logout/", views.parent_logout, name="parent_logout"),
    path("team_login", views.team_login, name="team_login"), 
    #   internal-assessment-entry/
    path("internal_assessment_entry", views.internal_assessment_entry, name="internal_assessment_entry"),
# student attendance 
    path('attendance_view', views.attendance_view, name='attendance_view'),
    path('attendance_list_view', views.attendance_list_view, name='attendance_list_view'),
    path('student_assessment_report', views.student_assessment_report, name='student_assessment_report'), 
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student/<int:student_id>/internal-assessment/', views.student_internal_assessment, name='student_internal_assessment'),
    
    path("solution_based_sorting_view",views.solution_based_sorting_view, name="solution_based_sorting_view"),

    path('create_academic_year', views.create_academic_year, name='create_academic_year'),
    path('academic_year_list', views.academic_year_list, name='academic_year_list'),
    path('working-days/<int:year_id>/', views.working_days_summary, name='working_days_summary'),
    path('academic-year/edit/<int:pk>/', views.edit_academic_year, name='academicyear_change'),
    path('holiday/add/', views.add_holiday, name='holiday_add'),

    path('yearly_event_list/', views.event_list, name='yearly_event_list'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),

     path('contact_page', views.contact_page, name='contact_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    