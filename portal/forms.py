from django import forms
from django.utils import timezone

from .models import Job, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "branch",
            "year",
            "cgpa",
            "skills",
            "interests",
            "projects",
            "certifications",
            "preferred_locations",
            "phone",
            "resume_file",
        ]
        widgets = {
            "skills": forms.Textarea(attrs={"rows": 2}),
            "interests": forms.Textarea(attrs={"rows": 2}),
            "projects": forms.Textarea(attrs={"rows": 3}),
            "certifications": forms.Textarea(attrs={"rows": 2}),
            "preferred_locations": forms.Textarea(attrs={"rows": 2}),
        }

    def clean_cgpa(self):
        cgpa = self.cleaned_data.get("cgpa")
        if cgpa is not None and (cgpa < 0 or cgpa > 10):
            raise forms.ValidationError("CGPA must be between 0 and 10.")
        return cgpa

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "w-full border border-slate-200 rounded-md px-3 py-2"}
            )
        if "cgpa" in self.fields:
            self.fields["cgpa"].widget.attrs.update({"step": "0.1"})
        if "last_date" in self.fields:
            self.fields["last_date"].widget.attrs.update({"type": "date"})
        if "min_cgpa" in self.fields:
            self.fields["min_cgpa"].widget.attrs.update({"step": "0.1"})


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "company",
            "description",
            "required_skills",
            "min_cgpa",
            "eligible_branches",
            "job_type",
            "location",
            "salary_min",
            "salary_max",
            "last_date",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "required_skills": forms.Textarea(attrs={"rows": 2}),
            "eligible_branches": forms.Textarea(attrs={"rows": 2}),
        }

    def clean_last_date(self):
        last_date = self.cleaned_data.get("last_date")
        if last_date and last_date < timezone.localdate():
            raise forms.ValidationError("Last date must be today or later.")
        return last_date

    def clean(self):
        cleaned = super().clean()
        salary_min = cleaned.get("salary_min")
        salary_max = cleaned.get("salary_max")
        if salary_min is not None and salary_max is not None and salary_max < salary_min:
            self.add_error("salary_max", "Max salary must be >= min salary.")
        return cleaned

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "w-full border border-slate-200 rounded-md px-3 py-2"}
            )
