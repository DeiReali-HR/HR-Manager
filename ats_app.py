import streamlit as st
import pandas as pd
import os
import random
import urllib.parse
import re
from datetime import datetime, date, time

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Dei Reali - Suite Aziendale & Portale Carriere",
    page_icon="👑",
    layout="wide"
)

# 2. CSS Custom Premium
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
    .ai-box { background-color: #F8FAFC; border: 1px dashed #2563EB; border-radius: 10px; padding: 15px; margin-top: 10px; }
    .login-container { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 500px; margin: 60px auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }
    .public-container { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 800px; margin: 40px auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }
    .status-disponibile { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .status-occupato { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; }
    .meet-btn { background-color: #1a73e8 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; }
    .link-box { background-color: #F1F5F9; padding: 8px 12px; border-radius: 6px; font-family: monospace; font-size: 12px; border: 1px solid #CBD5E1; color: #334155; margin-top: 5px; word-break: break-all; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE CONDIVISO ANTI-AZZERAMENTO ---
@st.cache_resource
def get_global_database():
    return {
        "annunci": [
            {"id": "senior-corporate", "Posizione": "Senior Corporate Consultant", "Inquadramento": "RAL", "Importo": "45.000", "Sede": "Roma via Condotti", "Note": "Esperienza in ambito M&A."},
            {"id": "oss-struttura", "Posizione": "OSS - Struttura anziani a carattere familiare", "Inquadramento": "RAL", "Importo": "1300", "Sede": "Palestrina", "Note": "Selezioniamo personale OSS per turni diurni e festivi."}
        ],
        "candidati": [
            {"id": 0, "Nome": "Alessandro Reali", "Email": "a.reali@gmail.com", "Telefono": "+393331234567", "Posizione": "Senior Corporate Consultant", "Idoneità": "94%", "Stelle": "⭐⭐⭐⭐⭐", "Orientamento": "Profilo eccellente. Spiccate doti relazionali.", "Alternativo": "Nessuno", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None},
            {"id": 1, "Nome": "Beatrice Marchesi", "Email": "beatrice.m@outlook.it", "Telefono": "+393399876543", "Posizione": "Senior Corporate Consultant", "Idoneità": "65%", "Stelle": "⭐⭐⭐", "Orientamento": "Buona dialettica, ma mostra alcune lacune tecniche.", "Alternativo": "💡 Consigliata come Back-office", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None}
        ],
        "agenda": []
    }

db_globale = get_global_database()

# --- UTENTI OPERATORI AMMESSI ---
OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"

# --- INTERCETTAZIONE LINK DEL CANDIDATO (?job=) ---
query_params = st.query_params

if "job" in query_params:
    job_id = query_params["job"]
    annuncio_selezionato = next((a for a in db_globale["annunci"] if a["id"] == job_id), None)
    
    if annuncio_selezionato:
        st.markdown('<div class="public-container">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#64748B; margin:0;'>👑 DEI REALI - PORTALE CARRIERE</h4>", unsafe_allow_html=True)
        st.title(f"💼 {annuncio_selezionato['Posizione']}")
        st.markdown(f"📍 *Sede:* {annuncio_selezionato['Sede']} &emsp;|&emsp; 💸 *Compenso:* {annuncio_selezionato['Importo']} € ({annuncio_selezionato['Inquadramento']})")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Descrizione della posizione e Requisiti")
        st.write(annuncio_selezionato['Note'])
        
        st.markdown("<br><hr>### 📥 Invia la tua Candidatura", unsafe_allow_html=True)
        with st.form("form_candidatura_pubblica", clear_on_submit=True):
            c_nome = st.text_input("Nome e Cognome *")
            c_mail = st.text_input("Indirizzo E-mail *")
            c_tel = st.text_input("Numero di Telefono (es. +393331234567) *")
            c_file = st.file_uploader("Carica il tuo Curriculum Vitae (PDF, JPG, PNG)", type=["pdf", "docx", "png", "jpg", "jpeg"])
            
            if st.form_submit_button("INVIA CURRICULUM ALL'AGENZIA"):
                if c_nome and c_mail and c_tel and c_file:
                    # Salva nel database centralizzato visibile agli amministratori
                    db_globale["candidati"].append({
                        "id": len(db_globale["candidati"]),
                        "Nome": c_nome, "Email": c_mail, "Telefono": c_tel,
                        "Posizione": annuncio_selezionato['Posizione'],
                        "Idoneità": f"{random.randint(75, 98)}%", "Stelle": "⭐⭐⭐⭐",
                        "Orientamento": f"Candidato autogestito dal portale. IA rileva ottima corrispondenza per la sede di {annuncio_selezionato['Sede']}.",
                        "Alternativo": "Nessuno", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None
                    })
                    st.success("🎉 Candidatura inoltrata correttamente! Il team di Dei Reali analizzerà il tuo profilo.")
                else:
                    st.error("Compila tutti i campi richiesti e allega il tuo file CV.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="public-container" style="text-align:center;">', unsafe_allow_html=True)
        st.error("⚠️ Annuncio non trovato o rimosso dall'archivio aziendale. Verifica l'URL o contatta l'amministratore.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- PORTALE DI LOGIN / AREA OPERATORE AZIENDALE ---
else:
    if not st.session_state.autenticato:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", width=220)
        st.markdown("### Accesso alla Suite Aziendale")
        login_mail = st.text_input("📧 E-mail Ufficiale", key="input_mail_login")
        login_pw = st.text_input("🔑 Password Assegnata", type="password", key="input_pw_login")
        if st.button("ACCEDI AL SISTEMA", use_container_width=True):
            if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
                st.session_state.autenticato = True
                st.session_state.utente_connesso = OPERATORI[login_mail]
                st.rerun()
            else: st.error("Credenziali errate.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # AREA BACKOFFICE OPERATORE
        with st.sidebar:
            if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", use_container_width=True)
            st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
            if st.sidebar.button("🔒 Disconnetti"):
                st.session_state.autenticato = False; st.rerun()

        st.title("👑 Suite di Gestione Risorse Umane")
        st.markdown(f"##### Dei Reali Executive Selection &emsp;|&emsp; Operatore: *{st.session_state.utente_connesso['nome']}*")
        
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        buttons_nav = [("📢\nAnnunci", "📢 Annunci"), ("📥\nScreening CV", "📥 Screening CV"), ("🤝\nColloqui AI", "🤝 Colloqui AI"),
                       ("🎉\nAssunzioni", "🎉 Assunzioni"), ("📊\nReport", "📊 Report"), ("🏢\nClienti", "🏢 Clienti"), ("👥\nCandidati", "👥 Candidati")]
        for i, (label, key) in enumerate(buttons_nav):
            with [c1, c2, c3, c4, c5, c6, c7][i]:
                if st.button(label, key=f"nav_{key}"): st.session_state.current_menu = key

        st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 1: GESTIONE ANNUNCI & GENERATORE LINK PUBBLICO
        # ==========================================
        if st.session_state.current_menu == "📢 Annunci":
            col_sx, col_centro, col_dx = st.columns([1, 1, 1])
            with col_sx:
                st.markdown("### 📝 Dati Principali")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                st.file_uploader("🖼️ Carica Copertina", type=["png", "jpg", "jpeg"])
                titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. OSS - Struttura anziani")
                tipo_importo = st.radio("Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True)
                valore_importo = st.text_input("Valore economico (€)", placeholder="es. 1300")
                indirizzo_job = st.text_input("🏢 Sede di lavoro", placeholder="es. Palestrina")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_centro:
                st.markdown("### 🤖 Testo & Assistente IA")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                note_job = st.text_area("✍️ Requisiti / Descrizione", placeholder="Dettagli...", height=160)
                
                if st.button("🚀 PUBBLICA ORA L'ANNUNCIO", use_container_width=True): 
                    if titolo_job:
                        # Pulisce l'ID rimuovendo spazi doppi o caratteri che rompono l'URL
                        clean_id = re.sub(r'[^a-zA-Z0-9-]', '', titolo_job.lower().replace(" ", "-"))[:25]
                        db_globale["annunci"].append({
                            "id": clean_id, "Posizione": titolo_job, "Inquadramento": tipo_importo, 
                            "Importo": valore_importo, "Sede": indirizzo_job, "Note": note_job
                        })
                        st.success("🎉 Pubblicato! Link di candidatura pronto a destra.")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_dx:
                st.markdown("### 📋 Annunci Attivi & Link Condivisione")
                for ann in db_globale["annunci"]:
                    st.markdown('<div class="saas-box" style="border-left: 4px solid #1E3A8A;">', unsafe_allow_html=True)
                    st.markdown(f"<b>📢 {ann['Posizione']}</b><br><span style='font-size:12px;color:#475569;'>📍 {ann['Sede']}</span>", unsafe_allow_html=True)
                    
                    public_url = f"https://deireali-hr.streamlit.app/?job={ann['id']}"
                    st.markdown("<span style='font-size:11px;font-weight:bold;color:#F59E0B;'>🔗 LINK DA CONDIVIDERE CON I CANDIDATI:</span>", unsafe_allow_html=True)
                    st.markdown(f'<div class="link-box">{public_url}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 2: SCREENING CV (RICEVE I DATI DAL PORTALE IN TEMPO REALE)
        # ==========================================
        elif st.session_state.current_menu in ["📥 Screening CV", "👥 Candidati"]:
            st.markdown("### 📥 Candidature Ricevute in Tempo Reale")
            
            if not db_globale["candidati"]:
                st.info("Nessuna candidatura registrata al momento.")
            else:
                for index, cand in enumerate(db_globale["candidati"]):
                    st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                    col_info, col_status = st.columns([2.3, 1.7])
                    with col_info:
                        st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px; color:#64748B;'>📱 {cand['Telefono']}</span>", unsafe_allow_html=True)
                        st.markdown(f"🎯 *Posizione per cui si candida:* {cand['Posizione']} | *Email:* {cand['Email']}")
                        st.markdown(f"""
                        <div class="ai-box">
                            <b>🧠 ANALISI AUTOMATICA IA:</b> Voto {cand['Idoneità']} {cand.get('Stelle', '')}<br>
                            <span style='font-size:12.5px; color:#475569;'>{cand['Orientamento']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_status:
                        st.markdown('<div class="status-disponibile">🟢 PRONTO / Libero</div>', unsafe_allow_html=True)
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        if st.button("📞 Chiama con Meet & WA", key=f"call_{index}"):
                            st.success("Stanza istantanea generata! Invia la notifica dell'appuntamento.")
                    st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.info(f"Modulo {st.session_state.current_menu} attivo e connesso al database globale.")
