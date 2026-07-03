# List of common technical skills
SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data analysis",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "docker",
    "aws",
    "excel",
    "power bi"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill.title())

    return found_skills