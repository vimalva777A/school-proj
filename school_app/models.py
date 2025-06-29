from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from django.db import models
from django.utils import timezone
from datetime import timedelta, date



class AcademicYear(models.Model):
    name = models.CharField(max_length=50, help_text="e.g., 2024-2025")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def total_days(self):
        """Returns the total number of calendar days in the academic year."""
        return (self.end_date - self.start_date).days + 1

    def get_all_dates(self):
        """Generates a list of all dates from start_date to end_date."""
        current = self.start_date
        dates = []
        while current <= self.end_date:
            dates.append(current)
            current += timedelta(days=1)
        return dates

    def working_days(self, exclude_weekends=True):
        """
        Returns total working days in the academic year, excluding holidays.
        Weekends are excluded unless `exclude_weekends=False`.
        """
        holidays = set(self.holiday_set.values_list('date', flat=True))
        working_days_count = 0
        current = self.start_date

        while current <= self.end_date:
            if exclude_weekends and current.weekday() >= 5:
                current += timedelta(days=1)
                continue
            if current not in holidays:
                working_days_count += 1
            current += timedelta(days=1)

        return working_days_count

    def working_days_upto_today(self, exclude_weekends=True):
        """
        Returns working days from start_date up to today, excluding holidays.
        """
        today = date.today()
        if today < self.start_date:
            return 0
        if today > self.end_date:
            today = self.end_date

        holidays = set(self.holiday_set.filter(date__lte=today).values_list('date', flat=True))
        working_days_count = 0
        current = self.start_date

        while current <= today:
            if exclude_weekends and current.weekday() >= 5:
                current += timedelta(days=1)
                continue
            if current not in holidays:
                working_days_count += 1
            current += timedelta(days=1)

        return working_days_count

    def __contains__(self, check_date):
        """Allows usage like `if some_date in academic_year:`"""
        return self.start_date <= check_date <= self.end_date


class SchoolProfile(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    principal_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Holiday(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=100)

    class Meta:
        unique_together = ('academic_year', 'date')
        verbose_name = "Holiday"
        verbose_name_plural = "Holidays"
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.reason}"


# Yearly Event Model
class YearlyEvent(models.Model):
    CATEGORY_CHOICES = [
        ("Exam", "Exam"),
        ("Meeting", "Meeting"),
        ("Extracurricular", "Extracurricular"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Other")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.category})"

class PeriodTiming(models.Model):
    period = models.IntegerField(unique=True)
    default_start_time = models.TimeField()
    default_end_time = models.TimeField()

    def __str__(self):
        return f"Period {self.period}: {self.default_start_time} - {self.default_end_time}"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    


class Class(models.Model):
    name = models.CharField("Class Name", max_length=100, unique=True)
    class_teacher = models.ForeignKey(
        "Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teaching_classes",
        help_text="Primary teacher responsible for this class"
    )
    syllabus = models.TextField(
        "Syllabus Overview", blank=True, null=True,
        help_text="Brief overview or topics covered"
    )
    academic_year = models.ForeignKey(
        "AcademicYear",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Academic year this class is associated with"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=100 , unique=True)

    def __str__(self):
        return self.name

# class ExamDate(models.Model):
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="exam_dates")
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.exam.name} - {self.date}"

class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="schedules")
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="class_exams")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    total_marks = models.IntegerField()

    class Meta:
        unique_together = ('exam', 'school_class', 'subject')  # Now each cell is unique

    def __str__(self):
        return f"{self.exam.name} - {self.school_class.name} - {self.subject.name} on {self.date}"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    employee_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    login_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    subjects = models.ManyToManyField("Subject", blank=True)
    assigned_classes = models.ManyToManyField("Class", blank=True)
    
    # Change related_name to avoid clash
    class_teacher_of = models.ForeignKey(
        "Class", 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name="class_teachers"  # Renamed this related_name to avoid clash
    )

    is_class_teacher = models.BooleanField(default=False)
    extra_skills = models.TextField(blank=True, null=True)
    is_absent = models.BooleanField(default=False)
    max_teaching_periods = models.PositiveIntegerField(default=6)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # First save to assign an ID

        if not self.login_id:
            self.login_id = f"T{self.pk:05d}"  # Format ID correctly
            super().save(update_fields=["login_id"])  # Update only login_id

    def __str__(self):
        return f"{self.name} - {self.login_id}"


class TeacherAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    reason = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('teacher', 'date')

class Teacher_Subject_Class_Relation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Allow NULL
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigned_classes = models.ManyToManyField(Class)
    is_priority_substitute = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        assigned_classes_str = ", ".join(cls.name for cls in self.assigned_classes.all())
        teacher_name = self.teacher.name if self.teacher else "No Teacher"  # ✅ Handle NULL teacher
        return f"{teacher_name} - {self.subject.name} ({assigned_classes_str})"


class SyllabusPerformance(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SoftSkillPerformance(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub_subjects")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.subject.name})"

# models.py

class ClassSubSubjectAssignment(models.Model):
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="subsubject_assignments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="class_assignments")
    subsubject = models.ForeignKey(SubSubject, on_delete=models.CASCADE, related_name="class_assignments")
    
    class Meta:
        unique_together = ('school_class', 'subject', 'subsubject')

    def __str__(self):
        return f"{self.school_class.name} - {self.subject.name} - {self.subsubject.name}"


class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    PERIOD_CHOICES = [(i, f"Period {i}") for i in range(1, 10)]
    
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="timetable")
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    date = models.DateField(null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)  # Assuming this is a foreign key to Teacher
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)  # Assuming this is a foreign key to Subject
    period = models.PositiveSmallIntegerField(choices=PERIOD_CHOICES)  # Changed to PositiveSmallIntegerField
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    teacher_subject = models.ForeignKey(Teacher_Subject_Class_Relation, on_delete=models.SET_NULL, null=True, blank=True)
    is_break = models.BooleanField(default=False)

    def __str__(self):
        if self.is_break:
            return f"{self.day} - Period {self.period} ({self.start_time} - {self.end_time}) (Break)"
        elif self.teacher_subject:
            return f"{self.day} - Period {self.period} ({self.start_time} - {self.end_time}) - {self.teacher_subject.teacher.name} ({self.teacher_subject.subject.name})"
        else:
            return f"{self.day} - Period {self.period} ({self.start_time} - {self.end_time}) (Free)"


class BreakPeriod(models.Model):
    BREAK_TYPE_CHOICES = [
        ("Short", "Short Break"),
        ("Lunch", "Lunch Break"),
    ]
    day = models.CharField(max_length=10, choices=Timetable.DAY_CHOICES)
    period = models.IntegerField(choices=Timetable.PERIOD_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_type = models.CharField(max_length=10, choices=BREAK_TYPE_CHOICES)



from django.contrib.auth.models import AbstractUser
from django.db import models


class Parent(models.Model):

    RELATION_CHOICES = [
        ("Father", "Father"),
        ("Mother", "Mother"),
        ("Local Guardian", "Local Guardian"),
    ]

    name = models.CharField(max_length=100)  # ✅ Add this field
    relation_type = models.CharField(max_length=20, choices=RELATION_CHOICES, default="Father")  # ✅ NEW
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    phone = models.CharField(max_length=15, unique=False)
    aadhar = models.CharField(max_length=12, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True) 
    def __str__(self):
        return self.username


class Student(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),]
    CATEGORY_CHOICES = [
        ("General", "General"),
        ("OBC", "OBC"),
        ("SC", "SC"),
        ("ST", "ST"),
        ("Others", "Others"),
    ]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Male") 
    aadhar = models.CharField(max_length=12, unique=True)
    pen = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, unique=False ,blank=True, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    address = models.TextField()
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="students")
    roll_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="General")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.roll_number:  # Generate only if roll number is empty
            last_student = Student.objects.filter(assigned_class=self.assigned_class).order_by('-id').first()
            last_roll = int(last_student.roll_number.split('-')[-1]) if last_student and last_student.roll_number else 0
            new_roll_number = f"C{self.assigned_class.id}-{last_roll + 1:03d}"
            
            # Ensure roll number is unique
            while Student.objects.filter(assigned_class=self.assigned_class, roll_number=new_roll_number).exists():
                last_roll += 1
                new_roll_number = f"C{self.assigned_class.id}-{last_roll + 1:03d}"

            self.roll_number = new_roll_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.roll_number}"

    class Meta:
        unique_together = ("assigned_class", "roll_number")  # Ensure uniqueness per class

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.FloatField(null=True, blank=True)  # ✅ Allow NULL values

    total_obtained_marks = models.FloatField(null=True, blank=True)  # Renamed from total_marks
    remarks = models.TextField(blank=True, null=True)  
    
    class Meta:
        unique_together = ('student', 'exam', 'subject')  # ⛔ Prevent duplicates

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks_obtained}/{self.total_obtained_marks}"

class StudentSubjectRemark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Remark for {self.student.name} in {self.subject.name}"
class InternalAssessment(models.Model):
    school_class = models.ForeignKey('Class', on_delete=models.CASCADE, related_name="assessments")
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name="internal_assessments")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name="assessments")
    subsubject = models.ForeignKey('SubSubject', on_delete=models.CASCADE, related_name="assessments", null=True, blank=True)

    syllabus_assessment = models.CharField(max_length=255, null=True, blank=True)  
    softskill_assessment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = (
            'student',
            'school_class',
            'exam',
            'subject',
            'subsubject',
        )
        verbose_name = "Internal Assessment"
        verbose_name_plural = "Internal Assessments"

    def __str__(self):
        sub_name = self.subsubject.name if self.subsubject else "General"
        student_name = self.student.name if self.student else "N/A"
        return f"{self.school_class.name} | {self.exam.name} | {self.subject.name} - {sub_name} | {student_name}"

class SkillOrDevelopmentArea(models.Model):
    school_class = models.ForeignKey('Class', on_delete=models.CASCADE, related_name="skill_development_areas")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name="skill_development_areas")
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="skill_development_areas")

    syllabus_assessment = models.CharField(max_length=255, null=True, blank=True)  
    softskill_assessment = models.CharField(max_length=255, null=True, blank=True)
    assessment_date = models.DateField(default=timezone.now)  # NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: track when created
    updated_at = models.DateTimeField(auto_now=True)      # Optional: track when updated

    class Meta:
        unique_together = ('student', 'school_class', 'subject', 'assessment_date')

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} Skills"

class StudentAttendance(models.Model):
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ])

    class Meta:
            unique_together = ('student', 'date')
            ordering = ['-date']

    def __str__(self):
            return f"{self.student.name} - {self.date} - {self.status}"
    
MEDIA_TYPE_CHOICES = (
    ('image', 'Image'),
    ('video', 'Video'),
)

class MediaFile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.ImageField(upload_to='uploads/')  # Change to ImageField for image-specific uploads
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    category = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class SchoolDay(models.Model):
    # For example: Monday, Tuesday, etc.
    DAY_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    day_name = models.CharField(max_length=3, choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return self.get_day_name_display()
    
class TransferredStudent(models.Model):
    name = models.CharField(max_length=255)
    parent_name = models.CharField(max_length=255)
    parent_email = models.EmailField(null=True, blank=True)
    student_class = models.CharField(max_length=100, null=True, blank=True)  # 
    parent_phone = models.CharField(max_length=20)
    marks_snapshot = models.JSONField()  # To store marks data
    transferred_on = models.DateTimeField(auto_now_add=True)


class AITimetableEntry(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True)
    school_day = models.ForeignKey(SchoolDay, on_delete=models.CASCADE)
    period_number = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('class_assigned', 'school_day', 'period_number')
        ordering = ['school_day', 'period_number']

    def __str__(self):
        return f"{self.class_assigned} - {self.subject} - {self.school_day} Period {self.period_number}"

# Optional: Stores AI generation settings
class AITimetableSettings(models.Model):
    num_periods = models.PositiveIntegerField(default=8)
    period_duration = models.PositiveIntegerField(help_text="In minutes")
    gap_between_periods = models.PositiveIntegerField(help_text="In minutes", default=5)
    break_after_period_1 = models.PositiveIntegerField(default=3)
    break_after_period_2 = models.PositiveIntegerField(default=6)
    break_duration = models.PositiveIntegerField(help_text="In minutes", default=15)
    start_hour = models.PositiveIntegerField(default=8)
    start_minute = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"AI Timetable Settings ({self.num_periods} periods, {self.period_duration} mins)"


class DailyTimeTableEntry(models.Model):
    date = models.DateField()
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    period_number = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('date', 'classroom', 'period_number')

class SubstituteAssignment(models.Model):
    date = models.DateField()
    period_number = models.PositiveSmallIntegerField()
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    original_teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='original_assignments')
    substitute_teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='substitute_assignments',null=True, blank=True)

