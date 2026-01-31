from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from portal.utils import split_csv


def _build_student_text(profile) -> str:
    fields = [
        profile.skills,
        profile.interests,
        profile.projects,
        profile.certifications,
    ]
    return " ".join([field for field in fields if field])


def _build_job_text(job) -> str:
    fields = [
        job.description,
        job.required_skills,
        job.title,
        job.company,
    ]
    return " ".join([field for field in fields if field])


def _rule_based_score(profile, job):
    reasons = []
    score = 0.0

    student_skills = set(split_csv(profile.skills))
    required_skills = set(split_csv(job.required_skills))
    overlap = sorted(student_skills.intersection(required_skills))
    if overlap:
        score += 5 * len(overlap)
        reasons.append(f"Matching skills: {', '.join(s.title() for s in overlap)}")

    if profile.cgpa is not None:
        if profile.cgpa < job.min_cgpa:
            score -= 50
            reasons.append("CGPA below minimum requirement")
        else:
            score += 10
            reasons.append("CGPA meets requirement")

    if profile.branch:
        branches = set(split_csv(job.eligible_branches))
        if profile.branch.strip().lower() in branches:
            score += 8
            reasons.append("Eligible branch match")

    if profile.preferred_locations:
        preferred = set(split_csv(profile.preferred_locations))
        if job.location.strip().lower() in preferred:
            score += 5
            reasons.append("Preferred location match")

    return score, reasons


def recommend_jobs(profile, jobs: List):
    if not jobs:
        return []

    student_text = _build_student_text(profile)
    job_texts = [_build_job_text(job) for job in jobs]

    corpus = [student_text] + job_texts
    if not any(corpus):
        return [
            {"job": job, "score": 0, "reasons": ["Insufficient data for recommendation."]}
            for job in jobs
        ]

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    except ValueError:
        similarity_scores = [0 for _ in jobs]

    results = []
    for job, similarity in zip(jobs, similarity_scores):
        base_score = float(similarity) * 70
        rule_score, reasons = _rule_based_score(profile, job)
        final_score = base_score + rule_score
        final_score = max(0, min(100, final_score))

        if not reasons and student_text:
            reasons.append("Profile text matched job description")
        elif not student_text:
            reasons.append("Complete your profile to get better matches")

        results.append(
            {
                "job": job,
                "score": round(final_score, 1),
                "reasons": reasons,
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results
