import streamlit as st
import pandas as pd
import psycopg2
import base64
from streamlit_searchbox import st_searchbox
from fuzzywuzzy import process

st.set_page_config(page_title= "Gradient - Professors", page_icon=":tada:", layout ="wide", initial_sidebar_state="expanded")

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

st.markdown(
    f'<div class="center-logo"></div>',
    unsafe_allow_html=True
)

def local_css(file_name):
    with open(file_name) as f :
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")


with st.container():
     st.write("Go to :")
     left, middle, right = st.columns(3)
     with middle:          
        if st.button("Four Year Plan", use_container_width= True):
            st.switch_page("pages/four_year.py")
    
     with left:

        if st.button("Profile", use_container_width= True):
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
        #password="password"  # Replace with your password
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


with st.container():
    @st.cache_data(ttl=600)  # cache for 10 minutes
    def load_professors():
        conn = get_connection()
        cur = conn.cursor()

        query = """
        SELECT prof_name, SQI, summary
        FROM professor
        """
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return pd.DataFrame(rows, columns=["Professor Name", "SQI", "Summary"])
    st.title("Professor Lookup")
    
    df = load_professors()
    prof_names = df["Professor Name"].tolist()

    def search_professors(search_term: str):
        if not search_term:
            return []
        return [name for name, _ in process.extract(search_term, prof_names, limit=5)]
    
    if len(df.index) != 0:
        with st.container(border=True):
            st.text("Search up your professors and find their ratings!")
            selected_prof = st_searchbox(search_professors, placeholder="Search for a professor by name...", clear_on_submit=True)

        # selected_prof = st_searchbox(search_professors, placeholder="Search for a Professor...")

        selected_prof_data = df[df["Professor Name"] == selected_prof]

        for _, row in selected_prof_data.iterrows():
            with st.container():
                sqi = round(row['SQI']*10 + 50 if pd.notnull(row['SQI']) else -1, 2)
                letter_grade, color = get_letter_grade(sqi)
                st.markdown(f"""
                <div style="background-color:#f5f5f5;padding:15px;border-radius:10px;margin-bottom:10px">
                <h5>{row['Professor Name']}</h5>
                <br><strong>SQI:</strong> <span style = \'color: {color}\'>{letter_grade} ({sqi if sqi != -1 else 'N/A'})</span>
                <div style="margin-top: 15px; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #bbb; border-radius: 8px;">
                    <p style="margin: 0 0 10px;"><strong>Professor Summary:</strong></p>
                    <p style="margin: 0; font-style: italic; color: #333;">{row['Summary']}</p>
                </div>
                </div>
                """, unsafe_allow_html=True)
            # with st.container():
            #     st.markdown(f"""
            #     <div style="background-color:#ffffff; padding:20px; border-radius:12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom:20px;">

            #     <h4 style="margin-bottom: 10px;">{row['Professor Name']}</h4>

            #     <p style="margin: 6px 0;"><strong>NetID:</strong> {row['NetID'] or 'N/A'}</p>
            #     <p style="margin: 6px 0;"><strong>Metrics:</strong> {row['Metrics']:.2f}</p>
            #     <p style="margin: 6px 0;"><strong>SQI:</strong> {row['SQI'] or 'N/A'}</p>

            #     <div style="margin-top: 15px; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #bbb; border-radius: 8px;">
            #         <p style="margin: 0 0 10px;"><strong>Professor Summary:</strong></p>
            #         <p style="margin: 0; font-style: italic; color: #333;">{row['Summary']}</p>
            #     </div>

            #     <div style="font-size: 0.85em; color: #666; background-color: #f0f0f0; padding: 8px; border-radius: 6px; margin-top: 10px;">
            #         ⚠️ <em>Summaries are generated by AI and may not be 100% accurate.</em>
            #     </div>

            #     </div>
            #     """, unsafe_allow_html=True)
    # else:
    #     st.warning("No professors found.")

    #     if rows:
    #         df = pd.DataFrame(rows, columns=["Professor Name", "SQI", "Summary"])
    #         print(rows)
    #         for _, row in df.iterrows():
    #             with st.container():
    #                 sqi = round(row['SQI']*10 + 50 if pd.notnull(row['SQI']) else -1, 2)
    #                 letter_grade, color = get_letter_grade(sqi)
    #                 st.markdown(f"""
    #                 <div style="background-color:#f5f5f5;padding:15px;border-radius:10px;margin-bottom:10px">
    #                 <h5>{row['Professor Name']}</h5>
    #                 <br><strong>SQI:</strong> <span style = \'color: {color}\'>{letter_grade} ({sqi if sqi != -1 else 'N/A'})</span>
    #                 <br><strong>Summary:</strong> {row['Summary']}</p>
    #                 </div>
    #                 """, unsafe_allow_html=True)
    #     else:
    #         st.warning("No professors found matching that name.")

    #     cur.close()
    #     conn.close()


