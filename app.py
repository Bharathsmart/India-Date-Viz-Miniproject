import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from altair import Latitude, Longitude
from streamlit import sidebar
import streamlit.components.v1 as components
import time

st.set_page_config(layout="wide")

df = pd.read_csv('final_india.csv')
list_of_sates = list(df['State'].unique())
list_of_sates.insert(0, 'Overall INDIA')


st.sidebar.title('INDIA Data Visualization')
selected_state = st.sidebar.selectbox('Select a State', list_of_sates )
primary = st.sidebar.selectbox('Select Primary Parameter', sorted(df.columns[5:]) )
secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(df.columns[5:]) )

plot = st.sidebar.button("Plot Data", use_container_width=True)


if plot:
    msg = st.sidebar.empty()  # create a placeholder in the sidebar
    msg.success("Plotting Data")  # show the success message
    time.sleep(1)  # wait for 3 seconds
    msg.empty()  # remove the message

    msg.markdown(
        """
        <div style='text-align: center; color: green; font-weight: bold;'>
            ✅ Data Plotted
        </div>
        """,
        unsafe_allow_html=True
    )

if plot:

    st.text("Size represents primary parameter")
    st.text("Color represents secondary parameter")

    if selected_state == 'Overall INDIA':
        #plot for india

        fig = px.scatter_mapbox(df, lat= 'Latitude', lon= 'Longitude',size = primary, color = secondary,
                                zoom = 4,size_max=35,  mapbox_style= "carto-positron", width=1200, height=800)
        st.plotly_chart(fig, use_container_width=True)
    else:
        #plot for state
        state_df = df[df['State'] == selected_state]

        fig = px.scatter_mapbox(state_df, lat='Latitude', lon='Longitude', size=primary, color=secondary,
                                zoom=4, size_max=35, mapbox_style="carto-positron", width=1200, height=800)
        fig.update_layout(uirevision='constant')

        st.plotly_chart(fig, use_container_width=True)

