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
    r'vehicles_us.csv')


# filling missing data
vehicles['paint_color'] = vehicles['paint_color'].fillna('unavailable')
vehicles['model_year'] = vehicles.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
vehicles['cylinders'] = vehicles.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))
vehicles['odometer'] = vehicles.groupby('model_year')['odometer'].transform(lambda x: x.fillna(x.mean()))
vehicles['odometer'] = vehicles.groupby('model')['odometer'].transform(lambda x: x.fillna(x.mean()))
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)


vehicles['manufacturer'] = vehicles['model'].apply(lambda x: x.split()[0])
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



st.header('Let\'s compare price distribution between manufacturers')
manufac_list = sorted(vehicles['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1', manufac_list, index=manufac_list.index('bmw'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                                manufac_list, index=manufac_list.index('toyota'))
mask_filter = (vehicles['manufacturer'] == manufacturer_1) | (vehicles['manufacturer'] == manufacturer_2)
vehicles_filtered = vehicles[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(vehicles_filtered,
                        x='price',
                        nbins=30,
                        color='manufacturer',
                        histnorm=histnorm,
                        barmode='overlay'))

with st.expander('Details'):
    st.write(''' This chart shows the price distributions among manufacturers. Here, 
        you are able to compare two manufacturers at a time. ''')


# Vehicle Price Histogram
st.header('Vehicle Price')
vehicle_price = vehicles['price']
vehicle_price_fig = px.histogram(vehicle_price, x='price')

st.plotly_chart(vehicle_price_fig, use_container_width=True)

with st.expander('Details'):
    st.write(''' This chart shows the distribution of vehicle prices. Most 
        vehicles are under $10,000, while a select few are much more than that. 
        A few outliers exist with cars in the 6 figure territory.''')

#-------------------------------#

# price distribution based on model year
st.header('Price based on Model Year')
model_price = vehicles[['price', 'model_year']]
model_price_fig = px.scatter(model_price, x='model_year', y='price', color='price')
st.plotly_chart(model_price_fig)


with st.expander('Details'):
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

with st.expander('Details'):
        st.write(''' This chart shows the most common vehicle types being sold. They are SUV's, 
        trucks, sedans, and then pickups. The other vehicle types are far less prevalent.''')


st.write(px.histogram(vehicles, x='manufacturer',  color='type', title='Vehicle Types by Manufacturer'))

#----------------------------------#

# Cost of vehicle per type of vehicle
st.header('Average Cost of Each Vehicle Type')
vehicle_type_cost = vehicles.groupby('type')['price'].mean().reset_index()
vehicle_type_cost = pd.DataFrame(vehicle_type_cost)

vehicle_type_cost_fig = px.bar(
    vehicle_type_cost, x='type', y='price', title='Average Cost of Vehicle Types')
st.write(vehicle_type_cost_fig)

with st.expander('Details'):
    st.write(''' This chart shows the average cost of each vehicle type. The most expensive 
        vehicles are buses, trucks, and pickups. The cheapest vehicles are sedans and hatchbacks.''')

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

    with st.expander('Details'):
        st.write(''' This chart shows the 20 newest vehicles for sale based on model year. The greatest 
            number of vehicles ranges from model years 2010 to 2016. ''')

st.title('')

# count of the oldest vehicles
vehicle_year_old = vehicles[['model_year']
                        ].value_counts().nsmallest(20).reset_index()
vehicle_year_old = pd.DataFrame(vehicle_year_old)
vehicle_year_old.columns = ['model_year', 'count']
vehicle_year_old['model_year'] = vehicle_year_old['model_year'].astype('int')

# oldest vehicle by year
vehicle_year_old_fig = px.bar(
    vehicle_year_old, x='model_year', y='count', title='Oldest Vehicles')
if old_cars:
    st.header('The 20 Oldest Vehicles')
    st.write('Check Out These Classic Cars')
    st.write(vehicle_year_old_fig)

    with st.expander('Details'):
        st.write(''' This chart shows the 20 oldest vehicles for sale based on model year. There are 2 vehicles made in 1908, while the majority range from the 1960s 
        to the 1980's. ''')

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

with st.expander('Details'):
    st.write(
        ''' Most of the vehicles for sale have an automatic transmission. ''')
st.header('Manufacturer Transmissions')
st.write(px.histogram(vehicles, x='manufacturer',  color='transmission', title='Manufacturer Transmission Types'))

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

with st.expander('Details'):
    st.write(''' Most of the vehicles for sale are either white or black paint. 
                Some cars have a custom paint color. The second highest count was an undefined color in the data. ''')


st.header('Paint Colors of Manufacturers')
st.write(px.histogram(vehicles, x='manufacturer',  color='paint_color', title='Manufacturer Paint Colors')) 
with st.expander('Details'):
    st.write(''' This shows the options for colors of the different manufacturers. ''')
#----------------------------------------------# 
#############################################

#----------------------------------------------#


# type/size of engine
st.header('Engine Size')
vehicle_cylinder = vehicles['cylinders'].value_counts().reset_index()
vehicle_cylinder.columns = ['cylinder', 'count']

# vehicle cylinders
vehicle_cylinder_fig = px.bar(
    vehicle_cylinder, x='cylinder', y='count', title='Vehicle Cylinders')
st.write(vehicle_cylinder_fig)


with st.expander('Details'):
    st.write(''' Most of the vehicles for sale are either V8, V6, or 4 cylinder engines. There are very 
            few engine types other than those mentioned for sale.''')



st.header('Different Engine Size of Manufacturers')
st.write(px.histogram(vehicles, x='manufacturer', color='cylinders', title='Manufacturer Engine Sizes'))

with st.expander('Details'):
    st.write(''' This graph shows the options of engine sizes for the different manufacturers.''')
#----------------------------------------------# 
#############################################

#----------------------------------------------#
   


# count of vehicles by condition

vehicle_condition = vehicles['condition'].value_counts().reset_index()
vehicle_condition.columns = ['condition', 'count']

# vehicle condition
st.header('Vehicle Condition')
vehicle_condition_fig = px.bar(
    vehicle_condition, x='condition', y='count', title='Vehicle Condition')
st.write(vehicle_condition_fig)

with st.expander('Details'):
    st.write(''' Most of the vehicles for sale are in excellent or good condition. Some are like new, 
            while there are very few bran new or salvage.''')

st.header('Model year and Vehicle Condition')
st.write(px.histogram(vehicles, x='model_year', color='condition', title='Distribution of Model Year and Condition'))
    
with st.expander('Details'):
    st.write(''' This graph shows the distribution of vehicle conditions. The most common conditions are excellent, good, and like new. ''')

#--------------------------------------------------#

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

with st.expander('Details'):
    st.write(''' These are the 20 vehicles with the highest milage. All of these vehicles have more than half a million miles on them! ''')

#-------------------------------------------#

# Cost of car by model year

st.header('Cost of Cars by Model Year')

vehicle_model_year_cost = vehicles.groupby(
        'model_year')['price'].mean().reset_index()
vehicle_model_year_cost = pd.DataFrame(vehicle_model_year_cost)

st.plotly_chart(px.histogram(
    vehicle_model_year_cost, x='model_year', y='price', title='Vehicle Mean Price by Model Year'))

with st.expander('Details'):
    st.write(''' This histogram shows  the distribution of mean price by vehicle year. Overall, vehicles form the 60's hold the most 
            value among these other vehicle model years. ''')

#-------------------------------------------#

# Manufacturer Fuel Types

st.header('Different Fuel Types by Manufacturer')

   
st.write(px.histogram(vehicles, x='manufacturer',  color='fuel', title='Manufacturer Fuel Types'))
    

with st.expander('Details'):
    st.write(''' These are the different fuel types of the vehicles. Gas powered vehicles predominate, while 
        some manufacturers have diesel and hybrids.   ''')

    
#------------------------------------------#



# Manufacturer car models

st.header('The Top Models and Count')

manu_models = vehicles[['manufacturer','model']].value_counts().reset_index(level=0)
manu_models.columns = [ 'manufacturer', 'count']

st.write(manu_models)
with st.expander('Details'):
    st.write(''' This is a list of the most popular models, by their frequency in the sales data.   ''')

st.header('Manufacturer Vehicle Models')

st.write(px.histogram(vehicles, x='manufacturer',  color='model', title='Manufacturer Models'))
with st.expander('Details'):
    st.write(''' This graph shows the different models of the manufacturers.   ''')


#-------------------------------------------#

# Manufacturer Drive Trains
    

st.header('Availability of 4 Wheel Drive')
st.write(px.histogram(vehicles, x='manufacturer',  color='is_4wd', title='Manufacturer Drive-Trains',text_auto='.2s'))

with st.expander('Details'):
    st.write(''' Options for 4 Wheel drive per manufacturer. Number 1  value represents the presence of 4WD, 0 is 
        the absence of 4WD.   ''')
#----------------------------------------------#


# Manufacturer mean price

st.header('Mean Price of Vehicle per Manufacturer')

st.write(px.bar(vehicles.groupby('manufacturer')['price'].mean(), title='Manufacturer Mean Vehicle Price', text_auto='.2s'))

    
with st.expander('Details'):
    st.write(''' This is what you can expect to pay when looking for a vehicle of each manufacturer. These vales represent
        the mean vehicle price. the most expensive cars, on average, are Mercedes-Benz.   ''')

   

#---------------------------------------------------#

#  Price of vehicles based on days posted
st.header('Price of Vehicles based on Days Posted')
vehicle_days_fig = px.scatter(vehicles, y='price', x='days_listed', size='days_listed', color='manufacturer', title='Price based on Days Posted')
st.write(vehicle_days_fig)

with st.expander('Details'):
    st.write(''' This graph illustrates the differences in price, based on the number of days the vehicle has been 
        posted for sale.  ''')
#-----------------------------------------------#

st.header('Vehicle Manufacturer Price')
st.write(px.scatter(vehicles, x='price', animation_frame='model_year', size='odometer', animation_group='model',  
            color='manufacturer', log_y=True, log_x=True, title='Manufacturer Vehicle Price Over Time '))
with st.expander('Details'):
    st.write(''' This is an animation of the fluctuations in vehicle prices, per manufacturer, over the model years.  ''')

# correlation of price and other variables

st.header('What is the Greatest Contributor to Vehicle Price')

st.write(vehicles.corr())

with st.expander('Details'):
    st.write(''' This correlation matrix shows somewhat of a positive relationship with price and model year, meaning 
            the price of the vehicle usually increases as the model year increases. On the other hand, the price of the vehicle usually 
            decreases as the milage increases, demonstrating a negative relationship.  ''')






st.title('')

st.title('')

st.title('')

helpful = st.button('Was This Helpful?')
if helpful:
    st.write('Glad to Help!!!')
