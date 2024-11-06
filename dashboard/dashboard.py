import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np


# Membaca data dari file CSV
dataDay_df = pd.read_csv('main_data.csv')

# Mengonversi kolom 'dteday' menjadi tipe datetime
dataDay_df['dteday'] = pd.to_datetime(dataDay_df['dteday'])

# Mengonversi nilai tahun dan musim sesuai keinginan
dataDay_df['yr'] = dataDay_df['yr'].map({0: 2011, 1: 2012})
dataDay_df['season'] = dataDay_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Menambahkan kolom 'dteday' untuk filter berdasarkan tanggal setelah groupby
dataDay_df['dteday'] = pd.to_datetime(dataDay_df['dteday'])  # memastikan kolom dteday dalam format datetime

# Mengelompokkan data dan menghitung total penggunaan sepeda berdasarkan tahun, musim, kondisi cuaca, dan hari kerja
total_cnt_by_season = dataDay_df.groupby(['yr', 'season', 'weathersit', 'weekday', 'dteday'])[['casual', 'registered']].sum()
total_cnt_by_season['total'] = total_cnt_by_season['casual'] + total_cnt_by_season['registered']
total_cnt_by_season = total_cnt_by_season.reset_index()

# Sidebar untuk filter
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun:", sorted(total_cnt_by_season['yr'].unique()))
selected_season = st.sidebar.multiselect("Pilih Musim:", options=['Spring', 'Summer', 'Fall', 'Winter'], default=['Spring', 'Summer', 'Fall', 'Winter'])
selected_weekday = st.sidebar.multiselect("Pilih Hari dalam Minggu:", options=[0, 1, 2, 3, 4, 5, 6], default=[0, 1, 2, 3, 4, 5, 6])

# Filter berdasarkan rentang tanggal
min_date = total_cnt_by_season['dteday'].min()
max_date = total_cnt_by_season['dteday'].max()

# Menambahkan filter tanggal
selected_dates = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date])

# Filter data berdasarkan pilihan
filtered_data = total_cnt_by_season[
    (total_cnt_by_season['yr'] == selected_year) &
    (total_cnt_by_season['season'].isin(selected_season)) &
    (total_cnt_by_season['weekday'].isin(selected_weekday)) &
    (total_cnt_by_season['dteday'] >= pd.to_datetime(selected_dates[0])) &
    (total_cnt_by_season['dteday'] <= pd.to_datetime(selected_dates[1]))
]

# Memeriksa apakah data ada setelah difilter
if filtered_data.empty:
    st.write("Tidak ada data yang cocok dengan filter yang dipilih.")
else:
    # Mempersiapkan data untuk visualisasi
    total_cnt_melted = filtered_data.melt(id_vars=['season', 'weathersit', 'weekday','dteday'], 
                                          value_vars=['casual', 'registered', 'total'],
                                          var_name='category', value_name='count')

    # Plot Total Penggunaan Sepeda
    st.subheader("Total Penggunaan Sepeda Berdasarkan Musim, Hari, dan Kondisi Cuaca")
    g_total = sns.FacetGrid(total_cnt_melted[total_cnt_melted['category'] == 'total'], 
                            col='weathersit', height=4, aspect=1, legend_out=False)
    g_total.map_dataframe(sns.barplot, x='season', y='count', hue='weekday', ci=None, palette='viridis')
    g_total.set_axis_labels("Musim", "Total Penggunaan Sepeda")
    g_total.set_titles(col_template="Kondisi Cuaca {col_name}")
    g_total.add_legend(title='Hari dalam Minggu')
    st.pyplot(g_total)

    # Plot Penggunaan Sepeda untuk Kategori Casual dan Registered dengan Warna yang Lebih Kontras
    st.subheader("Penggunaan Sepeda untuk Kategori Casual dan Registered")
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid")
    g = sns.barplot(data=total_cnt_melted, x='season', y='count', hue='category', ci=None, palette='coolwarm')

    # Menambahkan label angka di atas setiap batang
    for container in g.containers:
        g.bar_label(container, fmt="%.0f", padding=3)
    
    # Menambahkan label dan judul
    plt.title('Penggunaan Sepeda Berdasarkan Musim untuk Kategori Casual dan Registered')
    plt.xlabel('Musim')
    plt.ylabel('Penggunaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(plt)