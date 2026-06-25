import streamlit as st
import pandas as pd
import os
import random

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Dei Reali - Corporate ATS & Call Monitor",
    page_icon="👑",
    layout="wide"
)

# 2. CSS Custom per l'interfaccia Premium, Login e Badge di Stato
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    .stButton>button {
        background-color: #EFF6FF !important;
        color: #1E3A8A !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 10px 14px !important;
        width: 100% !important;
        min-height: 55px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #DBEAFE !important;
        border-color: #2563EB !important;
    }
    .section-indicator {
        font-size: 16px;
        font-weight: 700;
        color: #1E3A8A;
        background-color: #FFFFFF;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .saas-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .login-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 40px;
        max-width: 500px;
        margin: 60px auto;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    }
    .status-disponibile {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        display: inline-block;
    }
    .status-occupato {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE OPERATORI ---
OPERATORI = {
    "d.algozzino@deireali.com": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

# Inizializzazione degli stati della sessione
if 'autenticato' not in st.session_state:
    st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state:
    st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "📢 Annunci"

# Inizializzazione Database Candidati
if 'candidati_db' not in st.session_state:
    st.session_state.candidati_db = [
        {
            "id": 0,
            "Nome": "Alessandro Reali", 
            "Email": "a.reali@gmail.com", 
            "Posizione": "Senior Corporate Consultant", 
            "Idoneità": "94%", 
            "Stelle": "⭐⭐⭐⭐⭐", 
            "Orientamento": "Perfetto per il ruolo strategico.", 
            "Alternativo": "Nessuno",
            "Impegnato": True,
            "Operatore_Call": "Julian"
        },
        {
            "id": 1,
            "Nome": "Beatrice Marchesi", 
            "Email": "beatrice.m@outlook.it", 
            "Posizione": "Senior Corporate Consultant", 
            "Idoneità": "65%", 
            "Stelle": "⭐⭐⭐", 
            "Orientamento": "Buona dialettica, lacune in Financial modeling.", 
            "Alternativo": "💡 Consigliata come 'Junior Financial Analyst'",
            "Impegnato": False,
            "Operatore_Call": None
        }
    ]

if 'clienti_db' not in st.session_state:
    st.session_state.clienti_db = [
        {"Azienda": "Dei Reali Consulting", "Settore": "Consulenza Aziendale", "Referente": "Direzione HR", "Email": "info@deireali.com", "Posizioni_Aperte": 2}
    ]

# --- MODULO DI AUTENTICAZIONE (SCHERMATA INIZIALE) ---
if not st.session_state.autenticato:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Visualizzazione sicura del titolo o dell'immagine senza costrutti complessi inline
    logo_path = "1000376160.jpeg"
    if os.path.exists(logo_path):
        st.image(logo_path, width=220)
    else:
        st.markdown("<h2 style='color:#1E3A8A; margin-top:0;'>👑 DEI REALI</h2>", unsafe_allow_html=True)
        
    st.markdown("### Accesso alla Suite Aziendale")
    st.markdown("<p style='font-size:13px; color:#64748B;'>Inserisci le tue credenziali ufficiali per accedere alla tua plancia di lavoro.</p>", unsafe_allow_html=True)
    
    login_mail = st.text_input("📧 E-mail Ufficiale", key="input_mail_login")
    login_pw = st.text_input("🔑 Password Assegnata", type="password", key="input_pw_login")
    
    if st.button("ACCEDI AL SISTEMA", use_container_width=True, key="btn_submit_login"):
        if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
            st.session_state.autenticato = True
            st.session_state.utente_connesso = OPERATORI[login_mail]
            st.rerun()
        else:
            st.error("Credenziali non corrette o utente non abilitato.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- APPLICAZIONE COMPLETA (ACCESSIBILE SOLO DOPO IL LOGIN) ---
else:
    with st.sidebar:
        logo_side = "1000376160.jpeg"
        if os.path.exists(logo_side):
            st.image(logo_side, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"🟢 *Operatore:* {st.session_state.utente_connesso['nome']}")
        st.caption(f"💼 {st.session_state.utente_connesso['ruolo']}")
        
        if st.sidebar.button("🔒 Disconnetti", key="btn_logout_sidebar"):
            st.session_state.autenticato = False
            st.session_state.utente_connesso = None
            st.rerun()

    st.title("💼 Sistema di Gestione & Selezione Personale")
    st.markdown(f"##### Suite Multi-Operatore • Dei Reali &emsp;|&emsp; Operatore loggato: *{st.session_state.utente_connesso['nome']}*")
    st.markdown("<br>", unsafe_allow_html=True)

    # BARRA ORIZZONTALE A TASTI
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    buttons_nav = [("📢\nAnnunci", "📢 Annunci"), ("📥\nScreening CV", "📥 Screening CV"), ("🤝\nColloqui AI", "🤝 Colloqui AI"),
                   ("🎉\nAssunzioni", "🎉 Assunzioni"), ("📊\nReport", "📊 Report"), ("🏢\nClienti", "🏢 Clienti"), ("👥\nCandidati", "👥 Candidati")]
    
    for i, (label, key) in enumerate(buttons_nav):
        with [c1, c2, c3, c4, c5, c6, c7][i]:
            if st.button(label, key=f"nav_{key}"): 
                st.session_state.current_menu = key

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

    # --- SCREENING CV & ELENCO CANDIDATI CON STATO LIVE ---
    if st.session_state.current_menu == "📥 Screening CV" or st.session_state.current_menu == "👥 Candidati":
        st.markdown("### 👥 Elenco Candidati e Stato Linea Live")
        st.markdown("I candidati possono sostenere un solo colloquio alla volta. Controlla i badge colorati prima di avviare una stanza digitale.")
        
        with st.expander("➕ Aggiungi un nuovo Candidato alla lista", expanded=False):
            nuovo_n = st.text_input("Nome e Cognome", key="add_cand_name")
            nuova_m = st.text_input("E-mail", key="add_cand_mail")
            nuova_p = st.selectbox("Posizione", ["Senior Corporate Consultant", "Project Manager"], key="add_cand_pos")
            if st.button("PROCESSA E AGGIUNGI", key="btn_add_cand"):
                if nuovo_n and nuova_m:
                    st.session_state.candidati_db.append({
                        "id": len(st.session_state.candidati_db),
                        "Nome": nuovo_n, "Email": nuova_m, "Posizione": nuova_p,
                        "Idoneità": "72%", "Stelle": "⭐⭐⭐⭐", "Orientamento": "Profilo idoneo.", "Alternativo": "Nessuno",
                        "Impegnato": False, "Operatore_Call": None
                    })
                    st.success("Candidato aggiunto!")
                    st.rerun()

        for index, cand in enumerate(st.session_state.candidati_db):
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            col_info, col_status = st.columns([3, 1])
            
            with col_info:
                st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:14px; font-weight:normal; color:#64748B;'>({cand['Email']})</span>", unsafe_allow_html=True)
                st.markdown(f"🎯 *Candidato per:* {cand['Posizione']} &emsp;|&emsp; *Voto IA:* {cand['Idoneità']} ({cand['Stelle']})")
                st.markdown(f"🔄 *Orientamento Consigliato:* {cand['Alternativo']}")
                
            with col_status:
                if cand.get("Impegnato", False):
                    st.markdown(f'<div class="status-occupato">🔴 IMPEGNATO in altra chiamata ({cand.get("Operatore_Call", "N/D")})</div>', unsafe_allow_html=True)
                    if st.button("📴 Chiudi Chiamata", key=f"stop_btn_{index}"):
                        st.session_state.candidati_db[index]["Impegnato"] = False
                        st.session_state.candidati_db[index]["Operatore_Call"] = None
                        st.rerun()
                else:
                    st.markdown('<div class="status-disponibile">🟢 ATTIVO / Libero</div>', unsafe_allow_html=True)
                    if st.button("📞 Avvia Colloquio AI", key=f"start_btn_{index}"):
                        st.session_state.candidati_db[index]["Impegnato"] = True
                        st.session_state.candidati_db[index]["Operatore_Call"] = st.session_state.utente_connesso['nome']
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- SEZIONE COLLOQUI AI CON MONITORE ROOM ---
    elif st.session_state.current_menu == "🤝 Colloqui AI":
        st.markdown("### 🤝 Monitoraggio Stanze Colloqui in Background")
        st.markdown("Visualizzazione dei flussi audio/video operativi supportati dal Copilota IA.")
        
        occupati = [c for c in st.session_state.candidati_db if c.get("Impegnato", False)]
        col_stanze, col_ia = st.columns([2, 1])
        
        with col_stanze:
            st.markdown("#### 📞 Linee Telefoniche Occupate al momento")
            if not occupati:
                st.info("Nessuna chiamata attiva al momento. Tutti i candidati sono liberi ed in linea.")
            else:
                for c_occ in occupati:
                    st.markdown(f"""
                    <div class="saas-box" style="border-left: 4px solid #EF4444; background-color: #FEF2F2;">
                        🔒 <b>Linea Occupata da {c_occ.get('Operatore_Call', 'Operatore')}</b><br>
                        👥 Candidato connesso: <b>{c_occ['Nome']}</b><br>
                        🎯 Ruolo: <i>{c_occ['Posizione']}</i><br>
                        ⏱️ Supporto IA: <span style='color:#22C55E; font-weight:bold;'>● Trascrizione Silenziosa Attiva</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
        with col_ia:
            st.markdown("#### 🤖 Analisi Skill Live (Esempio)")
            st.markdown("""
            <div class="saas-box">
                <b>📡 Estrazione Dati Tacita</b><br>
                <p style="font-size:12px; color:#475569; font-style:italic;">
                   "L'IA sta elaborando i dati vocali per definire lo skill final score del profilo..."
                </p>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_menu == "📢 Annunci":
        col_sx, col_dx = st.columns(2)
        with col_sx:
            st.markdown("### 📝 Dati dell'Annuncio")
            uploaded_img = st.file_uploader("🖼️ Scegli file", type=["png", "jpg", "jpeg"], key="uploader_annunci_img")
            titolo_job = st.text_input("📍 Titolo della posizione", key="input_annuncio_titolo")
            tipo_importo = st.radio("Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True, key="radio_annuncio_tipo")
            valore_importo = st.text_input("Valore (€)", key="input_annuncio_valore")
            indirizzo_job = st.text_input("🏢 Sede di lavoro", key="input_annuncio_sede")
            if st.button("🚀 PUBBLICA ANNUNCIO", key="btn_annuncio_pubblica"): 
                st.success("Annuncio indicizzato!")
        with col_dx:
            st.markdown("### 🤖 Assistente Scrittura")
            st.text_area("Note sparse:", height=210, key="textarea_annuncio_note")

    elif st.session_state.current_menu == "🏢 Clienti":
        for cli in st.session_state.clienti_db:
            st.markdown(f'<div class="saas-box">🏢 <b>{cli["Azienda"]}</b> - Referente: {cli["Referente"]}</div>', unsafe_allow_html=True)
    else:
        st.info(f"Pannello {st.session_state.current_menu} attivo.")
