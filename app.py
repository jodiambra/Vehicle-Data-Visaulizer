#import packages
import streamlit as st
import pandas as pd
import plotly_express as px
from PIL import Image
from streamlit.commands.page_config import Layout


#----------------------------#
# Upgrade streamlit library
# pip install --upgrade streamlit

#-----------------------------#
# Page layout

st.set_page_config(page_title='US Vehicle Sales : Exploratory Data Analysis',
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state="auto",
                   menu_items=None)
#-----------------------------#


st.title('US Vehicle Sales')
# Title Picture

image_1 = Image.open('used cars.jpg')

st.image(image_1, width=1000)

#-------------------------------#


# First look at data table


st.subheader('Exploratory Data Analysis')
st.subheader('US Vehicles Data')

vehicles = pd.read_csv(
    r'C:/Users/XIX/Documents/coding/projects/Software-Development-Tools/vehicles_us.csv')
st.dataframe(vehicles)


st.title('')

looking = st.checkbox('I am looking to buy a car')
if looking:
    st.write('Great! Let\'s do some shopping!')

    budget = st.slider(
        'What is Your Budget',
        0.0, 400000.0, (200.0, 425000.0)


    )
    st.write('Budget:', budget)
    st.subheader('')

    st.title('')

    st.subheader('')
    #-------------------------------#

    # Vehicle Price Histogram
    st.header('Vehicle Price')
    vehicle_price = vehicles['price']
    vehicle_price_fig = px.histogram(vehicle_price, x='price')

    st.plotly_chart(vehicle_price_fig, use_container_width=True)

    with st.expander('Details') :
        st.write(''' This chart shows the distribution of vehicle prices. Most 
        vehicles are under $10,000, while a select few are much more than that. 
        A few outliers exist with cars in the 6 figure territory.''')

    #-------------------------------#

    # price distribution based on model year
    st.header('Price based on Model Year')
    model_price = vehicles[['price', 'model_year']]
    model_price_fig = px.scatter(
        model_price, x='model_year', y='price', color='price')
    st.plotly_chart(model_price_fig)

    with st.expander('Details') :
        st.write(''' This chart shows the relationship between vehicle model year and price. We see that 
        most newer vehicles are more expensive. Yet, many classic cars are also quite expensive.''')

    #--------------------------------#

    # most common vehicle types
    st.header('Most Common Vehicle Type')

    vehicle_type = vehicles[['type']].value_counts().reset_index()
    vehicle_type = pd.DataFrame(vehicle_type)
    vehicle_type.columns = ['type', 'count']

    # count of vehicle types
    vehicle_type_fig = px.bar(vehicle_type, x='type',
                              y='count', title='Vehicle Types', color='type')
    st.write(vehicle_type_fig)
    with st.expander('Details') :
        st.write(''' This chart shows the most common vehicle types being sold. They are SUV's, 
        trucks, and then sedans. The other vehicle types are far less prevalent.''')
    #----------------------------------#

    # Cost of vehicle per type of vehicle
    st.header('Average Cost of Each Vehicle Type')
    vehicle_type_cost = vehicles.groupby('type')['price'].mean().reset_index()
    vehicle_type_cost = pd.DataFrame(vehicle_type_cost)

    vehicle_type_cost_fig = px.bar(
        vehicle_type_cost, x='type', y='price', title='Average Cost of Vehicle Types')
    st.write(vehicle_type_cost_fig)

    with st.expander('Details') :
        st.write(''' This chart shows the distribution of vehicle prices. Most 
        vehicles are under $10,000, while a select few are much more than that. 
        A few outliers exist with cars in the 6 figure territory.''')

    #--------------------------------------#
    new_cars = st.checkbox('I Like Newer Model Cars')
    old_cars = st.checkbox('Show Me the Classic Cars')

    # number of vehicles in each model year

    vehicle_year_new = vehicles[['model_year']
                                ].value_counts().nlargest(20).reset_index()
    vehicle_year_new = pd.DataFrame(vehicle_year_new)
    vehicle_year_new.columns = ['model_year', 'count']
    vehicle_year_new['model_year'] = vehicle_year_new['model_year'].astype(
        'int')

    # 20 newest vehicles
    vehicle_year_new_fig = px.bar(
        vehicle_year_new, x='model_year', y='count', title='Newest Vehicles')
    if new_cars:
        st.header('The 20 Newest Vehicles')
        st.write(vehicle_year_new_fig)

    st.title('')

    # count of the oldest vehicles
    vehicle_year_old = vehicles[['model_year']
                                ].value_counts().nsmallest(20).reset_index()
    vehicle_year_old = pd.DataFrame(vehicle_year_old)
    vehicle_year_old.columns = ['model_year', 'count']
    vehicle_year_old['model_year'] = vehicle_year_old['model_year'].astype(
        'int')

    # oldest vehicle by year
    vehicle_year_old_fig = px.bar(
        vehicle_year_old, x='model_year', y='count', title='Oldest Vehicles')
    if old_cars:
        st.header('The 20 Oldest Vehicles')
        st.write('Check Out These Classic Cars')
        st.write(vehicle_year_old_fig)

    #----------------------------------------#

    # count of vehicles by transmission
    st.header('Vehicle Transmissions')
    vehicle_trans = vehicles['transmission'].value_counts().reset_index()
    vehicle_trans = pd.DataFrame(vehicle_trans)
    vehicle_trans.columns = ['transmission', 'count']

    # vehicle transmissions
    vehicle_trans_fig = px.bar(vehicle_trans, x='transmission',
                               y='count', title='Vehicle Transmission', color='transmission')
    st.write(vehicle_trans_fig)

    #----------------------------------------#

    # count of vehicles by color
    st.header('Vehicle Colors')
    vehicle_color = vehicles['paint_color'].value_counts().reset_index()
    vehicle_color = pd.DataFrame(vehicle_color)
    vehicle_color.columns = ['paint_color', 'count']

    # Vehicle colors
    vehicle_color_fig = px.bar(
        vehicle_color, x='paint_color', y='count', title='Vehicle Color')
    st.write(vehicle_color_fig)

    #-----------------------------------------#

    # type/size of engine
    st.header('Engine Size')
    vehicle_cylinder = vehicles['cylinders'].value_counts().reset_index()
    vehicle_cylinder.columns = ['cylinder', 'count']

    # vehicle cylinders
    vehicle_cylinder_fig = px.bar(
        vehicle_cylinder, x='cylinder', y='count', title='Vehicle Cylinders')
    st.write(vehicle_cylinder_fig)

    #----------------------------------------------#

    # count of vehicles by condition

    vehicle_condition = vehicles['condition'].value_counts().reset_index()
    vehicle_condition.columns = ['condition', 'count']

    # vehicle condition
    st.header('Vehicle Condition')
    vehicle_condition_fig = px.bar(
        vehicle_condition, x='condition', y='count', title='Vehicle Condition')
    st.write(vehicle_condition_fig)

    #---------------------------------------------#

    # Lemons

    # top 20 vehicles with the highest milage
    vehicle_milage_high = vehicles[['model', 'price', 'odometer']].nlargest(
        20, columns='odometer').reset_index(drop=True)

    # highest milage vehicles
    st.header('Half a Million Miles Cars...')
    vehicle_milage_high_fig = px.bar(vehicle_milage_high, x='model', y=(
        ['odometer', 'price']), title='Vehicle Milage', log_y=True)

    st.write(vehicle_milage_high_fig)

    #-------------------------------------------#

    # Cost of care by model year

    st.header('Cost of Cars by Model Year')

    vehicle_model_year_cost = vehicles.groupby(
        'model_year')['price'].mean().reset_index()
    vehicle_model_year_cost = pd.DataFrame(vehicle_model_year_cost)

    st.plotly_chart(px.histogram(
        vehicle_model_year_cost, x='model_year', y='price'))

    #-------------------------------------------#

    # correlation of price and other variables

    st.header('What is the Greatest Contributor to Vehicle Price')

    st.write(vehicles.corr())

    #------------------------------------------#

    st.title('')

    st.title('')

    st.title('')

    helpful = st.button('Was This Helpful?')
    if helpful:
        st.write('Glad to Help!!!')
