#import packages
import streamlit as st
import pandas as pd
import plotly_express as px
from PIL import Image
from streamlit.commands.page_config import Layout

#----------------------------#
# Upgrade S=streamlt library 
# pip install --upgrade streamlit

#-----------------------------#
# Page layout 
st.beta_set_page_config(layout='wide')
#-----------------------------#

# Title
image_1 = Image.open('used cars.jpg')

st.image(image_1, width = 1000 )

st.header('US Vehicle Sales')   

st.subheader('Exploratory Data Analysis')



vehicles = pd.read_csv(
    r'C:/Users/XIX/Documents/coding/projects/Software-Development-Tools/vehicles_us.csv')



