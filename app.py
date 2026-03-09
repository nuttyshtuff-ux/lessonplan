import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="Lesson Plan Stress Test", page_icon="🍎", layout="wide")

# 2. CSS
st.markdown("""
<style>
    .main-title { color: #1e3a8a; font-weight: 800; text-align: center; border: 3px solid #1e3a8a; padding: 20px; border-radius: 20px; background-color: #f8fbff; margin-bottom: 30px; }
    .stButton button { background-color: #facc15 !important; color: #1e3a8a !important; border: 2px solid #1e3a8a !important; font-weight: bold !important; border-radius: 12px !important; width: 100%; height: 3em; }
    [data-testid="stSidebar"] { background-color: #1e3a8a !important; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #000000 !important; font-weight: 700 !important; }
    .critique-card { background-color: #eff6ff; border-left: 10px solid #facc15; padding: 25px; border-radius: 15px; color: #1e3a8a; margin-top: 20px; white-space: pre-wrap; }
</style>
""", unsafe_allow_html=True)

# 3. API SETUP
try:
    api_key = st.secrets["api_key"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing!")
    st.stop()

# 4. DATA LOADING
@st.cache_data
def load_data():
    url = "https://www.cde.ca.gov/schooldirectory/report?rid=dl1&tp=txt"
    try:
        df = pd.read_csv(url, sep='\t', encoding='latin1', on_bad_lines='skip')
        return df[df['StatusType'] == 'Active'][['City', 'District', 'School']]
    except:
        return pd.DataFrame({"City": ["San Luis Obispo"], "District": ["SLCUSD"], "School": ["San Luis High"]})

df = load_data()

# 5. SIDEBAR
with st.sidebar:
    st.header("🏫 SETUP")
    city_input = st.text_input("City").strip()
    if city_input:
        dist_options = sorted(df[df['City'].str.contains(city_input, case=False, na=False)]['District'].unique())
        dist_choice = st.selectbox("District", options=dist_options, index=None)
    else:
        dist_choice = st.selectbox("District", options=[], disabled=True)

    if dist_choice:
        sch_options = sorted(df[df["District"] == dist_choice]["School"].unique())
        sch_choice = st.selectbox("School", options=sch_options, index=None)
    else:
        sch_choice = st.selectbox("School", options=[], disabled=True)

    grade = st.selectbox("Grade", ["Grade " + str(i) for i in range(1, 13)])
    subject = st.text_input("Subject", value="Math")

# 6. MAIN UI
st.markdown("<h1 class='main-title'>🍎 LESSON PLAN STRESS TEST</h1>", unsafe_allow_html=True)
lesson_input = st.text_area("Paste Lesson Plan:", height=300)

# 7. RUN
if st.button("🚀 RUN EVALUATION"):
    if not sch_choice or not lesson_input:
        st.warning("Fill in all fields!")
    else:
        with st.spinner("Talking to Gemini..."):
            try:
                # THE COMEDY APP FIX: Use the 'models/' prefix and NO request options
                model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
                
                prompt = f"Evaluate this {subject} lesson for {grade} at {sch_choice}. Plan: {lesson_input}"
                
                response = model.generate_content(prompt)
                st.session_state["result"] = response.text
                st.rerun()
            except Exception as e:
                # If that still fails, the API key might be the issue
                st.error(f"Error: {e}")

# 8. RESULTS
if "result" in st.session_state:
    st.markdown('<div class="critique-card">' + st.session_state["result"] + '</div>', unsafe_allow_html=True)
