import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

st.set_page_config(page_title="Lesson Plan Sim", page_icon="🍎", layout="wide")

# 1. CSS - Navy & Yellow Studio Vibe
st.markdown("""<style>
    .main-title { color: #1e3a8a; font-weight: 800; text-align: center; border: 3px solid #1e3a8a; padding: 20px; border-radius: 20px; background-color: #f8fbff; margin-bottom: 30px; }
    .stButton button { background-color: #facc15 !important; color: #1e3a8a !important; border: 2px solid #1e3a8a !important; font-weight: bold !important; border-radius: 12px !important; }
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] * { color: #fef08a !important; }
    .critique-card { background-color: #eff6ff; border-left: 8px solid #facc15; padding: 20px; border-radius: 10px; color: #1e3a8a; margin-bottom: 20px; }
</style>""", unsafe_allow_html=True)

# 2. DATA LOADING (Mocked for now - add your CSV later)
api_key = st.secrets.get("api_key")
client = genai.Client(api_key=api_key)

# Sample Data - Replace with pd.read_csv("pubschls.csv") once you upload it
data = {
    "City": ["San Luis Obispo", "San Luis Obispo", "Atascadero", "Arroyo Grande"],
    "District": ["SLCUSD", "SLCUSD", "Atascadero Unified", "Lucia Mar"],
    "School": ["San Luis High", "Laguna Middle", "Atascadero High", "Arroyo Grande High"]
}
df = pd.DataFrame(data)

# 3. SIDEBAR - The Classroom Setup
with st.sidebar:
    st.header("🏫 CLASSROOM SETUP")
    
    city = st.selectbox("City", options=sorted(df["City"].unique()), index=None, placeholder="Select City")
    
    if city:
        districts = sorted(df[df["City"] == city]["District"].unique())
        dist = st.selectbox("District", options=districts, index=None, placeholder="Select District")
    else:
        dist = st.selectbox("District", options=[], disabled=True, placeholder="Select City First")

    if dist:
        schools = sorted(df[df["District"] == dist]["School"].unique())
        school = st.selectbox("Specific School", options=schools, index=None, placeholder="Select School")
    else:
        school = st.selectbox("School", options=[], disabled=True, placeholder="Select District First")

    st.markdown("---")
    grade = st.selectbox("Grade Level", [f"Grade {i}" for i in range(1, 13)])
    subject = st.text_input("Subject", value="Algebra 1")
    
    st.subheader("📊 Demographics")
    iep_504 = st.slider("IEP/504 Load (%)", 0, 100, 15)
    el_load = st.slider("English Learners (%)", 0, 100, 10)
    
    st.markdown("---")
    st.info("💡 Pro-Tip: The Realist focuses on Prep-to-Benefit ROI.")

# 4. MAIN UI
st.markdown("<h1 class='main-title'>🍎 LESSON PLAN STRESS TEST</h1>", unsafe_allow_html=True)
instr = "Paste your lesson plan here. Include Objectives, Standards, and Activities."
lesson_plan = st.text_area("Your Lesson Plan:", height=400, placeholder=instr)

# 5. RUN LOGIC
if st.button("📝 RUN EVALUATION", use_container_width=True):
    if school and lesson_plan:
        with st.spinner("Analyzing pedagogical ROI..."):
            p = f"Evaluate this lesson for {school} ({dist}). Grade: {grade} {subject}. "
            p += f"Class Needs: {iep_504}% IEP/504, {el_load}% EL students. "
            p += f"Lesson: {lesson_plan}. "
            p += "Provide feedback from: 1. A Cal Poly Professor (TPA/Academic rigor), "
            p += "2. A Veteran Teacher (Practicality, ROI of prep-work vs student benefit), "
            p += "3. The Students (Simulated engagement/inner thoughts)."
            
            res = client.models.generate_content(model="gemini-1.5-flash", contents=p)
            st.session_state["eval"] = res.text
            st.rerun()
    else:
        st.warning("Please select a school and enter your plan!")

# 6. DISPLAY
if "eval" in st.session_state:
    st.markdown(f"<div class='critique-card'><h3>📋 The Feedback:</h3>{st.session_state['eval']}</div>", unsafe_allow_html=True)
