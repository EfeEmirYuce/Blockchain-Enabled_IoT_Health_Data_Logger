import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import json
import os
import time
import bcrypt
from io import StringIO
from yaml.loader import SafeLoader

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="IoT Sensor Dashboard", page_icon="📊", layout="wide")

DATA_FILE = "data/sensor_logs.jsonl"

def load_data():
    if not os.path.exists(DATA_FILE): return pd.DataFrame()
    data = []
    with open(DATA_FILE, 'r') as f:
        for line in f:
            try: data.append(json.loads(line))
            except: continue
    if not data: return pd.DataFrame()
    
    # Pandas Warning Düzeltmesi
    json_buffer = StringIO(json.dumps(data))
    df = pd.read_json(json_buffer)
    
    if 'received_at' in df.columns: df['received_at'] = pd.to_datetime(df['received_at'])
    return df

# --- LOGIN SİSTEMİ ---
password_plain = '123'
hashed_password = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()
config = {'credentials': {'usernames': {'admin': {'name': 'Admin', 'password': hashed_password, 'email': 'admin@test.com'}}}, 'cookie': {'expiry_days': 1, 'key': 'secret_key', 'name': 'cookie_name'}, 'preauthorized': {'emails': []}}
authenticator = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'])
authenticator.login('main')

if st.session_state["authentication_status"]:
    with st.sidebar:
        authenticator.logout('Çıkış Yap', 'sidebar')
        st.success(f"Giriş: {st.session_state['name']}")
        st.markdown("---")
        st.caption("IoT Dashboard v3.0 (Lite)")
    
    st.title("📊 IoT Sensör İzleme Paneli")
    df = load_data()

    if df.empty:
        st.warning("Veri bekleniyor...")
    else:
        last_entry = df.iloc[-1]
        
        # --- 1. METRİKLER ---
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("🌡️ Sıcaklık", f"{last_entry.get('temp', 0)} °C")
        with col2: st.metric("💨 Basınç", f"{last_entry.get('pressure', 0)} Pa")
        with col3: st.metric("📦 Toplam Veri", len(df))
        with col4: st.metric("⏱️ Son Güncelleme", last_entry['received_at'].strftime('%H:%M:%S'))
            
        st.markdown("---")
        
        # --- 2. GRAFİKLER ---
        c1, c2 = st.columns(2)
        with c1: 
            st.subheader("📈 Sıcaklık Grafiği")
            st.line_chart(df.set_index('received_at')['temp'].tail(50), color="#FF4B4B")
        with c2: 
            st.subheader("📉 Basınç Grafiği")
            st.line_chart(df.set_index('received_at')['pressure'].tail(50), color="#0068C9")
            
        st.markdown("---")
        
        # --- 3. HAM VERİ TABLOSU (Sadece Veri) ---
        st.subheader("📋 Son Gelen Veriler")
        
        # Son 10 veriyi göster
        recent_df = df.sort_values(by='received_at', ascending=False).head(10)
        
        # Tarih formatını güzelleştir
        recent_df['received_at'] = recent_df['received_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Tabloyu basitçe çiz (Hash, Renk vs. yok)
        st.dataframe(
            recent_df[['received_at', 'temp', 'pressure']], 
            hide_index=True,
            use_container_width=True # En uyumlu parametre
        )

    time.sleep(5)
    st.rerun()

elif st.session_state["authentication_status"] is False: st.error('Hatalı giriş')
elif st.session_state["authentication_status"] is None: st.warning('Lütfen giriş yapınız')