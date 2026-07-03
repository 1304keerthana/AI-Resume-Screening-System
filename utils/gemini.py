import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_feedback(resume_text, job_description):

    prompt = f"""
You are an ATS Resume Reviewer.

Analyze the resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Give the response in this format only:

## Resume Summary

## Strengths

## Weaknesses

## Missing Skills

## Suggestions

## Final Recommendation

Keep the answer concise and professional.
"""

    response = model.generate_content(prompt)

    return response.text