import streamlit as st
import pandas as pd
import psycopg2
import base64
from streamlit_searchbox import st_searchbox
from fuzzywuzzy import process
import streamlit.components.v1 as components

st.set_page_config(page_title="Gradient - Classes", page_icon=":tada:", layout="wide", initial_sidebar_state="expanded")
def load_logo_as_base64(logo_path):
    with open(logo_path, "rb") as logo_file:
        encoded_logo = base64.b64encode(logo_file.read()).decode()
    return encoded_logo

logo_base64 = load_logo_as_base64("logo.png")

st.markdown(
    f"""
    <style>
        .center-logo {{
            display: flex;
            justify-content: center;  /* Center horizontally */
            align-items: center;      /* Center vertically */
            height: 150px;            /* Full viewport height */
            background: url('data:image/png;base64,{logo_base64}') no-repeat center center; /* Set the image as background */
            background-size: contain; /* Ensure the logo scales nicely */
            width: 100%;              /* Full width of the container */
           padding: 0;               /* Remove extra padding */
        }}
        .stApp {{
            background: white !important; /* Apply white background */
        }}
    </style>
    """, unsafe_allow_html=True
)

# Display the div with centered background logo
st.markdown(
    f'<div class="center-logo"></div>',
    unsafe_allow_html=True
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

# Navigation buttons
with st.container():
    st.write("Go to :")
    left, middle, right = st.columns(3)
    with middle:
        if st.button("Four Year Plan", use_container_width=True):
            st.switch_page("pages/four_year.py")
    with left:
        if st.button("Profile", use_container_width=True):
            st.switch_page("pages/profile.py")
    with right:
        if st.button("Scheduling", use_container_width=True):
            st.switch_page("pages/schedule.py")
    st.write("---")

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="gradient",
        user="postgres",  
        # password="yourpassword"  # Optional
    )

def get_letter_grade(sqi):
    if sqi == -1:
        return '', 'black'
    if sqi < 60:
        return 'F', 'red'
    if sqi < 63:
        return 'D-', 'orange'
    if sqi < 67:
        return 'D', 'orange'
    if sqi < 70:
        return 'D+', 'orange'
    if sqi < 73:
        return 'C-', '#FFA600' # darker yellow for visibility
    if sqi < 77:
        return 'C', '#FFA600'
    if sqi < 80:
        return 'C+', '#FFA600'
    if sqi < 83:
        return 'B-', 'yellowgreen'
    if sqi < 87:
        return 'B', 'yellowgreen'
    if sqi < 90:
        return 'B+', 'yellowgreen'
    if sqi < 93:
        return 'A-', 'limegreen'
    if sqi < 97:
        return 'A', 'limegreen'
    if sqi <= 100:
        return 'A+', 'limegreen'
    
def approx_score(x):
    """
    Cubic on [0,5] → [0,100], strictly increasing,
    with f(0)=0, f(5)=100, fitted to your sample points.
    """
    a, b, c = -1.26900567,  8.69005666, 8.27485836
    return a*x**3 + b*x**2 + c*x


@st.cache_data(ttl=600)  # cache for 10 minutes
def load_classes():
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT c.course_code, c.course_name, c.SQI
    FROM Class c
    """
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return pd.DataFrame(rows, columns=["Course Code", "Course Name", "SQI"])

@st.cache_data(ttl=600)  # cache for 10 minutes
def load_teaches():
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT c.course_code, p.prof_name, t.sqi
    FROM Class c JOIN Teaches t ON c.id = t.class_id
    JOIN Professor p ON p.id = t.prof_id
    """
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return pd.DataFrame(rows, columns=["Course Code", "Professor Name", "SQI"])

with st.container():
    st.title("Class Lookup",anchor=False)

    df = load_classes()
    teaches_df = load_teaches()
    combined_courses = [f"{row['Course Code']} - {row['Course Name']}" for _, row in df.iterrows()]

    def search_courses(search_term: str):
        if not search_term:
            return []

        matches = process.extract(
            search_term, 
            combined_courses, 
            limit=10
        )
        return [match[0] for match in matches]
    
    if len(df.index) != 0:
        with st.container(border=True):
            st.text("Search for your courses by name or code!")
            # selected_course = st_searchbox(
            #     search_courses, 
            #     debounce=0,
            #     key="class_search",
            #     rerun_on_update=False,
            #     placeholder="Search for a course...")
            selected_course = st.selectbox(
                label="Search up your courses and find their ratings!",
                label_visibility="collapsed",
                options=combined_courses,
                index=None, # initially empty 
                placeholder="Search for a course by name or code...")

        if selected_course:
            code, _ = selected_course.split("-", 1)
            code = code.strip()

            sel = df[df["Course Code"].str.strip() == code]
            teaches_sel = teaches_df[teaches_df["Course Code"].str.strip() == code].sort_values("SQI", ascending = False).head(5)

            if not sel.empty:
                for _, row in sel.iterrows():
                    with st.container():
                        sqi = round(approx_score(row['SQI']) if pd.notnull(row['SQI']) else -1, 2)
                        letter_grade, color = get_letter_grade(sqi)

                        top_profs = ""
                        for _, prof in teaches_sel.iterrows():
                            teaches_sqi = round(approx_score(prof["SQI"]) if pd.notnull(prof["SQI"]) else -1, 2)
                            teaches_letter_grade, teaches_color = get_letter_grade(approx_score(prof["SQI"]))
                            top_profs += f"{prof['Professor Name']}: <span style='color:{teaches_color}'>{teaches_letter_grade} ({teaches_sqi if teaches_sqi != -1 else 'N/A'})</span><br>"
                        top_profs = "No professors found for this course" if len(top_profs) == 0 else top_profs

                        st.markdown(f"""
                        <div style="background-color:#f5f5f5;padding:15px;border-radius:10px;margin-bottom:10px">
                            <h2>{row['Course Code']} - {row['Course Name']}</h2>
                            <p><strong>SQI: </strong><span style='color:{color}'>{letter_grade} ({sqi if sqi != -1 else 'N/A'})</span></p>

                            <details style="margin-top:10px;">
                            <summary style="font-weight:bold;cursor:pointer;">View Top Professors</summary>
                            <p style="margin-left:15px;margin-top:10px;">Top professors for this course will be displayed here.</p>
                            </details>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(top_profs, unsafe_allow_html=True)
                    
            else:
                st.error(f"No course found with code {code!r}.")


    # search_term = st.text_input("Search for a class by name or course code:")

    # if search_term:
    #     st.write("You searched for class:", search_term)

    #     conn = get_connection()
    #     cur = conn.cursor()

    #     query = """
    #     SELECT c.course_code, c.course_name, 
    #             c.SQI
    #     FROM Class c
    #     WHERE LOWER(c.course_code) LIKE %s OR LOWER(c.course_name) LIKE %s
    #     """
    #     cur.execute(query, (f"%{search_term.lower()}%", f"%{search_term.lower()}%"))
    #     rows = cur.fetchall()

    #     if rows:
    #         df = pd.DataFrame(rows, columns=["Course Code", "Course Name", "SQI"])
    #         for _, row in df.iterrows():
    #             with st.container():
    #                 sqi = round(row['SQI']*10 + 50 if pd.notnull(row['SQI']) else -1, 2)
    #                 letter_grade, color = get_letter_grade(sqi)
    #                 st.markdown(f"""
    #                 <div style="background-color:#f5f5f5;padding:15px;border-radius:10px;margin-bottom:10px">
    #                 <h5>{row['Course Code']} - {row['Course Name']}</h5>
    #                 <br><strong>SQI: </strong><span style = \'color: {color}\'>{letter_grade} ({sqi if sqi != -1 else 'N/A'})</span></p>
    #                 </div>
    #                 """, unsafe_allow_html=True)
    #     else:
    #         st.warning("No classes found matching your query.")

    #     cur.close()
    #     conn.close()