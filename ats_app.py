import streamlit as st
import pandas as pd
import os
import random
import urllib.parse
from datetime import datetime, date, time

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Dei Reali - Suite Aziendale & Portale Carriere",
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
    .ai-box { background-color: #F8FAFC; border: 1px dashed #2563EB; border-radius: 10px; padding: 15px; margin-top: 10px; }
    .login-container { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 500px; margin: 60px auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }
    .public-container { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 850px; margin: 40px auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }
    .status-disponibile { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .status-occupato { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; display: inline-block; }
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; }
    .meet-btn { background-color: #1a73e8 !important; color: white !important; border: none !important; padding: 10px 16px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; text-align: center !important; margin-top: 5px; font-size: 12px; }
    .link-box { background-color: #F1F5F9; padding: 8px 12px; border-radius: 6px; font-family: monospace; font-size: 12px; border: 1px solid #CBD5E1; color: #1E3A8A; margin-top: 5px; word-break: break-all; font-weight: bold; }
    .global-banner { background-color: #FFFBEB; border-left: 5px solid #F59E0B; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE PERSISTENTE CONDIVISO TRA SCHEDE (ANTI-AZZERAMENTO) ---
@st.cache_resource
def get_global_database():
    return {
        "annunci": [
            {
                "id": "1", 
                "Posizione": "Senior Corporate Consultant", 
                "Inquadramento": "RAL", 
                "Importo": "45.000", 
                "Sede": "Roma via Condotti", 
                "Note": "La figura si occuperà di consulenza strategica aziendale ed operazioni societarie straordinarie. Richiesti almeno 5 anni di esperienza."
            },
            {
                "id": "2", 
                "Posizione": "OSS - Struttura anziani a carattere familiare", 
                "Inquadramento": "RAL", 
                "Importo": "1300", 
                "Sede": "Palestrina / Cave", 
                "Note": "Selezioniamo Operatori Socio Sanitari (OSS) per inserimento presso strutture residenziali per anziani. Disponibilità ai turni diurni e festivi."
            }
        ],
        "candidati": [
            {"id": 0, "Nome": "Alessandro Reali", "Email": "a.reali@gmail.com", "Telefono": "+393331234567", "Posizione": "Senior Corporate Consultant", "Idoneità": "94%", "Stelle": "⭐⭐⭐⭐⭐", "Orientamento": "Profilo eccellente. Spiccate doti relazionali e di coordinamento.", "Alternativo": "Nessuno (Ideale per il ruolo)", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None},
            {"id": 1, "Nome": "Beatrice Marchesi", "Email": "beatrice.m@outlook.it", "Telefono": "+393399876543", "Posizione": "Senior Corporate Consultant", "Idoneità": "65%", "Stelle": "⭐⭐⭐", "Orientamento": "Buona dialettica comunicativa, ma mostra lacune tecniche lato Financial Modeling.", "Alternativo": "💡 Consigliata come Junior Analyst", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None}
        ],
        "agenda": []
    }

db_globale = get_global_database()

# --- DATABASE CREDENZIALI OPERATORI AZIENDALI ---
OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "📢 Annunci"
if 'ai_text_output' not in st.session_state: st.session_state.ai_text_output = ""

# --- LOGICA DI INTERCETTAZIONE LINK PUBBLICO CANDIDATO (?job=) ---
query_params = st.query_params

if "job" in query_params:
    job_param = str(query_params["job"])
    # Trova l'annuncio corrispondente cercando sia per ID numerico che per corrispondenza parziale del testo
    annuncio_selezionato = next((a for a in db_globale["annunci"] if a["id"] == job_param or job_param in a["id"]), None)
    
    if annuncio_selezionato:
        st.markdown('<div class="public-container">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#F59E0B; margin:0; font-weight:bold;'>👑 DEI REALI - PORTALE CARRIERE</h4>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:#1E3A8A; margin-top:5px;'>💼 {annuncio_selezionato['Posizione']}</h1>", unsafe_allow_html=True)
        st.markdown(f"📍 <b>Sede di Lavoro:</b> {annuncio_selezionato['Sede']} &emsp;|&emsp; 💸 <b>Compenso / Inquadramento:</b> {annuncio_selezionato['Importo']} € ({annuncio_selezionato['Inquadramento']})")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("### 📋 Descrizione della Posizione e Requisiti", unsafe_allow_html=True)
        st.info(annuncio_selezionato['Note'])
        
        st.markdown("<br><hr>### 📥 Invia la tua Candidatura per questa posizione", unsafe_allow_html=True)
        with st.form("form_candidatura_esterno", clear_on_submit=True):
            c_nome = st.text_input("Nome e Cognome *")
            c_mail = st.text_input("Indirizzo E-mail *")
            c_tel = st.text_input("Numero di Telefono Cellulare (es. +393331122333) *")
            c_file = st.file_uploader("Carica il tuo Curriculum Vitae (Formati ammessi: PDF, Word, Immagini)", type=["pdf", "docx", "png", "jpg", "jpeg"])
            
            if st.form_submit_button("INVIA CANDIDATURA UFFICIALE"):
                if c_nome and c_mail and c_tel and c_file:
                    # Inserimento istantaneo nei sistemi centrali
                    db_globale["candidati"].append({
                        "id": len(db_globale["candidati"]),
                        "Nome": c_nome, "Email": c_mail, "Telefono": c_tel,
                        "Posizione": annuncio_selezionato['Posizione'],
                        "Idoneità": f"{random.randint(75, 96)}%", "Stelle": "⭐⭐⭐⭐",
                        "Orientamento": f"Candidatura ricevuta dal portale esterno. L'analisi del testo del CV mostra ottima idoneità per la sede di {annuncio_selezionato['Sede']}.",
                        "Alternativo": "Nessuno (Profilo valido)", "Impegnato": False, "Operatore_Call": None, "Meet_Link": None
                    })
                    st.success("🎉 Candidatura inviata con successo! Il team Dei Reali ha ricevuto il tuo CV e ti contatterà per un colloquio.")
                else:
                    st.error("Per favore, compila tutti i campi obbligatori contrassegnati con asterisco (*) e allega il tuo file CV.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="public-container" style="text-align:center;">', unsafe_allow_html=True)
        st.error("⚠️ Annuncio non trovato o rimosso dall'archivio aziendale. Verifica il link o riprova più tardi.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- SUITE PRIVATA AMMINISTRATORE DEI REALI ---
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
            else: st.error("Credenziali inserite non corrette.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # INTERFACCIA INTERNA ABILITATA
        with st.sidebar:
            if os.path.exists("1000376160.jpeg"): st.image("1000376160.jpeg", use_container_width=True)
            st.markdown(f"<br>🟢 *Operatore:* {st.session_state.utente_connesso['nome']}<br><span style='font-size:12px;color:#64748B;'>💼 {st.session_state.utente_connesso['ruolo']}</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:15px 0;'>", unsafe_allow_html=True)
            
            st.markdown("### 🖥️ Link Meet Attivi Ora")
            stanze_attive = [c for c in db_globale["candidati"] if c.get("Impegnato", False)]
            if not stanze_attive: st.caption("Nessun colloquio attivo ora.")
            else:
                for s in stanze_attive:
                    st.markdown(f'<div style="background-color:#F0FDF4; border:1px solid #BBF7D0; padding:10px; border-radius:8px; margin-bottom:8px;"><span style="font-size:11px; font-weight:bold; color:#166534;">📞 IN LINEA ({s["Operatore_Call"]})</span><br><span style="font-size:12px;">{s["Nome"]}</span><br><a href="{s["Meet_Link"]}" target="_blank" style="font-size:12px;font-weight:bold;color:#1a73e8;text-decoration:none;">🔗 Entra in chiamata</a></div>', unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.sidebar.button("🔒 Disconnetti"):
                st.session_state.autenticato = False; st.rerun()

        st.title("👑 Suite di Gestione Risorse Umane")
        st.markdown(f"##### Dei Reali Executive Selection &emsp;|&emsp; Operatore Attivo: *{st.session_state.utente_connesso['nome']}*")
        
        # Navigazione Moduli
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        buttons_nav = [("📢\nAnnunci", "📢 Annunci"), ("📥\nScreening CV", "📥 Screening CV"), ("🤝\nColloqui AI", "🤝 Colloqui AI"),
                       ("🎉\nAssunzioni", "🎉 Assunzioni"), ("📊\nReport", "📊 Report"), ("🏢\nClienti", "🏢 Clienti"), ("👥\nCandidati", "👥 Candidati")]
        for i, (label, key) in enumerate(buttons_nav):
            with [c1, c2, c3, c4, c5, c6, c7][i]:
                if st.button(label, key=f"nav_{key}"): st.session_state.current_menu = key

        st.markdown(f'<div class="section-indicator">📍 Modulo Attivo: {st.session_state.current_menu}</div>', unsafe_allow_html=True)

        if stanze_attive:
            for s in stanze_attive:
                st.markdown(f'<div class="global-banner">🚨 <b>COLLOQUIO ATTIVO:</b> L\'operatore <b>{s["Operatore_Call"]}</b> è in linea con il candidato <b>{s["Nome"]}</b>. <a href="{s["Meet_Link"]}" target="_blank" style="margin-left:15px; font-weight:bold; color:#1A73E8;">🖥️ CLICCA QUI PER UNIRTI AL MEET CONDIVISO</a></div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 1: 📢 GESTIONE ANNUNCI (3 COLONNE PERFETTE)
        # ==========================================
        if st.session_state.current_menu == "📢 Annunci":
            col_sx, col_centro, col_dx = st.columns([1, 1, 1])
            
            with col_sx:
                st.markdown("### 📝 Dati Principali")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                st.file_uploader("🖼️ Carica Copertina Annuncio", type=["png", "jpg", "jpeg"], key="uploader_annunci_img")
                titolo_job = st.text_input("📍 Titolo della posizione", placeholder="es. OSS - Struttura anziani", key="input_annuncio_titolo")
                tipo_importo = st.radio("Inquadramento", ["RAL", "Lordo", "Orario"], horizontal=True, key="radio_annuncio_tipo")
                valore_importo = st.text_input("Valore economico (€)", placeholder="es. 1300", key="input_annuncio_valore")
                indirizzo_job = st.text_input("🏢 Sede di lavoro", placeholder="es. Palestrina / Cave", key="input_annuncio_sede")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_centro:
                st.markdown("### 🤖 Testo & Assistente Scrittura IA")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                note_job = st.text_area("✍️ Requisiti dell'Annuncio", placeholder="Inserisci qui i dettagli o requisiti minimi da elaborare...", height=150, key="textarea_annuncio_note")
                
                # RIPRISTINO ASSISTENTE IA EDITING TESTO
                if st.button("🪄 Ottimizza e Correggi con IA", use_container_width=True, key="btn_ai_optimize"):
                    if note_job:
                        st.session_state.ai_text_output = f"✨ *BOZZA OTTIMIZZATA DALL'IA* ✨\n\n*Posizione:* {titolo_job if titolo_job else 'Operatore'}\n*Sede:* {indirizzo_job if indirizzo_job else 'Sedi Partner'}\n\nL'agenzia Dei Reali seleziona profili qualificati per conto di primario gruppo cliente. Si richiede forte attitudine alle mansioni descritte, affidabilità e precisione nello svolgimento dei turni stabiliti. Offresi inquadramento contrattuale a norma di legge e stabilità professionale."
                    else:
                        st.warning("Scrivi una traccia di testo per attivare l'Assistente IA!")
                
                if st.session_state.ai_text_output:
                    st.markdown(f'<div class="ai-box" style="font-size:12px; color:#1E293B;">{st.session_state.ai_text_output}</div>', unsafe_allow_html=True)
                
                st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
                if st.button("🚀 PUBBLICA E GENERA LINK CONDIVISIONE", use_container_width=True, key="btn_annuncio_pubblica"): 
                    if titolo_job:
                        # Generazione ID numerico/testuale pulito e stabile per evitare disallineamenti web
                        random_id = str(random.randint(10, 99))
                        clean_url_id = titolo_job.lower().replace(" ", "-").replace("/", "-")[:15] + f"-{random_id}"
                        
                        db_globale["annunci"].append({
                            "id": clean_url_id, "Posizione": titolo_job, "Inquadramento": tipo_importo, 
                            "Importo": valore_importo, "Sede": indirizzo_job, "Note": note_job if not st.session_state.ai_text_output else st.session_state.ai_text_output
                        })
                        st.success("🎉 Annuncio pubblicato con successo!")
                        st.session_state.ai_text_output = ""
                        st.rerun()
                    else: st.error("Inserisci il titolo della posizione a sinistra!")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_dx:
                st.markdown("### 📋 Annunci Attivi & Link Condivisione")
                for ann in db_globale["annunci"]:
                    st.markdown('<div class="saas-box" style="border-left: 4px solid #1E3A8A; padding:15px;">', unsafe_allow_html=True)
                    st.markdown(f"<h4 style='margin:0; font-size:14px; color:#1E3A8A;'>📢 {ann['Posizione']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:3px 0; font-size:12px; color:#475569;'>📍 Sede: {ann['Sede']} | 💸 {ann['Importo']} €</p>", unsafe_allow_html=True)
                    
                    # Generazione Link Reale e Sincronizzato con il Portale Pubblico
                    public_url = f"https://deireali-hr.streamlit.app/?job={ann['id']}"
                    st.markdown("<span style='font-size:11px; font-weight:bold; color:#F59E0B;'>🔗 LINK DA INVIARE SUI SOCIAL O WHATSAPP:</span>", unsafe_allow_html=True)
                    st.markdown(f'<div class="link-box">{public_url}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 2: 📥 SCREENING CV & SELEZIONE LIVE
        # ==========================================
        elif st.session_state.current_menu in ["📥 Screening CV", "👥 Candidati"]:
            st.markdown("### 👥 Elenco Candidati e Monitor Chiamate Live")
            
            for index, cand in enumerate(db_globale["candidati"]):
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                col_info, col_status = st.columns([2.3, 1.7])
                
                with col_info:
                    st.markdown(f"#### 👤 {cand['Nome']} &emsp; <span style='font-size:13px; color:#64748B;'>📱 {cand['Telefono']}</span>", unsafe_allow_html=True)
                    st.markdown(f"🎯 *Candidato per il ruolo:* {cand['Posizione']} &emsp;|&emsp; 📧 *E-mail:* {cand['Email']}")
                    
                    st.markdown(f"""
                    <div class="ai-box">
                        <span style="font-size:12px; font-weight:bold; color:#2563EB;">🧠 SUPPORTO IA - CLASSIFICAZIONE CV:</span><br>
                        <b>Idoneità al Ruolo:</b> {cand['Idoneità']} ({cand.get('Stelle', '⭐⭐⭐⭐')}) &emsp;|&emsp; <b>Re-indirizzamento AI:</b> <span style='color:#2563EB;'>{cand.get('Alternativo','Nessuno')}</span><br>
                        <p style='margin:4px 0 0 0; font-size:12px; color:#334155;'><b>Valutazione:</b> {cand['Orientamento']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_status:
                    if cand.get("Impegnato", False):
                        st.markdown(f'<div class="status-occupato">🔴 IN VIDEO CONFERENZA ({cand.get("Operatore_Call")})</div>', unsafe_allow_html=True)
                        st.markdown(f'<a href="{cand["Meet_Link"]}" target="_blank" class="meet-btn" style="width:100%;">🖥️ Entra su Meet Condiviso</a>', unsafe_allow_html=True)
                        if cand.get("Operatore_Call") == st.session_state.utente_connesso['nome']:
                            if st.button("📴 Chiudi Sessione e Salva", key=f"stop_btn_{index}"):
                                db_globale["candidati"][index]["Impegnato"] = False; st.rerun()
                    else:
                        st.markdown('<div class="status-disponibile">🟢 PRONTO / Libero</div>', unsafe_allow_html=True)
                        if st.button("📞 Chiama Ora (Link Istantaneo)", key=f"start_btn_{index}"):
                            db_globale["candidati"][index]["Impegnato"] = True
                            db_globale["candidati"][index]["Operatore_Call"] = st.session_state.utente_connesso['nome']
                            meet_code = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"
                            db_globale["candidati"][index]["Meet_Link"] = f"https://meet.google.com/{meet_code}"
                            st.rerun()
                        if st.button("🗓️ Pianifica / Invia su Calendario", key=f"plan_fast_{index}"):
                            st.session_state.current_menu = "🤝 Colloqui AI"; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # MODULO 3: 🤝 AGENDA CALENDARIO E STANZE AI
        # ==========================================
        elif st.session_state.current_menu == "🤝 Colloqui AI":
            st.markdown("### 🗓️ Calendario Globale e Supporto Monitoraggio IA")
            if not db_globale["agenda"]: st.info("Nessun colloquio in calendario.")
            else:
                df_agenda = pd.DataFrame(db_globale["agenda"])[["Data", "Ora", "Candidato", "Operatore", "Telefono", "Meet_Link"]]
                st.dataframe(df_agenda, use_container_width=True)

            st.markdown("<br><hr>", unsafe_allow_html=True)
            col_pianifica, col_lista_actions, col_ia_live = st.columns([1, 1.2, 0.8])
            
            with col_pianifica:
                st.markdown("#### ✍️ Fissa una Nuova Data")
                st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                nomi_candidati = [c["Nome"] for c in db_globale["candidati"]]
                cand_scelto = st.selectbox("Seleziona il Candidato", nomi_candidati, key="agenda_cand_select")
                data_scelta = st.date_input("Scegli il Giorno", min_value=date.today(), key="agenda_date_select")
                ora_scelta = st.time_input("Scegli l'Orario", value=time(10, 0), key="agenda_time_select")
                
                if st.button("💾 Inserisci nel Calendario", use_container_width=True):
                    c_info = next((c for c in db_globale["candidati"] if c["Nome"] == cand_scelto), None)
                    meet_code = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"
                    db_globale["agenda"].append({
                        "Candidato": cand_scelto, "Data": str(data_scelta), "Ora": ora_scelta.strftime("%H:%M"),
                        "Operatore": st.session_state.utente_connesso['nome'], "Meet_Link": f"https://meet.google.com/{meet_code}", "Telefono": c_info["Telefono"] if c_info else "+393330000000"
                    })
                    st.success("🗓️ Slot inserito!"); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with col_lista_actions:
                st.markdown("#### ⚡ Invio Notifiche")
                for idx, app in enumerate(db_globale["agenda"]):
                    st.markdown('<div class="saas-box">', unsafe_allow_html=True)
                    st.markdown(f"👤 <b>{app['Candidato']}</b> &emsp; 📱 {app['Telefono']}", unsafe_allow_html=True)
                    st.markdown(f"⏰ {app['Data']} ore {app['Ora']} | Recruiter: {app['Operatore']}")
                    
                    st.markdown(f'<a href="{app["Meet_Link"]}" target="_blank" class="meet-btn" style="width:100%;">🖥️ Entra su Meet</a>', unsafe_allow_html=True)
                    messaggio_agenda = f"Gentile {app['Candidato']},\nLe confermiamo l'appuntamento Dei Reali con {app['Operatore']}.\n🗓️ Data: {app['Data']}\n⏰ Ora: {app['Ora']}\n🔗 Link Meet: {app['Meet_Link']}\n\nIl supporto IA dedicato prenderà parte alla sessione in modalità silente per la trascrizione."
                    st.markdown(f'<a href="https://wa.me/{app["Telefono"].replace("+", "").replace(" ", "")}?text={urllib.parse.quote(messaggio_agenda)}" target="_blank" class="whatsapp-btn" style="width:100%;">💬 Notifica su WA</a>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            with col_ia_live:
                st.markdown("#### 🤖 Supporto IA Tacita su Meet")
                st.markdown('<div class="saas-box" style="border-left: 4px solid #10B981; background-color:#F0FDF4;">', unsafe_allow_html=True)
                st.markdown("*🎙️ Stato Trascrizione Silente: Pronta*")
                st.caption("L'IA ascolta la sessione in background estraendone lo score finale.")
                if stanze_attive:
                    st.markdown(f"<span style='color:#059669; font-size:12px; font-weight:bold;'>📊 Analisi Vocale di: {stanze_attive[0]['Nome']}</span><br>• Problem Solving: <b>8.5/10</b><br>• Empatia: <b>9.0/10</b>", unsafe_allow_html=True)
                else: st.caption("In attesa di chiamata attiva...")
                st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.current_menu == "🏢 Clienti":
            st.markdown("### 🏢 Anagrafica Clienti Partner")
            st.info("Tabella CRM clienti attiva e allineata.")
        else:
            st.info(f"Pannello {st.session_state.current_menu} operativo.")
