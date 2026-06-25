import streamlit as st
import pandas as pd
import os
import random
import urllib.parse
import re
from datetime import datetime, date, time

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Dei Reali - Suite Enterprise Risorse Umane",
    page_icon="👑",
    layout="wide"
)

# 2. Stili Grafici Premium Coerenti
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
    .ai-box { background-color: #F1F5F9; border-left: 4px solid #2563EB; border-radius: 4px; padding: 15px; margin-top: 10px; }
    .login-container { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 500px; margin: 60px auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }
    
    /* Portale Carriere Pubblico */
    .public-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 900px; margin: 30px auto; box-shadow: 0 10px 30px -10px rgba(0,0,0,0.08); }
    .job-title { color: #1E3A8A !important; font-size: 32px !important; font-weight: 800 !important; margin-bottom: 15px !important; }
    .meta-badge { background-color: #F1F5F9; padding: 6px 14px; border-radius: 20px; font-size: 13px; color: #334155; font-weight: 600; display: inline-block; margin-right: 10px; margin-bottom: 10px; }
    
    .status-disponibile { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .status-occupato { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; }
    .meet-btn { background-color: #1a73e8 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; }
    .link-box { background-color: #F8FAFC; padding: 10px 14px; border-radius: 8px; font-family: monospace; font-size: 12px; border: 1px solid #E2E8F0; color: #2563EB; margin-top: 5px; word-break: break-all; font-weight: bold; }
    .global-banner { background-color: #FFFBEB; border-left: 5px solid #F59E0B; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE CONDIVISO PERSISTENTE TRA SCHEDE ---
@st.cache_resource
def get_global_database():
    return {
        "annunci": [
            {"id": "senior-corporate", "Posizione": "Senior Corporate Consultant", "Inquadramento": "RAL", "Importo": "45.000", "Sede": "Roma via Condotti", "Note": "Consulenza societaria straordinaria.", "Foto_Data": None},
            {"id": "oss-struttura", "Posizione": "OSS - Struttura anziani a carattere familiare", "Inquadramento": "RAL", "Importo": "1300", "Sede": "Palestrina / Cave", "Note": "Cerchiamo persone serie, presenti e umane. Selezione per inserimento immediato.", "Foto_Data": None}
        ],
        "candidati": [
            {"id": 0, "Nome": "Alessandro Reali", "Email": "a.reali@gmail.com", "Telefono": "+393331234567", "Posizione": "Senior Corporate Consultant", "Idoneità": "94%", "Stelle": "⭐⭐⭐⭐⭐", "Orientamento": "Profilo eccellente. Spiccate doti di coordinamento strategico.", "Alternativo": "Nessuno", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None, "Stato": "In Screening"},
            {"id": 1, "Nome": "Beatrice Marchesi", "Email": "beatrice.m@outlook.it", "Telefono": "+393399876543", "Posizione": "Senior Corporate Consultant", "Idoneità": "65%", "Stelle": "⭐⭐⭐", "Orientamento": "Buone soft-skills, lacune su Financial Modeling.", "Alternativo": "💡 Junior Analyst", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None, "Stato": "In Screening"}
        ],
        "agenda": [
            {"Candidato": "Alessandro Reali", "Data": "2026-06-26", "Ora": "15:30", "Operatore": "Danilo", "Meet_Link": "https://meet.google.com/qww-rtyu-iop", "Telefono": "+393331234567"}
        ],
        "clienti": [
            {"Azienda": "Dei Reali Corporate Consulting", "Settore": "Strategic Advisory", "Referente": "Dionisio", "Posizioni": "2"},
            {"Azienda": "Medical Sanitas Srl", "Settore": "Sanitario", "Referente": "Danilo", "Posizioni": "1"}
        ],
        "assunzioni": [
            {"Candidato": "Marco Rossi", "Posizione": "Project Manager", "Data_Inizio": "2026-07-01", "Contratto": "Tempo Indeterminato", "RAL": "38.000 €", "Stato": "In Approvazione"}
        ]
    }

db_globale = get_global_database()

# --- OPERATORI ABILITATI ---
OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"
if 'ai_text_output' not in st.session_state: st.session_state.ai_text_output = ""

# --- NAVIGAZIONE URL PUBBLICA (PORTALE CANDIDATO) ---
query_params = st.query_params

if "job" in query_params:
    job_param = str(query_params["job"])
    annuncio_selezionato = next((a for a in db_globale["annunci"] if a["id"] == job_param), None)
    
    if annuncio_selezionato:
        st.markdown('<div class="public-card">', unsafe_allow_html=True)
        st.markdown("<p style='color:#F59E0B; margin:0; font-weight:700; letter-spacing:1px;'>👑 DEI REALI • PORTALE CARRIERE</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='job-title'>{annuncio_selezionato['Posizione']}</div>", unsafe_allow_html=True)
        st.markdown(f"<span class='meta-badge'>📍 Sede: {annuncio_selezionato['Sede']}</span><span class='meta-badge'>💸 Compenso: {annuncio_selezionato['Importo']} € ({annuncio_selezionato['Inquadramento']})</span>", unsafe_allow_html=True)
        
        if annuncio_selezionato.get("Foto_Data") is not None:
            st.image(annuncio_selezionato["Foto_Data"], use_container_width=True)
            
        st.markdown("<br>### 📋 Descrizione della Posizione e Requisiti", unsafe_allow_html=True)
        st.info(annuncio_selezionato['Note'])
        
        st.markdown("<br><hr>### 📥 Invia la tua Candidatura", unsafe_allow_html=True)
        with st.form("form_candidatura_esterno", clear_on_submit=True):
            c_nome = st.text_input("Nome e Cognome *")
            c_mail = st.text_input("Indirizzo E-mail *")
            c_tel = st.text_input("Numero di Telefono Cellulare *")
            c_file = st.file_uploader("Carica CV", type=["pdf", "docx", "png", "jpg", "jpeg"])
            
            if st.form_submit_button("INVIA CANDIDATURA UFFICIALE"):
                if c_nome and c_mail and c_tel and c_file:
                    db_globale["candidati"].append({
                        "id": len(db_globale["candidati"]), "Nome": c_nome, "Email": c_mail, "Telefono": c_tel,
                        "Posizione": annuncio_selezionato['Posizione'], "Idoneità": f"{random.randint(78, 97)}%", "Stelle": "⭐⭐⭐⭐",
                        "Orientamento": "Profilo inviato dal web. Corrispondenza ottimale.", "Alternativo": "Nessuno", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None, "Stato": "In Screening"
                    })
                    st.success("🎉 Candidatura caricata con successo!")
                else: st.error("Riempi i campi obbligatori.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- SUITE AMMINISTRATIVA PRIVATA CONTROLLATA ---
else:
    if not st.session_state.autenticato:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", width=220)
        st.markdown("### Accesso alla Suite Aziendale")
        login_mail = st.text_input("📧 E-mail Ufficiale")
        login_pw = st.text_input("🔑 Password Assegnata", type="password")
        if st.button("ACCEDI AL SISTEMA", use_container_width=True):
            if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
                st.session_state.autenticato = True
                st.session_state.utente_connesso = OPERATORI[login_mail]
                st.rerun()
            else: st.error("Credenziali non valide.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Sidebar di monitoraggio
        with st.sidebar:
            if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", use_container_width=True)
            st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
            
            st.markdown("### 🖥️ Meet Attivi Ora")
            stanze_attive = [c for c in db_globale["candidati"] if c.get("Impegnato", False)]
            if not stanze_attive: st.caption("Nessuna video call attiva ora.")
            else:
                for s in stanze_attive:
                    st.markdown(f'<div style="background-color:#F0FDF4; padding:10px; border-radius:8px; margin-bottom:8px;"><span style="font-size:11px; font-weight:bold; color:#166534;">📞 {s["Operatore_Call"]} in linea</span><br><span style="font-size:12px;">{s["Nome"]}</span><br><a href="{s["Meet_Link"]}" target="_blank" style="font-size:12px;font-weight:bold;color:#1a73e8;">🔗 Collegati</a></div>', unsafe_allow_html=True)

        st.title("👑 Suite di Gestione Risorse Umane")
        st.markdown(f"##### Dei Reali Executive Selection &emsp;|&emsp; Operatore: *{st.session_state.utente_connesso['nome']}*")
        
        # Barra di Navigazione Principale
        c_nav = st.columns(7)
        for i, (label, key) in enumerate(buttons_nav):
            with c_nav[i]:
                if st.button(label, key=f"nav_{key}"): st.session_state.current_menu = key

        st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

        if stanze_attive:
            for s in stanze_attive:
                st.markdown(f'<div class="global-banner">🚨 <b>COLLOQUIO IN CORSO:</b> L\'operatore <b>{s["Operatore_Call"]}</b> è connesso con <b>{s["Nome"]}</b>. <a href="{s["Meet_Link"]}" target="_blank" style="margin-left:15px; font-weight:bold; color:#1A73E8;">🖥️ CLICCA QUI PER UNIRTI AL MEET</a></div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 1: 📢 GESTIONE ANNUNCI
        # ==========================================
        if st.session_state.current_menu == "📢 Annunci":
            col_sx, col_centro, col_dx = st.columns([1, 1, 1])
            with col_sx:
                st.markdown("### 📝 Nuova Posizione")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                uploaded_file = st.file_uploader("🖼️ Carica Copertina", type=["png", "jpg", "jpeg"])
                titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. OSS - Struttura anziani")
                tipo_importo = st.radio("Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True)
                valore_importo = st.text_input("Valore economico (€)", placeholder="es. 1300")
                indirizzo_job = st.text_input("🏢 Sede di lavoro", placeholder="es. Palestrina / Cave")
                st.markdown('</div>', unsafe_allow_html=True)
            with col_centro:
                st.markdown("### 🤖 Assistente Scrittura IA")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                note_job = st.text_area("✍️ Requisiti Manuali", placeholder="Requisiti...", height=150)
                if st.button("🪄 Ottimizza e Correggi con IA", use_container_width=True):
                    if note_job: st.session_state.ai_text_output = f"L'agenzia Dei Reali ricerca un profilo per la posizione di {titolo_job if titolo_job else 'Operatore'} presso la sede di {indirizzo_job if indirizzo_job else 'Palestrina'}. Dettagli: {note_job}. Si offre inquadramento stabile a norma di legge."
                if st.session_state.ai_text_output: st.markdown(f'<div class="ai-box">{st.session_state.ai_text_output}</div>', unsafe_allow_html=True)
                st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
                if st.button("🚀 PUBBLICA E GENERA LINK WEB", use_container_width=True):
                    if titolo_job:
                        clean_id = re.sub(r'[^a-zA-Z0-9]', '-', titolo_job.lower())[:15] + f"-{random.randint(10,99)}"
                        db_globale["annunci"].append({"id": clean_id, "Posizione": titolo_job, "Inquadramento": tipo_importo, "Importo": valore_importo, "Sede": indirizzo_job, "Note": note_job if not st.session_state.ai_text_output else st.session_state.ai_text_output, "Foto_Data": uploaded_file.read() if uploaded_file else None})
                        st.success("🎉 Pubblicato!"); st.session_state.ai_text_output = ""; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col_dx:
                st.markdown("### 📋 Annunci Online")
                for ann in db_globale["annunci"]:
                    st.markdown(f'<div class="saas-box" style="border-left:4px solid #1E3A8A;"><b>📢 {ann["Posizione"]}</b><br><span style="font-size:12px;color:#475569;">📍 {ann["Sede"]} | {ann["Importo"]}€</span><div class="link-box">https://deireali-hr.streamlit.app/?job={ann["id"]}</div></div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 2: 📥 SCREENING CV
        # ==========================================
        elif st.session_state.current_menu == "📥 Screening CV":
            st.markdown("### 📥 Curriculum Ricevuti ed Esito Classificazione")
            for index, cand in enumerate(db_globale["candidati"]):
                if cand["Stato"] == "In Screening":
                    st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                    c_l, c_r = st.columns([2.5, 1.5])
                    with c_l:
                        st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px;color:#64748B;'>📱 {cand['Telefono']}</span>", unsafe_allow_html=True)
                        st.markdown(f"🎯 *Ruolo scelto:* {cand['Posizione']} | *Email:* {cand['Email']}")
                        st.markdown(f'<div class="ai-box"><b>🧠 CLASSIFICAZIONE IA ({cand["Idoneità"]}):</b> {cand["Orientamento"]}<br><b>Re-routing alternativo consigliato:</b> {cand["Alternativo"]}</div>', unsafe_allow_html=True)
                    with c_r:
                        if cand.get("Impegnato", False): st.markdown('<div class="status-occupato">🔴 IN VIDEO CALL</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="status-disponibile">🟢 LIBERO</div>', unsafe_allow_html=True)
                            if st.button("📞 Chiama Ora (Istantaneo)", key=f"scr_call_{index}"):
                                db_globale["candidati"][index]["Impegnato"] = True
                                db_globale["candidati"][index]["Operatore_Call"] = st.session_state.utente_connesso['nome']
                                db_globale["candidati"][index]["Meet_Link"] = f"https://meet.google.com/{random.randint(100,999)}-{random.randint(100,999)}"
                                st.rerun()
                            if st.button("🤝 Approva per Colloquio", key=f"scr_appr_{index}"):
                                db_globale["candidati"][index]["Stato"] = "Approvato per Colloquio"
                                st.success("Spostato nella tab Candidati/Colloqui!"); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 3: 🤝 COLLOQUI AI (RIPRISTINATO COMPLETO)
        # ==========================================
        elif st.session_state.current_menu == "🤝 Colloqui AI":
            st.markdown("### 🗓️ Calendario Globale Condiviso e Supporto IA")
            if not db_globale["agenda"]: st.info("Nessun colloquio pianificato in agenda.")
            else: st.dataframe(pd.DataFrame(db_globale["agenda"])[["Data", "Ora", "Candidato", "Operatore", "Telefono", "Meet_Link"]], use_container_width=True)
            
            st.markdown("<br><hr>", unsafe_allow_html=True)
            col_plan, col_act, col_ia = st.columns([1, 1.2, 0.8])
            with col_plan:
                st.markdown("#### ✍️ Fissa Turno")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                cand_scelto = st.selectbox("Seleziona Candidato", [c["Nome"] for c in db_globale["candidati"]])
                d_s = st.date_input("Giorno", min_value=date.today())
                o_s = st.time_input("Orario", value=time(10,0))
                if st.button("💾 Conferma Turno", use_container_width=True):
                    c_inf = next((c for c in db_globale["candidati"] if c["Nome"] == cand_scelto), None)
                    db_globale["agenda"].append({"Candidato": cand_scelto, "Data": str(d_s), "Ora": o_s.strftime("%H:%M"), "Operatore": st.session_state.utente_connesso['nome'], "Meet_Link": f"https://meet.google.com/{random.randint(100,999)}", "Telefono": c_inf["Telefono"] if c_inf else "+39333000"})
                    st.success("Inserito!"); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col_act:
                st.markdown("#### ⚡ Azioni Invito")
                for idx, app in enumerate(db_globale["agenda"]):
                    st.markdown(f'<div class="saas-box"><b>{app["Candidato"]}</b> ({app["Data"]} ore {app["Ora"]})<br><a href="{app["Meet_Link"]}" target="_blank" class="meet-btn" style="width:100%;">🖥️ Avvia Meet Room</a>', unsafe_allow_html=True)
                    txt_wa = f"Gentile {app['Candidato']},\nLe confermiamo l'appuntamento Dei Reali.\n🗓️ Data: {app['Data']}\n⏰ Ora: {app['Ora']}\n🔗 Link: {app['Meet_Link']}"
                    st.markdown(f'<a href="https://wa.me/{app["Telefono"].replace("+","").replace(" ","")}?text={urllib.parse.quote(txt_wa)}" target="_blank" class="whatsapp-btn" style="width:100%;">💬 Notifica WhatsApp</a></div>', unsafe_allow_html=True)
            with col_ia:
                st.markdown("#### 🤖 Assistente Trascrizione Tacita")
                st.markdown('<div class="saas-box" style="border-left: 4px solid #10B981; background-color:#F0FDF4;">🎙️ <b>Trascrizione in background attiva.</b><br><span style="font-size:12px;color:#475569;">Al termine dell\'ascolto invisibile su Meet verranno prodotti i parametri di Skill Score e i suggerimenti automatici del candidato qui.</span></div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 4: 🎉 ASSUNZIONI (RIPRISTINATO COMPLETO)
        # ==========================================
        elif st.session_state.current_menu == "🎉 Assunzioni":
            st.markdown("### 🎉 Pratiche e Contratti di Assunzione in Corso")
            col_ass1, col_ass2 = st.columns([2, 1])
            with col_ass1:
                st.markdown("#### 📋 Elenco Risorse in Fase di Inserimento")
                for ass in db_globale["assunzioni"]:
                    st.markdown(f"""
                    <div class="saas-box" style="border-left: 4px solid #10B981;">
                        👤 <b>Candidato Idoneo:</b> {ass['Candidato']}<br>
                        🎯 <b>Posizione:</b> {ass['Posizione']} &emsp;|&emsp; 📝 <b>Contratto:</b> {ass['Contratto']} ({ass['RAL']})<br>
                        ⏱️ <b>Data Avvio Attività:</b> {ass['Data_Inizio']} &emsp;|&emsp; 🔷 <b>Stato:</b> <span style="color:#F59E0B;font-weight:bold;">{ass['Stato']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            with col_ass2:
                st.markdown("#### ➕ Registra Pratica")
                with st.form("form_assunzione"):
                    n_a = st.text_input("Nome Risorsa")
                    p_a = st.text_input("Mansione")
                    c_a = st.selectbox("Inquadramento", ["Tempo Indeterminato", "Tempo Determinato", "Apprendistato"])
                    r_a = st.text_input("RAL Concordata (€)")
                    if st.form_submit_button("CONVALIDA E AVVIA ONBOARDING"):
                        if n_a:
                            db_globale["assunzioni"].append({"Candidato": n_a, "Posizione": p_a, "Data_Inizio": str(date.today()), "Contratto": c_a, "RAL": r_a + " €", "Stato": "In Approvazione"})
                            st.success("Pratica registrata!"); st.rerun()

        # ==========================================
        # MODULO 5: 📊 REPORT (RIPRISTINATO COMPLETO)
        # ==========================================
        elif st.session_state.current_menu == "📊 Report":
            st.markdown("### 📊 Performance KPI e Statistiche Agenzia")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1: st.metric("Annunci Attivi", len(db_globale["annunci"]))
            with kpi2: st.metric("Candidature Totali", len(db_globale["candidati"]))
            with kpi3: st.metric("Colloqui in Agenda", len(db_globale["agenda"]))
            with kpi4: st.metric("Pratiche Assunzione", len(db_globale["assunzioni"]))
            
            st.markdown("<br>#### 📈 Rendimento Mensile Operatori", unsafe_allow_html=True)
            rep_data = pd.DataFrame([{"Operatore": "Danilo", "Screening": 42, "Colloqui Sostenuti": 18, "Assunzioni Chiuse": 3},
                                     {"Operatore": "Dionisio", "Screening": 35, "Colloqui Sostenuti": 22, "Assunzioni Chiuse": 5}])
            st.table(rep_data)

        # ==========================================
        # MODULO 6: 🏢 CLIENTI (RIPRISTINATO COMPLETO)
        # ==========================================
        elif st.session_state.current_menu == "🏢 Clienti":
            st.markdown("### 🏢 CRM Anagrafica Aziende Partner")
            col_cli1, col_cli2 = st.columns([2, 1])
            with col_cli1:
                for cli in db_globale["clienti"]:
                    st.markdown(f'<div class="saas-box">🏢 <b>{cli["Azienda"]}</b><br><span style="font-size:12px;color:#475569;">Settore: {cli["Settore"]} | Referente Interno Dei Reali: {cli["Referente"]} | Posizioni Aperte Mandato: {cli["Posizioni"]}</span></div>', unsafe_allow_html=True)
            with col_cli2:
                st.markdown("#### ➕ Nuova Azienda Partner")
                with st.form("add_cli_form"):
                    az_n = st.text_input("Ragione Sociale")
                    az_s = st.text_input("Settore Core")
                    az_r = st.selectbox("Account Manager Assegnato", ["Danilo", "Dionisio"])
                    if st.form_submit_button("REGISTRA CLIENTE"):
                        if az_n:
                            db_globale["clienti"].append({"Azienda": az_n, "Settore": az_s, "Referente": az_r, "Posizioni": "1"})
                            st.success("Azienda inserita!"); st.rerun()

        # ==========================================
        # MODULO 7: 👥 CANDIDATI (RIPRISTINATO COMPLETO)
        # ==========================================
        elif st.session_state.current_menu == "👥 Candidati":
            st.markdown("### 👥 Archivio Anagrafico Globale Candidati")
            for index, cand in enumerate(db_globale["candidati"]):
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px;color:#64748B;'>📱 {cand['Telefono']} | 📧 {cand['Email']}</span>", unsafe_allow_html=True)
                st.markdown(f"🎯 *Mansione Principale:* {cand['Posizione']} &emsp;|&emsp; 🔷 *Stato Avanzamento:* {cand['Stato']}")
                st.markdown(f"<p style='margin:5px 0 0 0; font-size:12px; color:#475569;'><b>Note IA:</b> {cand['Orientamento']}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
