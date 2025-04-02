import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title= "Gradient - Four Year Plan", page_icon=":tada:", layout ="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        div[data-testid="collapsedControl"] {
            visibility: hidden;
        }
    </style>
    """,
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
     with left:          
        if st.button("Profile", use_container_width= True):
            st.switch_page("pages/profile.py")
    
     with middle:

        if st.button("Professors", use_container_width= True):
            st.switch_page("pages/professors.py")

     with right:
        if st.button("Scheduling", use_container_width=True):
            st.switch_page("pages/schedule.py")
     st.write("---")


with st.container():
    

    st.title("Four Year Plan")
    Major = st.selectbox(
        'Pick a Major:',
        (' ','Aerospace Engineering','Biomedical Engineering', 'Biochemical Engineering', 'Chemical Engineering', 'Civil Engineering', 'Environmental Engineering', 'Electrical and Computer Engineering', 'Industrial and Systems Engineering', 'Materials Science Engineering', 'Mechanical and Aerospace Engineering','Packaging Engineering')
    )
    
    # major = text_search = st.text_input("Search up a major for the 4 year plan!")
    # if major: 
    #     st.write("4 year schedule for " , major)




#year 1 and 2
with st.container():

        st.subheader("Year 1:")
        fall, spring = st.columns(2)
                
        with fall: 
            df = pd.DataFrame(
                np.zeros((5, 4)), columns=("Class","Code", "Credits", "Difficulty")
            )

            st.table(df)

        with spring: 
            df = pd.DataFrame(
                np.zeros((5, 4)), columns=("Class","Code", "Credits", "Difficulty")
            )

            st.table(df)

with st.container():
        st.subheader("Year 2:")
        
        fall, spring = st.columns(2)
        with fall: 
            df = pd.DataFrame(
                np.zeros((5, 4)), columns=("Class","Code", "Credits", "Difficulty")
            
            )

            st.table(df)

        with spring: 
            df = pd.DataFrame(
                np.zeros((5, 4)), columns=("Class","Code", "Credits", "Difficulty")
            
            )

            st.table(df)

# year 4 and 4 


with st.container():
    
        st.subheader("Year 4:")
        fall, spring = st.columns(2)
        with fall: 
            df = pd.DataFrame(
                np.zeros((5, 4)), columns=("Class","Code", "Credits", "Difficulty")
            
            )

            st.table(df)

        with spring: 
            df = pd.DataFrame(
                np.zeros((5, 4)), columns=("Class","Code", "Credits", "Difficulty")
            
            )

            st.table(df)

with st.container():

    st.subheader("Year 4:")

    fall, spring = st.columns(2)
    with fall: 
            df = pd.DataFrame(
                np.zeros((5, 4)), columns=("Class","Code", "Credits", "Difficulty")
            
            )

            st.table(df)

    with spring: 
            df = pd.DataFrame(
                np.zeros((5, 4)), columns=("Class","Code", "Credits", "Difficulty")
            
            )

            st.table(df)

