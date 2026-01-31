from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    ROLE_STUDENT = "student"
    ROLE_RECRUITER = "recruiter"
    ROLE_CHOICES = [
        (ROLE_STUDENT, "Student"),
        (ROLE_RECRUITER, "Recruiter/Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    branch = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=20, blank=True)
    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    preferred_locations = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    resume_file = models.FileField(upload_to="resumes/", null=True, blank=True)

    def clean(self) -> None:
        if self.cgpa is not None and (self.cgpa < 0 or self.cgpa > 10):
            raise ValidationError({"cgpa": "CGPA must be between 0 and 10."})

    def __str__(self) -> str:
        return f"{self.user.username} ({self.get_role_display()})"


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("Intern", "Intern"),
        ("Full-time", "Full-time"),
    ]

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    min_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    eligible_branches = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    last_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        if self.last_date < timezone.localdate():
            raise ValidationError({"last_date": "Last date must be today or later."})
        if self.salary_max < self.salary_min:
            raise ValidationError({"salary_max": "Max salary must be >= min salary."})

    def __str__(self) -> str:
        return f"{self.title} at {self.company}"


class Application(models.Model):
    STATUS_APPLIED = "Applied"
    STATUS_SHORTLISTED = "Shortlisted"
    STATUS_REJECTED = "Rejected"
    STATUS_HIRED = "Hired"

    STATUS_CHOICES = [
        (STATUS_APPLIED, "Applied"),
        (STATUS_SHORTLISTED, "Shortlisted"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_HIRED, "Hired"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_APPLIED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["job", "student"], name="unique_application")
        ]

    def __str__(self) -> str:
        return f"{self.student.username} -> {self.job.title} ({self.status})"
