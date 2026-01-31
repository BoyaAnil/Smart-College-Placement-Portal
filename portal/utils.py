from collections import Counter


def split_csv(text: str):
    if not text:
        return []
    return [item.strip().lower() for item in text.split(",") if item.strip()]


def split_projects(text: str):
    if not text:
        return []
    raw = text.replace("\n", ";")
    parts = [item.strip() for item in raw.split(";") if item.strip()]
    if not parts:
        parts = [item.strip() for item in raw.split(",") if item.strip()]
    return parts


SKILL_ROADMAP = {
    "python": [
        "Revise Python fundamentals and data structures.",
        "Build a mini project using APIs and file handling.",
        "Practice coding challenges focused on Python.",
    ],
    "django": [
        "Learn Django models, views, and templates basics.",
        "Build CRUD app with authentication.",
        "Deploy a demo project locally.",
    ],
    "sql": [
        "Learn SELECT, JOIN, GROUP BY queries.",
        "Practice normalization and schema design.",
        "Solve SQL interview questions daily.",
    ],
    "react": [
        "Understand components, state, and props.",
        "Build a small dashboard UI.",
        "Learn API integration with fetch/axios.",
    ],
    "ml": [
        "Revise linear regression and classification basics.",
        "Practice with scikit-learn pipelines.",
        "Build a simple text similarity model.",
    ],
}


def generate_skill_gap(profile, job):
    student_skills = set(split_csv(profile.skills))
    required_skills = set(split_csv(job.required_skills))
    missing = sorted(required_skills - student_skills)

    roadmap = []
    for skill in missing:
        steps = SKILL_ROADMAP.get(
            skill,
            [
                f"Learn {skill} fundamentals.",
                f"Build a mini project using {skill}.",
                f"Practice interview questions on {skill}.",
            ],
        )
        roadmap.append({"skill": skill.title(), "steps": steps})
    return missing, roadmap


def generate_resume_bullets(profile, job):
    projects = split_projects(profile.projects)
    job_skills = split_csv(job.required_skills)
    keywords = [k.title() for k in job_skills[:3]]
    if not keywords:
        keywords = ["Problem Solving", "Collaboration"]

    fallback_project = "Academic project"
    bullets = []
    templates = [
        "Built {project} leveraging {skill} to deliver measurable results.",
        "Designed and implemented {project} focusing on {skill} and clean architecture.",
        "Collaborated on {project} to improve {skill} proficiency and delivery speed.",
        "Optimized {project} by applying {skill} for better performance.",
        "Documented {project} outcomes highlighting {skill} and impact.",
    ]

    for idx, template in enumerate(templates):
        project = projects[idx % len(projects)] if projects else fallback_project
        skill = keywords[idx % len(keywords)]
        bullets.append(template.format(project=project, skill=skill))

    return bullets


def top_skills_from_profiles(profiles, limit=8):
    counter = Counter()
    for profile in profiles:
        counter.update(split_csv(profile.skills))
    return counter.most_common(limit)
