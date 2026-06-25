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

# 2. CSS Custom per l'interfaccia Premium e Badge di Stato
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

# Inizializzazione Database Candidati Completo di Stati Live
if 'candidati_db' not in st.session_state:
    st.session_state.candidati_db = [
        {"id": 0, "Nome": "Alessandro Reali", "Email": "a.reali@gmail.com", "Telefono": "+393331234567", "Posizione": "Senior Corporate Consultant", "Idoneità": "94%", "Stelle": "⭐⭐⭐⭐⭐", "Orientamento": "Perfetto per il ruolo.", "Alternativo": "Nessuno", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None},
        {"id": 1, "Nome": "Beatrice Marchesi", "Email": "beatrice.m@outlook.it", "Telefono": "+393399876543", "Posizione": "Senior Corporate Consultant", "Idoneità": "65%", "Stelle": "⭐⭐⭐", "Orientamento": "Buone soft-skills.", "Alternativo": "💡 Consigliata come 'Junior Financial Analyst'", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None}
    ]

# Inizializzazione Database Agenda
if 'agenda_db' not in st.session_state:
    st.session_state.agenda_db = []

# Inizializzazione Database Clienti
if 'clienti_db' not in st.session_state:
    st.session_state.clienti_db = [
        {"Azienda": "Dei Reali Consulting", "Settore": "Consulenza Aziendale", "Referente": "Direzione HR", "Email": "info@deireali.com", "Posizioni_Aperte": 2}
    ]

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

# --- SUITE COMPLETA AUTENTICATA ---
else:
    with st.sidebar:
        if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", use_container_width=True)
        st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
        if st.sidebar.button("🔒 Disconnetti", key="btn_logout"):
            st.session_state.autenticato = False; st.rerun()

    st.title("💼 Sistema di Gestione & Selezione Personale")
    st.markdown(f"##### Suite Multi-Operatore • Dei Reali &emsp;|&emsp; Operatore: *{st.session_state.utente_connesso['nome']}*")
    
    # Barra di navigazione a 7 pulsanti orizzontali
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    buttons_nav = [("📢\nAnnunci", "📢 Annunci"), ("📥\nScreening CV", "📥 Screening CV"), ("🤝\nColloqui AI", "🤝 Colloqui AI"),
                   ("🎉\nAssunzioni", "🎉 Assunzioni"), ("📊\nReport", "📊 Report"), ("🏢\nClienti", "🏢 Clienti"), ("👥\nCandidati", "👥 Candidati")]
    for i, (label, key) in enumerate(buttons_nav):
        with [c1, c2, c3, c4, c5, c6, c7][i]:
            if st.button(label, key=f"nav_{key}"): st.session_state.current_menu = key

    st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

    # ==========================================
    # MODULO 1: 📢 GESTIONE ANNUNCI (RIPRISTINATO)
    # ==========================================
    if st.session_state.current_menu == "📢 Annunci":
        col_sx, col_dx = st.columns(2)
        with col_sx:
            st.markdown("### 📝 Dati dell'Annuncio")
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            uploaded_img = st.file_uploader("🖼️ Carica Copertina Annuncio", type=["png", "jpg", "jpeg"], key="uploader_annunci_img")
            titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. Senior Corporate Consultant", key="input_annuncio_titolo")
            tipo_importo = st.radio("Inquadramento", ["RAL (Annua)", "Importo Lordo", "Costo Orario"], horizontal=True, key="radio_annuncio_tipo")
            valore_importo = st.text_input("Valore economico (€)", placeholder="es. 45.000", key="input_annuncio_valore")
            indirizzo_job = st.text_input("🏢 Sede di lavoro", placeholder="es. Via Condotti, Roma", key="input_annuncio_sede")
            
            st.markdown("*📞 Contatti Veloci*")
            cx1, cx2 = st.columns(2)
            with cx1: st.text_input("Cellulare", placeholder="es. +39 333...", key="annuncio_cell")
            with cx2: st.text_input("E-mail", placeholder="es. hr@deireali.com", key="annuncio_mail")
            
            if st.button("🚀 PUBBLICA NUOVO ANNUNCIO SU WEB", use_container_width=True, key="btn_annuncio_pubblica"): 
                if titolo_job:
                    st.success("🎉 Annuncio indicizzato e pubblicato con successo nel sistema centralizzato!")
                else:
                    st.error("Inserisci almeno il titolo della posizione!")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_dx:
            st.markdown("### 🤖 Assistente di Scrittura IA")
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            st.text_area("Note e requisiti sparsi da elaborare:", placeholder="Cerchiamo un profilo con esperienza di almeno 3 anni...", height=210, key="textarea_annuncio_note")
            st.selectbox("Tono dell'editing AI", ["Professionale", "Istituzionale", "Moderno"], key="tono_annuncio")
            if st.button("🪄 OTTIMIZZA LAYOUT E CONTENUTO CON IA", use_container_width=True, key="btn_ai_copy"):
                st.info("Bozza ottimizzata generata correttamente dall'assistente virtuale.")
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # MODULO 2: 📥 SCREENING CV & ELENCO LIVE CANDIDATI (COMPLETO)
    # ==========================================
    elif st.session_state.current_menu in ["📥 Screening CV", "👥 Candidati"]:
        st.markdown("### 👥 Elenco Candidati e Monitor Linea Chiamate Live")
        st.markdown("In questa sezione vedi chi è libero o occupato in tempo reale. Puoi avviare una chiamata istantanea Meet + WhatsApp.")
        
        with st.expander("➕ Inserisci Manualmente un Nuovo Candidato", expanded=False):
            nuovo_n = st.text_input("Nome e Cognome", key="add_cand_name")
            nuova_m = st.text_input("E-mail", key="add_cand_mail")
            nuovo_t = st.text_input("Telefono (con +39)", placeholder="+393331122333", key="add_cand_tel")
            nuova_p = st.selectbox("Posizione", ["Senior Corporate Consultant", "Project Manager"], key="add_cand_pos")
            if st.button("PROCESSA E AGGIUNGI IN GRADUATORIA", key="btn_add_cand"):
                if nuovo_n and nuova_m:
                    st.session_state.candidati_db.append({
                        "id": len(st.session_state.candidati_db),
                        "Nome": nuovo_n, "Email": nuova_m, "Telefono": nuovo_t if nuovo_t else "+393330000000", "Posizione": nuova_p,
                        "Idoneità": "75%", "Stelle": "⭐⭐⭐⭐", "Orientamento": "Profilo idoneo.", "Alternativo": "Nessuno",
                        "Impegnato": False, "Operatore_Call": None, "Meet_Link": None
                    })
                    st.success("Candidato aggiunto con successo!")
                    st.rerun()

        for index, cand in enumerate(st.session_state.candidati_db):
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            col_info, col_status = st.columns([2.5, 1.5])
            
            with col_info:
                st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px; color:#64748B;'>📱 {cand['Telefono']}</span>", unsafe_allow_html=True)
                st.markdown(f"🎯 *Candidato per:* {cand['Posizione']} &emsp;|&emsp; *Affinità IA:* {cand['Idoneità']} ({cand['Stelle']})")
                st.markdown(f"🔄 *Orientamento Consigliato:* {cand['Orientamento']}")
                
            with col_status:
                if cand.get("Impegnato", False):
                    st.markdown(f'<div class="status-occupato">🔴 IMPEGNATO in altra chiamata ({cand.get("Operatore_Call")})</div>', unsafe_allow_html=True)
                    
                    if cand.get("Operatore_Call") == st.session_state.utente_connesso['nome']:
                        st.markdown(f'<a href="{cand["Meet_Link"]}" target="_blank" class="meet-btn" style="width:100%;">🖥️ Entra su Meet</a>', unsafe_allow_html=True)
                        
                        orario_attuale = datetime.now().strftime("%H:%M")
                        messaggio_testo = f"Gentile {cand['Nome']},\n\nEcco il link per la video conferenza Dei Reali attiva ora con {st.session_state.utente_connesso['nome']}.\n🔗 Link: {cand['Meet_Link']}\n\nNota: Il supporto IA prenderà parte alla sessione in modalità silente."
                        msg_encoded = urllib.parse.quote(messaggio_testo)
                        st.markdown(f'<a href="https://wa.me/{cand["Telefono"].replace("+", "")}?text={msg_encoded}" target="_blank" class="whatsapp-btn" style="width:100%;">💬 Notifica su WhatsApp</a>', unsafe_allow_html=True)
                        
                        if st.button("📴 Chiudi Chiamata e Libera", key=f"stop_btn_{index}"):
                            st.session_state.candidati_db[index]["Impegnato"] = False
                            st.session_state.candidati_db[index]["Operatore_Call"] = None
                            st.rerun()
                else:
                    st.markdown('<div class="status-disponibile">🟢 PRONTO / Libero</div>', unsafe_allow_html=True)
                    if st.button("📞 Seleziona e Chiama Ora", key=f"start_btn_{index}"):
                        st.session_state.candidati_db[index]["Impegnato"] = True
                        st.session_state.candidati_db[index]["Operatore_Call"] = st.session_state.utente_connesso['nome']
                        meet_code = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"
                        st.session_state.candidati_db[index]["Meet_Link"] = f"https://meet.google.com/{meet_code}"
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # MODULO 3: 🤝 AGENDA CALENDARIO & STANZE AI
    # ==========================================
    elif st.session_state.current_menu == "🤝 Colloqui AI":
        st.markdown("### 🤝 Agenda Appuntamenti & Gestione Stanze Digitali")
        
        col_pianifica, col_lista = st.columns([1.2, 1.8])
        
        with col_pianifica:
            st.markdown("#### 🗓️ Pianifica Nuovo Colloquio")
            st.markdown('<div class="saas-box">', unsafe_allow_html=True)
            nomi_candidati = [c["Nome"] for c in st.session_state.candidati_db]
            cand_scelto = st.selectbox("Seleziona il Candidato da Chiamare", nomi_candidati, key="agenda_cand_select")
            data_scelta = st.date_input("Scegli la Data", min_value=date.today(), key="agenda_date_select")
            ora_scelta = st.time_input("Scegli l'Orario", value=time(10, 0), key="agenda_time_select")
            
            if st.button("💾 Consegna ad Agenda & Genera Invito", use_container_width=True, key="btn_save_agenda"):
                meet_code = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"
                st.session_state.agenda_db.append({
                    "Candidato": cand_scelto,
                    "Data": str(data_scelta),
                    "Ora": ora_scelta.strftime("%H:%M"),
                    "Operatore": st.session_state.utente_connesso['nome'],
                    "Meet_Link": f"https://meet.google.com/{meet_code}"
                })
                st.success(f"🗓️ Colloquio programmato in agenda!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_lista:
            st.markdown("#### 📋 Appuntamenti Fissati e Supporto IA Silente")
            if not st.session_state.agenda_db:
                st.info("Nessun colloquio programmato in agenda al momento.")
            else:
                for idx, app in enumerate(st.session_state.agenda_db):
                    c_info = next((c for c in st.session_state.candidati_db if c["Nome"] == app["Candidato"]), None)
                    tel_cand = c_info["Telefono"] if c_info else "+393330000000"
                    
                    st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                    c_app1, c_app2 = st.columns([2, 1])
                    with c_app1:
                        st.markdown(f"👤 *Candidato:* <span style='color:#1E3A8A; font-weight:bold;'>{app['Candidato']}</span>", unsafe_allow_html=True)
                        st.markdown(f"📅 *Data:* {app['Data']} &emsp;|&emsp; ⏰ *Ora:* {app['Ora']}")
                        st.markdown(f"💼 *Operatore Assegnato:* {app['Operatore']}")
                    with c_app2:
                        st.markdown(f'<a href="{app["Meet_Link"]}" target="_blank" class="meet-btn" style="width:100%;">🖥️ Apri Meet Room</a>', unsafe_allow_html=True)
                        messaggio_agenda = f"Gentile {app['Candidato']},\n\nTi confermiamo il colloquio con Dei Reali con l'operatore {app['Operatore']}.\n🗓️ Data: {app['Data']}\n⏰ Ora: {app['Ora']}\n🔗 Link: {app['Meet_Link']}\n\nNota: Il supporto IA analizzerà la sessione tacitamente."
                        msg_enc = urllib.parse.quote(messaggio_agenda)
                        st.markdown(f'<a href="https://wa.me/{tel_cand.replace("+", "")}?text={msg_enc}" target="_blank" class="whatsapp-btn" style="width:100%;">💬 Invita via WA</a>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # MODULO 6: 🏢 ANAGRAFICA CLIENTI
    # ==========================================
    elif st.session_state.current_menu == "🏢 Clienti":
        st.markdown("### 🏢 Anagrafica Clienti Partner")
        with st.expander("➕ Registra Nuova Azienda Cliente", expanded=False):
            nome_az = st.text_input("Ragione Sociale")
            set_az = st.text_input("Settore")
            ref_az = st.text_input("HR Manager Referente")
            if st.button("SALVA AZIENDA"):
                if nome_az:
                    st.session_state.clienti_db.append({"Azienda": nome_az, "Settore": set_az, "Referente": ref_az, "Email": "hr@client.com", "Posizioni_Aperte": 1})
                    st.success("Azienda registrata!")
                    st.rerun()

        for cli in st.session_state.clienti_db:
            st.markdown(f'<div class="saas-box">🏢 <b>{cli["Azienda"]}</b> - Settore: {cli.get("Settore","N/D")} <br>👤 Referente: {cli.get("Referente","N/D")}</div>', unsafe_allow_html=True)
            
    else:
        st.info(f"Pannello {st.session_state.current_menu} attivo e connesso.")
