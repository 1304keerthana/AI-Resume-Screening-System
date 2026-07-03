from utils.skills import extract_skills

def analyze_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # Keywords to detect sections
    education_keywords = [
        "b.tech", "b.e", "b.sc", "m.sc", "m.tech",
        "degree", "university", "college"
    ]

    project_keywords = [
        "project", "projects", "developed", "built", "implemented"
    ]

    experience_keywords = [
        "experience", "intern", "worked", "employment", "company"
    ]

    education_found = any(word in resume_text.lower() for word in education_keywords)
    projects_found = any(word in resume_text.lower() for word in project_keywords)
    experience_found = any(word in resume_text.lower() for word in experience_keywords)
    return {
    "matched": len(matched_skills),
    "total": len(jd_skills),
    "missing": len(missing_skills),
    "education": education_found,
    "projects": projects_found,
    "experience": experience_found,
    "matched_skills": matched_skills,
    "missing_skills": missing_skills
    }
