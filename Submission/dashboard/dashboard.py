import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")

# Load data
df = pd.read_csv("main_data.csv")

# Convert datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("Filter Data")

season = st.sidebar.multiselect(
    "Pilih Musim",
    options=sorted(df['season'].unique()),
    default=sorted(df['season'].unique())
)

df_filtered = df[df['season'].isin(season)]

# ======================
# METRIC
# ======================
col1, col2 = st.columns(2)

col1.metric("Total Rental", int(df_filtered['cnt'].sum()))
col2.metric("Rata-rata Rental", int(df_filtered['cnt'].mean()))

# ======================
# TIME SERIES
# ======================
st.subheader(" Tren Penyewaan Sepeda")

st.line_chart(df_filtered.set_index('dteday')['cnt'])

# ======================
# SEASON ANALYSIS
# ======================
st.subheader(" Penyewaan Berdasarkan Musim")

fig, ax = plt.subplots()
sns.barplot(x='season', y='cnt', data=df_filtered, ax=ax)
ax.set_title("Rata-rata Penyewaan per Musim")
st.pyplot(fig)

# ======================
# WEATHER ANALYSIS
# ======================
st.subheader(" Pengaruh Cuaca")

weather = df_filtered.groupby('weathersit')['cnt'].mean()

fig2, ax2 = plt.subplots()
weather.plot(kind='bar', ax=ax2)
ax2.set_title("Rata-rata Penyewaan berdasarkan Cuaca")
st.pyplot(fig2)