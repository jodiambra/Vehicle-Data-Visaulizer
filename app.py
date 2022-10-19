#import packages
import streamlit as st
import pandas as pd
import plotly_express as px
from PIL import Image
from streamlit.commands.page_config import Layout 
import csv 


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

st.header('US Vehicle Sales')
st.subheader('Exploratory Data Analysis')

vehicles = pd.read_csv(r'C:/Users/XIX/Documents/coding/projects/Software-Development-Tools/vehicles_us.csv')
st.dataframe(vehicles)



st.title('')

looking = st.checkbox('I am looking to buy a car')
if looking :
    st.write('Great! Let\'s do some shopping!')


st.title('')

st.subheader('')
#-------------------------------#

# Vehicle Price Histogram
st.subheader('Vehicle Price')
vehicle_price = vehicles['price']
vehicle_price_fig = px.histogram(vehicle_price, x='price')

st.plotly_chart(vehicle_price_fig, use_container_width=True)


#-------------------------------#

# price distribution based on model year
st.subheader('Price based on Model Year')
model_price = vehicles[['price', 'model_year']]
model_price_fig = px.scatter(model_price, x='model_year', y='price', color='price')
st.plotly_chart(model_price_fig)


#--------------------------------#

# most common vehicle types
st.subheader('Most Common Vehicle Type')

vehicle_type = vehicles[['type']].value_counts().reset_index()
vehicle_type = pd.DataFrame(vehicle_type)
vehicle_type.columns = ['type','count']

# count of vehicle types
vehicle_type_fig = px.bar(vehicle_type, x='type', y='count', title='Vehicle Types', color='type')
st.write(vehicle_type_fig)


#----------------------------------#

# Cost of vehicle per type of vehicle
st.subheader('Average Cost of Each Vehicle Type')
vehicle_type_cost = vehicles.groupby('type')['price'].mean().reset_index()
vehicle_type_cost = pd.DataFrame(vehicle_type_cost)

vehicle_type_cost_fig = px.bar(vehicle_type_cost, x='type', y='price', title='Average Cost of Vehicle Types')
st.write(vehicle_type_cost_fig)

#--------------------------------------#

# number of vehicles in each model year
st.subheader('The 20 Newest Vehicles')
vehicle_year_new = vehicles[['model_year']].value_counts().nlargest(20).reset_index()
vehicle_year_new = pd.DataFrame(vehicle_year_new)
vehicle_year_new.columns = ['model_year','count']
vehicle_year_new['model_year'] = vehicle_year_new['model_year'].astype('int')

# 20 newest vehicles
vehicle_year_new_fig = px.bar(vehicle_year_new, x='model_year', y='count', title='Newest Vehicles')
st.write(vehicle_year_new_fig)


# count of the oldest vehicles
st.subheader('The 20 Oldest Vehicles')
vehicle_year_old = vehicles[['model_year']].value_counts().nsmallest(20).reset_index()
vehicle_year_old = pd.DataFrame(vehicle_year_old)
vehicle_year_old.columns = ['model_year','count']
vehicle_year_old['model_year'] = vehicle_year_old['model_year'].astype('int')


# oldest vehicle by year
vehicle_year_old_fig = px.bar(vehicle_year_old, x='model_year', y='count', title='Oldest Vehicles')
st.write(vehicle_year_old_fig)


#----------------------------------------#

# count of vehicles by transmission
st.subheader('Vehicle Transmissions')
vehicle_trans = vehicles['transmission'].value_counts().reset_index()
vehicle_trans = pd.DataFrame(vehicle_trans)
vehicle_trans.columns = ['transmission', 'count']

# vehicle transmissions
vehicle_trans_fig = px.bar(vehicle_trans, x='transmission', y='count', title='Vehicle Transmission', color='transmission')
st.write(vehicle_trans_fig)


#----------------------------------------#


# count of vehicles by color
st.subheader('Vehicle Colors')
vehicle_color = vehicles['paint_color'].value_counts().reset_index()
vehicle_color = pd.DataFrame(vehicle_color)
vehicle_color.columns = ['paint_color', 'count']

# Vehicle colors
vehicle_color_fig = px.bar(vehicle_color, x='paint_color', y='count', title='Vehicle Color')
st.write(vehicle_color_fig)