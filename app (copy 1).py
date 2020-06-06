import streamlit as st
import pandas as pd
import numpy  as np

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
st.header("where are the most people injured in NY ? ")
injured_people = st.slider("Number of persons injured due to vehicle:",0,19)
st.map(data.query("injured_persons >= @injured_people")[['latitude','longitude']].dropna(how="any"))



if st.checkbox ("SHOW DATA",False) :
    st.subheader ('RAW DATA')
    st.write(data)
