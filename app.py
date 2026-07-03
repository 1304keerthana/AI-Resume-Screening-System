import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from utils.analyzer import analyze_resume
from utils.feedback import generate_feedback
from utils.gemini import generate_ai_feedback
from utils.parser import extract_text
from utils.similarity import calculate_similarity

# ---------------- Page Configuration ---------------- #
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Styling and Animation ---------------- #

def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


def load_background(file_name, script_file=None):
    with open(file_name, "r", encoding="utf-8") as html_file:
        html = html_file.read()

    if script_file:
        with open(script_file, "r", encoding="utf-8") as js_file:
            html = html.replace("/* INJECT_PARTICLES_JS */", js_file.read())

    components.html(html, height=20, scrolling=False)


load_css("assets/style.css")
load_background("assets/animation.html", "assets/particles.js")

# ---------------- UI Helpers ---------------- #

def build_gauge(score):
    data = pd.DataFrame(
        {
            "status": ["Match", "Remaining"],
            "value": [score, max(0, 100 - score)],
        }
    )

    gauge = (
        alt.Chart(data)
        .mark_arc(innerRadius=80, outerRadius=120)
        .encode(
            theta=alt.Theta("value:Q"),
            color=alt.Color(
                "status:N",
                scale=alt.Scale(domain=["Match", "Remaining"], range=["#06B6D4", "rgba(148, 163, 184, 0.18)"],),
                legend=None,
            ),
            tooltip=["status:N", "value:Q"],
        )
        .properties(width=300, height=300)
    )

    label = (
        alt.Chart(pd.DataFrame({"score": [score]}))
        .mark_text(fontSize=32, fontWeight=700, color="#ffffff")
        .encode(text=alt.Text("score:Q", format=".0f"))
        .properties(width=300, height=300)
    )

    suffix = (
        alt.Chart(pd.DataFrame({"score": [score]}))
        .mark_text(dy=20, fontSize=14, color="#94a3b8")
        .encode(text=alt.Text("score:Q", format="'%'"))
        .properties(width=300, height=300)
    )

    return (
        (gauge + label + suffix)
        .configure_view(strokeWidth=0)
        .configure(background='transparent')
        .configure_axis(labelColor='#cbd5e1', titleColor='#cbd5e1')
        .configure_legend(labelColor='#cbd5e1', titleColor='#cbd5e1')
    )


def build_skill_pie(matched, missing):
    chart_data = pd.DataFrame(
        {
            "status": ["Matched Skills", "Missing Skills"],
            "value": [matched, missing],
        }
    )

    chart = (
        alt.Chart(chart_data)
        .mark_arc(innerRadius=60, outerRadius=110)
        .encode(
            theta=alt.Theta("value:Q"),
            color=alt.Color(
                "status:N",
                scale=alt.Scale(domain=["Matched Skills", "Missing Skills"], range=["#22c55e", "rgba(148, 163, 184, 0.14)"],),
                legend=None,
            ),
            tooltip=["status:N", "value:Q"],
        )
        .properties(width=300, height=300)
    )

    return chart.configure_view(strokeWidth=0).configure(background='transparent').configure_axis(labelColor='#cbd5e1', titleColor='#cbd5e1').configure_legend(labelColor='#cbd5e1', titleColor='#cbd5e1')


# ---------------- Header and Intro ---------------- #

st.markdown(
    """
    <div class='hero-panel'>
        <div class='hero-copy'>
            <div class='hero-eyebrow'>Recruiter Workspace</div>
            <h1>AI Resume Screening System</h1>
            <p>Hire smarter with artificial intelligence and automated candidate matching.</p>
            <div class='hero-pill-row'>
                <span>⚡ Fast resume parsing</span>
                <span>🔍 ATS-ready scoring</span>
                <span>🤖 Gemini-powered insights</span>
            </div>
        </div>
        <div class='hero-card small-card'>
            <div class='profile-badge'>👤</div>
            <div>
                <div class='profile-title'>Recruiter</div>
                <div class='profile-subtitle'>Your AI hiring assistant is ready.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<div class='sidebar-brand'>🤖 AI Resume Assistant</div>", unsafe_allow_html=True)
    st.markdown("<p>Analyze resumes faster, prioritize top candidates, and surface skills that matter.</p>")
    st.markdown("---")
    st.markdown("### Workflow")
    st.markdown("- Upload candidate resume")
    st.markdown("- Paste job description")
    st.markdown("- Review ATS match score")
    st.markdown("- Explore AI feedback")


# ---------------- Input Section ---------------- #

st.markdown("<div class='section-title'>Resume Screening</div>", unsafe_allow_html=True)

upload_col, description_col = st.columns([1, 1], gap="large")

with upload_col:
    st.markdown("<div class='glass-panel'><h3>📂 Upload Resume</h3><p>Drag & drop your PDF or DOCX resume.</p></div>", unsafe_allow_html=True)
    resume = st.file_uploader("", type=["pdf", "docx"], label_visibility="hidden")

with description_col:
    st.markdown("<div class='glass-panel'><h3>💼 Job Description</h3><p>Paste the role details and required skills.</p></div>", unsafe_allow_html=True)
    job_description = st.text_area("", height=260, placeholder="Enter the full job description here...", label_visibility="hidden")

_, button_col, _ = st.columns([1, 2, 1])
with button_col:
    analyze_pressed = st.button("🚀 Analyze Resume", use_container_width=True)


# ---------------- Results ---------------- #

if analyze_pressed:
    if resume is not None and job_description.strip():
        resume_text = extract_text(resume)
        score = calculate_similarity(resume_text, job_description)
        analysis = analyze_resume(resume_text, job_description)
        with st.spinner("🤖 Gemini AI is analyzing the resume..."):
            ai_feedback = generate_ai_feedback(resume_text, job_description)

        feedback = generate_feedback(score, analysis)

        st.markdown("<div class='section-title'>Screening Results</div>", unsafe_allow_html=True)

        metric_columns = st.columns(4, gap="large")
        metric_values = [
            ("ATS SCORE", f"{score:.2f}%", "Resume-job match"),
            ("SKILL MATCH", f"{analysis['matched']}/{analysis['total']}", "Top skills found"),
            ("PROJECTS", "Found" if analysis["projects"] else "Not Found", "Project section"),
            ("EDUCATION", "Found" if analysis["education"] else "Not Found", "Education details"),
        ]

        for col, (title, value, subtitle) in zip(metric_columns, metric_values):
            col.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>{title}</div>
                    <div class='kpi-value'>{value}</div>
                    <div class='kpi-subtitle'>{subtitle}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

        chart_col, pie_col = st.columns([1, 1], gap="large")

        with chart_col:
            st.markdown("<div class='chart-card'><h3>🎯 ATS Gauge</h3></div>", unsafe_allow_html=True)
            st.altair_chart(build_gauge(score), use_container_width=True)

        with pie_col:
            st.markdown("<div class='chart-card'><h3>📊 Skill Match Breakdown</h3></div>", unsafe_allow_html=True)
            st.altair_chart(build_skill_pie(analysis["matched"], analysis["missing"]), use_container_width=True)

        st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class='ai-card'>
                <div class='ai-card-header'>
                    <div>
                        <span class='ai-badge'>🤖</span>
                        <div class='ai-title'>Gemini AI Review</div>
                    </div>
                    <div class='recommendation-pill'>Recommendation</div>
                </div>
                <div class='ai-summary'>
                    <p class='ai-summary-text'>This candidate has a strong match score and provides the key signals needed for ATS-based screening.</p>
                </div>
                <div class='ai-grid'>
                    <div class='ai-block'>
                        <h4>Strengths</h4>
                        <ul>
                            {''.join(f'<li>{item}</li>' for item in feedback['strengths'])}
                        </ul>
                    </div>
                    <div class='ai-block'>
                        <h4>Areas for Improvement</h4>
                        <ul>
                            {''.join(f'<li>{item}</li>' for item in feedback['improvements'])}
                        </ul>
                    </div>
                    <div class='ai-block ai-full'>
                        <h4>Suggestions</h4>
                        <ul>
                            {''.join(f'<li>{item}</li>' for item in feedback['suggestions'])}
                        </ul>
                    </div>
                </div>
                <div class='recommendation-card'>
                    <span>Final Recommendation</span>
                    <strong>{feedback['recommendation']}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("📄 Resume Preview & Gemini Feedback", expanded=False):
            st.markdown("<div class='resume-card'>", unsafe_allow_html=True)
            st.write(resume_text)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
            st.subheader("🤖 Gemini AI Resume Analysis")
            st.markdown(ai_feedback)
    else:
        st.warning("⚠ Please upload a resume and enter the job description.")
else:
    st.markdown(
        "<div class='empty-state'>Upload a resume and paste a job description, then click <strong>Analyze Resume</strong> to see the AI screening dashboard.</div>",
        unsafe_allow_html=True,
    )
