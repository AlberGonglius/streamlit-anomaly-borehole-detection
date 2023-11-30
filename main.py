import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from functions import generate_range, get_datetime, generate_range_hours
from datetime import datetime, timedelta

# Load your custom CSS file
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

col1, col2 = st.columns([5,20])
with col1:
   st.image('images/logohocol.jpg')

with col2:
   st.markdown("<h1 style='text-align: center;'>Detección de anomalías en Sistemas de extraccion</h1>", unsafe_allow_html=True)

field_mapping = {'OCELOTE':['Pintada Norte 8H','OCELOTE 30H', 'OCELOTE 120H', 'OCELOTE 138H']}

option = st.selectbox(
'Elija un campo',
['OCELOTE', ''])

if len(option) > 0:
    fechas_falla = {'Pintada Norte 8H': [datetime.strptime('2023-06-05 05:00:00', '%Y-%m-%d %H:%M:%S').date()],
                    'OCELOTE 30H': [datetime.strptime('2023-05-24 05:00:00', '%Y-%m-%d %H:%M:%S').date()],
                    'OCELOTE 120H': [datetime.strptime('2023-01-25 05:00:00', '%Y-%m-%d %H:%M:%S').date()],
                    'OCELOTE 138H': [datetime.strptime('2023-01-08 05:00:00', '%Y-%m-%d %H:%M:%S').date()]}
    boreholes = field_mapping[option]
    borehole_states = {'Pintada Norte 8H':True,
                       'OCELOTE 30H': False,
                       'OCELOTE 120H': False,
                       'OCELOTE 138H': False}
    
    option_2 = st.selectbox(
    'Elija cómo ver los pozos',
    ['Ver todos los pozos', 'Ver los pozos individualmente'])
    if option_2 == 'Ver todos los pozos':
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Ver Pozos en estado normal", expanded=True):
                st.markdown("<h3 style='text-align: center;'>Pozos estado normal</h3>", unsafe_allow_html=True)
                col_img1,col_img2,col_img3 = st.columns(3)
                with col_img2:
                    st.image('images/green_dot.png')
                st.markdown("<h3 style='text-align: center;'>OCELOTE 30H</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center;'>OCELOTE 120H</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center;'>OCELOTE 138H</h3>", unsafe_allow_html=True)
            
        with col2:
            with st.expander("Ver Pozos en estado de alarma", expanded=True):
                st.markdown("<h3 style='text-align: center;'>Pozos estado alarma</h3>", unsafe_allow_html=True)
                col_img1,col_img2,col_img3 = st.columns(3)
                with col_img2:
                    st.image('images/red_dot.png')
                st.markdown("<h3 style='text-align: center;'>Pintada Norte 80H</h3>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center;'>Ver Score de Anomalía</h3>", unsafe_allow_html=True)
        st.write("Las anomalías ocurren cuando el score de anomalía sobrepasa uno de los umbrales, que se ven en la imagen como lineas negras horizontales.")
        options = st.multiselect(
                    'Elige los pozos',
                    boreholes,
                    boreholes)
        colors = ['gray','navy','lightblue','slateblue']
        plt.figure(facecolor='azure')
        ax = plt.axes()
        ax.set_facecolor("azure")
        plt.title('Score de Anomalía')
        for i in range(len(boreholes)):
            if boreholes[i] in options:
                start_date = get_datetime(1,1,2023)
                end_date = get_datetime(6,6,2023)
                days = end_date - start_date
                days = days.days
                y = np.random.random(days)*0.4 - 0.2
                x = generate_range(start_date, end_date)
                
                for j in range(len(x)):
                    if x[j].date() in fechas_falla[boreholes[i]]:
                        y[j] = -0.5
                plt.plot(x,y,label = boreholes[i], color=colors[i])
                plt.axhline(y=0.2,lw=0.8,color='k')
                plt.axhline(y=-0.2,lw=0.8,color='k')
                plt.legend()
        st.pyplot(plt.gcf())
    elif option_2 == 'Ver los pozos individualmente':
        option_3 = st.selectbox(
                    'Elija un pozo',
                    boreholes)
        state = borehole_states[option_3]
        with st.expander("Ver estado del pozo", expanded=True):
            col_img1,col_img2,col_img3,col_image4,col_image5 = st.columns(5)
            with col_img3:
                if not state:
                    st.image('images/green_dot.png')
                else:
                    st.image('images/red_dot.png')
            if not state:        
                st.markdown("<h5 style='text-align: center;'>El pozo {} está en estado normal</h5>".format(option_3), unsafe_allow_html=True)
            else:
                st.markdown("<h5 style='text-align: center;'>El pozo {} está en estado anómalo</h5>".format(option_3), unsafe_allow_html=True)
        option_4 = st.selectbox(
                    'Elija una opción para visualizar',
                    ['Score de anomalía últimas 48 horas',
                     'Score de anomalías último mes',
                     'Número de anomalías por mes',
                     'Historial de mantenimiento preventivo'])
        if option_4 == 'Score de anomalía últimas 48 horas':
            start_date = get_datetime(4,6,2023)
            end_date = get_datetime(6,6,2023)
            plt.figure(facecolor='azure')
            ax = plt.axes()
            ax.set_facecolor("azure")
            plt.title('Score de Anomalía últimas 48 horas')
            hours = end_date - start_date
            hours = int(hours.total_seconds()//3600)
            y = np.random.random(hours)*0.4 - 0.2
            x = generate_range_hours(start_date, end_date)
            for j in range(len(x)):
                if x[j].date() in fechas_falla[option_3]:
                    y[j] = -0.5
            plt.title('Score de Anomalía últimas 48 horas')
            plt.plot(x,y,label = option_3, color='navy')
            
            list_of_ticks = [start_date,start_date+timedelta(hours=12),
                             start_date+timedelta(hours=24),start_date+timedelta(hours=36),
                             start_date+timedelta(hours=48)]
            list_of_str_ticks = [l.strftime("%m-%d-%H") for l in list_of_ticks]
            plt.xticks(list_of_ticks, list_of_str_ticks)
            plt.axhline(y=0.2,lw=0.8,color='k')
            plt.axhline(y=-0.2,lw=0.8,color='k')
            plt.legend()
            st.pyplot(plt.gcf())
        if option_4 == 'Score de anomalías último mes':
            plt.figure(facecolor='azure')
            ax = plt.axes()
            ax.set_facecolor("azure")
            start_date = get_datetime(5,5,2023)
            end_date = get_datetime(6,6,2023)
            days = end_date - start_date
            days = days.days
            y = np.random.random(days)*0.4 - 0.2
            x = generate_range(start_date, end_date)
            for j in range(len(x)):
                if x[j].date() in fechas_falla[option_3]:
                    y[j] = -0.5
            list_of_ticks = [start_date,start_date+timedelta(days=6),
                             start_date+timedelta(days=12),start_date+timedelta(days=18),
                             start_date+timedelta(days=24), end_date]
            list_of_str_ticks = [l.strftime("%m-%d") for l in list_of_ticks]
            plt.plot(x,y,label = option_3, color='navy')
            plt.xticks(list_of_ticks, list_of_str_ticks)
            plt.axhline(y=0.2,lw=0.8,color='k')
            plt.axhline(y=-0.2,lw=0.8,color='k')
            plt.legend()
            st.pyplot(plt.gcf())
        if option_4 == 'Número de anomalías por mes':
            plt.figure(facecolor='azure')
            ax = plt.axes()
            ax.set_facecolor("azure")
            anomalies_per_month = {'months':['Enero','Febrero','Marzo','Abril','Mayo','Junio'],
                                   'anomalies':[0,0,0,0,0,0]}
            for d in fechas_falla[option_3]:
                mts = list(anomalies_per_month['months'])
                anomalies_per_month['anomalies'][d.month-1] +=1
            
            anomalies_per_month = pd.DataFrame(anomalies_per_month)
            anomalies_per_month = anomalies_per_month.sort_values(by=['anomalies'],ascending=True)
            plt.title('Número de anomalías por mes')
            plt.barh(anomalies_per_month['months'],anomalies_per_month['anomalies'],color='navy')
            st.pyplot(plt.gcf())
        if option_4 == 'Historial de mantenimiento preventivo':
            plt.figure(facecolor='azure')
            ax = plt.axes()
            ax.set_facecolor("azure")
            anomalies_per_month = {'months':['Enero','Febrero','Marzo','Abril','Mayo','Junio'],
                                   'anomalies':[0,0,0,0,0,0]}
            for d in fechas_falla[option_3]:
                mts = list(anomalies_per_month['months'])
                anomalies_per_month['anomalies'][d.month-1] +=1
            anomalies_per_month = pd.DataFrame(anomalies_per_month)
            anomalies_per_month = anomalies_per_month.sort_values(by=['anomalies'],ascending=True)
            plt.title('Número de mantenimientos por mes')
            plt.barh(anomalies_per_month['months'],anomalies_per_month['anomalies'],color='navy')
            st.pyplot(plt.gcf())
            
            
            