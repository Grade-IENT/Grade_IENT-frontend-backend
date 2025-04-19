import streamlit as st
import pandas as pd
import psycopg2
from pathlib import Path
import sys


# ─────────────── Add repo root to path ───────────────
sys.path.append(str(Path(__file__).resolve().parents[2]))

# ─────────────── Import scheduler ───────────────
from course_scheduler import build_plan, DEFAULT_MIN_CR, DEFAULT_MAX_CR

# ─────────────── Paths & Constants ───────────────
DATA_DIR = Path(__file__).resolve().parents[2] / "backend" / "4_Year_input_Data"
AP_CREDIT_CSV = DATA_DIR / "rutgers_ap_credits.csv"

MAJOR_CSV = {
    "Aerospace Engineering":                 "aerospace_engineering_courses.csv",
    "Biomedical Engineering":                "biomedical_engineering_courses.csv",
    "Biochemical Engineering":               "biochemical_engineering_courses.csv",
    "Chemical Engineering":                  "chemical_engineering_courses.csv",
    "Civil Engineering":                     "civil_engineering_courses.csv",
    "Environmental Engineering":             "environmental_engineering_courses.csv",
    "Computer Engineering":                  "computer_engineering_courses.csv",
    "Electrical Engineering":                "electrical_engineering_courses.csv",
    "Industrial and Systems Engineering":    "industrial_systems_engineering_courses.csv",
    "Materials Science Engineering":         "materials_science_engineering_courses.csv",
    "Mechanical Engineering":                "mechanical_engineering_courses.csv",
    "Packaging Engineering":                 "packaging_engineering_courses.csv",
}

# ─────────────── Page setup ───────────────
st.set_page_config(page_title="Gradient – Four‑Year Plan", page_icon=":tada:", layout="wide", initial_sidebar_state="collapsed")

# ─────────────── Style Injection ───────────────
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

st.markdown("""
<style>
    div[data-testid="collapsedControl"] { visibility: hidden; }
    div[data-baseweb="slider"] {
        background-color: white !important;
        padding: 10px;
        border-radius: 8px;
    }
    input[type="range"] { accent-color: black !important; }
    div[data-baseweb="slider"] span {
        color: black !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.write("Go to:")
    left, middle, right = st.columns(3)
    with left:
        if st.button("Profile", use_container_width=True):
            st.switch_page("pages/profile.py")
    with middle:
        if st.button("Professors", use_container_width=True):
            st.switch_page("pages/professors.py")
    with right:
        if st.button("Scheduling", use_container_width=True):
            st.switch_page("pages/schedule.py")
    st.write("---")

# Inputs
st.title("Four Year Plan")

majors = list(MAJOR_CSV.keys())
col1, col2 = st.columns(2)
major = st.selectbox("Select Major", ["Select a major"] + majors)

cr_col1, cr_col2 = st.columns([1, 1])
with cr_col1:
    min_cr = st.number_input("Min Credits / Semester", value=DEFAULT_MIN_CR, min_value=6, max_value=18)
with cr_col2:
    max_cr = st.number_input("Max Credits / Semester", value=DEFAULT_MAX_CR, min_value=min_cr, max_value=21)

# ─────────────── AP Section ───────────────
ap_catalog = pd.read_csv(AP_CREDIT_CSV, dtype=str)
exams = sorted(ap_catalog["AP Exam"].unique())

st.markdown("### Optional: Add AP Credits")
chosen = st.multiselect("Select AP Exams", exams)
ap_scores = {exam: int(st.slider(f"{exam} score", 1, 5, 5, key=exam)) for exam in chosen}

build_btn = st.button("Generate Plan")

# DB connection function
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="gradient",
        user="postgres"
    )

# Save to DB logic

def save_plan_to_db(df):
    print("hi")
    if "user_id" not in st.session_state:
        st.error("You must be logged in to save your plan.")
        return

    inserted_ids = set()

    try:
        with get_connection() as conn:
            cur = conn.cursor()
            print(st.session_state["user_id"])
            # Clear existing saved plan
            cur.execute("DELETE FROM PlanCourse WHERE user_id = %s", (st.session_state["user_id"],))

            for sem_idx, column in enumerate(df.columns):
                year = (sem_idx // 2) + 1
                semester = "Fall" if sem_idx % 2 == 0 else "Spring"

                for entry in df[column].dropna():
                    try:
                        course_code = entry.split()[0]
                        cur.execute("SELECT id FROM Class WHERE course_code = %s", (course_code,))
                        result = cur.fetchone()
                        if result:
                            class_id = result[0]
                            # Only insert if not already added
                            if class_id not in inserted_ids:
                                cur.execute(
                                    "INSERT INTO PlanCourse (user_id, class_id, year, semester) VALUES (%s, %s, %s, %s)",
                                    (st.session_state["user_id"], class_id, year, semester)
                                )
                                inserted_ids.add(class_id)
                    except Exception as e:
                        st.warning(f"⚠️ Could not save entry: {entry} — {e}")

            conn.commit()
            st.success("✅ Plan saved to your account!")

    except psycopg2.Error as e:
        st.error(f"❌ Database error: {e.pgerror}")

# ─────────────── Generate Plan ───────────────
st.session_state["build_btn"] = False
if build_btn and major in majors:
    st.session_state["build_btn"] = True
    csv_path = DATA_DIR / MAJOR_CSV[major]
    if not csv_path.exists():
        st.error(f"Catalog file not found: **{csv_path}**")
        st.stop()

    sched, sem_credits, df = build_plan(csv_path, ap_scores, min_cr=int(min_cr), max_cr=int(max_cr), mode="var")

    st.markdown(f"### Showing 4-Year Plan for **{major}**")

    for year in range(4):
        st.subheader(f"Year {year + 1}")
        col_fall, col_spring = st.columns(2)
        for sem_idx, col in zip((year * 2, year * 2 + 1), (col_fall, col_spring)):
            with col:
                sem_name = f"Semester {sem_idx + 1}"
                raw_rows = df[sem_name].replace("", pd.NA).dropna().tolist()

                parsed = []
                for entry in raw_rows:
                    try:
                        code, rest = entry.split(' ', 1)
                        name, rest = rest.rsplit('(', 1)
                        credits_part, sqi_part = rest.rstrip(')').split(', SQI ')
                        credits = credits_part.strip().replace('cr', '').strip()
                        sqi = float(sqi_part.strip())
                        parsed.append({
                            "Course Code": code.strip(),
                            "Course Name": name.strip(),
                            "Credits": int(credits),
                            "SQI": sqi
                        })
                    except Exception:
                        parsed.append({
                            "Course Code": "",
                            "Course Name": entry.strip(),
                            "Credits": "",
                            "SQI": ""
                        })

                parsed_df = pd.DataFrame(parsed)
                parsed_df.columns = ["Course Code", "Course Name", "Credits", "SQI"]

                st.markdown(f"**{sem_name}** — Total Credits: **{sem_credits[sem_idx]}**")

                valid_sqis = [row["SQI"] for row in parsed if isinstance(row["SQI"], float)]
                if valid_sqis:
                    avg_sqi = sum(valid_sqis) / len(valid_sqis)
                    st.markdown(f"Average SQI: **{avg_sqi:.2f}**")
                else:
                    st.markdown("Average SQI: **N/A**")

                st.dataframe(parsed_df.style.hide(axis="index"), hide_index=True, use_container_width=True)

    # Download and Save buttons
    col_dl, col_save = st.columns([2, 1])
    with col_dl:
        st.download_button("Download Plan as CSV",
                           data=df.to_csv(index=False).encode(),
                           file_name="four_year_plan.csv")
    with col_save:
        
        if st.session_state.get("build_btn"):
            if st.button("Save Plan to Account"):
                print('hi')
                save_plan_to_db(df)

    
elif build_btn:
    st.warning("Please select a valid major to continue.")


