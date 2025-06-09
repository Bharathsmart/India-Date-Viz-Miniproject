import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ------------------------- Page Config -------------------------
st.set_page_config(page_title="Indian Census 2011", layout="wide")

# ---------------------- Welcome Section ------------------------
st.title("🇮🇳 Indian Census Data 2011 - Geospatial Visualization")
st.markdown("""
Welcome to the interactive visualization of the **Indian Census 2011** using geospatial indexing.  
This tool allows you to explore population and demographic metrics across Indian states and districts using:
- 📍 Geolocation-based map plots
- 📊 Comparative bar charts
- 🧭 Dynamic filters  
""")

st.markdown("---")

# ---------------------- Load Data ------------------------------
df = pd.read_csv('final_india.csv')

# Prepare sidebar lists
list_of_states = list(df['State'].unique())
list_of_states.insert(0, 'Overall INDIA')
metric_columns = sorted(df.columns[5:])

# ---------------------- Sidebar UI -----------------------------
st.sidebar.title('🔍 Data Controls')
selected_state = st.sidebar.selectbox('Select a State', list_of_states)
primary = st.sidebar.selectbox('Primary Parameter (Size)', metric_columns)
secondary = st.sidebar.selectbox('Secondary Parameter (Color)', metric_columns)
plot = st.sidebar.button("Plot Data", use_container_width=True)

# ---------------------- Plot Logic -----------------------------
if plot:
    # Temporary sidebar message
    msg = st.sidebar.empty()
    msg.success("Plotting Data...")
    time.sleep(1)
    msg.empty()
    msg.markdown(
        """
        <div style='text-align: center; color: green; font-weight: bold;'>
            ✅ Data Plotted
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"### 📍 Geospatial Plot for: **{selected_state}**")
    st.caption(f"Size: {primary} | Color: {secondary}")

    if selected_state == 'Overall INDIA':
        fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', size=primary, color=secondary,
                                zoom=4, size_max=35, mapbox_style="carto-positron", width=1200, height=800)
        st.plotly_chart(fig, use_container_width=True)

        # ---------------- Histogram ----------------
        st.markdown("### 📈 Histogram of Primary Parameter")
        hist_fig = px.histogram(df, x=primary, nbins=30, title=f'Distribution of {primary}')
        st.plotly_chart(hist_fig, use_container_width=True)

        # ---------------- Scatter Plot ----------------
        st.markdown("### 🔬 Scatter Plot: Primary vs Secondary")
        scatter_fig = px.scatter(df, x=primary, y=secondary, color='District',
                                 title=f'{primary} vs {secondary} in {selected_state}',
                                 size=primary, hover_name='District')
        st.plotly_chart(scatter_fig, use_container_width=True)

        # ---------------- Boxplot ----------------
        st.markdown("### 📦 Boxplot of Primary Parameter by District")
        box_fig = px.box(df, x='District', y=primary, title=f'Boxplot of {primary} across Districts')
        st.plotly_chart(box_fig, use_container_width=True)

        # ---------------- Heatmap (Correlation Matrix) ----------------
        st.markdown("### 🔥 Correlation Heatmap")
        corr_df = df.select_dtypes(include=['float64', 'int64']).corr()
        heatmap_fig = px.imshow(corr_df, text_auto=True, aspect="auto", title='Correlation of Census Metrics')
        st.plotly_chart(heatmap_fig, use_container_width=True)

        # ---------------- Optional Line Chart ----------------
        # Uncomment and adapt if time-series or yearly data is present
        # st.markdown("### 📅 Line Chart of Primary Parameter Over Time")
        # line_fig = px.line(state_df.sort_values('Year'), x='Year', y=primary, color='District')
        # st.plotly_chart(line_fig, use_container_width=True)


    else:
        state_df = df[df['State'] == selected_state]
        fig = px.scatter_mapbox(state_df, lat='Latitude', lon='Longitude', size=primary, color=secondary,
                                zoom=5, size_max=35, mapbox_style="carto-positron", width=1200, height=800)
        st.plotly_chart(fig, use_container_width=True)

        # ---------------- Additional Charts ----------------
        st.markdown("### 📊 State-wise Bar Chart")
        bar_fig = px.bar(state_df.sort_values(primary, ascending=False),
                         x='District', y=primary, color=primary,
                         title=f'{primary} Across Districts in {selected_state}')
        st.plotly_chart(bar_fig, use_container_width=True)

        st.markdown("### 🥧 Top 10 Districts Pie Chart")
        top_districts = state_df.sort_values(primary, ascending=False).head(10)
        pie_fig = px.pie(top_districts, names='District', values=primary,
                         title=f'Top 10 Districts in {selected_state} by {primary}')
        st.plotly_chart(pie_fig, use_container_width=True)

        # ---------------- Histogram ----------------
        st.markdown("### 📈 Histogram of Primary Parameter")
        hist_fig = px.histogram(state_df, x=primary, nbins=30, title=f'Distribution of {primary}')
        st.plotly_chart(hist_fig, use_container_width=True)

        # ---------------- Scatter Plot ----------------
        st.markdown("### 🔬 Scatter Plot: Primary vs Secondary")
        scatter_fig = px.scatter(state_df, x=primary, y=secondary, color='District',
                                 title=f'{primary} vs {secondary} in {selected_state}',
                                 size=primary, hover_name='District')
        st.plotly_chart(scatter_fig, use_container_width=True)

        # ---------------- Boxplot ----------------
        st.markdown("### 📦 Boxplot of Primary Parameter by District")
        box_fig = px.box(state_df, x='District', y=primary, title=f'Boxplot of {primary} across Districts')
        st.plotly_chart(box_fig, use_container_width=True)

        # ---------------- Heatmap (Correlation Matrix) ----------------
        st.markdown("### 🔥 Correlation Heatmap")
        corr_df = state_df.select_dtypes(include=['float64', 'int64']).corr()
        heatmap_fig = px.imshow(corr_df, text_auto=True, aspect="auto", title='Correlation of Census Metrics')
        st.plotly_chart(heatmap_fig, use_container_width=True)

        # ---------------- Optional Line Chart ----------------
        # Uncomment and adapt if time-series or yearly data is present
        # st.markdown("### 📅 Line Chart of Primary Parameter Over Time")
        # line_fig = px.line(state_df.sort_values('Year'), x='Year', y=primary, color='District')
        # st.plotly_chart(line_fig, use_container_width=True)


# Optional Footer
st.markdown("---")
st.caption("Developed for educational purposes using Census 2011 data and Plotly.")
