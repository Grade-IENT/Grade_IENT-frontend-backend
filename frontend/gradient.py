# frontend/pages/login.py
import streamlit as st
import psycopg2
from psycopg2 import sql
from pathlib import Path
import bcrypt
import base64

# Set page config
st.set_page_config(page_title="Gradient - Login", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS
login_box_css = """
<style>
.login-box {
    background-color: #ffffff10;
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 3rem;
    width: 350px;
    margin: 0 auto;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    text-align: center;
}
.login-box input {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border-radius: 10px;
    border: 1px solid #ccc;
    font-size: 16px;
}
.login-box button {
    margin-top: 15px;
    width: 100%;
    padding: 10px;
    border-radius: 10px;
    background-color: #4CAF50;
    color: white;
    font-size: 16px;
    border: none;
}
.login-box a {
    display: block;
    margin-top: 1rem;
    font-size: 14px;
    color: #007bff;
}
</style>
"""
st.markdown(login_box_css, unsafe_allow_html=True)

# DB connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="gradient",
        user="postgres"
    )

st.markdown("<div class='login-box'>", unsafe_allow_html=True)

st.image("redcap.jpg", width=100)
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
            st.success("✅ Logged in successfully!")
import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title= "Gradient", page_icon=":tada:", layout ="wide", initial_sidebar_state="collapsed")

st.markdown(
    f'<a href="/"><img class="logo" src="data:image/png;base64,{base64.b64encode(open("logo.png", "rb").read()).decode()}" alt="Logo"></a>',
    unsafe_allow_html=True
)

# use CSS
with open('./style/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

#HEADER
with st.container():
    left, right = st.columns((5,1))

    with left:
        st.subheader("Hi,")
        st.title("Welcome to Gradient!")
        st.write("Excited to have you test out our website! We are your one stop shop to scheduling, prereqs, professors and 4 year plans!")
        #st.write("[click here](https://www.google.com/search?q=oscars+2025&rlz=1C1ONGR_enUS1032US1032&oq=oscars+2025&gs_lcrp=EgZjaHJvbWUqDQgAEAAYgwEYsQMYgAQyDQgAEAAYgwEYsQMYgAQyDQgBEAAYgwEYsQMYgAQyDQgCEAAYgwEYsQMYgAQyDQgDEAAYgwEYsQMYgAQyDQgEEAAYgwEYsQMYgAQyDQgFEAAYgwEYsQMYgAQyDQgGEAAYgwEYsQMYgAQyDQgHEAAYgwEYsQMYgAQyEAgIEAAYgwEYsQMYgAQYigUyEAgJEAAYgwEYsQMYgAQYigXSAQgyMjI5ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8)")
    with right: 
        st.image("redcap.jpg", width= 150)


#--log in ------
with st.container():
    st.write("---")
    st.header("LOG IN:")

    contact_form = """
    <form action="https://formsubmit.co/insiyachitalwala@gmail.com" method="POST">
        <input type = "hidden" name = "_captcha" value="false">
        <input type="email" name="email" placeholder= "Email" required>
        <input type="text" name="password" placeholder="Password" required>
        
    </form>
    """

#        <textarea name = "message" placeholder="your message here" required></textarea>



    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form,unsafe_allow_html=True)
        if st.button("Log In:"):
            st.switch_page("pages/profile.py")
        else:
            st.error("❌ Invalid username or password")

st.markdown("<a href='/create_account'>Create Account</a>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)




