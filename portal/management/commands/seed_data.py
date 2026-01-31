from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from portal.models import Job, Profile


class Command(BaseCommand):
    help = "Seed initial data for Smart College Placement Portal"

    def handle(self, *args, **options):
        recruiter_user, _ = User.objects.get_or_create(
            username="recruiter1",
            defaults={"email": "recruiter@example.com", "first_name": "Riya", "last_name": "Recruiter"},
        )
        if not recruiter_user.check_password("Recruiter@123"):
            recruiter_user.set_password("Recruiter@123")
            recruiter_user.save()
        Profile.objects.update_or_create(
            user=recruiter_user,
            defaults={"role": Profile.ROLE_RECRUITER, "branch": "HR", "cgpa": 9.0},
        )

        students = [
            {
                "username": "student1",
                "email": "student1@example.com",
                "first_name": "Aarav",
                "last_name": "Mehta",
                "branch": "CSE",
                "year": "Final",
                "cgpa": 8.6,
                "skills": "python, django, sql, javascript, html, css",
                "interests": "web development, backend, cloud",
                "projects": "Placement portal, Smart attendance system",
                "certifications": "AWS Cloud Practitioner",
                "preferred_locations": "bengaluru, remote",
            },
            {
                "username": "student2",
                "email": "student2@example.com",
                "first_name": "Isha",
                "last_name": "Kulkarni",
                "branch": "ECE",
                "year": "Final",
                "cgpa": 7.9,
                "skills": "c++, data structures, embedded systems, iot",
                "interests": "embedded, iot, automation",
                "projects": "Smart home automation, IoT water quality monitor",
                "certifications": "NPTEL Embedded Systems",
                "preferred_locations": "pune, hyderabad",
            },
            {
                "username": "student3",
                "email": "student3@example.com",
                "first_name": "Zoya",
                "last_name": "Khan",
                "branch": "IT",
                "year": "Final",
                "cgpa": 9.1,
                "skills": "machine learning, python, pandas, scikit-learn, sql",
                "interests": "data science, analytics, ai",
                "projects": "Sales forecasting, Resume classifier",
                "certifications": "Google Data Analytics",
                "preferred_locations": "mumbai, remote",
            },
        ]

        for student in students:
            user, _ = User.objects.get_or_create(
                username=student["username"],
                defaults={
                    "email": student["email"],
                    "first_name": student["first_name"],
                    "last_name": student["last_name"],
                },
            )
            if not user.check_password("Student@123"):
                user.set_password("Student@123")
                user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "role": Profile.ROLE_STUDENT,
                    "branch": student["branch"],
                    "year": student["year"],
                    "cgpa": student["cgpa"],
                    "skills": student["skills"],
                    "interests": student["interests"],
                    "projects": student["projects"],
                    "certifications": student["certifications"],
                    "preferred_locations": student["preferred_locations"],
                },
            )

        if Job.objects.filter(recruiter=recruiter_user).exists():
            self.stdout.write(self.style.WARNING("Jobs already seeded. Skipping job creation."))
            return

        today = timezone.localdate()
        jobs = [
            {
                "title": "Backend Developer Intern",
                "company": "TechNova",
                "description": "Work on Django APIs, databases, and deployment automation for internal tools.",
                "required_skills": "python, django, sql, rest",
                "min_cgpa": 7.0,
                "eligible_branches": "cse, it, ece",
                "job_type": "Intern",
                "location": "Bengaluru",
                "salary_min": 15000,
                "salary_max": 25000,
                "last_date": today + timedelta(days=30),
            },
            {
                "title": "Data Analyst",
                "company": "Insightify",
                "description": "Analyze business data, build dashboards, and present insights to stakeholders.",
                "required_skills": "sql, excel, python, data visualization",
                "min_cgpa": 7.5,
                "eligible_branches": "cse, it, ece, eee",
                "job_type": "Full-time",
                "location": "Mumbai",
                "salary_min": 600000,
                "salary_max": 900000,
                "last_date": today + timedelta(days=25),
            },
            {
                "title": "Frontend Engineer",
                "company": "PixelWorks",
                "description": "Develop responsive web interfaces and integrate REST APIs.",
                "required_skills": "javascript, html, css, react",
                "min_cgpa": 7.0,
                "eligible_branches": "cse, it",
                "job_type": "Full-time",
                "location": "Pune",
                "salary_min": 550000,
                "salary_max": 850000,
                "last_date": today + timedelta(days=20),
            },
            {
                "title": "ML Engineer Intern",
                "company": "Neuron Labs",
                "description": "Build ML pipelines and evaluate models for classification tasks.",
                "required_skills": "python, machine learning, scikit-learn, pandas",
                "min_cgpa": 8.0,
                "eligible_branches": "cse, it, ece",
                "job_type": "Intern",
                "location": "Remote",
                "salary_min": 20000,
                "salary_max": 30000,
                "last_date": today + timedelta(days=35),
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudBridge",
                "description": "Maintain CI/CD pipelines and infrastructure automation.",
                "required_skills": "linux, docker, ci/cd, aws",
                "min_cgpa": 7.2,
                "eligible_branches": "cse, it, ece",
                "job_type": "Full-time",
                "location": "Hyderabad",
                "salary_min": 700000,
                "salary_max": 1000000,
                "last_date": today + timedelta(days=28),
            },
            {
                "title": "Business Analyst",
                "company": "StrategyFirst",
                "description": "Gather requirements, document processes, and create KPI reports.",
                "required_skills": "excel, communication, analysis, documentation",
                "min_cgpa": 7.0,
                "eligible_branches": "cse, it, ece, eee, mech",
                "job_type": "Full-time",
                "location": "Delhi",
                "salary_min": 500000,
                "salary_max": 750000,
                "last_date": today + timedelta(days=22),
            },
            {
                "title": "IoT Engineer",
                "company": "SmartGrid",
                "description": "Build IoT solutions using sensors and microcontrollers.",
                "required_skills": "embedded systems, iot, c++, networking",
                "min_cgpa": 7.5,
                "eligible_branches": "ece, eee",
                "job_type": "Full-time",
                "location": "Pune",
                "salary_min": 600000,
                "salary_max": 850000,
                "last_date": today + timedelta(days=26),
            },
            {
                "title": "QA Automation Intern",
                "company": "QualityHub",
                "description": "Write automated tests and maintain regression suites.",
                "required_skills": "python, selenium, testing, automation",
                "min_cgpa": 6.8,
                "eligible_branches": "cse, it, ece",
                "job_type": "Intern",
                "location": "Chennai",
                "salary_min": 12000,
                "salary_max": 20000,
                "last_date": today + timedelta(days=18),
            },
            {
                "title": "Full Stack Developer",
                "company": "AppForge",
                "description": "Develop APIs and modern UI for scalable web products.",
                "required_skills": "python, django, javascript, react, sql",
                "min_cgpa": 8.0,
                "eligible_branches": "cse, it",
                "job_type": "Full-time",
                "location": "Bengaluru",
                "salary_min": 800000,
                "salary_max": 1200000,
                "last_date": today + timedelta(days=32),
            },
            {
                "title": "Data Science Intern",
                "company": "DataWave",
                "description": "Work on data cleaning, feature engineering, and model evaluation.",
                "required_skills": "python, pandas, numpy, machine learning",
                "min_cgpa": 7.8,
                "eligible_branches": "cse, it, ece",
                "job_type": "Intern",
                "location": "Remote",
                "salary_min": 18000,
                "salary_max": 28000,
                "last_date": today + timedelta(days=27),
            },
        ]

        for job_data in jobs:
            Job.objects.create(recruiter=recruiter_user, **job_data)

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))
