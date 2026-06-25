import streamlit as st
import pandas as pd
import os
import random
import urllib.parse
from datetime import datetime, date, time

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Dei Reali - Corporate ATS & Agenda",
    page_icon="👑",
    layout="wide"
)

# 2. CSS Custom per l'interfaccia Premium
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    .stButton>button {
        background-color: #EFF6FF !important; color: #1E3A8A !important;
        border: 1px solid #BFDBFE !important; border-radius: 12px !important;
        font-weight: bold !important; padding: 10px 14px !important;
        width: 100% !important; min-height: 55px !important; transition: all 0.2s ease;
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
    .status-disponibile { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; }
    .status-occupato { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; }
    .whatsapp-btn {
        background-color: #25D366 !important; color: white !important; border: none !important;
        padding: 10px 18px !important; border-radius: 10px !important; font-weight: bold !important;
        text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 13px;
    }
    .meet-btn {
        background-color: #1a73e8 !important; color: white !important; border: none !important;
        padding: 10px 18px !important; border-radius: 10px !important; font-weight: bold !important;
        text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE OPERATORI ---
OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"

# Database Candidati
if 'candidati_db' not in st.session_state:
    st.session_state.candidati_db = [
        {"id": 0, "Nome": "Alessandro Reali", "Email": "a.reali@gmail.com", "Telefono": "+393331234567", "Posizione": "Senior Corporate Consultant", "Idoneità": "94%", "Stelle": "⭐⭐⭐⭐⭐", "Orientamento": "Perfetto per il ruolo.", "Alternativo": "Nessuno", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None},
        {"id": 1, "Nome": "Beatrice Marchesi", "Email": "beatrice.m@outlook.it", "Telefono": "+393399876543", "Posizione": "Senior Corporate Consultant", "Idoneità": "65%", "Stelle": "⭐⭐⭐", "Orientamento": "Buone soft-skills.", "Alternativo": "💡 Consigliata come 'Junior Financial Analyst'", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None}
    ]

# Inizializzazione Database Appuntamenti Calendario
if 'agenda_db' not in st.session_state:
    st.session_state.agenda_db = [
        {
            "Candidato": "Alessandro Reali",
            "Data": "2026-06-26",
            "Ora": "15:30",
            "Operatore": "Daniele",
            "Meet_Link": "https://meet.google.com/abc-defg-hij"
        }
    ]

if 'clienti_db' not in st.session_state:
    st.session_state.clienti_db = [{"Azienda": "Dei Reali Consulting", "Settore": "Consulenza Aziendale", "Referente": "Direzione HR", "Email": "info@deireali.com", "Posizioni_Aperte": 2}]

# --- SCHERMATA LOGIN ---
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

# --- APP INTERNA ---
else:
    with st.sidebar:
        if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", use_container_width=True)
        st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
        if st.sidebar.button("🔒 Disconnetti", key="btn_logout"):
            st.session_state.autenticato = False; st.rerun()

    st.title("💼 Sistema di Gestione & Selezione Personale")
    st.markdown(f"##### Suite Multi-Operatore • Dei Reali &emsp;|&emsp; Operatore: *{st.session_state.utente_connesso['nome']}*")
    
    # Navigazione Orizzontale
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    buttons_nav = [("📢\nAnnunci", "📢 Annunci"), ("📥\nScreening CV", "📥 Screening CV"), ("🤝\nColloqui AI", "🤝 Colloqui AI"),
                   ("🎉\nAssunzioni", "🎉 Assunzioni"), ("📊\nReport", "📊 Report"), ("🏢\nClienti", "🏢 Clienti"), ("👥\nCandidati", "👥 Candidati")]
    for i, (label, key) in enumerate(buttons_nav):
        with [c1, c2, c3, c4, c5, c6, c7][i]:
            if st.button(label, key=f"nav_{key}"): st.session_state.current_menu = key

    st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

    # --- MODULO COLLOQUI AI & AGENDA APPUNTAMENTI ---
    if st.session_state.current_menu == "🤝 Colloqui AI":
        st.markdown("### 🤝 Agenda Appuntamenti & Gestione Stanze Digitali")
        st.markdown("Pianifica i colloqui futuri, genera gli inviti automatici per i candidati e monitora le sessioni live assistite dal Copilota IA.")
        
        col_pianifica, col_lista = st.columns([1.2, 1.8])
        
        # SOTTO-MODULO 1: FORM DI PIANIFICAZIONE CALENDARIO (SINISTRA)
        with col_pianifica:
            st.markdown("#### 🗓️ Pianifica Nuovo Colloquio")
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            
            nomi_candidati = [c["Nome"] for c in st.session_state.candidati_db]
            cand_scelto = st.selectbox("Seleziona il Candidato", nomi_candidati)
            
            data_scelta = st.date_input("Scegli la Data", min_value=date.today())
            ora_scelta = st.time_input("Scegli l'Orario", value=time(10, 0))
            
            if st.button("💾 Consegna ad Agenda & Genera Invito", use_container_width=True):
                meet_code = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"
                nuovo_meet = f"https://meet.google.com/{meet_code}"
                
                st.session_state.agenda_db.append({
                    "Candidato": cand_scelto,
                    "Data": str(data_scelta),
                    "Ora": ora_scelta.strftime("%H:%M"),
                    "Operatore": st.session_state.utente_connesso['nome'],
                    "Meet_Link": nuovo_meet
                })
                st.success(f"🗓️ Colloquio con {cand_scelto} registrato correttamente!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # SOTTO-MODULO 2: LISTA CRONOLOGICA DEGLI APPUNTAMENTI (DESTRA)
        with col_lista:
            st.markdown("#### 📋 Elenco Appuntamenti e Dispacciamento WhatsApp")
            
            if not st.session_state.agenda_db:
                st.info("Nessun colloquio programmato in agenda.")
            else:
                for idx, app in enumerate(st.session_state.agenda_db):
                    # Trova i dati del candidato per recuperare il telefono
                    c_info = next((c for c in st.session_state.candidati_db if c["Nome"] == app["Candidato"]), None)
                    tel_cand = c_info["Telefono"] if c_info else "+393330000000"
                    
                    st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                    c_app1, c_app2 = st.columns([2, 1])
                    
                    with c_app1:
                        st.markdown(f"👤 *Candidato:* <span style='color:#1E3A8A; font-weight:bold;'>{app['Candidato']}</span>", unsafe_allow_html=True)
                        st.markdown(f"📅 *Data:* {app['Data']} &emsp;|&emsp; ⏰ *Ora:* {app['Ora']}")
                        st.markdown(f"💼 *Selezionatore Assegnato:* {app['Operatore']}")
                        
                    with c_app2:
                        # Bottone per entrare su Google Meet
                        st.markdown(f'<a href="{app["Meet_Link"]}" target="_blank" class="meet-btn" style="width:100%; text-align:center;">🖥️ Entra su Meet</a>', unsafe_allow_html=True)
                        
                        # Costruzione testo WhatsApp per appuntamento futuro
                        messaggio_agenda = (
                            f"Gentile {app['Candidato']},\n\n"
                            f"Ti confermiamo il colloquio ufficiale di selezione con l'agenzia Dei Reali.\n"
                            f"Il colloquio sarà tenuto dal selezionatore {app['Operatore']}.\n\n"
                            f"🗓️ Data: {app['Data']}\n"
                            f"⏰ Ora: {app['Ora']}\n"
                            f"🔗 Link Google Meet a cui connettersi: {app['Meet_Link']}\n\n"
                            f"Nota: Alla sessione prenderà parte in modalità silente il nostro supporto IA dedicato per la strutturazione automatica dello skill score finali."
                        )
                        msg_enc = urllib.parse.quote(messaggio_agenda)
                        wa_url = f"https://wa.me/{tel_cand.replace('+', '')}?text={msg_enc}"
                        st.markdown(f'<a href="{wa_url}" target="_blank" class="whatsapp-btn" style="width:100%; text-align:center;">💬 Notifica su WA</a>', unsafe_allow_html=True)
                        
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- MODULO SCREENING CV ---
    elif st.session_state.current_menu in ["📥 Screening CV", "👥 Candidati"]:
        st.markdown("### 👥 Elenco Anagrafica Candidati")
        for cand in st.session_state.candidati_db:
            st.markdown(f'<div class="saas-box">👤 <b>{cand["Nome"]}</b> ({cand["Email"]})<br>🎯 Ruolo: {cand["Posizione"]} | Esito IA: {cand["Idoneità"]}</div>', unsafe_allow_html=True)

    # --- RESTANTI MODULI ---
    elif st.session_state.current_menu == "📢 Annunci":
        st.info("Sezione Annunci attiva.")
    elif st.session_state.current_menu == "🏢 Clienti":
        for cli in st.session_state.clienti_db: st.markdown(f'<div class="saas-box">🏢 <b>{cli["Azienda"]}</b></div>', unsafe_allow_html=True)
    else:
        st.info(f"Pannello {st.session_state.current_menu} attivo.")
