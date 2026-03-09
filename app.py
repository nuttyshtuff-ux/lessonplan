import streamlit as st
import pandas as pd
from google import genai

# 1. PAGE SETUP
st.set_page_config(page_title="Lesson Plan Stress Test", page_icon="🍎", layout="wide")

# 2. CSS (Navy & Yellow)
st.markdown("""
<style>
    .main-title { color: #1e3a8a; font-weight: 800; text-align: center; border: 3px solid #1e3a8a; padding: 20px; border-radius: 20px; background-color: #f8fbff; margin-bottom: 30px; }
    .stButton button { background-color: #facc15 !important; color: #1e3a8a !important; border: 2px solid #1e3a8a !important; font-weight: bold !important; border-radius: 12px !important; width: 100%; height: 3em; }
    [data-testid="stSidebar"] { background-color: #1e3a8a !important; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #000000 !important; font-weight: 700 !important; }
    .critique-card { background-color: #eff6ff; border-left: 10px solid #facc15; padding: 25px; border-radius: 15px; color: #1e3a8a; margin-top: 20px; white-space: pre-wrap; }
    .info-box { background-color: #fef08a; padding: 15px; border-radius: 10px; color: #1e3a8a; border: 1px solid #facc15; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 3. API SETUP
try:
    api_key = st.secrets["api_key"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing in Streamlit Secrets!")
    st.stop()

# 4. DATA LOADING
@st.cache_data
def load_school_data():
    url = "https://www.cde.ca.gov/schooldirectory/report?rid=dl1&tp=txt"
    try:
        df = pd.read_csv(url, sep='\t', encoding='latin1', on_bad_lines='skip')
        return df[df['StatusType'] == 'Active'][['City', 'District', 'School']]
    except:
        return pd.DataFrame({"City": ["San Luis Obispo"], "District": ["SLCUSD"], "School": ["San Luis High"]})

df = load_school_data()

# 5. SIDEBAR
with st.sidebar:
    st.header("🏫 CLASSROOM SETUP")
    
    city_input = st.text_input("Enter city to select district").strip()
    
    if city_input:
        match = df[df['City'].str.contains(city_input, case=False, na=False)]
        dist_choice = st.selectbox("Select District", options=sorted(match['District'].unique()), index=None)
    else:
        dist_choice = st.selectbox("Select District", options=[], disabled=True)

    if dist_choice:
        sch_choice = st.selectbox("Select School", options=sorted(df[df["District"] == dist_choice]["School"].unique()), index=None)
    else:
        sch_choice = st.selectbox("Select School", options=[], disabled=True)

    st.markdown("---")
    grade = st.selectbox("Grade Level", ["Kindergarten"] + ["Grade " + str(i) for i in range(1, 13)])
    subject = st.text_input("Subject Area", value="History")

    st.subheader("📊 Class Composition")
    c_size = st.slider("Total Class Size", 5, 50, 30)
    g_ratio = st.slider("Gender Ratio (% Female)", 0, 100, 50)
    
    st.subheader("📝 Support Needs")
    sped_val = st.slider("SPED / IEP (%)", 0, 100, 10)
    fof_val = st.slider("504 Plan (%)", 0, 100, 5)
    el_val = st.slider("English Learners (%)", 0, 100, 10)

# 6. MAIN UI
st.markdown("<h1 class='main-title'>🍎 LESSON PLAN STRESS TEST</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>📋 What you'll get:</strong><br>
    • <strong>The Cal Poly Professor:</strong> High-level feedback on TPA alignment.<br>
    • <strong>The Veteran Teacher:</strong> A reality check on prep-time vs. student benefit.<br>
    • <strong>The Students:</strong> What the kids are actually thinking.
</div>
""", unsafe_allow_html=True)

p_text = "Paste your lesson plan here (Word, PDF, and Google Doc text formats accepted). For best evaluation be sure your plan includes:\n- Learning Objectives\n- Standards (CCSS, NGSS, etc.)\n- Step-by-Step Activities\n- How you will check for understanding"

lesson_input = st.text_area("Your Lesson Plan:", height=300, placeholder=p_text)

# 7. RUN EVALUATION
if st.button("🚀 RUN EVALUATION"):
    if not sch_choice or not lesson_input:
        st.warning("Please select a school and paste your lesson plan first!")
    else:
        with st.spinner("Analyzing pedagogical ROI..."):
            p = f"Evaluate this {subject} lesson for {grade} at {sch_choice}. "
            p += f"Class Size: {c_size}, Gender: {g
