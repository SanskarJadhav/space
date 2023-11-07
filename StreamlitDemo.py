
import streamlit as st
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/SanskarJadhav/space/main/Spacedata.csv')

tk = 0

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpaperaccess.com/full/17068.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

st.title('Space Travel')
add_bg_from_url()
col1, col2 = st.columns(2)

with col1:
	ship_name = st.selectbox('Select your ship: ', df['Ship'], index=0)

with col2:
	cost = st.slider('Cost of ship: ', 1000, 4000, 2000)
	if st.button('Submit'):
        	tk = 1

if tk==1:
	if(cost>2000):
		st.markdown('This is very expensive!')
	else:
		st.markdown('This is within budget.')



