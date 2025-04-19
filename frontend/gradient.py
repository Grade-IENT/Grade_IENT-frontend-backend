# frontend/pages/login.py
import streamlit as st
import psycopg2
from psycopg2 import sql
from pathlib import Path
import bcrypt
import base64
from PIL import Image

st.set_page_config(page_title="Gradient - Login", layout="centered", initial_sidebar_state="collapsed")

st.markdown(
    f'<a href="/"><img class="logo" src="data:image/png;base64,{base64.b64encode(open("logo.png", "rb").read()).decode()}" alt="Logo"></a>',
    unsafe_allow_html=True
)

#HEADER
with st.container():
    left, right = st.columns((5,1))

    with left:
        st.subheader("Hi,")
        st.title("Welcome to Gradient!")
        st.write("Excited to have you test out our website! We are your one stop shop to scheduling, prereqs, professors and 4 year plans!")
        #st.write("[click here](https://www.google.com/search?q=oscars+2025&rlz=1C1ONGR_enUS1032US1032&oq=oscars+2025&gs_lcrp=EgZjaHJvbWUqDQgAEAAYgwEYsQMYgAQyDQgAEAAYgwEYsQMYgAQyDQgBEAAYgwEYsQMYgAQyDQgCEAAYgwEYsQMYgAQyDQgDEAAYgwEYsQMYgAQyDQgEEAAYgwEYsQMYgAQyDQgFEAAYgwEYsQMYgAQyDQgGEAAYgwEYsQMYgAQyDQgHEAAYgwEYsQMYgAQyEAgIEAAYgwEYsQMYgAQYigUyEAgJEAAYgwEYsQMYgAQYigXSAQgyMjI5ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8)")
  

# Custom CSS to center the logo
login_box_css = """
<style>
.center-logo {
    display: flex;
    justify-content: center;
    align-items: center;
}
.center-logo img {
    width: auto;
    height: 100px;  /* Adjust height as needed */
}
</style>
"""

st.markdown(login_box_css, unsafe_allow_html=True)

# Read the logo and encode it into base64
with open("logo.png", "rb") as logo_file:
    encoded_logo = base64.b64encode(logo_file.read()).decode()

# Centered logo
st.markdown(
    f'<div class="center-logo"><img src="data:image/png;base64,{encoded_logo}" alt="Logo"></div>',
    unsafe_allow_html=True
)

# DB connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="gradient",
        user="postgres"
    )

st.markdown("<div class='login-box'>", unsafe_allow_html=True)

st.markdown("## Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log In"):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, userPassword FROM UserAccount WHERE username = %s", (username,))
        result = cur.fetchone()

        if result and bcrypt.checkpw(password.encode(), result[1].encode()):
            st.session_state["user_id"] = result[0]
         #   st.experimental_rerun()  # Rerun first to trigger switch_page

# Then redirect at the top of the file (or just below the login logic)
if "user_id" in st.session_state:
    st.switch_page("pages/profile.py")

# use CSS
with open('./style/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


st.markdown("<a href='/create_account'>Create Account</a>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)




