from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ai.recommender import recommend_jobs
from .decorators import role_required
from .forms import JobForm, ProfileForm
from .models import Application, Job, Profile
from .utils import generate_resume_bullets, generate_skill_gap, top_skills_from_profiles


def landing(request: HttpRequest) -> HttpResponse:
    latest_jobs = Job.objects.order_by("-created_at")[:6]
    stats = {
        "jobs": Job.objects.count(),
        "applications": Application.objects.count(),
    }
    return render(request, "landing.html", {"latest_jobs": latest_jobs, "stats": stats})


@login_required
@role_required(Profile.ROLE_STUDENT)
def student_dashboard(request: HttpRequest) -> HttpResponse:
    profile, _ = Profile.objects.get_or_create(user=request.user)
    jobs = Job.objects.all().order_by("-created_at")
    recommendations = recommend_jobs(profile, list(jobs))[:5]
    applications = Application.objects.filter(student=request.user).select_related("job")
    return render(
        request,
        "student/dashboard.html",
        {
            "profile": profile,
            "recommendations": recommendations,
            "applications": applications,
        },
    )


@login_required
@role_required(Profile.ROLE_STUDENT)
def student_profile(request: HttpRequest) -> HttpResponse:
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect(reverse("student_profile"))
    else:
        form = ProfileForm(instance=profile)
    return render(request, "student/profile.html", {"form": form, "profile": profile})


@login_required
@role_required(Profile.ROLE_STUDENT)
def student_jobs(request: HttpRequest) -> HttpResponse:
    jobs = Job.objects.all().order_by("-created_at")
    location = request.GET.get("location", "").strip()
    branch = request.GET.get("branch", "").strip()
    job_type = request.GET.get("job_type", "").strip()
    min_cgpa = request.GET.get("min_cgpa", "").strip()

    if location:
        jobs = jobs.filter(location__icontains=location)
    if branch:
        jobs = jobs.filter(eligible_branches__icontains=branch)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if min_cgpa:
        jobs = jobs.filter(min_cgpa__lte=min_cgpa)

    return render(
        request,
        "student/jobs.html",
        {
            "jobs": jobs,
            "filters": {
                "location": location,
                "branch": branch,
                "job_type": job_type,
                "min_cgpa": min_cgpa,
            },
        },
    )


@login_required
@role_required(Profile.ROLE_STUDENT)
def student_job_detail(request: HttpRequest, job_id: int) -> HttpResponse:
    job = get_object_or_404(Job, id=job_id)
    applied = Application.objects.filter(job=job, student=request.user).exists()
    return render(
        request,
        "student/job_detail.html",
        {"job": job, "applied": applied},
    )


@login_required
@role_required(Profile.ROLE_STUDENT)
def apply_job(request: HttpRequest, job_id: int) -> HttpResponse:
    job = get_object_or_404(Job, id=job_id)
    if Application.objects.filter(job=job, student=request.user).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect(reverse("student_job_detail", args=[job.id]))

    Application.objects.create(job=job, student=request.user)
    messages.success(request, "Application submitted successfully.")
    return redirect(reverse("student_job_detail", args=[job.id]))


@login_required
@role_required(Profile.ROLE_STUDENT)
def recommendations(request: HttpRequest) -> HttpResponse:
    profile, _ = Profile.objects.get_or_create(user=request.user)
    jobs = Job.objects.all().order_by("-created_at")
    results = recommend_jobs(profile, list(jobs))
    return render(request, "student/recommendations.html", {"recommendations": results})


@login_required
@role_required(Profile.ROLE_STUDENT)
def roadmap(request: HttpRequest, job_id: int) -> HttpResponse:
    profile, _ = Profile.objects.get_or_create(user=request.user)
    job = get_object_or_404(Job, id=job_id)
    missing, roadmap_items = generate_skill_gap(profile, job)
    return render(
        request,
        "student/roadmap.html",
        {"job": job, "missing_skills": missing, "roadmap_items": roadmap_items},
    )


@login_required
@role_required(Profile.ROLE_STUDENT)
def resume_bullets(request: HttpRequest, job_id: int) -> HttpResponse:
    profile, _ = Profile.objects.get_or_create(user=request.user)
    job = get_object_or_404(Job, id=job_id)
    bullets = generate_resume_bullets(profile, job)
    return render(
        request,
        "student/resume_bullets.html",
        {"job": job, "bullets": bullets},
    )


@login_required
@role_required(Profile.ROLE_RECRUITER)
def recruiter_dashboard(request: HttpRequest) -> HttpResponse:
    jobs = Job.objects.filter(recruiter=request.user).order_by("-created_at")
    application_count = Application.objects.filter(job__recruiter=request.user).count()
    return render(
        request,
        "recruiter/dashboard.html",
        {"jobs": jobs, "application_count": application_count},
    )


@login_required
@role_required(Profile.ROLE_RECRUITER)
def job_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect(reverse("recruiter_dashboard"))
    else:
        form = JobForm()
    return render(request, "recruiter/job_form.html", {"form": form, "is_edit": False})


@login_required
@role_required(Profile.ROLE_RECRUITER)
def job_edit(request: HttpRequest, job_id: int) -> HttpResponse:
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect(reverse("recruiter_dashboard"))
    else:
        form = JobForm(instance=job)
    return render(request, "recruiter/job_form.html", {"form": form, "is_edit": True})


@login_required
@role_required(Profile.ROLE_RECRUITER)
def job_delete(request: HttpRequest, job_id: int) -> HttpResponse:
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == "POST":
        job.delete()
        messages.info(request, "Job deleted.")
        return redirect(reverse("recruiter_dashboard"))
    return render(request, "recruiter/job_confirm_delete.html", {"job": job})


@login_required
@role_required(Profile.ROLE_RECRUITER)
def job_applicants(request: HttpRequest, job_id: int) -> HttpResponse:
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == "POST":
        application_id = request.POST.get("application_id")
        status = request.POST.get("status")
        application = get_object_or_404(Application, id=application_id, job=job)
        application.status = status
        application.save()
        messages.success(request, "Application status updated.")
        return redirect(reverse("job_applicants", args=[job.id]))

    applicants = (
        Application.objects.filter(job=job)
        .select_related("student", "student__profile")
        .order_by("-created_at")
    )
    return render(
        request,
        "recruiter/job_applicants.html",
        {"job": job, "applicants": applicants, "status_choices": Application.STATUS_CHOICES},
    )


@login_required
@role_required(Profile.ROLE_RECRUITER)
def analytics(request: HttpRequest) -> HttpResponse:
    jobs = Job.objects.filter(recruiter=request.user)
    applications = Application.objects.filter(job__recruiter=request.user)
    profiles = Profile.objects.filter(user__applications__job__recruiter=request.user).distinct()
    top_skills = top_skills_from_profiles(profiles)
    status_counts = (
        applications.values("status")
        .annotate(total=Count("status"))
        .order_by("-total")
    )
    return render(
        request,
        "recruiter/analytics.html",
        {
            "total_jobs": jobs.count(),
            "total_applications": applications.count(),
            "top_skills": top_skills,
            "status_counts": status_counts,
        },
    )
