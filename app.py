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
    st.error("🔑 API Key Missing!")
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
    st.header("🏫 SETUP")
    city_input = st.text_input("City").strip()
    if city_input:
        match = df[df['City'].str.contains(city_input, case=False, na=False)]
        dist_choice = st.selectbox("District", options=sorted(match['District'].unique()), index=None)
    else:
        dist_choice = st.selectbox("District", options=[], disabled=True)

    if dist_choice:
        sch_choice = st.selectbox("School", options=sorted(df[df["District"] == dist_choice]["School"].unique()), index=None)
    else:
        sch_choice = st.selectbox("Select School", options=[], disabled=True)

    grade = st.selectbox("Grade", ["Grade " + str(i) for i in range(1, 13)])
    subject = st.text_input("Subject", value="History")

# 6. MAIN UI
st.markdown("<h1 class='main-title'>🍎 LESSON PLAN STRESS TEST</h1>", unsafe_allow_html=True)
lesson_input = st.text_area("Your Lesson Plan:", height=300)

# 7. RUN EVALUATION
if st.button("🚀 RUN EVALUATION"):
    if not sch_choice or not lesson_input:
        st.warning("Please select a school and paste your lesson plan!")
    else:
        with st.spinner("Analyzing pedagogical ROI..."):
            prompt = f"Evaluate this {subject} lesson for {grade} at {sch_choice}. Feedback from: 1. Professor, 2. Veteran Teacher, 3. Students. Plan: {lesson_input}"
            
            # THE FALLBACK LOOP: We try the current 2026 stable models one by one
            success = False
            for model_name in ["gemini-2.0-flash-001", "gemini-2.0-flash-exp", "gemini-1.5-pro"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    st.session_state["result"] = response.text
                    success = True
                    break # Stop if we get a result
                except Exception:
                    continue # Try the next model if it fails
            
            if success:
                st.rerun()
            else:
                st.error("All available models failed. Please check your API key quota.")

# 8. RESULTS
if "result" in st.session_state:
    st.markdown('<div class="critique-card"><h3>📋 The Feedback:</h3>' + str(st.session_state["result"]) + '</div>', unsafe_allow_html=True)
    if st.button("Clear Results"):
        del st.session_state["result"]
        st.rerun()
