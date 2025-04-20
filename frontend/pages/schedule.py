import streamlit as st
import base64

st.set_page_config(page_title= "Gradient - Scheduling", layout="wide", initial_sidebar_state="collapsed")

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

# use CSS
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
    
     with right:

        if st.button("Professors", use_container_width= True):
            st.switch_page("pages/professors.py")

     with left:
        if st.button("Profile", use_container_width=True):
            st.switch_page("pages/profile.py")
     st.write("---")



#HEADER
with st.container():
    st.subheader("Here is your")
    st.title("Schedule")
    ##st.write("[click here](https://www.google.com/search?q=oscars+2025&rlz=1C1ONGR_enUS1032US1032&oq=oscars+2025&gs_lcrp=EgZjaHJvbWUqDQgAEAAYgwEYsQMYgAQyDQgAEAAYgwEYsQMYgAQyDQgBEAAYgwEYsQMYgAQyDQgCEAAYgwEYsQMYgAQyDQgDEAAYgwEYsQMYgAQyDQgEEAAYgwEYsQMYgAQyDQgFEAAYgwEYsQMYgAQyDQgGEAAYgwEYsQMYgAQyDQgHEAAYgwEYsQMYgAQyEAgIEAAYgwEYsQMYgAQYigUyEAgJEAAYgwEYsQMYgAQYigXSAQgyMjI5ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8)")



