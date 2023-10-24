import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(
    layout='centered',
    page_title='Lelis Weather'
)

api_key = st.secrets['token']

#-------------------** Every time the language is changed, the page is reloaded and the city too. With session state, the city variable keeps its value
if 'city' in st.session_state:
    session_city = st.session_state['city']
else:
    session_city = 'Brasília'



row_header = st.columns(2)

with row_header[0]: is_english = st.toggle('English (°F)', False)

if is_english:
    with row_header[1]: st.write('Developed with Streamlit and OpenWeatherMap.org API')

    st.title('Current Weather Data', False)

    st.subheader('by Lelis', False)

    city = st.text_input('City name', value=session_city)
    st.session_state['city'] = city

    lang = 'en'
    units = 'imperial'
else:
    with row_header[1]: st.write('Desenvolvido com Streamlit e API da OpenWeatherMap.org')

    st.title('Clima Atual', False)

    st.subheader('por Lelis', False)

    city = st.text_input('Nome da Cidade', value=session_city)
    st.session_state['city'] = city

    lang = 'pt_br'
    units = 'metric'

#-------------------** Getting coordinates by selected city

response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=2&appid={api_key}').json()

lat = response[0]['lat']
lon = response[0]['lon']
state = response[0]['state']
country = response[0]['country']

map = folium.Map(location=[lat, lon], zoom_start=11)
folium.Marker([lat, lon], popup=f'{city}', tooltip=f'{city + ", " + country}').add_to(map)
st_data = st_folium(map, width=725, height=300)

#-------------------** Getting weather data

response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lang={lang}&units={units}&lat={lat}&lon={lon}&appid={api_key}').json()


description = response['weather'][0]['description']
temperature = response['main']['temp']
feels_like = response['main']['feels_like']
temp_min = response['main']['temp_min']
temp_max = response['main']['temp_max']
pressure = response['main']['pressure']
humidity = response['main']['humidity']
visibility = response['visibility']
wind_speed = response['wind']['speed']


#-------------------** Page Layout

row0 = st.columns(1)
row1 = st.columns(4)
row2 = st.columns(4)

if is_english:
    with row0[0]: st.subheader(f'{description.title()}', False)

    with row1[0]: st.metric('Temperature', f'{round(temperature)} °F')
    with row1[1]: st.metric('Feels Like Temperature', f'{round(feels_like)} °F')
    with row1[2]: st.metric('Min',f'{round(temp_min)} °F')
    with row1[3]: st.metric('Max', f'{round(temp_max)} °F')

    with row2[0]: st.metric('Humidity', f'{humidity}%')
    with row2[1]: st.metric('Atmospheric Pressure', f'{pressure} hPa')
    with row2[2]: st.metric('Visibility', f'{visibility/1000} km')
    with row2[3]: st.metric('Wind Speed', f'{wind_speed}m/s')
else:
    with row0[0]: st.subheader(f'{description.title()}', False)

    with row1[0]: st.metric('Temperatura', f'{round(temperature)} °C')
    with row1[1]: st.metric('Sensação Térmica', f'{round(feels_like)} °C')
    with row1[2]: st.metric('Temperatura Mínima',f'{round(temp_min)} °C')
    with row1[3]: st.metric('Temperatura Máxima', f'{round(temp_max)} °C')

    with row2[0]: st.metric('Umidade do ar', f'{humidity}%')
    with row2[1]: st.metric('Pressão atmosférica', f'{pressure} hPa')
    with row2[2]: st.metric('Visibilidade', f'{visibility/1000} km')
    with row2[3]: st.metric('Velocidade do vento', f'{wind_speed}m/s', )