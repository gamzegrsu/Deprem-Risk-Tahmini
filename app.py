
import streamlit as st
import pandas as pd
import math
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")
st.title("🌍 İstanbul Deprem Risk Tahmini")
st.markdown("Bu uygulama, geçmiş deprem verilerine göre İstanbul ilçelerinin deprem riskini analiz eder ve harita üzerinde görselleştirir.")

uploaded_file = st.file_uploader("📁 Deprem kayıtlarını yükleyin (.csv)", type="csv")
if uploaded_file is not None:
    deprem_df = pd.read_csv(uploaded_file)
    st.success("Kendi veriniz yüklendi.")
else:
    deprem_df = pd.read_csv("data/deprem_kaydi.csv")
    st.info("Varsayılan veri kullanılıyor.")

deprem_df = deprem_df[deprem_df["ML"] != "-.-"]
deprem_df["ML"] = deprem_df["ML"].astype(float)

# Tüm İstanbul ilçeleri ve zemin çarpanları
istanbul_ilceleri = {
    "Adalar": {"enlem": 40.8746, "boylam": 29.1228, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Arnavutköy": {"enlem": 41.2018, "boylam": 28.7392, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Ataşehir": {"enlem": 40.9925, "boylam": 29.1244, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Avcılar": {"enlem": 40.9797, "boylam": 28.7219, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Bağcılar": {"enlem": 41.0390, "boylam": 28.8567, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Bahçelievler": {"enlem": 41.0027, "boylam": 28.8598, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Bakırköy": {"enlem": 40.9760, "boylam": 28.8570, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Başakşehir": {"enlem": 41.0932, "boylam": 28.8028, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Bayrampaşa": {"enlem": 41.0493, "boylam": 28.9126, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Beşiktaş": {"enlem": 41.0438, "boylam": 29.0090, "zemin_sinifi": "A", "zemin_carpani": 0.8},
    "Beykoz": {"enlem": 41.1256, "boylam": 29.1044, "zemin_sinifi": "A", "zemin_carpani": 0.8},
    "Beylikdüzü": {"enlem": 41.0010, "boylam": 28.6416, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Beyoğlu": {"enlem": 41.0383, "boylam": 28.9703, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Büyükçekmece": {"enlem": 41.0200, "boylam": 28.5800, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Çatalca": {"enlem": 41.1450, "boylam": 28.4600, "zemin_sinifi": "A", "zemin_carpani": 0.8},
    "Çekmeköy": {"enlem": 41.0167, "boylam": 29.1333, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Esenler": {"enlem": 41.0430, "boylam": 28.8820, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Esenyurt": {"enlem": 41.0343, "boylam": 28.6801, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Eyüpsultan": {"enlem": 41.0789, "boylam": 28.9336, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Fatih": {"enlem": 41.0166, "boylam": 28.9497, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Gaziosmanpaşa": {"enlem": 41.0750, "boylam": 28.9120, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Güngören": {"enlem": 41.0220, "boylam": 28.8690, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Kadıköy": {"enlem": 40.9917, "boylam": 29.0300, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Kağıthane": {"enlem": 41.0645, "boylam": 28.9648, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Kartal": {"enlem": 40.8990, "boylam": 29.1830, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Küçükçekmece": {"enlem": 40.9950, "boylam": 28.7890, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Maltepe": {"enlem": 40.9350, "boylam": 29.1600, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Pendik": {"enlem": 40.8798, "boylam": 29.2576, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Sancaktepe": {"enlem": 40.9870, "boylam": 29.2310, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Sarıyer": {"enlem": 41.1700, "boylam": 29.0500, "zemin_sinifi": "A", "zemin_carpani": 0.8},
    "Şile": {"enlem": 41.1750, "boylam": 29.6130, "zemin_sinifi": "A", "zemin_carpani": 0.8},
    "Silivri": {"enlem": 41.0730, "boylam": 28.2460, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Sultanbeyli": {"enlem": 40.9600, "boylam": 29.2700, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Sultangazi": {"enlem": 41.0930, "boylam": 28.9020, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Şişli": {"enlem": 41.0600, "boylam": 28.9870, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Tuzla": {"enlem": 40.8167, "boylam": 29.3000, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Ümraniye": {"enlem": 41.0330, "boylam": 29.1000, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Üsküdar": {"enlem": 41.0329, "boylam": 29.0327, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Zeytinburnu": {"enlem": 40.9930, "boylam": 28.9000, "zemin_sinifi": "B", "zemin_carpani": 1.0}
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

ilce_riskleri = {ilce: 0 for ilce in istanbul_ilceleri}

for _, deprem in deprem_df.iterrows():
    deprem_lat = deprem["Enlem"]
    deprem_lon = deprem["Boylam"]
    deprem_ml = deprem["ML"]
    for ilce, info in istanbul_ilceleri.items():
        mesafe = haversine(deprem_lat, deprem_lon, info["enlem"], info["boylam"])
        if mesafe < 100:
            risk = (deprem_ml / mesafe) * info["zemin_carpani"]
            ilce_riskleri[ilce] += risk

maks_risk = max(ilce_riskleri.values())
m = folium.Map(location=[41.0082, 28.9784], zoom_start=10)

for ilce, risk in ilce_riskleri.items():
    lat = istanbul_ilceleri[ilce]["enlem"]
    lon = istanbul_ilceleri[ilce]["boylam"]
    renk = "green"
    if risk > maks_risk * 0.66:
        renk = "red"
    elif risk > maks_risk * 0.33:
        renk = "orange"
    folium.CircleMarker(
        location=(lat, lon),
        radius=10,
        color=renk,
        fill=True,
        fill_opacity=0.7,
        popup=f"{ilce}\nRisk Skoru: {risk:.2f}"
    ).add_to(m)

st.subheader("🗺️ Risk Haritası")
folium_static(m)

sorted_risk = sorted(ilce_riskleri.items(), key=lambda x: x[1], reverse=True)
st.subheader("📋 İlçe Bazlı Risk Sıralaması")
risk_df = pd.DataFrame(sorted_risk, columns=["İlçe", "Risk Skoru"])
st.dataframe(risk_df, use_container_width=True)
