import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np


# Load the data
dataDay_df = pd.read_csv('main_data.csv')

# Judul aplikasi Streamlit
st.title('Dashboard Penggunaan Sepeda')

# Sidebar untuk filter tahun (yr), musim (season), dan hari kerja (weekday)
st.sidebar.header("Filter Data")
unique_years = dataDay_df['yr'].unique()
unique_seasons = dataDay_df['season'].unique()
unique_weekdays = dataDay_df['weekday'].unique()

# Membuat filter tahun di sidebar dan filter multi-select untuk musim dan hari kerja
selected_year = st.sidebar.selectbox('Pilih Tahun:', unique_years)
selected_seasons = st.sidebar.multiselect('Pilih Musim:', unique_seasons, default=unique_seasons)
selected_weekdays = st.sidebar.multiselect('Pilih Hari Kerja:', unique_weekdays, default=unique_weekdays)

# Memfilter data berdasarkan input pengguna untuk tahun, musim, dan hari kerja
filtered_data = dataDay_df[
    (dataDay_df['yr'] == selected_year) & 
    (dataDay_df['season'].isin(selected_seasons)) &
    (dataDay_df['weekday'].isin(selected_weekdays))
]

# Menghitung total penggunaan sepeda untuk kategori casual dan registered pada data yang sudah difilter
total_casual = filtered_data['casual'].sum()
total_registered = filtered_data['registered'].sum()

# Menampilkan total pengguna dalam bentuk kotak di atas visualisasi
st.subheader('Total Penggunaan Sepeda Berdasarkan Filter yang Dipilih')
col1, col2 = st.columns(2)
col1.metric(label="Total Pengguna Casual", value=total_casual)
col2.metric(label="Total Pengguna Registered", value=total_registered)

# Membagi tampilan menjadi dua kolom untuk visualisasi grafis
col1, col2 = st.columns(2)

# Kolom 1: Visualisasi berdasarkan Musim dan Tahun
with col1:
    st.subheader('Musim dan Tahun')

    # Mengelompokkan data berdasarkan musim dan tahun pada data yang sudah difilter
    total_cnt_by_season_year = filtered_data.groupby(['yr', 'season'])[['casual', 'registered']].sum().reset_index()
    total_cnt_melted = total_cnt_by_season_year.melt(id_vars=['yr', 'season'], value_vars=['casual', 'registered'],
                                                     var_name='category', value_name='total')

    # Membuat plot untuk penggunaan sepeda berdasarkan musim dan tahun
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set(style="whitegrid")
    sns.barplot(data=total_cnt_melted, x='season', y='total', hue='category', ci=None, palette='Set2', ax=ax)
    ax.set_title(f'Total Penggunaan Sepeda pada Tahun {selected_year} untuk Musim yang Dipilih')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Penggunaan Sepeda')
    ax.legend(title='Kategori')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    st.pyplot(fig)

# Kolom 2: Visualisasi berdasarkan Hari Kerja
with col2:
    st.subheader('Hari Kerja')

    # Mengelompokkan data berdasarkan hari kerja pada data yang sudah difilter
    total_weekday_by_day = filtered_data.groupby(['weekday'])[['casual', 'registered']].sum().reset_index()

    # Membuat plot untuk penggunaan sepeda berdasarkan hari kerja
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=total_weekday_by_day, x='weekday', y='casual', marker='o', label='Casual', ax=ax)
    sns.lineplot(data=total_weekday_by_day, x='weekday', y='registered', marker='o', label='Registered', ax=ax)
    ax.set_title('Total Penggunaan Sepeda Casual dan Registered Berdasarkan Hari Kerja yang Dipilih')
    ax.set_xlabel('Hari Kerja')
    ax.set_ylabel('Total Penggunaan Sepeda')
    ax.legend(title='Kategori')
    st.pyplot(fig)