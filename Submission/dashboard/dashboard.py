import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

sns.set_style("whitegrid")

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("dashboard/main_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# ======================
# TITLE
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penggunaan sepeda berdasarkan waktu, musim, dan kondisi cuaca.")

# ======================
# SIDEBAR
# ======================
st.sidebar.header("🔎 Filter Data")

season = st.sidebar.multiselect(
    "Pilih Musim",
    options=sorted(df['season'].unique()),
    default=sorted(df['season'].unique())
)

df_filtered = df[df['season'].isin(season)]

# ======================
# METRICS
# ======================
st.subheader("📊 Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
col2.metric("Rata-rata Rental", f"{df_filtered['cnt'].mean():.0f}")
col3.metric("Max Rental", f"{df_filtered['cnt'].max():,}")

# ======================
# TIME SERIES
# ======================
st.subheader("📈 Tren Penyewaan Sepeda")

st.line_chart(df_filtered.set_index('dteday')['cnt'])

st.caption("📌 Terlihat pola peningkatan pada waktu tertentu yang menunjukkan aktivitas harian pengguna.")

# ======================
# SEASON ANALYSIS
# ======================
st.subheader("🌤️ Penyewaan Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x='season', y='cnt', data=df_filtered, palette="Blues", ax=ax)

ax.set_title("Rata-rata Penyewaan per Musim", fontsize=12)
ax.set_xlabel("Season (1=Spring, 2=Summer, 3=Fall, 4=Winter)")
ax.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig)

st.caption("📌 Musim dingin memiliki jumlah penyewaan paling rendah dibanding musim lainnya.")

# ======================
# WEATHER ANALYSIS
# ======================
st.subheader("🌦️ Pengaruh Cuaca")

weather = df_filtered.groupby('weathersit')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(8,5))
sns.barplot(x='weathersit', y='cnt', data=weather, palette="Reds", ax=ax2)

ax2.set_title("Rata-rata Penyewaan Berdasarkan Cuaca", fontsize=12)
ax2.set_xlabel("Weather Situation")
ax2.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig2)

st.caption("📌 Kondisi cuaca buruk secara signifikan menurunkan jumlah penyewaan.")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("📊 Dibuat untuk submission analisis data - Bike Sharing Dataset")
