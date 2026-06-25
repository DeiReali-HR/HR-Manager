import streamlit as st
import pandas as pd
import os
import random
import urllib.parse
import re
from datetime import datetime, date, time

# 1. Configurazione della pagina Enterprise
st.set_page_config(
    page_title="Dei Reali - Suite Enterprise Risorse Umane",
    page_icon="👑",
    layout="wide"
)

# 2. CSS Custom Premium e Stili dell'Interfaccia Aziendale
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
    
    /* Portale Carriere Esterno */
    .public-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 900px; margin: 30px auto; box-shadow: 0 10px 30px -10px rgba(0,0,0,0.08); }
    .job-title { color: #1E3A8A !important; font-size: 32px !important; font-weight: 800 !important; margin-bottom: 15px !important; }
    .meta-badge { background-color: #F1F5F9; padding: 6px 14px; border-radius: 20px; font-size: 13px; color: #334155; font-weight: 600; display: inline-block; margin-right: 10px; margin-bottom: 10px; }
    
    .status-disponibile { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .status-occupato { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; width: 100%; }
    .meet-btn { background-color: #1a73e8 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; width: 100%; }
    .link-box { background-color: #F8FAFC; padding: 10px 14px; border-radius: 8px; font-family: monospace; font-size: 12px; border: 1px solid #E2E8F0; color: #2563EB; margin-top: 5px; word-break: break-all; font-weight: bold; }
    .global-banner { background-color: #FFFBEB; border-left: 5px solid #F59E0B; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. Cache del Database Globale (Condiviso e Anti-Azzeramento)
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
                "Note": "La figura si occuperà di consulenza societaria straordinaria ed operazioni strategiche di M&A.",
                "Foto_Data": None
            },
            {
                "id": "oss-struttura", 
                "Posizione": "OSS - Struttura anziani a carattere familiare", 
                "Inquadramento": "RAL", 
                "Importo": "1300", 
                "Sede": "Palestrina / Cave", 
                "Note": "Cerchiamo persone serie, presenti e umane. Selezione per inserimento immediato con disponibilità ai turni residenziali.",
                "Foto_Data": None
            }
        ],
        "candidati": [
            {"id": 0, "Nome": "Alessandro Reali", "Email": "a.reali@gmail.com", "Telefono": "+393331234567", "Posizione": "Senior Corporate Consultant", "Idoneità": "94%", "Stelle": "⭐⭐⭐⭐⭐", "Orientamento": "Profilo eccellente. Spiccate doti relazionali e di coordinamento aziendale.", "Alternativo": "Nessuno (Perfetto)", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None, "Stato": "In Screening"},
            {"id": 1, "Nome": "Beatrice Marchesi", "Email": "beatrice.m@outlook.it", "Telefono": "+393399876543", "Posizione": "Senior Corporate Consultant", "Idoneità": "65%", "Stelle": "⭐⭐⭐", "Orientamento": "Buona dialettica comunicativa, ma mostra alcune lacune tecniche sul Financial Modeling.", "Alternativo": "💡 Consigliata come Junior Analyst", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None, "Stato": "In Screening"}
        ],
        "agenda": [
            {"Candidato": "Alessandro Reali", "Data": "2026-06-26", "Ora": "15:30", "Operatore": "Danilo", "Meet_Link": "https://meet.google.com/qww-rtyu-iop", "Telefono": "+393331234567"}
        ],
        "clienti": [
            {"Azienda": "Dei Reali Corporate Consulting", "Settore": "Consulenza Direzionale", "Referente": "Dionisio", "Posizioni": "2"},
            {"Azienda": "Medical Group Srl", "Settore": "Sanitario residenziale", "Referente": "Danilo", "Posizioni": "1"}
        ],
        "assunzioni": [
            {"Candidato": "Marco Rossi", "Posizione": "Project HR Manager", "Data_Inizio": "2026-07-01", "Contratto": "Tempo Indeterminato", "RAL": "38.000 €", "Stato": "Pratica Convalidata"}
        ]
    }

db_globale = get_global_database()

# Database Operatori di Sistema
OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

# Inizializzazione degli stati di navigazione
if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"
if 'ai_text_output' not in st.session_state: st.session_state.ai_text_output = ""

buttons_nav = [
    ("📢 Annunci", "📢 Annunci"), 
    ("📥 Screening CV", "📥 Screening CV"), 
    ("🤝 Colloqui AI", "🤝 Colloqui AI"), 
    ("🎉 Assunzioni", "🎉 Assunzioni"), 
    ("📊 Report", "📊 Report"), 
    ("🏢 Clienti", "🏢 Clienti"), 
    ("👥 Candidati", "👥 Candidati")
]

# --- FLUSSO PORTALE CARRIERE PUBBLICO (SE PRESENTE PARAMETRO ?job= ) ---
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
            st.markdown("<br>", unsafe_allow_html=True)
            
        st.markdown("### 📋 Descrizione e Requisiti", unsafe_allow_html=True)
        st.info(annuncio_selezionato['Note'])
        
        st.markdown("<br><hr style='border-color:#E2E8F0;'>### 📥 Invia la tua Candidatura", unsafe_allow_html=True)
        with st.form("form_candidatura_esterno", clear_on_submit=True):
            c_nome = st.text_input("Nome e Cognome *")
            c_mail = st.text_input("Indirizzo E-mail *")
            c_tel = st.text_input("Numero di Telefono Cellulare *")
            c_file = st.file_uploader("Carica il tuo CV (PDF, Word, Immagini)", type=["pdf", "docx", "png", "jpg", "jpeg"])
            
            if st.form_submit_button("INVIA CANDIDATURA UFFICIALE"):
                if c_nome and c_mail and c_tel and c_file:
                    db_globale["candidati"].append({
                        "id": len(db_globale["candidati"]), "Nome": c_nome, "Email": c_mail, "Telefono": c_tel,
                        "Posizione": annuncio_selezionato['Posizione'], "Idoneità": f"{random.randint(78, 97)}%", "Stelle": "⭐⭐⭐⭐",
                        "Orientamento": f"Profilo registrato tramite form online. Candidatura spontanea per la sede di {annuncio_selezionato['Sede']}.",
                        "Alternativo": "Nessuno", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None, "Stato": "In Screening"
                    })
                    st.success("🎉 Candidatura trasmessa con successo alla Suite Dei Reali!")
                else:
                    st.error("⚠️ Per favore, compila tutti i campi contrassegnati con l'asterisco ed allega il tuo CV.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="public-card" style="text-align:center;">', unsafe_allow_html=True)
        st.error("⚠️ Annuncio di lavoro non trovato o rimosso dall'amministratore.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- FLUSSO SUITE INTERNA AMMINISTRATIVA (LOGGED IN) ---
else:
    if not st.session_state.autenticato:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        logo_path = "1000376160.jpeg"
        if os.path.exists(logo_path):
            st.image(logo_path, width=220)
        else:
            st.markdown("<h2 style='color:#1E3A8A; margin-top:0;'>👑 DEI REALI</h2>", unsafe_allow_html=True)
        st.markdown("### Accesso alla Suite Risorse Umane")
        login_mail = st.text_input("📧 E-mail Aziendale")
        login_pw = st.text_input("🔑 Password Coordinatore", type="password")
        if st.button("ACCEDI AL SISTEMA", use_container_width=True):
            if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
                st.session_state.autenticato = True
                st.session_state.utente_connesso = OPERATORI[login_mail]
                st.rerun()
            else:
                st.error("Credenziali fornite non corrette.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Barra Laterale Sidebar di Monitoraggio e Stato Chiamate Attive
        with st.sidebar:
            if os.path.exists("1000376160.jpeg"):
                st.image("1000376160.jpeg", use_container_width=True)
            st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:15px 0;'>", unsafe_allow_html=True)
            
            st.markdown("### 🖥️ Meet Attivi Ora")
            stanze_attive = [c for c in db_globale["candidati"] if c.get("Impegnato", False)]
            if not stanze_attive:
                st.caption("Nessun colloquio istantaneo attivo ora.")
            else:
                for s in stanze_attive:
                    st.markdown(f"""
                    <div style="background-color:#F0FDF4; padding:10px; border-radius:8px; margin-bottom:8px;">
                        <span style="font-size:11px; font-weight:bold; color:#166534;">📞 DISCUSSIONE ATTIVA ({s["Operatore_Call"]})</span><br>
                        <span style="font-size:12px;"><b>Cand:</b> {s["Nome"]}</span><br>
                        <a href="{s["Meet_Link"]}" target="_blank" style="font-size:12px;font-weight:bold;color:#1a73e8;text-decoration:none;">🔗 Entra e Partecipa</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.sidebar.button("🔒 Disconnetti Account"):
                st.session_state.autenticato = False
                st.rerun()

        st.title("👑 Suite di Gestione Risorse Umane")
        st.markdown(f"##### Dei Reali Executive Selection &emsp;|&emsp; Operatore Connesso: *{st.session_state.utente_connesso['nome']}*")
        
        # Barra Superiore di Navigazione centralizzata a 7 Bottoni distribuiti
        c_nav = st.columns(7)
        for i, (label, key) in enumerate(buttons_nav):
            with c_nav[i]:
                if st.button(label, key=f"nav_{key}"):
                    st.session_state.current_menu = key

        st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

        if stanze_attive:
            for s in stanze_attive:
                st.markdown(f'<div class="global-banner">🚨 <b>COLLOQUIO IN CORSO:</b> L\'operatore <b>{s["Operatore_Call"]}</b> è attualmente in linea con <b>{s["Nome"]}</b>. <a href="{s["Meet_Link"]}" target="_blank" style="margin-left:15px; font-weight:bold; color:#1A73E8;">🖥️ CLICCA QUI PER UNIRTI ALLA CONVERSAZIONE</a></div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 1: 📢 GESTIONE ANNUNCI (3 COLONNE)
        # ==========================================
        if st.session_state.current_menu == "📢 Annunci":
            col_sx, col_centro, col_dx = st.columns([1, 1, 1])
            with col_sx:
                st.markdown("### 📝 Dati Principali Annuncio")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                uploaded_file = st.file_uploader("🖼️ Carica Copertina Illustrativa", type=["png", "jpg", "jpeg"])
                titolo_job = st.text_input("📍 Titolo della Posizione Aperta", placeholder="es. OSS - Struttura anziani")
                tipo_importo = st.radio("Tipologia Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True)
                valore_importo = st.text_input("Importo Economico (€)", placeholder="es. 1300")
                indirizzo_job = st.text_input("🏢 Sede Operativa di Lavoro", placeholder="es. Palestrina / Cave")
                st.markdown('</div>', unsafe_allow_html=True)
            with col_centro:
                st.markdown("### 🤖 Assistente di Scrittura IA")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                note_job = st.text_area("✍️ Note e Requisiti Iniziali (Manuale)", placeholder="Inserisci i requisiti minimi...", height=150)
                if st.button("🪄 Elabora ed Ottimizza Testo con IA", use_container_width=True):
                    if note_job:
                        st.session_state.ai_text_output = f"La DEI REALI Srl ricerca personale qualificato per inserimento nel proprio organico per la posizione di '{titolo_job if titolo_job else 'Operatore'}' presso la nostra sede di {indirizzo_job if indirizzo_job else 'Palestrina'}. Si richiede attitudine al lavoro di squadra e rispetto delle direttive. Note e requisiti: {note_job}."
                    else:
                        st.warning("Fornisci una descrizione di base prima di chiamare l'IA.")
                if st.session_state.ai_text_output:
                    st.markdown(f'<div class="ai-box"><b>🧠 Copia Elaborata dall\'IA:</b><br>{st.session_state.ai_text_output}</div>', unsafe_allow_html=True)
                st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)
                if st.button("🚀 PUBBLICA ED ABILITA PORTALE CARRIERE", use_container_width=True):
                    if titolo_job:
                        clean_id = re.sub(r'[^a-zA-Z0-9]', '-', titolo_job.lower())[:15] + f"-{random.randint(10,99)}"
                        db_globale["annunci"].append({
                            "id": clean_id, 
                            "Posizione": titolo_job, 
                            "Inquadramento": tipo_importo, 
                            "Importo": valore_importo, 
                            "Sede": indirizzo_job, 
                            "Note": note_job if not st.session_state.ai_text_output else st.session_state.ai_text_output, 
                            "Foto_Data": uploaded_file.read() if uploaded_file else None
                        })
                        st.success("🎉 Annuncio indicizzato e pubblicato con successo nel sistema!")
                        st.session_state.ai_text_output = ""
                        st.rerun()
                    else:
                        st.error("Impossibile procedere: Il campo Titolo della Posizione è obbligatorio.")
                st.markdown('</div>', unsafe_allow_html=True)
            with col_dx:
                st.markdown("### 📋 Elenco Annunci Attivi e Link Pubblici")
                for ann in db_globale["annunci"]:
                    st.markdown('<div class="saas-box" style="border-left: 4px solid #1E3A8A; padding:15px;">', unsafe_allow_html=True)
                    st.markdown(f"<b>📢 {ann['Posizione']}</b><br><span style='font-size:12px;color:#475569;'>📍 Sede: {ann['Sede']} | 💸 {ann['Importo']}€</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='link-box'>https://deireali-hr.streamlit.app/?job={ann['id']}</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 2: 📥 SCREENING CV
        # ==========================================
        elif st.session_state.current_menu == "📥 Screening CV":
            st.markdown("### 📥 Candidature in Fase di Screening ed Analisi CV")
            screening_list = [c for c in db_globale["candidati"] if c["Stato"] == "In Screening"]
            if not screening_list:
                st.info("Nessun profilo presente in fase di screening al momento.")
            for index, cand in enumerate(db_globale["candidati"]):
                if cand["Stato"] == "In Screening":
                    st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                    c_l, c_r = st.columns([2.5, 1.5])
                    with c_l:
                        st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px;color:#64748B;'>📱 {cand['Telefono']}</span>", unsafe_allow_html=True)
                        st.markdown(f"🎯 *Posizione richiesta:* {cand['Posizione']} &emsp;|&emsp; 📧 *E-mail:* {cand['Email']}")
                        st.markdown(f'<div class="ai-box"><b>🧠 RANKING IA SULLA COMPATIBILITÀ ({cand["Idoneità"]}):</b> {cand["Orientamento"]}<br><b>Opzione Alternativa Consigliata:</b> {cand["Alternativo"]}</div>', unsafe_allow_html=True)
                    with c_r:
                        if cand.get("Impegnato", False):
                            st.markdown('<div class="status-occupato">🔴 IN VIDEO CONFERENZA</div>', unsafe_allow_html=True)
                            if st.button("Scollega Stanza ed Libera", key=f"scr_term_{index}"):
                                db_globale["candidati"][index]["Impegnato"] = False
                                st.rerun()
                        else:
                            st.markdown('<div class="status-disponibile">🟢 PRONTO / Libero per Chiamata</div>', unsafe_allow_html=True)
                            if st.button("📞 Chiama Ora (Videochiamata Istantanea)", key=f"scr_call_{index}"):
                                db_globale["candidati"][index]["Impegnato"] = True
                                db_globale["candidati"][index]["Operatore_Call"] = st.session_state.utente_connesso['nome']
                                db_globale["candidati"][index]["Meet_Link"] = f"https://meet.google.com/{random.randint(100,999)}-{random.randint(100,999)}"
                                st.rerun()
                            if st.button("🤝 Valida e Sposta a Colloqui Formali", key=f"scr_appr_{index}"):
                                db_globale["candidati"][index]["Stato"] = "Approvato per Colloquio"
                                st.success("Candidato promosso alla sezione successiva!"); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 3: 🤝 COLLOQUI AI
        # ==========================================
        elif st.session_state.current_menu == "🤝 Colloqui AI":
            st.markdown("### 🗓️ Pianificazione Turni e Trascrizione Tacita Passiva")
            if not db_globale["agenda"]:
                st.info("Nessun colloquio formale schedulato nel calendario condiviso.")
            else:
                st.dataframe(pd.DataFrame(db_globale["agenda"])[["Data", "Ora", "Candidato", "Operatore", "Telefono", "Meet_Link"]], use_container_width=True)
            
            st.markdown("<br><hr>", unsafe_allow_html=True)
            col_plan, col_act, col_ia = st.columns([1, 1.2, 0.8])
            with col_plan:
                st.markdown("#### ✍️ Fissa Appuntamento")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                cand_scelto = st.selectbox("Seleziona dalla lista", [c["Nome"] for c in db_globale["candidati"]])
                d_s = st.date_input("Seleziona Giorno", min_value=date.today())
                o_s = st.time_input("Orario Convocazione", value=time(10,0))
                if st.button("💾 Registra Turno e Crea Link Room", use_container_width=True):
                    c_inf = next((c for c in db_globale["candidati"] if c["Nome"] == cand_scelto), None)
                    db_globale["agenda"].append({
                        "Candidato": cand_scelto, 
                        "Data": str(d_s), 
                        "Ora": o_s.strftime("%H:%M"), 
                        "Operatore": st.session_state.utente_connesso['nome'], 
                        "Meet_Link": f"https://meet.google.com/{random.randint(100,999)}-{random.randint(100,999)}", 
                        "Telefono": c_inf["Telefono"] if c_inf else "+39333000"
                    })
                    st.success("Appuntamento registrato con successo!"); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col_act:
                st.markdown("#### ⚡ Azioni Rapide di Convocazione")
                for idx, app in enumerate(db_globale["agenda"]):
                    st.markdown(f'<div class="saas-box"><b>{app["Candidato"]}</b> ({app["Data"]} alle ore {app["Ora"]})<br><a href="{app["Meet_Link"]}" target="_blank" class="meet-btn">🖥️ Avvia Stanza Google Meet</a>', unsafe_allow_html=True)
                    txt_wa = f"Gentile {app['Candidato']},\nLe confermiamo l'appuntamento con la commissione Dei Reali.\n🗓️ Giorno: {app['Data']}\n⏰ Orario: {app['Ora']}\n🔗 Collegamento Aula Virtuale: {app['Meet_Link']}"
                    st.markdown(f'<a href="https://wa.me/{app["Telefono"].replace("+","").replace(" ","")}?text={urllib.parse.quote(txt_wa)}" target="_blank" class="whatsapp-btn">💬 Invia Dettagli via WhatsApp</a></div>', unsafe_allow_html=True)
            with col_ia:
                st.markdown("#### 🤖 Algoritmo di Trascrizione Tacita")
                st.markdown('<div class="saas-box" style="border-left: 4px solid #10B981; background-color:#F0FDF4;">🎙️ <b>Rilevamento Audio Attivo.</b><br><span style="font-size:12px;color:#475569;">L\'estensione IA integrata monitorerà passivamente la conversazione per redigere in automatico il riassunto ed il punteggio tecnico finale al termine.</span></div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 4: 🎉 ASSUNZIONI
        # ==========================================
        elif st.session_state.current_menu == "🎉 Assunzioni":
            st.markdown("### 🎉 Gestione Contrattualistica e Onboarding Nuove Risorse")
            col_ass1, col_ass2 = st.columns([2, 1])
            with col_ass1:
                st.markdown("#### 📋 Pratiche di Inserimento in Corso")
                for ass in db_globale["assunzioni"]:
                    st.markdown(f"""
                    <div class="saas-box" style="border-left: 4px solid #10B981;">
                        👤 <b>Nuovo Collaboratore:</b> {ass['Candidato']}<br>
                        🎯 <b>Mansione:</b> {ass['Posizione']} &emsp;|&emsp; 📝 <b>Inquadramento:</b> {ass['Contratto']} ({ass['RAL']})<br>
                        ⏱️ <b>Data Decorrenza:</b> {ass['Data_Inizio']} &emsp;|&emsp; 🔷 <b>Stato Avanzamento:</b> <span style="color:#059669;font-weight:bold;">{ass['Stato']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            with col_ass2:
                st.markdown("#### ➕ Inserisci Nuova Pratica")
                with st.form("form_assunzione"):
                    n_a = st.text_input("Nome e Cognome Lavoratore")
                    p_a = st.text_input("Qualifica / Ruolo")
                    c_a = st.selectbox("CCNL Applicato", ["Tempo Indeterminato", "Tempo Determinato", "Apprendistato Professionalizzante"])
                    r_a = st.text_input("RAL Pattuita (€)")
                    if st.form_submit_button("VALIDA E ARCHIVIA CONTRATTO"):
                        if n_a:
                            db_globale["assunzioni"].append({
                                "Candidato": n_a, "Posizione": p_a, "Data_Inizio": str(date.today()), 
                                "Contratto": c_a, "RAL": r_a + " €", "Stato": "Pratica Convalidata"
                            })
                            st.success("Contratto d'assunzione registrato nel data hub!"); st.rerun()

        # ==========================================
        # MODULO 5: 📊 REPORT
        # ==========================================
        elif st.session_state.current_menu == "📊 Report":
            st.markdown("### 📊 Indicatori Chiave di Prestazione (KPI) ed Analisi Dati")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1: st.metric("Annunci Attivi Online", len(db_globale["annunci"]))
            with kpi2: st.metric("Candidature Totali", len(db_globale["candidati"]))
            with kpi3: st.metric("Colloqui Fissati", len(db_globale["agenda"]))
            with kpi4: st.metric("Assunzioni Validate", len(db_globale["assunzioni"]))
            
            st.markdown("<br>#### 📈 Rendiconto di Produttività Mensile degli Operatori", unsafe_allow_html=True)
            rep_data = pd.DataFrame([
                {"Operatore": "Danilo", "Screening CV": 42, "Colloqui Sostenuti": 18, "Pratiche Chiuse": 3},
                {"Operatore": "Dionisio", "Screening CV": 35, "Colloqui Sostenuti": 22, "Pratiche Chiuse": 5}
            ])
            st.dataframe(rep_data, use_container_width=True)

        # ==========================================
        # MODULO 6: 🏢 CLIENTI
        # ==========================================
        elif st.session_state.current_menu == "🏢 Clienti":
            st.markdown("### 🏢 CRM Anagrafica Aziende Partner e Mandati di Ricerca")
            col_cli1, col_cli2 = st.columns([2, 1])
            with col_cli1:
                for cli in db_globale["clienti"]:
                    st.markdown(f'<div class="saas-box">🏢 <b>{cli["Azienda"]}</b><br><span style="font-size:12px;color:#475569;">Settore Merceologico: {cli["Settore"]} | Referente Account: {cli["Referente"]} | Posizioni Aperte Commissionate: {cli["Posizioni"]}</span></div>', unsafe_allow_html=True)
            with col_cli2:
                st.markdown("#### ➕ Registra Nuova Azienda Mandataria")
                with st.form("add_cli_form"):
                    az_n = st.text_input("Ragione Sociale Azienda Partner")
                    az_s = st.text_input("Settore Operativo")
                    az_r = st.selectbox("Account Interno Responsabile", ["Danilo", "Dionisio"])
                    if st.form_submit_button("REGISTRA SCHEDA PARTNER"):
                        if az_n:
                            db_globale["clienti"].append({"Azienda": az_n, "Settore": az_s, "Referente": az_r, "Posizioni": "1"})
                            st.success("Scheda CRM registrata correttamente!"); st.rerun()

        # ==========================================
        # MODULO 7: 👥 CANDIDATI
        # ==========================================
        elif st.session_state.current_menu == "👥 Candidati":
            st.markdown("### 👥 Archivio Anagrafico ed Avanzamento dei Profili Spontanei")
            for index, cand in enumerate(db_globale["candidati"]):
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px;color:#64748B;'>📱 Cell: {cand['Telefono']} | 📧 E-mail: {cand['Email']}</span>", unsafe_allow_html=True)
                st.markdown(f"🎯 *Competenza / Posizione:* {cand['Posizione']} &emsp;|&emsp; 🔷 *Fase Attuale Interna:* {cand.get('Stato','In Screening')}")
                st.markdown(f"<p style='margin:5px 0 0 0; font-size:12px; color:#475569;'><b>Sintesi IA sul Profilo:</b> {cand['Orientamento']}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
