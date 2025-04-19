import streamlit as st
import psycopg2

# --- DB Connection ---
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="gradient",
        user="postgres"
    )

# --- Login Check ---
if "user_id" not in st.session_state:
    st.error("🚫 You must be logged in to view this page.")
    st.stop()

# --- Get Username ---
with get_connection() as conn:
    cur = conn.cursor()
    cur.execute("SELECT username FROM UserAccount WHERE id = %s", (st.session_state["user_id"],))
    result = cur.fetchone()
    username = result[0] if result else "Unknown User"

# --- Page Config & CSS ---
st.set_page_config(page_title=f"Gradient - {username}'s Profile", page_icon=":tada:", layout="wide", initial_sidebar_state="collapsed")
import base64

st.set_page_config(page_title= "Gradient - Your Profile", page_icon=":tada:", layout ="wide", initial_sidebar_state="collapsed")
st.markdown(
    f'<a href="/"><img class="logo" src="data:image/png;base64,{base64.b64encode(open("logo.png", "rb").read()).decode()}" alt="Logo"></a>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
        div[data-testid="collapsedControl"] {
            visibility: hidden;
        }
        #logout-menu {
            position: fixed;
            top: 1.2rem;
            right: 2rem;
            background-color: #f8f9fa;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            z-index: 9999;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load external style ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

# --- Top-right Logout Dropdown ---
st.markdown("<div id='logout-menu'>", unsafe_allow_html=True)
with st.expander(f"👤 {username}"):
    if st.button("🚪 Log Out"):
        st.session_state.clear()
        st.success("Logged out successfully.")
        st.switch_page("gradient.py")
st.markdown("</div>", unsafe_allow_html=True)

# --- Header Section ---
with st.container():
    st.title(f"{username}'s Profile")

    info, picture = st.columns((5, 2))
    with info:
        st.write("---")
        st.write("Intended Major: Undecided")
        st.write("Completed Credits: 31")
        st.write("GPA: N/A")

    with picture:
        st.image("blankprofilepic.jpg", caption="Profile Picture", width=200)

    st.write("---")

    with st.expander("Four Year Plan"):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.course_code, c.course_name, pc.year, pc.semester, c.sqi, c.id
                FROM PlanCourse pc
                JOIN Class c ON pc.class_id = c.id
                WHERE pc.user_id = %s
                ORDER BY pc.year, pc.semester, c.course_code
            """, (st.session_state["user_id"],))
            rows = cur.fetchall()

        if not rows:
            st.info("No saved plan found. Go to the Four Year Plan tab to generate one.")
        else:
            # Organize by year and semester
            plan = { (year, semester): [] for year in range(1, 5) for semester in ("Fall", "Spring") }
            for code, name, year, semester, sqi, _ in rows:
                plan[(year, semester)].append({
                    "Course Code": code,
                    "Course Name": name,
                    "SQI": sqi
                })

            for year in range(1, 5):
                st.subheader(f"Year {year}")
                col_fall, col_spring = st.columns(2)
                for semester, col in zip(("Fall", "Spring"), (col_fall, col_spring)):
                    with col:
                        sem_courses = plan[(year, semester)]
                        st.markdown(f"**{semester}**")
                        if not sem_courses:
                            st.write("_No courses scheduled._")
                        else:
                            df = pd.DataFrame(sem_courses)
                            df["Credits"] = "N/A"  # Placeholder if credits not stored
                            df = df[["Course Code", "Course Name", "Credits", "SQI"]]
                            df["SQI"] = df["SQI"].apply(lambda x: f"{x:.2f}" if isinstance(x, float) else "")
                            st.dataframe(df.style.hide(axis='index'), hide_index=True, use_container_width=True)

                            valid_sqis = [c["SQI"] for c in sem_courses if isinstance(c["SQI"], float)]
                            if valid_sqis:
                                avg_sqi = sum(valid_sqis) / len(valid_sqis)
                                st.markdown(f"Average SQI: **{avg_sqi:.2f}**")
                            else:
                                st.markdown("Average SQI: **N/A**")