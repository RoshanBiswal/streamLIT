import streamlit as st
import pandas as pd
import numpy  as np
import pydeck as pdk
import plotly.express as px
###st.title("I am batman !")
###st.markdown("### MY FIRST STREAM LIT APP")

data_url = (
"/home/rhyme/Desktop/Project/Motor_Vehicle_Collisions_-_Crashes.csv"
)
st.title("Motor Vehicle Collisions")
st.markdown("Dashboard for NY Collisions")
@st.cache(persist=True)### ONLY RUN WHEN INPUT IS CHANGE
def load_data(nrows):
    data = pd.read_csv(data_url, nrows = nrows , parse_dates = [['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'], inplace=True)
    lowercase = lambda x : str(x).lower()
    data.rename(lowercase, axis = 'columns' , inplace = True)
    data.rename(columns={'crash_date_crash_time' : 'date/time'}, inplace =True)
    return data

data = load_data(100000)
Org_data = data
st.header("where are the most people injured in NY ? ")
injured_people = st.slider("Number of persons injured due to vehicle:",0,19)
st.map(data.query("injured_persons >= @injured_people")[['latitude','longitude']].dropna(how="any"))




st.header("How many collision occue during a given time of day ? ")
hour = st.selectbox("Hour to look at" , range(0,24),1)
data = data[data['date/time'].dt.hour == hour ]

st.markdown("Vechicle collisions between %i:00 and %i:00" %(hour,(hour+1) %24))
midpoint = (np.average(data['latitude']),np.average(data['longitude']))
st.write(pdk.Deck(
   map_style="mapbox://style/mapbox/light-v9",
   initial_view_state ={
   "latitude" : midpoint[0],
   "longitude" : midpoint[1],
   "zoom" : 11,
   "pitch" :50,

   },
   layers = [
        pdk.Layer(
        "HexagonLayer",
        data=data[['date/time', 'latitude', 'longitude']],
        get_position=['longitude','latitude'],
        radius = 50,
        extruded = True,##3d
        pickable = True,
        elevation_scale = 6,
        elevation_range = [0,1000],
        ),
   ],
))







st.header("breakdown by minute between %i:00 and %i:00" %(hour,(hour+1) %24))
filtered = data[
           (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute,bins=60,range = (0,60))[0]
chart_data = pd.DataFrame({'minute' : range(60),'crashes':hist})
fig = px.bar(chart_data , x ='minute', y = 'crashes' ,hover_data = ['minute','crashes'], height = 400 )
st.write(fig)

st.header("Top 5 dangerous streets by affected type")
select = st.selectbox('Affected type of people' ,  ['Pedestrians','cyclists','motorists' ])
if select == 'Pedestrians':
    st.write(Org_data.query('injured_pedestrians >= 1')[["on_street_name","injured_pedestrians"]].sort_values(by=['injured_pedestrians'],ascending=False).dropna(how='any')[:5])
elif select == 'cyclists':
    st.write(Org_data.query('injured_cyclists >= 1')[["on_street_name","injured_cyclists"]].sort_values(by=['injured_cyclists'],ascending=False).dropna(how='any')[:5])
elif select == 'motorists':
    st.write(Org_data.query('injured_motorists >= 1')[["on_street_name","injured_motorists"]].sort_values(by=['injured_motorists'],ascending=False).dropna(how='any')[:5])




if st.checkbox ("SHOW DATA",False) :
    st.subheader ('RAW DATA')
    st.write(data)
