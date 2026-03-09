import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# 1. PAGE SETUP
st.set_page_config(page_title="Lesson Plan Stress Test", page_icon="🍎", layout="wide")

# 2. CSS - Navy & Yellow Studio Vibe with High-Contrast Text
st.markdown("""
<style>
    /* Main Background and Titles */
    .main-title { color: #1e3a8a; font-weight: 800; text-align: center; border: 3px solid #1e3a8a; padding: 20px; border-radius: 20px; background-color: #f8fbff; margin-bottom: 30px; }
    
    /* Buttons */
    .stButton button { background-color: #facc15 !important; color: #1e3a8a !important; border: 2px solid #1e3a8a !important; font-weight: bold !important; border-radius: 12px !important; width: 100%; height: 3em; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #1e3a8a; color: white; }
    
    /* Force Sidebar labels and text to be high-contrast Black */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stSlider { color: #000000 !important; font-weight: 700 !important; }

    /* Results Card */
    .critique-card { background-color: #eff6ff; border-left: 10px solid #facc15; padding: 25px; border-radius: 15px; color: #1e3a8a; margin-top: 20px; border-top: 1px solid #dbeafe; border-right: 1px solid #dbeafe; border-bottom: 1px solid #dbeafe; }
</style>
""", unsafe_allow_html=True)

# 3. API & DATA SETUP
try:
    api_key = st.secrets["api_key"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing! Check your Streamlit Secrets.")
    st.stop()

# Local Mock Data (Replace with full CSV later)
data = {
    "City": ["San Luis Obispo", "Atascadero", "Paso Robles", "Arroyo Grande"],
    "District": ["SLCUSD", "Atascadero Unified", "Paso Robles Joint", "Lucia Mar"],
    "School": ["San Luis High", "Atascadero High", "Paso High", "Arroyo Grande High"]
}
df = pd.DataFrame(data)

# 4. SIDEBAR - THE ROSTER
with st.sidebar:
    st.header("🏫 CLASSROOM SETUP")
    
    # Dependent Dropdowns
    city_choice = st.selectbox("Select City", options=sorted(df["City"].unique()), index=None)
    
    if city_choice:
        dist_options = sorted(df[df["City"] == city_choice]["District"].unique())
        dist_choice = st.selectbox("Select District", options=dist_options, index=None)
    else:
        dist_choice = st.selectbox("Select District", options=[], disabled=True)

    if dist_choice:
        sch_options = sorted(df[df["District"] == dist_choice]["School"].unique())
        sch_choice = st.selectbox("Select School", options=sch_options, index=None)
    else:
        sch_choice = st.selectbox("Select School", options=[], disabled=True)

    st.markdown("---")
    grade = st.selectbox("Grade Level", [f"Grade {i}" for i in range(1, 13)] + ["Kindergarten"])
    subject = st.text_input("Subject Area", value="General Ed")
    
    st.subheader("📊 Class Composition")
    c_size = st.slider("Total Class Size", 5, 50, 30)
    g_ratio = st.slider("Gender Ratio (% Female)", 0, 100, 50)
    
    st.subheader("📝 Support Needs")
    sped_val = st.slider("SPED / IEP (%)", 0, 100, 10)
    fof_val = st.slider("504 Plans (%)", 0, 100, 5)
    el_val = st.slider("English Learners (%)", 0, 100, 10)

# 5. MAIN UI
st.markdown("<h1 class='main-title'>🍎 LESSON PLAN STRESS TEST</h1>", unsafe_allow_html=True)
st.subheader("The 'Teacher Lounge' Evaluation")

lesson_input = st.text_area("Paste your lesson plan here (Objectives, Activities, Assessments):", height=400)

# 6. RUN EVALUATION
if st.button("📝 RUN EVALUATION"):
    if not sch_choice or not lesson_input:
        st.warning("Please select a school and paste your lesson plan first!")
    else:
        with st.spinner("Class is in session..."):
            # Construct the persona-driven prompt
            prompt = f"""
            Evaluate this {subject} lesson plan for {grade} at {sch_choice} in {dist_choice}.
            Class Size: {c_size} students. Gender Ratio: {g_ratio}% Female.
            Student Needs: {sped_val}% SPED/IEP, {fof_val}% 504 Plans, {el_val}% English Learners.
            
            Lesson Plan Content:
            {lesson_input}
            
            Provide specific feedback from three voices:
            1. The Cal Poly Professor: Focus on TPA alignment, academic rigor, and measurable objectives.
            2. The Veteran Teacher (The Realist): Focus on classroom management, physical prep work (ROI), 
               and whether the 'extra' work involved for the teacher actually leads to real-world benefit for the kids.
            3. The Students: A simulated 'inner monologue' or dialogue from the students during the lesson.
            """
            
            try:
                response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                st.session_state["result"] = response.text
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# 7. RESULTS DISPLAY
if "result" in st.session_state:
    st.markdown(f"<div class='critique-card'>{
