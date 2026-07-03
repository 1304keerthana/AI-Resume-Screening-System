def generate_feedback(score, analysis):

    strengths = []
    improvements = []
    suggestions = []

    # Strengths
    if analysis["matched"] >= 5:
        strengths.append("Strong technical skill match with the job description.")

    if analysis["projects"]:
        strengths.append("Projects are included in the resume.")

    if analysis["education"]:
        strengths.append("Educational qualifications are clearly mentioned.")

    # Improvements
    if not analysis["experience"]:
        improvements.append("No work experience or internship found.")

    if analysis["missing"] > 0:
        improvements.append(f"{analysis['missing']} important skills are missing.")

    # Suggestions
    suggestions.append("Customize your resume for every job application.")
    suggestions.append("Add GitHub and LinkedIn profile links.")
    suggestions.append("Mention achievements using numbers whenever possible.")

    if score < 60:
        recommendation = "🔴 Not Recommended"
    elif score < 80:
        recommendation = "🟡 Suitable for Interview with Improvements"
    else:
        recommendation = "🟢 Highly Recommended"

    return {
        "strengths": strengths,
        "improvements": improvements,
        "suggestions": suggestions,
        "recommendation": recommendation
    }