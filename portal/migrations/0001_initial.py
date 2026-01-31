from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("student", "Student"), ("recruiter", "Recruiter/Admin")], default="student", max_length=20)),
                ("branch", models.CharField(blank=True, max_length=100)),
                ("year", models.CharField(blank=True, max_length=20)),
                ("cgpa", models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])),
                ("skills", models.TextField(blank=True)),
                ("interests", models.TextField(blank=True)),
                ("projects", models.TextField(blank=True)),
                ("certifications", models.TextField(blank=True)),
                ("preferred_locations", models.TextField(blank=True)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("resume_file", models.FileField(blank=True, null=True, upload_to="resumes/")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("company", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("required_skills", models.TextField()),
                ("min_cgpa", models.DecimalField(decimal_places=2, max_digits=4, validators=[MinValueValidator(0), MaxValueValidator(10)])),
                ("eligible_branches", models.TextField()),
                ("job_type", models.CharField(choices=[("Intern", "Intern"), ("Full-time", "Full-time")], max_length=20)),
                ("location", models.CharField(max_length=100)),
                ("salary_min", models.PositiveIntegerField()),
                ("salary_max", models.PositiveIntegerField()),
                ("last_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("recruiter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="jobs", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("Applied", "Applied"), ("Shortlisted", "Shortlisted"), ("Rejected", "Rejected"), ("Hired", "Hired")], default="Applied", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to="portal.job")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name="application",
            constraint=models.UniqueConstraint(fields=("job", "student"), name="unique_application"),
        ),
    ]
