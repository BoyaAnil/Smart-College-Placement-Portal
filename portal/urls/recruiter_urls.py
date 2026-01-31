from django.urls import path

from .. import views


urlpatterns = [
    path("dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("jobs/new/", views.job_create, name="job_create"),
    path("jobs/<int:job_id>/edit/", views.job_edit, name="job_edit"),
    path("jobs/<int:job_id>/delete/", views.job_delete, name="job_delete"),
    path("jobs/<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path("analytics/", views.analytics, name="analytics"),
]
