import streamlit as st
import pandas as pd
import psycopg2
import base64

st.set_page_config(page_title= "Gradient - Professors", page_icon=":tada:", layout ="wide", initial_sidebar_state="collapsed")

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

with st.container():

    st.title("Professor Lookup")
    image_column, search_column = st.columns((1,9))

    with image_column:
        st.image("search.png", caption= None, width= 100)

    with search_column:
        prof = st.text_input("Search up your professors and find their ratings!")

        if prof:
            st.write("You searched Professor:", prof)

            conn = get_connection()
            cur = conn.cursor()


            query = """
            SELECT prof_name, netid, metrics, SQI, summary
            FROM professor
            WHERE LOWER(prof_name) LIKE %s
            """
            cur.execute(query, (f"%{prof.lower()}%",))
            rows = cur.fetchall()

            if rows:
                df = pd.DataFrame(rows, columns=["Professor Name", "NetID", "Metrics", "SQI", "Summary"])
                print(rows)
                for _, row in df.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color:#f5f5f5;padding:15px;border-radius:10px;margin-bottom:10px">
                        <h5>{row['Professor Name']}</h5>
                        <p><strong>NetID:</strong> {row['NetID'] or 'N/A'}  
                        <br><strong>Metrics:</strong> {row['Metrics']:.2f}  
                        <br><strong>SQI:</strong> {row['SQI'] or 'N/A'}  
                        <br><strong>Summary:</strong> {row['Summary']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No professors found matching that name.")

            cur.close()
            conn.close()


