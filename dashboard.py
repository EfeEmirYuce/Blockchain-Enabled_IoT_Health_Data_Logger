import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import json
import os
import time
import bcrypt
from io import StringIO
from yaml.loader import SafeLoader
# --- YENİ KÜTÜPHANE ---
from streamlit_js_eval import streamlit_js_eval

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
        st.header("🦊 Web3 Cüzdan")
        
        # --- YÖNTEM 1: OTOMATİK BAĞLANTI ---
        # Bu buton tarayıcıdaki MetaMask'ı tetikler
        if st.button("Cüzdanı Bağla (Otomatik)"):
            streamlit_js_eval(
                js_expressions='window.ethereum.request({method: "eth_requestAccounts"}).then((accounts) => {return accounts[0]})',
                key = 'wallet_auto',
                want_output = True
            )

        # Otomatik bağlantıdan gelen veriyi kontrol et
        # streamlit_js_eval sonucu bazen session_state içinde tutar
        
        # --- YÖNTEM 2: MANUEL GİRİŞ (YEDEK PLAN) ---
        # Eğer otomatik bağlantı güvenlik duvarına takılırsa bu kutu hayat kurtarır.
        manual_wallet = st.text_input("Veya Adresi Elle Yapıştır:", placeholder="0x...")

        # Hangi adresi kullanacağımıza karar verelim
        final_wallet = None
        
        # 1. Otomatik gelen var mı? (Session state kontrolü)
        if 'wallet_auto' in st.session_state and st.session_state['wallet_auto']:
            final_wallet = st.session_state['wallet_auto']
        
        # 2. Manuel girilen var mı?
        elif manual_wallet and manual_wallet.startswith("0x"):
            final_wallet = manual_wallet

        # Sonuç Gösterimi
        if final_wallet:
            st.success("✅ Bağlandı!")
            st.code(final_wallet, language="text")
            st.session_state['active_wallet'] = final_wallet
        else:
            st.info("Bağlantı bekleniyor...")
            
        st.markdown("---")
        
        authenticator.logout('Çıkış Yap', 'sidebar')
        st.caption("IoT Dashboard v3.4 (Stable)")
    
    # --- ANA EKRAN ---
    st.title("📊 IoT Sensör İzleme Paneli")
    df = load_data()

    if df.empty:
        st.warning("Veri bekleniyor...")
    else:
        last_entry = df.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("🌡️ Sıcaklık", f"{last_entry.get('temp', 0)} °C")
        with col2: st.metric("💨 Basınç", f"{last_entry.get('pressure', 0)} Pa")
        with col3: st.metric("📦 Veri Adedi", len(df))
        
        with col4: 
            if 'active_wallet' in st.session_state:
                st.metric("🔗 Cüzdan", "Bağlandı")
                st.caption(f"{st.session_state['active_wallet'][:6]}...")
            else:
                st.metric("⏱️ Son Kayıt", last_entry['received_at'].strftime('%H:%M:%S'))
            
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1: 
            st.subheader("📈 Sıcaklık")
            st.line_chart(df.set_index('received_at')['temp'].tail(50), color="#FF4B4B")
        with c2: 
            st.subheader("📉 Basınç")
            st.line_chart(df.set_index('received_at')['pressure'].tail(50), color="#0068C9")
            
        st.subheader("📋 Son Gelen Veriler")
        recent_df = df.sort_values(by='received_at', ascending=False).head(10)
        recent_df['received_at'] = recent_df['received_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        st.dataframe(
            recent_df[['received_at', 'temp', 'pressure']], 
            hide_index=True,
            width="stretch"
        )

    # st_js_eval kullanırken st.rerun() döngüsüne dikkat etmek gerekir.
    # Manuel refresh butonu eklemek daha sağlıklı olabilir.
    if st.button("Verileri Yenile"):
        st.rerun()

elif st.session_state["authentication_status"] is False: st.error('Hatalı giriş')
elif st.session_state["authentication_status"] is None: st.warning('Lütfen giriş yapınız')