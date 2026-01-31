from django.urls import path

from .. import views


urlpatterns = [
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("profile/", views.student_profile, name="student_profile"),
    path("jobs/", views.student_jobs, name="student_jobs"),
    path("jobs/<int:job_id>/", views.student_job_detail, name="student_job_detail"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("recommendations/", views.recommendations, name="recommendations"),
    path("roadmap/<int:job_id>/", views.roadmap, name="roadmap"),
    path("resume-bullets/<int:job_id>/", views.resume_bullets, name="resume_bullets"),
]
