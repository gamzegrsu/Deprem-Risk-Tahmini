import streamlit as st
import pandas as pd
import math
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")
st.title("🌍 İstanbul Deprem Risk Analizi")
st.markdown("Geçmiş deprem verilerine göre İstanbul ilçelerinin göreli deprem risklerini hesaplayan ve haritada gösteren interaktif uygulama.")

uploaded_file = st.file_uploader("📁 Deprem kayıtlarını yükleyin (.csv)", type="csv")
if uploaded_file is not None:
    deprem_df = pd.read_csv(uploaded_file)
    st.success("Kendi veriniz yüklendi.")
else:
    deprem_df = pd.read_csv("data/deprem_kaydi.csv")
    st.info("Varsayılan veri kullanılıyor.")

    # 📥 Varsayılan CSV dosyasını indir
    with open("data/deprem_kaydi.csv", "rb") as f:
        st.download_button(
            label="📥 Varsayılan Veri Dosyasını İndir",
            data=f,
            file_name="deprem_kaydi.csv",
            mime="text/csv"
        )

deprem_df = deprem_df[deprem_df["ML"] != "-.-"]
deprem_df["ML"] = deprem_df["ML"].astype(float)

# İlçeler sözlüğü (kısaltılmış)
istanbul_ilceleri = {
    "Adalar": {"enlem": 40.8746, "boylam": 29.1228, "zemin_sinifi": "C", "zemin_carpani": 1.2},
    "Arnavutköy": {"enlem": 41.2018, "boylam": 28.7392, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Ataşehir": {"enlem": 40.9925, "boylam": 29.1244, "zemin_sinifi": "B", "zemin_carpani": 1.0},
    "Avcılar": {"enlem": 40.9797, "boylam": 28.7219, "zemin_sinifi": "C", "zemin_carpani": 1.2}
    # ... (devamı için tam listeyi ekleyin)
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
        popup=f"{ilce}\\nRisk Skoru: {risk:.2f}"
    ).add_to(m)

st.subheader("🗺️ Risk Haritası")
folium_static(m)

sorted_risk = sorted(ilce_riskleri.items(), key=lambda x: x[1], reverse=True)
st.subheader("📋 İlçe Bazlı Risk Sıralaması")
risk_df = pd.DataFrame(sorted_risk, columns=["İlçe", "Risk Skoru"])
st.dataframe(risk_df, use_container_width=True)
