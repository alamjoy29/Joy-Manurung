import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='whitegrid')
sns.set_theme(style='whitegrid')

# Dataframe yang berisi data penggunaan sepeda sewa
day_df = pd.read_csv("all_data.csv")  

# Membuat fungsi untuk menentukan kategori kecepatan angin
def wind_speed_category(speed):
    if speed <= 0.2:
        return 'Calm'
    elif speed <= 1.5:
        return 'Light air'
    elif speed <= 3.3:
        return 'Light breeze'
    elif speed <= 5.4:
        return 'Gentle breeze'
    elif speed <= 7.9:
        return 'Moderate breeze'
    elif speed <= 10.7:
        return 'Fresh breeze'
    elif speed <= 13.8:
        return 'Strong breeze'
    elif speed <= 17.1:
        return 'Moderate gale'
    elif speed <= 20.7:
        return 'Fresh gale'
    elif speed <= 24.4:
        return 'Strong gale'
    elif speed <= 28.4:
        return 'Whole gale'
    elif speed <= 32.6:
        return 'Storm'
    else:
        return 'Hurricane'

# Menambahkan kolom baru untuk kategori kecepatan angin
day_df['wind_speed_category'] = day_df['windspeed'].apply(wind_speed_category)

# Mengelompokkan data berdasarkan suhu, kelembaban, dan kategori kecepatan angin, 
# kemudian menghitung jumlah peminjaman sepeda untuk setiap kelompok
weather_effect = day_df.groupby(by=['temp', 'hum', 'wind_speed_category']).agg({
    'cnt': 'sum'
}).reset_index()

# Fungsi untuk menghitung total peminjaman sepeda per season
def calculate_season_rentals(df):
    total_rentals_season1 = df[df['season'] == 1]['cnt'].sum()
    total_rentals_season2 = df[df['season'] == 2]['cnt'].sum()
    total_rentals_season3 = df[df['season'] == 3]['cnt'].sum()
    total_rentals_season4 = df[df['season'] == 4]['cnt'].sum()

    return [total_rentals_season1, total_rentals_season2, total_rentals_season3, total_rentals_season4]

# Fungsi untuk menampilkan grafik total peminjaman sepeda per season
def show_season_rentals_chart(total_rentals_seasons):
    season_labels = ['season 1', 'season 2', 'season 3', 'season 4']
    fig, ax = plt.subplots(figsize=(10, 5))  # Membuat objek gambar dan sumbu
    ax.bar(season_labels, total_rentals_seasons, color='skyblue')
    ax.set_title('Total Peminjaman Sepeda per Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Peminjaman Sepeda')
    ax.grid(True)
    st.pyplot(fig)  # Memberikan objek gambar ke st.pyplot()

# Fungsi untuk menampilkan scatter plot suhu dan kelembaban
def show_temperature_humidity_scatter():
    fig, ax = plt.subplots(figsize=(10, 6))  # Membuat objek gambar dan sumbu
    ax.scatter(weather_effect['temp'], weather_effect['hum'], s=weather_effect['cnt']*0.01, alpha=0.5)
    ax.set_title('Pengaruh Suhu dan Kelembaban terhadap Penggunaan Sepeda')
    ax.set_xlabel('Suhu (Celsius)')
    ax.set_ylabel('Kelembaban')
    ax.grid(True)
    st.pyplot(fig)  # Memberikan objek gambar ke st.pyplot()

# Fungsi untuk menampilkan data peminjaman sepeda per season
def show_season_rentals_data():
    st.subheader('Data Peminjaman Sepeda per Season')
    season_rentals_df = day_df.groupby(by=['season']).agg({
        'casual': ['sum','mean'],
        'registered': ['sum','mean']
    })
    st.write(season_rentals_df)

# Fungsi untuk menampilkan data efek cuaca terhadap peminjaman sepeda
def show_weather_effect_data():
    st.subheader('Efek Cuaca terhadap Peminjaman Sepeda')
    st.write(weather_effect)

# Fungsi untuk menampilkan data dari DataFrame
def show_dataframe(df):
    st.subheader('Data')
    st.write(df)

# Menampilkan judul
st.title('Bike Sharing Dashboard')

# Menu navigasi
menu = st.sidebar.selectbox('Navigation', ['Total Peminjaman Sepeda per Season', 'Scatter Plot Suhu dan Kelembaban', 'Data Peminjaman Sepeda per Season', 'Efek Cuaca terhadap Peminjaman Sepeda', 'Dataframe'])

# Memproses pilihan menu
if menu == 'Total Peminjaman Sepeda per Season':
    st.subheader('Total Peminjaman Sepeda per Season')
    total_rentals_seasons = calculate_season_rentals(day_df)
    show_season_rentals_chart(total_rentals_seasons)

elif menu == 'Scatter Plot Suhu dan Kelembaban':
    st.subheader('Scatter Plot Suhu dan Kelembaban')
    show_temperature_humidity_scatter()

elif menu == 'Data Peminjaman Sepeda per Season':
    show_season_rentals_data()

elif menu == 'Efek Cuaca terhadap Peminjaman Sepeda':
    show_weather_effect_data()

elif menu == 'Dataframe':
    show_dataframe(day_df)

elif menu == 'Banyak Peminjam Sepeda Berdasarkan Suhu dan Kelembapan':
    st.subheader('Banyak Peminjam Sepeda Berdasarkan Suhu dan Kelembapan')
    
    # Tentukan rentang nilai untuk setiap kolom
    temp_bins = pd.cut(day_df['temp'], bins=5)  # Misalnya, kita bagi ke dalam 5 interval
    hum_bins = pd.cut(day_df['hum'], bins=5)

    # Gabungkan hasil binning ke dalam DataFrame
    day_df['temp_bins'] = temp_bins
    day_df['hum_bins'] = hum_bins

    # Lakukan groupby dan agg
    result = day_df.groupby(by=['temp_bins', 'hum_bins']).agg({
        'cnt': 'sum'
    }).reset_index()

    # Scatter plot untuk analisis pengaruh suhu dan kelembaban terhadap jumlah peminjaman sepeda
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='temp', y='hum', size='cnt', data=result, alpha=0.7)
    plt.title('Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman Sepeda')
    plt.xlabel('Suhu (Celsius)')
    plt.ylabel('Kelembaban')
    plt.grid(True)
    st.pyplot(plt)  # Memberikan objek gambar ke st.pyplot()