import streamlit as st
import pandas as pd
import os
import random
import urllib.parse
from datetime import datetime, date, time

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Dei Reali - Corporate ATS Full Suite",
    page_icon="👑",
    layout="wide"
)

# 2. CSS Custom Premium per l'interfaccia aziendale
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    .stButton>button {
        background-color: #EFF6FF !important; color: #1E3A8A !important;
        border: 1px solid #BFDBFE !important; border-radius: 12px !important;
        font-weight: bold !important; padding: 10px 14px !important;
        width: 100% !important; min-height: 50px !important; transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #DBEAFE !important; border-color: #2563EB !important; }
    .section-indicator {
        font-size: 16px; font-weight: 700; color: #1E3A8A; background-color: #FFFFFF;
        padding: 10px 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 20px;
    }
    .saas-box {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .login-container {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px;
        padding: 40px; max-width: 500px; margin: 60px auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    }
    .status-disponibile { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .status-occupato { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .whatsapp-btn {
        background-color: #25D366 !important; color: white !important; border: none !important;
        padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important;
        text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px;
    }
    .meet-btn {
        background-color: #1a73e8 !important; color: white !important; border: none !important;
        padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important;
        text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px;
    }
    .global-banner {
        background-color: #FFFBEB; border-left: 5px solid #F59E0B; padding: 15px; border-radius: 8px; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE UTENTI / OPERATORI ---
OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"

# Inizializzazione Database Annunci Condiviso (Per conservare i dati inseriti)
if 'annunci_db' not in st.session_state:
    st.session_state.annunci_db = [
        {"Posizione": "Senior Corporate Consultant", "Inquadramento": "RAL", "Importo": "45.000", "Sede": "Roma via Condotti"},
        {"Posizione": "OSS - Struttura anziani a carattere familiare", "Inquadramento": "RAL", "Importo": "1300", "Sede": "Palestrina"}
    ]

# Database Candidati Condiviso
if 'candidati_db' not in st.session_state:
    st.session_state.candidati_db = [
        {"id": 0, "Nome": "Alessandro Reali", "Email": "a.reali@gmail.com", "Telefono": "+393331234567", "Posizione": "Senior Corporate Consultant", "Idoneità": "94%", "Stelle": "⭐⭐⭐⭐⭐", "Orientamento": "Perfetto per il ruolo.", "Alternativo": "Nessuno", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None},
        {"id": 1, "Nome": "Beatrice Marchesi", "Email": "beatrice.m@outlook.it", "Telefono": "+393399876543", "Posizione": "Senior Corporate Consultant", "Idoneità": "65%", "Stelle": "⭐⭐⭐", "Orientamento": "Buone soft-skills.", "Alternativo": "💡 Consigliata come 'Junior Analyst'", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None}
    ]

# Database dell'Agenda Comune
if 'agenda_db' not in st.session_state:
    st.session_state.agenda_db = [
        {"Candidato": "Alessandro Reali", "Data": "2026-06-26", "Ora": "15:30", "Operatore": "Danilo", "Meet_Link": "https://meet.google.com/qww-rtyu-iop", "Telefono": "+393331234567"}
    ]

if 'clienti_db' not in st.session_state:
    st.session_state.clienti_db = [{"Azienda": "Dei Reali Consulting", "Settore": "Consulenza Aziendale"}]

# --- INTERFACCIA DI LOG-IN ---
if not st.session_state.autenticato:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path): st.image(logo_path, width=220)
    else: st.markdown("<h2 style='color:#1E3A8A; margin-top:0;'>👑 DEI REALI</h2>", unsafe_allow_html=True)
    st.markdown("### Accesso alla Suite Aziendale")
    login_mail = st.text_input("📧 E-mail Ufficiale", key="input_mail_login")
    login_pw = st.text_input("🔑 Password Assegnata", type="password", key="input_pw_login")
    if st.button("ACCEDI AL SISTEMA", use_container_width=True, key="btn_submit_login"):
        if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
            st.session_state.autenticato = True
            st.session_state.utente_connesso = OPERATORI[login_mail]
            st.rerun()
        else: st.error("Credenziali non corrette.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- AREA RISERVATA AZIENDALE ---
else:
    with st.sidebar:
        if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", use_container_width=True)
        st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:15px 0;'>", unsafe_allow_html=True)
        
        st.markdown("### 🖥️ Link Meet Attivi Ora")
        stanze_attive = [c for c in st.session_state.candidati_db if c.get("Impegnato", False)]
        if not stanze_attive:
            st.caption("Nessuna stanza Meet attiva al momento.")
        else:
            for s in stanze_attive:
                st.markdown(f"""
                <div style="background-color:#F0FDF4; border:1px solid #BBF7D0; padding:10px; border-radius:8px; margin-bottom:8px;">
                    <span style="font-size:12px; font-weight:bold; color:#166534;">📞 IN CORSO ({s['Operatore_Call']})</span><br>
                    <span style="font-size:13px; color:#0F172A;">Cand: {s['Nome']}</span><br>
                    <a href="{s['Meet_Link']}" target="_blank" style="font-size:12px; font-weight:bold; color:#1a73e8; text-decoration:none;">🔗 Entra</a>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.sidebar.button("🔒 Disconnetti", key="btn_logout"):
            st.session_state.autenticato = False; st.rerun()

    st.title("👑 Suite di Gestione Risorse Umane")
    st.markdown(f"##### Dei Reali Executive Selection &emsp;|&emsp; Operatore Attivo: *{st.session_state.utente_connesso['nome']}*")
    
    # Barra dei moduli (7 Pulsanti)
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    buttons_nav = [("📢\nAnnunci", "📢 Annunci"), ("📥\nScreening CV", "📥 Screening CV"), ("🤝\nColloqui AI", "🤝 Colloqui AI"),
                   ("🎉\nAssunzioni", "🎉 Assunzioni"), ("📊\nReport", "📊 Report"), ("🏢\nClienti", "🏢 Clienti"), ("👥\nCandidati", "👥 Candidati")]
    for i, (label, key) in enumerate(buttons_nav):
        with [c1, c2, c3, c4, c5, c6, c7][i]:
            if st.button(label, key=f"nav_{key}"): st.session_state.current_menu = key

    st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

    if stanze_attive:
        for s in stanze_attive:
            st.markdown(f"""
            <div class="global-banner">
                🚨 <b>COLLOQUIO IN CORSO SULLA SCHERMATA PRINCIPALE:</b> L'operatore <b>{s['Operatore_Call']}</b> è in linea con il candidato <b>{s['Nome']}</b>. 
                <a href="{s['Meet_Link']}" target="_blank" style="margin-left:15px; font-weight:bold; color:#1A73E8;">🖥️ CLICCA QUI PER UNIRTI</a>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # MODULO 1: 📢 GESTIONE E STORICO ANNUNCI (AGGIORNATO)
    # ==========================================
    if st.session_state.current_menu == "📢 Annunci":
        col_sx, col_dx = st.columns(2)
        with col_sx:
            st.markdown("### 📝 Pubblica un Nuovo Annuncio")
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            st.file_uploader("🖼️ Carica Copertina Annuncio", type=["png", "jpg", "jpeg"], key="uploader_annunci_img")
            titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. OSS - Struttura anziani", key="input_annuncio_titolo")
            tipo_importo = st.radio("Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True, key="radio_annuncio_tipo")
            valore_importo = st.text_input("Valore economico (€)", placeholder="es. 1300", key="input_annuncio_valore")
            indirizzo_job = st.text_input("🏢 Sede di lavoro", placeholder="es. Palestrina", key="input_annuncio_sede")
            
            if st.button("🚀 PUBBLICA NUOVO ANNUNCIO", use_container_width=True, key="btn_annuncio_pubblica"): 
                if titolo_job:
                    st.session_state.annunci_db.append({
                        "Posizione": titolo_job,
                        "Inquadramento": tipo_importo,
                        "Importo": valore_importo,
                        "Sede": indirizzo_job
                    })
                    st.success("🎉 Pubblicato online e salvato nello storico!")
                    st.rerun()
                else:
                    st.error("Inserisci il titolo della posizione!")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_dx:
            st.markdown("### 📋 Elenco Annunci Attivi Centralizzati")
            if not st.session_state.annunci_db:
                st.info("Nessun annuncio pubblicato finora.")
            else:
                for ann in st.session_state.annunci_db:
                    st.markdown(f"""
                    <div class="saas-box" style="border-left: 4px solid #1E3A8A;">
                        <h4 style="margin:0; color:#1E3A8A;">📢 {ann['Posizione']}</h4>
                        <p style="margin:5px 0; font-size:13px; color:#475569;">
                            🏢 Sede: <b>{ann['Sede']}</b> &nbsp;|&nbsp; 💸 Importo: <b>{ann['Importo']} €</b> ({ann['Inquadramento']})
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

    # ==========================================
    # MODULO 2: 📥 SCREENING CV & SELEZIONE LIVE
    # ==========================================
    elif st.session_state.current_menu in ["📥 Screening CV", "👥 Candidati"]:
        st.markdown("### 👥 Elenco Candidati e Monitor Chiamate Live")
        
        for index, cand in enumerate(st.session_state.candidati_db):
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            col_info, col_status = st.columns([2.3, 1.7])
            with col_info:
                st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px; color:#64748B;'>📱 {cand['Telefono']}</span>", unsafe_allow_html=True)
                st.markdown(f"🎯 *Posizione:* {cand['Posizione']} &emsp;|&emsp; *Voto IA:* {cand['Idoneità']} ({cand['Stelle']})")
            with col_status:
                if cand.get("Impegnato", False):
                    st.markdown(f'<div class="status-occupato">🔴 IN VIDEO CONFERENZA ({cand.get("Operatore_Call")})</div>', unsafe_allow_html=True)
                    st.markdown(f'<a href="{cand["Meet_Link"]}" target="_blank" class="meet-btn" style="width:100%;">🖥️/📳 Entra su Meet</a>', unsafe_allow_html=True)
                    if cand.get("Operatore_Call") == st.session_state.utente_connesso['nome']:
                        if st.button("📴 Chiudi Sessione", key=f"stop_btn_{index}"):
                            st.session_state.candidati_db[index]["Impegnato"] = False; st.rerun()
                else:
                    st.markdown('<div class="status-disponibile">🟢 PRONTO / Libero</div>', unsafe_allow_html=True)
                    if st.button("📞 Chiama Ora (Link Istantaneo)", key=f"start_btn_{index}"):
                        st.session_state.candidati_db[index]["Impegnato"] = True
                        st.session_state.candidati_db[index]["Operatore_Call"] = st.session_state.utente_connesso['nome']
                        meet_code = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"
                        st.session_state.candidati_db[index]["Meet_Link"] = f"https://meet.google.com/{meet_code}"
                        st.rerun()
                    if st.button("🗓️ Pianifica / Invia su Calendario", key=f"plan_fast_{index}"):
                        st.session_state.current_menu = "🤝 Colloqui AI"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # MODULO 3: 🤝 AGENDA CALENDARIO E STANZE AI
    # ==========================================
    elif st.session_state.current_menu == "🤝 Colloqui AI":
        st.markdown("### 🗓️ Calendario Globale Condiviso")
        if not st.session_state.agenda_db: st.info("Nessun colloquio in calendario.")
        else:
            df_agenda = pd.DataFrame(st.session_state.agenda_db)[["Data", "Ora", "Candidato", "Operatore", "Telefono", "Meet_Link"]]
            st.dataframe(df_agenda, use_container_width=True)

        st.markdown("<br><hr>", unsafe_allow_html=True)
        col_pianifica, col_lista_azioni = st.columns([1.2, 1.8])
        with col_pianifica:
            st.markdown("#### ✍️ Fissa una Nuova Data")
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            nomi_candidati = [c["Nome"] for c in st.session_state.candidati_db]
            cand_scelto = st.selectbox("Seleziona il Candidato", nomi_candidati, key="agenda_cand_select")
            data_scelta = st.date_input("Scegli il Giorno", min_value=date.today(), key="agenda_date_select")
            ora_scelta = st.time_input("Scegli l'Orario", value=time(10, 0), key="agenda_time_select")
            
            if st.button("💾 Inserisci nel Calendario Comune", use_container_width=True):
                c_info = next((c for c in st.session_state.candidati_db if c["Nome"] == cand_scelto), None)
                meet_code = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"
                st.session_state.agenda_db.append({
                    "Candidato": cand_scelto, "Data": str(data_scelta), "Ora": ora_scelta.strftime("%H:%M"),
                    "Operatore": st.session_state.utente_connesso['nome'], "Meet_Link": f"https://meet.google.com/{meet_code}", "Telefono": c_info["Telefono"] if c_info else "+393330000000"
                })
                st.success("🗓️ Slot inserito!"); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_lista_azioni:
            st.markdown("#### ⚡ Invio Notifiche")
            for idx, app in enumerate(st.session_state.agenda_db):
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                c_app1, c_app2 = st.columns([1.8, 1.2])
                with c_app1:
                    st.markdown(f"👤 <b>{app['Candidato']}</b> &emsp; 📱 {app['Telefono']}", unsafe_allow_html=True)
                    st.markdown(f"⏰ {app['Data']} ore {app['Ora']} | Recruiter: {app['Operatore']}")
                with c_app2:
                    st.markdown(f'<a href="{app["Meet_Link"]}" target="_blank" class="meet-btn" style="width:100%;">🖥️ Entra su Meet</a>', unsafe_allow_html=True)
                    messaggio_agenda = f"Gentile {app['Candidato']},\nLe confermiamo l'appuntamento Dei Reali con {app['Operatore']}.\n🗓️ Data: {app['Data']}\n⏰ Ora: {app['Ora']}\n🔗 Link Meet: {app['Meet_Link']}\n\nIl supporto IA dedicato prenderà parte alla sessione in modalità silente."
                    st.markdown(f'<a href="https://wa.me/{app["Telefono"].replace("+", "").replace(" ", "")}?text={urllib.parse.quote(messaggio_agenda)}" target="_blank" class="whatsapp-btn" style="width:100%;">💬 Notifica su WA</a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.current_menu == "🏢 Clienti":
        for cli in st.session_state.clienti_db: st.markdown(f'<div class="saas-box">🏢 <b>{cli["Azienda"]}</b></div>', unsafe_allow_html=True)
    else:
        st.info(f"Pannello {st.session_state.current_menu} attivo.")
