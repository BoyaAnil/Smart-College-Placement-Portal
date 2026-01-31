# Smart College Placement Portal (AI Recommendations)

Final-year placement portal with AI-powered job recommendations, skill-gap roadmaps, and resume bullet suggestions.

## Features
- Role-based authentication (Student, Recruiter/Admin)
- Student profile management (skills, CGPA, projects, certifications, resume upload)
- AI recommendations (TF-IDF similarity + rule-based boosts)
- Job search with filters and apply flow
- Skill-gap roadmap and resume bullet generator
- Recruiter job management and applicant tracking
- Basic analytics (top skills, application status counts)

## Tech Stack
- Django 4+
- SQLite (default), PostgreSQL-ready settings
- Tailwind CSS (CDN)
- scikit-learn (TF-IDF + cosine similarity)

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

For Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Seeded Logins
- Recruiter: `recruiter1` / `Recruiter@123`
- Students: `student1` / `Student@123`, `student2` / `Student@123`, `student3` / `Student@123`

## Screenshots
- Add screenshots here after running the project.

## How Recommendations Work
The recommender builds TF-IDF vectors from student profile text (skills, interests, projects,
certifications) and job text (description + required skills). Cosine similarity provides the
base match score. Rule-based boosts are added for skill overlaps, branch eligibility, preferred
location match, and CGPA compliance. The final score is normalized to 0-100 with human-readable
reasons.
