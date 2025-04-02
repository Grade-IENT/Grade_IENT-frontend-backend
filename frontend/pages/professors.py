import streamlit as st

st.set_page_config(page_title= "Gradient - Professors", page_icon=":tada:", layout ="wide", initial_sidebar_state="collapsed")
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



with st.container():

    st.title("Professor Lookup")
    image_column, search_column = st.columns((1,9))

    with image_column:
        st.image("search.png", caption= None, width= 100)


    with search_column:
        prof = text_search = st.text_input("Search up your professors and find their ratings!")
        if prof: 
            st.write("You searched Professor " , prof)
