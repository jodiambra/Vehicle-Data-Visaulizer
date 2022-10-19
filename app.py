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

st.set_page_config(page_title='US Vehicle Sales : Exploratory Data Analysis', 
page_icon=None, 
layout='wide', 
initial_sidebar_state="auto", 
menu_items=None)
#-----------------------------#

# Title Picture

image_1 = Image.open('used cars.jpg')

st.image(image_1, width = 1000 )

#-------------------------------#


# First look at data table  

st.subheader('Vehicles')

@st.cache
vehicles = pd.read_csv('/vehicles_us.csv')
st.checkbox("Use container width", value=False, key="use_container_width")
st.dataframe(vehicles)


#-------------------------------#

# Vehicle Price Histogram

vehicle_price = vehicles['price']
vehicle_price_fig = px.histogram(vehicle_price, x='price')
st.write(vehicle_price_fig)


#-------------------------------#