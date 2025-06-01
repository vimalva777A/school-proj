from django.contrib import admin
from .models import YearlyEvent, PeriodTiming, Subject, Class, Exam, ExamSchedule, Teacher, Teacher_Subject_Class_Relation, SubSubject, ClassSubSubjectAssignment, Timetable, BreakPeriod, Parent, Student, Marks
from .models import MediaFile
admin.site.register(YearlyEvent)
admin.site.register([PeriodTiming,MediaFile])
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(Exam)
admin.site.register(ExamSchedule)
admin.site.register(Teacher)
admin.site.register(Teacher_Subject_Class_Relation)
admin.site.register(SubSubject)
admin.site.register(ClassSubSubjectAssignment)
admin.site.register(Timetable)
admin.site.register(BreakPeriod)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Marks)
# admin.py

from django.contrib import admin
from .models import AcademicYear, Holiday

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'total_days', 'working_days']

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['date', 'reason', 'academic_year']
    list_filter = ['academic_year']
