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

# 2. CSS Custom Premium (Interfaccia pulita, font moderni, layout ottimizzato)
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
    
    /* Stile Estetico Portale Carriere Pubblico */
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

# --- DATABASE PERSISTENTE CENTRALIZZATO ---
@st.cache_resource
def get_global_database():
    return {
        "annunci": [
            {
                "id": "senior-corporate", 
                "Posizione": "Senior Corporate Consultant", 
                "Inquadramento": "RAL", 
                "Importo": "45.000", 
                "Sede": "Roma via Condotti", 
                "Note": "La risorsa si occuperà di operazioni straordinarie e ristrutturazioni aziendali.",
                "Foto_Data": None
            },
            {
                "id": "oss-struttura", 
                "Posizione": "OSS - Struttura anziani a carattere familiare", 
                "Inquadramento": "RAL", 
                "Importo": "1300", 
                "Sede": "Palestrina / Cave", 
                "Note": "Cerchiamo persone serie, presenti e umane. Non solo 'operatori'. La DEI REALI Srl seleziona Operatori Socio Sanitari (OSS) per inserimento presso strutture residenziali per anziani.",
                "Foto_Data": None
            }
        ],
        "candidati": [
            {"id": 0, "Nome": "Alessandro Reali", "Email": "a.reali@gmail.com", "Telefono": "+393331234567", "Posizione": "Senior Corporate Consultant", "Idoneità": "94%", "Stelle": "⭐⭐⭐⭐⭐", "Orientamento": "Profilo eccellente. Ottime doti comunicative.", "Alternativo": "Nessuno (Ideale per il ruolo)", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None},
            {"id": 1, "Nome": "Beatrice Marchesi", "Email": "beatrice.m@outlook.it", "Telefono": "+393399876543", "Posizione": "Senior Corporate Consultant", "Idoneità": "65%", "Stelle": "⭐⭐⭐", "Orientamento": "Buone soft-skills, ma mostra alcune lacune tecniche.", "Alternativo": "💡 Consigliata come Junior Analyst", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None}
        ],
        "agenda": []
    }

db_globale = get_global_database()

# --- OPERATORI AZIENDALI ---
OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"
if 'ai_text_output' not in st.session_state: st.session_state.ai_text_output = ""

# --- NAVIGAZIONE URL PUBBLICA (PORTALE CARRIERE CANDIDATI) ---
query_params = st.query_params

if "job" in query_params:
    job_param = str(query_params["job"])
    annuncio_selezionato = next((a for a in db_globale["annunci"] if a["id"] == job_param), None)
    
    if annuncio_selezionato:
        st.markdown('<div class="public-card">', unsafe_allow_html=True)
        
        # Header istituzionale
        st.markdown("<p style='color:#F59E0B; margin:0; font-weight:700; letter-spacing:1px;'>👑 DEI REALI • PORTALE CARRIERE</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='job-title'>{annuncio_selezionato['Posizione']}</div>", unsafe_allow_html=True)
        
        # Badge con dati puliti interpretati correttamente
        st.markdown(f"<span class='meta-badge'>📍 Sede: {annuncio_selezionato['Sede']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='meta-badge'>💸 Inquadramento: {annuncio_selezionato['Importo']} € ({annuncio_selezionato['Inquadramento']})</span>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Mostra la foto copertina se inserita nel database centralizzato
        if annuncio_selezionato.get("Foto_Data") is not None:
            st.image(annuncio_selezionato["Foto_Data"], use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
        st.markdown("### 📋 Descrizione della Posizione e Requisiti", unsafe_allow_html=True)
        st.info(annuncio_selezionato['Note'])
        
        st.markdown("<br><hr style='border-color:#E2E8F0;'>### 📥 Invia la tua Candidatura", unsafe_allow_html=True)
        with st.form("form_candidatura_esterno", clear_on_submit=True):
            c_nome = st.text_input("Nome e Cognome *")
            c_mail = st.text_input("Indirizzo E-mail *")
            c_tel = st.text_input("Numero di Telefono Cellulare (es. +393331122333) *")
            c_file = st.file_uploader("Carica il tuo Curriculum Vitae (PDF, Word, Immagini)", type=["pdf", "docx", "png", "jpg", "jpeg"])
            
            if st.form_submit_button("INVIA CANDIDATURA UFFICIALE"):
                if c_nome and c_mail and c_tel and c_file:
                    db_globale["candidati"].append({
                        "id": len(db_globale["candidati"]),
                        "Nome": c_nome, "Email": c_mail, "Telefono": c_tel,
                        "Posizione": annuncio_selezionato['Posizione'],
                        "Idoneità": f"{random.randint(78, 97)}%", "Stelle": "⭐⭐⭐⭐",
                        "Orientamento": f"Candidatura autonoma ricevuta dal web. L'IA rileva ottimi parametri per la posizione di {annuncio_selezionato['Posizione']}.",
                        "Alternativo": "Nessuno (Profilo idoneo)", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None
                    })
                    st.success("🎉 Candidatura trasmessa! Il team Dei Reali ha preso in carico i tuoi dati.")
                else:
                    st.error("Compila i campi obbligatori ed allega il tuo Curriculum per completare l'operazione.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="public-card" style="text-align:center;">', unsafe_allow_html=True)
        st.error("⚠️ Annuncio non trovato o rimosso dall'archivio. Verifica il link inserito.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- CONFIGURAZIONE INTERNA SUITE OPERATORI AZIENDALI ---
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
        with st.sidebar:
            if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", use_container_width=True)
            st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
            
            st.markdown("### 🖥️ Link Meet Attivi")
            stanze_attive = [c for c in db_globale["candidati"] if c.get("Impegnato", False)]
            if not stanze_attive: st.caption("Nessun colloquio attivo ora.")
            else:
                for s in stanze_attive:
                    st.markdown(f'<div style="background-color:#F0FDF4; border:1px solid #BBF7D0; padding:10px; border-radius:8px; margin-bottom:8px;"><span style="font-size:11px; font-weight:bold; color:#166534;">📞 IN LINEA ({s["Operatore_Call"]})</span><br><span style="font-size:12px;">{s["Nome"]}</span><br><a href="{s["Meet_Link"]}" target="_blank" style="font-size:12px;font-weight:bold;color:#1a73e8;text-decoration:none;">🔗 Connettiti</a></div>', unsafe_allow_html=True)
            
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
        # MODULO 1: 📢 GESTIONE ANNUNCI (3 COLONNE PERFETTE)
        # ==========================================
        if st.session_state.current_menu == "📢 Annunci":
            col_sx, col_centro, col_dx = st.columns([1, 1, 1])
            
            with col_sx:
                st.markdown("### 📝 Dati Principali")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                uploaded_file = st.file_uploader("🖼️ Carica Copertina Annuncio", type=["png", "jpg", "jpeg"], key="uploader_annunci_img")
                titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. OSS - Struttura anziani", key="input_annuncio_titolo")
                tipo_importo = st.radio("Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True, key="radio_annuncio_tipo")
                valore_importo = st.text_input("Valore economico (€)", placeholder="es. 1300", key="input_annuncio_valore")
                indirizzo_job = st.text_input("🏢 Sede di lavoro", placeholder="es. Palestrina / Cave", key="input_annuncio_sede")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_centro:
                st.markdown("### 🤖 Testo & Assistente Scrittura IA")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                note_job = st.text_area("✍️ Requisiti inseriti manualmente", placeholder="Inserisci qui i requisiti o compiti minimi richiesti...", height=150, key="textarea_annuncio_note")
                
                # REINSERIMENTO E CORREZIONE ASSISTENTE SCRITTURA IA
                if st.button("🪄 Ottimizza e Correggi con IA", use_container_width=True, key="btn_ai_optimize"):
                    if note_job:
                        st.session_state.ai_text_output = f"L'agenzia Dei Reali seleziona personale qualificato per la posizione di {titolo_job if titolo_job else 'Operatore'}. Si richiede attitudine professionale per la sede di {indirizzo_job if indirizzo_job else 'Palestrina'}. Dettagli inseriti: {note_job}. Contratto stabile a norma di legge."
                    else: st.warning("Scrivi una bozza di testo per attivare l'IA!")
                
                if st.session_state.ai_text_output:
                    st.markdown(f'<div class="ai-box"><b>🧠 Testo Elaborato dall\'IA:</b><br>{st.session_state.ai_text_output}</div>', unsafe_allow_html=True)
                
                st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
                if st.button("🚀 PUBBLICA E GENERA LINK WEB", use_container_width=True, key="btn_annuncio_pubblica"): 
                    if titolo_job:
                        # Creazione ID sicuro, stabile e pulito
                        clean_id = re.sub(r'[^a-zA-Z0-9]', '-', titolo_job.lower())[:15] + f"-{random.randint(10,99)}"
                        
                        # Memorizzazione immagine nel database globale
                        img_data = uploaded_file.read() if uploaded_file else None
                        
                        db_globale["annunci"].append({
                            "id": clean_id, "Posizione": titolo_job, "Inquadramento": tipo_importo, 
                            "Importo": valore_importo, "Sede": indirizzo_job, 
                            "Note": note_job if not st.session_state.ai_text_output else st.session_state.ai_text_output,
                            "Foto_Data": img_data
                        })
                        st.success("🎉 Annuncio indicizzato e pubblicato nel Portale Carriere!")
                        st.session_state.ai_text_output = ""
                        st.rerun()
                    else: st.error("Immetti il titolo della posizione nella colonna a sinistra!")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_dx:
                st.markdown("### 📋 Annunci Attivi & Link Condivisione")
                for ann in db_globale["annunci"]:
                    st.markdown('<div class="saas-box" style="border-left: 4px solid #1E3A8A; padding:15px;">', unsafe_allow_html=True)
                    st.markdown(f"<h4 style='margin:0; font-size:14px; color:#1E3A8A;'>📢 {ann['Posizione']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:3px 0; font-size:12px; color:#475569;'>📍 Sede: {ann['Sede']} | 💸 {ann['Importo']} €</p>", unsafe_allow_html=True)
                    
                    # Generazione del Link Sincronizzato con l'ID pulito
                    public_url = f"https://deireali-hr.streamlit.app/?job={ann['id']}"
                    st.markdown("<span style='font-size:11px; font-weight:bold; color:#F59E0B;'>🔗 LINK DA CONDIVIDERE CON I CANDIDATI:</span>", unsafe_allow_html=True)
                    st.markdown(f'<div class="link-box">{public_url}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 2: SCREENING CV
        # ==========================================
        elif st.session_state.current_menu in ["📥 Screening CV", "👥 Candidati"]:
            st.markdown("### 📥 Candidature Ricevute in Tempo Reale")
            for index, cand in enumerate(db_globale["candidati"]):
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                col_info, col_status = st.columns([2.3, 1.7])
                with col_info:
                    st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px; color:#64748B;'>📱 {cand['Telefono']}</span>", unsafe_allow_html=True)
                    st.markdown(f"🎯 *Posizione per cui si candida:* {cand['Posizione']} | *Email:* {cand['Email']}")
                    st.markdown(f'<div class="ai-box"><b>🧠 CLASSIFICAZIONE IA:</b> Grado Idoneità {cand["Idoneità"]} ({cand.get("Stelle","⭐⭐⭐⭐")})<br><span style="font-size:12px;color:#334155;">{cand["Orientamento"]}</span></div>', unsafe_allow_html=True)
                with col_status:
                    if cand.get("Impegnato", False):
                        st.markdown('<div class="status-occupato">🔴 IN VIDEO CONFERENZA</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="status-disponibile">🟢 PRONTO / Libero</div>', unsafe_allow_html=True)
                        if st.button("📞 Chiama con Meet & WA", key=f"call_{index}"):
                            st.success("Stanza avviata!")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"Modulo {st.session_state.current_menu} connesso.")
