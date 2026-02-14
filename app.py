import streamlit as st
from PyPDF2 import PdfReader
import re
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Career Co-Pilot", layout="wide")

st.markdown("""
<h1 style='text-align: center;'>🚀 AI Personal Career Co-Pilot</h1>
<p style='text-align: center;'>Your Adaptive Career Intelligence System</p>
""", unsafe_allow_html=True)

st.divider()

# Sidebar
st.sidebar.header("📂 Upload Your Profile")

resume = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])
github_link = st.sidebar.text_input("Enter GitHub Profile URL")
linkedin_link = st.sidebar.text_input("Enter LinkedIn Profile URL")

dream_role = st.sidebar.selectbox(
    "Select Your Dream Role",
    ["AI Engineer", "Data Scientist", "Full Stack Developer"]
)

launch = st.sidebar.button("🚀 Launch Career Agent")

# Market role requirements
role_requirements = {
    "AI Engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Model Deployment", "Git"],
        "why": {
            "Deep Learning": "Core for building neural networks and AI models.",
            "TensorFlow": "Used widely for production-grade ML systems.",
            "PyTorch": "Popular framework for research and AI development.",
            "Model Deployment": "Critical to move models from notebook to production."
        }
    },
    "Data Scientist": {
        "skills": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization", "Pandas"],
        "why": {}
    },
    "Full Stack Developer": {
        "skills": ["JavaScript", "React", "Node.js", "Databases", "Git", "HTML", "CSS"],
        "why": {}
    }
}

def extract_resume_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def extract_skills_local(text, required_skills):
    detected = []
    for skill in required_skills:
        if re.search(skill.lower(), text.lower()):
            detected.append(skill)
    return list(set(detected))

def generate_roadmap(role, missing_skills):
    roadmap = f"### 🗺 30-Day Roadmap to Become a {role}\n\n"

    roadmap += "#### Week 1: Foundations\n"
    roadmap += "- Strengthen core fundamentals\n"
    for skill in missing_skills[:2]:
        roadmap += f"- Learn basics of {skill}\n"

    roadmap += "\n#### Week 2: Practical Projects\n"
    for skill in missing_skills[2:4]:
        roadmap += f"- Build mini project using {skill}\n"

    roadmap += "\n#### Week 3: Advanced Integration\n"
    roadmap += "- Combine skills into one strong portfolio project\n"
    roadmap += "- Practice real interview questions\n"

    roadmap += "\n#### Week 4: Market Positioning\n"
    roadmap += "- Upload projects to GitHub\n"
    roadmap += "- Optimize LinkedIn\n"
    roadmap += "- Apply strategically to internships/jobs\n"

    return roadmap

if launch and resume:

    st.header("🔍 Analyzing Profile...")

    resume_text = extract_resume_text(resume)
    full_profile = resume_text + github_link + linkedin_link

    required_skills = role_requirements[dream_role]["skills"]
    extracted_skills = extract_skills_local(full_profile, required_skills)
    missing_skills = list(set(required_skills) - set(extracted_skills))

    readiness = int((len(required_skills) - len(missing_skills)) / len(required_skills) * 100)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Detected Skills")
        for skill in extracted_skills:
            st.success(skill)

        st.subheader("❌ Skill Gaps")
        for skill in missing_skills:
            st.error(skill)
            if skill in role_requirements[dream_role]["why"]:
                st.caption("Why important: " + role_requirements[dream_role]["why"][skill])

    with col2:
        st.subheader("🎯 Readiness Score")
        st.progress(readiness / 100)
        st.write(f"{readiness}% Ready for {dream_role}")

        st.subheader("📊 Skill Distribution")

        skill_status = ["Have"] * len(extracted_skills) + ["Missing"] * len(missing_skills)
        labels = extracted_skills + missing_skills

        df = pd.DataFrame({
            "Skill": labels,
            "Status": skill_status
        })

        fig, ax = plt.subplots()
        df["Status"].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    st.divider()

    st.markdown(generate_roadmap(dream_role, missing_skills))

    st.divider()
    st.header("🧠 AI Career Strategy Mode")

    if readiness < 50:
        st.warning("🔹 Strategy: Focus on learning + internships before targeting full-time roles.")
    elif readiness < 80:
        st.info("🔹 Strategy: Build 2 strong projects and start applying strategically.")
    else:
        st.success("🔹 Strategy: Aggressively apply and leverage referrals.")
      

    # ================================
    # 🎤 AI Mock Interview Simulator
    # ================================

    st.divider()
    st.header("🎤 AI Mock Interview Simulator")
        # Select interview type
    interview_type = st.selectbox(
        "Choose interview type:",
        ["Behavioral", "Technical", "HR"]
    )

    start_interview = st.button("Start Mock Interview")

    if start_interview:
        st.subheader("🧠 Interview Question")

        if interview_type == "Behavioral":
            question = "Tell me about a time you handled a difficult challenge."
        elif interview_type == "Technical":
            question = "Explain a technical project you worked on and your role in it."
        else:
            question = "Why do you want to work for this company?"

        st.write("👉", question)

        answer = st.text_area("Type your answer here:")

        if st.button("Get Feedback"):
            if answer.strip() == "":
                st.warning("Please enter your answer first.")
            else:
                st.subheader("📊 AI Feedback")

                if len(answer) < 80:
                    st.error("Your answer is too short. Add more detail and structure.")
                else:
                    st.success("Good response! Try to structure it using STAR method (Situation, Task, Action, Result).")



    