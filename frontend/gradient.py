import streamlit as st
import psycopg2
import bcrypt
import base64

st.set_page_config(page_title="Gradient - Login", layout="wide", initial_sidebar_state="collapsed")

# Function to load CSS for styling
def load_css():
    with open("./style/style.css") as f:  # Make sure the path to your CSS is correct
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_logo():
    with open("logo.png", "rb") as logo_file:
        encoded_logo = base64.b64encode(logo_file.read()).decode()
        st.markdown(
        f'<img src="data:image/png;base64,{encoded_logo}" alt="Logo">',
        unsafe_allow_html=True
    )

display_logo()


# DB connection (No changes here)
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="gradient",
        user="postgres"
    )


# Main container for left and right sections
with st.container():
    left, right = st.columns(2)  # Two equal columns for the left and right sections

    with left:
        st.markdown(
            """
            <div style="color: white; text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; font-size: 36px; padding: 150px;">
                Welcome to Grade-IENT. <br> Our goal is to help students achieve academic success by helping them create their path through their Engineering major at Rutgers! We are excited to have you test out our website! We are your one stop shop to scheduling, prereqs, professors, and 4-year plans.
            </div>
            """, 
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            """
            <div style="text-align: left; display: flex; flex-direction: column; justify-content: center; align-items: center; font-size: 25px; height: 100%; padding-left: 20px; padding-right: 20px; margin-top: 100px;">
                <h2>Welcome back!</h2>
                You can sign in to access your existing account.
            </div>
            """,
            unsafe_allow_html=True
        )
       
        st.markdown(
            """
            <div style="padding-top: 20px; padding-bottom: 20px; margin-left: 100px; font-size: 40px; font-weight: bold; color: #8c4bbf;">
                 Sign In
            </div>
            """, unsafe_allow_html=True
        )
        
        username = st.text_input("Username or email")
        password = st.text_input("Password", type="password")

        st.markdown(
            """
            <style>
                .stTextInput, .stPasswordInput {
                    max-width: 900px;
                    margin-left: 100px;  /* Position the input fields 100px from the left */
                    margin-bottom: 20px;  /* Adds space between the fields */
                }

                .stButton > button {
                    color: white;
                    padding: 15px 30px;  /* Adding consistent padding to the Sign In button */
                    cursor: pointer;
                    max-width: 900px;
                    margin-left: 100px;  /* Position the Sign In button 100px from the left */
                    margin-top: 20px;    /* Spacing above the button */
                    background-color: #8c4bf2;  /* Correct purple background color for the Sign In button */
                    border-radius: 8px;  /* Rounded corners */
                    text-align: center;  /* Center text within the button */
                    border: none;  /* Remove any default border */``
                }
                
                .stCheckbox {
                    margin-left: 100px;  /* Position both checkbox and 'Forgot password?' link 100px from the left */
                    margin-bottom: 20px;  /* Adds space between the checkbox/link and the next element */
                }

                .stMarkdown a{
                    margin-left: 100px;  /* Position both checkbox and 'Forgot password?' link 100px from the left */
                    margin-bottom: 20px;  /* Adds space between the checkbox/link and the next element */
                    color: #8c4bf2
                }

            </style>
            """, unsafe_allow_html=True
        )
        
        remember_me = st.checkbox("Remember me")
     #   forgot_password = st.markdown('<a href="/forgot_password">Forgot password?</a>', unsafe_allow_html=True)
        
        if st.button("Sign In"):
            # Your sign-in logic goes here
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, userPassword FROM UserAccount WHERE username = %s", (username,))
                result = cur.fetchone()

                if result and bcrypt.checkpw(password.encode(), result[1].encode()):
                    st.session_state["user_id"] =  result[0]
                    st.switch_page("pages/profile.py")  # Rerun to trigger page switch
        st.markdown("<a href='/create_account'>New here? Create an Account</a>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # Close the div here

# Load custom styles
load_css()
