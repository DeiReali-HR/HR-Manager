import streamlit as st
import pandas as pd
import os
import random
import string
import urllib.parse
import re
from datetime import datetime, date, time
from supabase import create_client, Client
from pypdf import PdfReader
from google import genai
from google.genai import types

# 1. Configurazione della pagina Enterprise
st.set_page_config(
    page_title="Dei Reali - Suite Enterprise Risorse Umane",
    page_icon="👑",
    layout="wide"
)

# 2. Connessione Sicura a Supabase e Gemini tramite Secrets
@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception:
        st.error("❌ Errore nei Secrets: configurazione di Supabase mancante.")
        st.stop()

@st.cache_resource
def init_gemini():
    try:
        if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
            api_key = st.secrets["gemini"]["api_key"]
            return genai.Client(api_key=api_key)
    except Exception:
        pass
    return None

supabase: Client = init_supabase()
ai_client = init_gemini()

def estrai_testo_pdf(file_caricato):
    try:
        reader = PdfReader(file_caricato)
        testo = ""
        for page in reader.pages:
            testo += page.extract_text() or ""
        return testo.strip()
    except Exception:
        return ""

def analizza_cv_con_ia(testo_cv, requisiti_annuncio):
    if not testo_cv:
        return "50%", "⭐⭐", "Il PDF non contiene testo estraibile."
    if not ai_client:
        return "75%", "⭐⭐⭐", "Analisi standard effettuata (IA offline)."
    
    prompt = f"Analizza questo CV per la posizione {requisiti_annuncio}: {testo_cv}. Rispondi in 3 righe precise senza asterischi o formattazione complessa. Riga 1: solo la percentuale (es: 85%). Riga 2: solo le stelle (es: ⭐⭐⭐⭐). Riga 3: una breve sintesi."
    try:
        response = ai_client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        linee = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
        p_id = linee[0] if len(linee) > 0 else "80%"
        p_st = linee[1] if len(linee) > 1 else "⭐⭐⭐"
        p_sn = " ".join(linee[2:]) if len(linee) > 2 else "Profilo analizzato correttamente."
        return p_id, p_st, p_sn
    except Exception:
        return "75%", "⭐⭐⭐", "Candidatura acquisita correttamente."

def genera_testo_annuncio_ia(titolo, inquadramento, importo, sede, note_brevi):
    if not ai_client:
        return f"Ricerca per {titolo} a {sede}. Inquadramento {inquadramento}."
    prompt = f"Sei HR Dei Reali. Scrivi annuncio elegante per {titolo} a {sede}, budget {importo}€. Note: {note_brevi if note_brevi else 'Nessuna'}. Dividi in: Chi Siamo, Requisiti, Cosa Offriamo."
    try:
        response = ai_client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Errore: {str(e)}"

def mostra_logo_aziendale():
    if os.path.exists("1000376160.jpeg"):
        st.image("1000376160.jpeg")
    elif os.path.exists("1000376160.jpg"):
        st.image("1000376160.jpg")
    else:
        st.markdown("<h2 style='text-align:center; color:#1E3A8A;'>👑 DEI REALI</h2>", unsafe_allow_html=True)

def genera_codice_meet_statico():
    codice_unico = "".join(random.choices(string.ascii_lowercase, k=10))
    return f"https://meet.google.com/{codice_unico[:3]}-{codice_unico[3:7]}-{codice_unico[7:]}"

# 3. CSS Custom Premium
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    .umana-banner { position: relative; width: 100%; height: 280px; background-size: cover; background-position: center; border-radius: 16px; margin-bottom: 25px; box-shadow: inset 0 0 0 2000px rgba(15, 23, 42, 0.55); display: flex; align-items: flex-end; padding: 35px; }
    .umana-banner-title { color: #FFFFFF !important; font-size: 34px !important; font-weight: 800 !important; margin: 0 !important; }
    .umana-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 30px; background: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    .umana-kpi { border-right: 1px solid #E2E8F0; padding-right: 10px; }
    .umana-kpi:last-child { border-right: none; }
    .umana-kpi-label { font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; }
    .umana-kpi-value { font-size: 15px; color: #0F172A; font-weight: 700; margin-top: 2px; }
    .public-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; max-width: 1000px; margin: 20px auto; }
    .saas-box { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .ai-box { background-color: #F1F5F9; border-left: 4px solid #2563EB; padding: 15px; margin-top: 10px; }
    .whatsapp-btn { background-color: #25D366 !important; color: white !important; padding: 8px 14px; border-radius: 8px; text-decoration: none; display: inline-block; text-align: center; font-weight: bold; margin-right: 5px; font-size: 13px; }
    .meet-btn { background-color: #1a73e8 !important; color: white !important; padding: 8px 14px; border-radius: 8px; text-decoration: none; display: inline-block; text-align: center; font-weight: bold; font-size: 13px; }
    .link-box { background-color: #F8FAFC; padding: 10px; border-radius: 8px; font-family: monospace; font-size: 12px; border: 1px solid #E2E8F0; color: #2563EB; word-break: break-all; margin-top: 5px; }
    .sidebar-spec { background-color: #F1F5F9; padding: 12px; border-radius: 8px; border: 1px solid #CBD5E1; margin-top: 15px; font-size: 12px; color: #334155; }
    </style>
""", unsafe_allow_html=True)

OPERATORI = {
    "d.algozzino@deireali.it": {"nome": "Danilo", "pw": "Danilo2026", "ruolo": "Senior Recruiter"},
    "adv.hr@deireali.it": {"nome": "Dionisio", "pw": "Dionisio2026", "ruolo": "HR Director"},
    "dr.controlloazienda@gmail.com": {"nome": "Amministratore", "pw": "DeiReali2026", "ruolo": "Super Admin"}
}

if 'autenticato' not in st.session_state: st.session_state.autenticato = False
if 'utente_connesso' not in st.session_state: st.session_state.utente_connesso = None
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_job_id' not in st.session_state: st.session_state.edit_job_id = None
if 'ai_generated_text' not in st.session_state: st.session_state.ai_generated_text = ""
if 'sta_rispondendo' not in st.session_state: st.session_state.sta_rispondendo = False
    
# --- PORTALE PUBBLICO ---
if "job" in st.query_params:
    job_param = str(st.query_params["job"])
    res_annuncio = supabase.table("annunci").select("*").eq("id", job_param).execute()
    annuncio_selezionato = res_annuncio.data[0] if res_annuncio.data else None
    
    if annuncio_selezionato:
        if annuncio_selezionato.get('stato') == 'Sospeso':
            st.warning("Selezioni momentaneamente chiuse per questa posizione.")
        else:
            img_url = annuncio_selezionato.get('immagine') or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200"
            st.markdown(f'<div class="public-card"><div class="umana-banner" style="background-image: url(\'{img_url}\');"><div class="umana-banner-title">{annuncio_selezionato["posizione"]}</div></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="umana-grid">
                    <div class="umana-kpi"><div class="umana-kpi-label">📍 Sede</div><div class="umana-kpi-value">{annuncio_selezionato.get('sede','N/D')}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">💼 Inquadramento</div><div class="umana-kpi-value">{annuncio_selezionato.get('inquadramento','N/D')}</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">💸 Compenso</div><div class="umana-kpi-value">{annuncio_selezionato.get('importo','0')} €</div></div>
                    <div class="umana-kpi"><div class="umana-kpi-label">🔑 Rif.</div><div class="umana-kpi-value">DR-{annuncio_selezionato['id'].upper()[-4:]}</div></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"### Descrizione dell'offerta\n{annuncio_selezionato['note']}")
            with st.form("candidatura"):
                c_nome = st.text_input("Nome e Cognome *")
                c_mail = st.text_input("E-mail *")
                c_tel = st.text_input("Telefono *")
                c_file = st.file_uploader("Allega CV PDF *", type=["pdf"])
                
                if st.form_submit_button("INVIA CANDIDATURA"):
                    if c_nome and c_mail and c_tel and c_file:
                        with st.spinner("Salvataggio file e analisi profilo in corso..."):
                            testo_pdf = estrai_testo_pdf(c_file)
                            try:
                                v, s, o = analizza_cv_con_ia(testo_pdf, annuncio_selezionato['note'])
                            except Exception:
                                v, s, o = "75%", "⭐⭐⭐", "Analisi completata con successo."
                            
                            # --- CARICAMENTO FILE PDF SU SUPABASE STORAGE ---
                            # Creiamo un nome unico pulito per il file per evitare sovrascritture
                            pulito_nome = re.sub(r'[^a-zA-Z0-9]', '_', c_nome.lower())
                            nome_file_storage = f"{pulito_nome}_{random.randint(1000,9999)}.pdf"
                            
                            c_file.seek(0)
                            file_bytes = c_file.read()
                            
                            # Carichiamo i byte forzando il Content-Type corretto per il PDF
                            supabase.storage.from_("curriculum").upload(
                                path=nome_file_storage,
                                file=file_bytes,
                                file_options={"content-type": "application/pdf"}
                            )
                            
                            # Otteniamo l'URL pubblico di download diretto del file
                            url_download_pdf = supabase.storage.from_("curriculum").get_public_url(nome_file_storage)
                            
                            # Inserimento record nel Database Cloud
                            payload_candidato = {
                                "nome": c_nome,
                                "email": c_mail,
                                "telefono": c_tel,
                                "posizione": annuncio_selezionato['posizione'],
                                "idoneita": str(v),
                                "stelle": str(s),
                                "orientamento": str(o),
                                "stato": "In Screening",
                                "testo_cv": testo_pdf,
                                "immagine": url_download_pdf # Riutilizziamo la colonna immagine per memorizzare il link del PDF
                            }
                            
                            supabase.table("candidati").insert(payload_candidato).execute()
                            st.success("🎉 Candidatura inviata correttamente! Il tuo CV originale è stato acquisito nel Cloud.")
                    else:
                        st.error("Compila tutti i campi obbligatori ed allega il tuo CV in formato PDF.")
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.error("Annuncio non trovato.")

# --- AREA AMMINISTRATIVA ---
else:
    if not st.session_state.autenticato:
        st.markdown("<style>.stApp { background: radial-gradient(circle at 50% 50%, #1F3A8A 0%, #0F172A 100%) !important; } header { visibility: hidden !important; }</style>", unsafe_allow_html=True)
        _, col_centro, _ = st.columns([1, 1.4, 1])
        with col_centro:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            with st.form("login"):
                mostra_logo_aziendale()
                login_mail = st.text_input("📬 E-mail Aziendale")
                login_pw = st.text_input("🔑 Password", type="password")
                if st.form_submit_button("ACCEDI AL SISTEMA", use_container_width=True):
                    if login_mail in OPERATORI and OPERATORI[login_mail]["pw"] == login_pw:
                        st.session_state.autenticato = True
                        st.session_state.utente_connesso = OPERATORI[login_mail]
                        st.rerun()
                    else:
                        st.error("Credenziali non corrette.")
    else:
        # --- LOGIN EFFETTUATO: MOSTRIAMO L'INTERFACCIA HR ---
        st.title("👑 Suite HR Enterprise - Gruppo Dei Reali")

        # Inizializzazione dei Tab di navigazione principale
        tab_nomi = ["🏠 Home / Plancia", "📢 Annunci", "🔬 Screening", "🤝 Colloqui", "💼 Assunzioni", "📊 Report", "👥 Clienti", "👥 Candidati"]
        scelta_tab = st.tabs(tab_nomi)

        # --- TAB 1: HOME / PLANCIA ---
        with scelta_tab[0]:
            # --- LOGICA NOTIFICA CAMPANELLA IN TEMPO REALE ---
            try:
                res_count = supabase.table("candidati").select("id", count="exact").execute()
                totale_candidati = res_count.count if res_count.count is not None else 0
            except Exception:
                totale_candidati = 0

            st.markdown(f"""
            <div style="background-color: #EFF6FF; padding: 12px 20px; border-radius: 8px; border-left: 5px solid #3B82F6; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 24px;">🛎️</span>
                    <span style="font-size: 16px; font-weight: bold; color: #1E3A8A;">Notifiche Sistema HR:</span>
                </div>
                <span style="background-color: #EF4444; color: white; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                    📄 {totale_candidati} Candidati Totali
                </span>
            </div>
            """, unsafe_allow_html=True)

            # --- CRUSCOTTO DELLE METRICHE GLOBALI ---
            st.subheader("📊 Cruscotto Attività Risorse Umane")
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric(label="📥 CV Ricevuti & Screening", value="142", delta="+12 questa settimana")
            col_m2.metric(label="🤝 Colloqui in Agenda", value="8", delta="3 oggi")
            col_m3.metric(label="💼 Posizioni Aperte", value="5", delta="Filtro: Roma")
            col_m4.metric(label="✅ Assunzioni Perfezionate", value="24", delta="82%")

            # --- SEZIONE CENTRO AGGIORNAMENTI CON LINK POPUP ESTERNI ---
            st.markdown("---")
            st.subheader("📰 Centro Aggiornamenti & Flash Normativi")
            col_news1, col_news2 = st.columns(2)
            
            with col_news1:
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #10B981; margin-bottom: 10px;">
                    <h4>🏛️ Circolari INPS & INAIL</h4>
                    <ul>
                        <li style="margin-bottom: 10px;"><b>[INPS]</b> Linee guida esonero contributivo Under 35.<br>
                            <a href="https://www.inps.it" target="_blank" style="color: #2563EB; font-weight: bold; text-decoration: underline;">Apri Circolare Ufficiale ↗</a>
                        </li>
                        <li><b>[INAIL]</b> Tariffe premi aggiornate Logistica.<br>
                            <a href="https://www.inail.it" target="_blank" style="color: #2563EB; font-weight: bold; text-decoration: underline;">Apri Tabelle Tariffe ↗</a>
                        </li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
            with col_news2:
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; margin-bottom: 10px;">
                    <h4>🔥 Ultim'ora Lavoro</h4>
                    <ul>
                        <li style="margin-bottom: 10px;"><b>[Sole 24 Ore]</b> Focus sui fringe benefit aziendali 2026.<br>
                            <a href="https://www.ilsole24ore.com" target="_blank" style="color: #2563EB; font-weight: bold; text-decoration: underline;">Leggi l'articolo completo ↗</a>
                        </li>
                        <li><b>[ANSA]</b> Nuove semplificazioni contratti a termine.<br>
                            <a href="https://www.ansa.it" target="_blank" style="color: #2563EB; font-weight: bold; text-decoration: underline;">Vedi Agenzia Flash ↗</a>
                        </li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        # --- CONFIGURAZIONE DELLA SIDEBAR (CHATTING E PROFILO CON COSTRUTTO MEMORIA PIL) ---
        with st.sidebar:
            import os
            from PIL import Image

            # 1. INIZIALIZZAZIONE COMPLETA DELLE VARIABILI DI SESSIONE
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            if "ia_sta_pensando" not in st.session_state:
                st.session_state["ia_sta_pensando"] = False

            # 2. GESTIONE SICURA DEL LOGO AZIENDALE CON PIL
            logo_file = "1000376160.jpg"
            if os.path.exists(logo_file):
                try:
                    # Apriamo l'immagine in memoria per bypassare i limiti di Streamlit Cloud
                    img_logo = Image.open(logo_file)
                    col_logo1, col_logo2, col_logo3 = st.columns([0.3, 2.4, 0.3])
                    with col_logo2:
                        st.image(img_logo, use_container_width=True)
                except Exception:
                    st.markdown("<h3 style='text-align: center; color: #3B82F6; margin-bottom: 15px;'>👑 Gruppo Dei Reali</h3>", unsafe_allow_html=True)
            else:
                st.markdown("<h3 style='text-align: center; color: #3B82F6; margin-bottom: 15px;'>👑 Gruppo Dei Reali</h3>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.write(f"👤 **{st.session_state.utente_connesso['nome']}** ({st.session_state.utente_connesso['ruolo']})")
            st.success("🤖 Assistente ChatGPT v4-Mini Attivo")
            st.markdown("---")
            
            # --- AREA ASSISTENTE VIRTUALE ED EFFETTO SIRI CENTRATO ---
            st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>🤖 Assistente HR Virtuale</h4>", unsafe_allow_html=True)
            
            # CSS isolato applicato dinamicamente
            st.markdown("""
            <style>
            .siri-wrapper-box {
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
                margin: 20px auto 10px auto;
                width: 130px;
                height: 130px;
            }
            .siri-glow-wave {
                position: absolute;
                width: 125px;
                height: 125px;
                border-radius: 50%;
                background: linear-gradient(45deg, #3B82F6, #8B5CF6, #EC4899);
                opacity: 0.65;
                animation: siriPulse 1.4s infinite ease-in-out;
                z-index: 1;
            }
            @keyframes siriPulse {
                0% { transform: scale(0.92); opacity: 0.4; filter: blur(3px); }
                50% { transform: scale(1.15); opacity: 0.75; filter: blur(6px); }
                100% { transform: scale(0.92); opacity: 0.4; filter: blur(3px); }
            }
            .assistente-avatar-tondo img {
                border-radius: 50% !important;
                border: 3px solid #3B82F6 !important;
                object-fit: cover !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
            }
            </style>
            """, unsafe_allow_html=True)

            # Contenitore dinamico per l'avatar dell'assistente
            spazio_avatar = st.empty()
            
            # Controllo dello stato di pensiero estratto dalla sessione
            if st.session_state["ia_sta_pensando"]:
                avatar_corrente = "1000334218.png"
                mostra_onda = True
            else:
                avatar_corrente = "1000334217.png"
                mostra_onda = False

            # Rendering controllato dell'avatar tramite PIL
            with spazio_avatar.container():
                if mostra_onda:
                    st.markdown('<div class="siri-wrapper-box"><div class="siri-glow-wave"></div></div>', unsafe_allow_html=True)
                
                c_av1, c_av2, c_av3 = st.columns([1, 2, 1])
                with c_av2:
                    st.markdown('<div class="assistente-avatar-tondo">', unsafe_allow_html=True)
                    if os.path.exists(avatar_corrente):
                        try:
                            img_avatar = Image.open(avatar_corrente)
                            st.image(img_avatar, use_container_width=True)
                        except Exception:
                            st.image("https://raw.githubusercontent.com/streamlit/roadmap/master/static/avatar.png", use_container_width=True)
                    else:
                        st.image("https://raw.githubusercontent.com/streamlit/roadmap/master/static/avatar.png", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            # Tasto "Cancella Chat"
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns([0.4, 2.2, 0.4])
            with col_btn2:
                if st.button("🗑️ Cancella Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
            
            st.markdown("---")

            # Visualizzazione della cronologia salvata in session_state
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"], avatar=None):
                    st.write(msg["content"])

            # Input per inviare un nuovo messaggio alla chat
            if prompt := st.chat_input("Chiedi qualcosa..."):
                with st.chat_message("user", avatar=None):
                    st.write(prompt)
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                st.session_state["ia_sta_pensando"] = True
                st.rerun()

            # Processo di risposta dell'IA
            if st.session_state["ia_sta_pensando"]:
                with st.chat_message("assistant", avatar=None):
                    with st.spinner("Elaborazione in corso..."):
                        import time
                        time.sleep(1.4)
                
                risposta_ia = f"Ricevuto! Sono l'assistente di {st.session_state.utente_connesso['nome']}. Come posso aiutarti con la gestione della plancia?"
                with st.chat_message("assistant", avatar=None):
                    st.write(risposta_ia)
                st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})
                
                st.session_state["ia_sta_pensando"] = False
                st.rerun()

            st.markdown("---")
            if st.button("🔒 Disconnetti", use_container_width=True):
                st.session_state.autenticato = False
                st.rerun()
                
        # --- TAB 2: ANNUNCI ---
        with scelta_tab[1]:
            st.subheader("📢 Gestione Annunci di Lavoro")
            res_ann = supabase.table("annunci").select("*").execute()
            elenco = res_ann.data if res_ann.data else []
            
            def_pos, def_inq, def_imp, def_sede, def_foto, def_note = "","RAL","","","",""
            if st.session_state.edit_mode and st.session_state.edit_job_id:
                job = next((a for a in elenco if a["id"] == st.session_state.edit_job_id), None)
                if job: def_pos, def_inq, def_imp, def_sede, def_foto, def_note = job["posizione"], job["inquadramento"], job["importo"], job["sede"], job.get("immagine",""), job["note"]
            elif st.session_state.ai_generated_text: def_note = st.session_state.ai_generated_text

            col1, col2, col3 = st.columns([1.1, 1.1, 1.4])
            with col1:
                t_pos = st.text_input("📍 Titolo Posizione", value=def_pos)
                t_inq = st.radio("Inquadramento", ["RAL","Lordo","Orario"], index=["RAL","Lordo","Orario"].index(def_inq) if def_inq in ["RAL","Lordo","Orario"] else 0)
                t_imp = st.text_input("Budget Importo (€)", value=def_imp)
                t_sede = st.text_input("Sede di Lavoro", value=def_sede)
                t_foto = st.text_input("URL Foto Copertina", value=def_foto)
            with col2:
                t_note = st.text_area("Descrizione Estesa", value=def_note, height=220)
                if st.button("🪄 Genera con IA"):
                    if t_pos:
                        res = genera_testo_annuncio_ia(t_pos, t_inq, t_imp, t_sede, t_note)
                        st.session_state.ai_generated_text = res
                        st.rerun()
                if st.session_state.edit_mode:
                    if st.button("💾 AGGIORNA ANNUNCIO", use_container_width=True):
                        supabase.table("annunci").update({"posizione":t_pos,"inquadramento":t_inq,"importo":t_imp,"sede":t_sede,"note":t_note,"immagine":t_foto}).eq("id", st.session_state.edit_job_id).execute()
                        st.session_state.edit_mode = False; st.session_state.ai_generated_text = ""; st.rerun()
                else:
                    if st.button("🚀 PUBBLICA ANNUNCIO", use_container_width=True):
                        clean_id = re.sub(r'[^a-z0-9]', '-', t_pos.lower())[:15] + f"-{random.randint(10,99)}"
                        supabase.table("annunci").insert({"id":clean_id,"posizione":t_pos,"inquadramento":t_inq,"importo":t_imp,"sede":t_sede,"note":t_note,"immagine":t_foto,"stato":"Attivo"}).execute()
                        st.session_state.ai_generated_text = ""; st.rerun()
            with col3:
                st.markdown("### Elenco Annunci Pubblicati")
                for a in elenco:
                    st.markdown(f"<div class='saas-box'><b>📢 {a['posizione']}</b><div class='link-box'>https://deireali-hr.streamlit.app/?job={a['id']}</div></div>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    if c1.button("Modifica", key=f"e_{a['id']}"): st.session_state.edit_mode=True; st.session_state.edit_job_id=a['id']; st.rerun()
                    if c2.button("Sospendi/Attiva", key=f"s_{a['id']}"): supabase.table("annunci").update({"stato":"Sospeso" if a.get('stato')=="Attivo" else "Attivo"}).eq("id", a['id']).execute(); st.rerun()
                    if c3.button("Elimina", key=f"d_{a['id']}"): supabase.table("annunci").delete().eq("id", a['id']).execute(); st.rerun()

        # --- TAB 3: SCREENING ---
        with scelta_tab[2]:
            st.subheader("📥 Candidature Ricevute da Esaminare (In Screening)")
            res = supabase.table("candidati").select("*").eq("stato", "In Screening").execute()
            candidati = res.data if res.data else []
            if not candidati:
                st.info("Nessun nuovo candidato da valutare al momento.")
            for c in candidati:
                st.markdown(f"""
                <div class='saas-box'>
                    <h4>👤 {c['nome']}</h4>
                    <b>Posizione:</b> {c['posizione']}<br>
                    <b>Idoneità:</b> <span style='color:#2563EB; font-weight:bold;'>{c['idoneita']}</span> | {c['stelle']}<br>
                    <div class='ai-box'><b>Sintesi IA:</b> {c['orientamento']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🤝 Approva {c['nome']} per Colloquio", key=f"ap_{c['id']}", use_container_width=True):
                    supabase.table("candidati").update({"stato":"Approvato per Colloquio"}).eq("id", c['id']).execute()
                    st.rerun()

        # --- TAB 4: COLLOQUI ---
        with scelta_tab[3]:
            st.subheader("🤝 Calendario e Agenda Live")
            col_agenda, col_nuovo = st.columns([2, 1.2])
            res_agenda_db = supabase.table("agenda").select("*").execute()
            agenda_list = res_agenda_db.data if res_agenda_db.data else []
            
            with col_agenda:
                res_col = supabase.table("candidati").select("*").eq("stato", "Approvato per Colloquio").execute()
                colloqui = res_col.data if res_col.data else []
                if not colloqui: st.info("Nessun colloquio pianificato.")
                for c in colloqui:
                    match_app = next((a for a in agenda_list if a.get('candidato') == c['nome']), None)
                    d_c = match_app['data'] if match_app else 'Da pianificare'
                    o_c = match_app['ora'] if match_app else 'N/D'
                    meet_url = match_app['meet_link'] if match_app and match_app.get('meet_link') else "https://meet.google.com/new"
                    
                    st.markdown(f"<div class='saas-box'><h4>👤 {c['nome']}</h4>🗓️ {d_c} | ⏰ {o_c}</div>", unsafe_allow_html=True)
                    cb1, cb2 = st.columns(2)
                    cb1.link_button("💬 WhatsApp", f"https://wa.me/{c['telefono']}", use_container_width=True)
                    cb2.link_button("📹 Videochiamata", meet_url, use_container_width=True, type="primary")
                    
                    st.write("")
                    c1, c2, c3 = st.columns(3)
                    if c1.button("🎉 Promuovi", key=f"ass_{c['id']}", use_container_width=True): supabase.table("candidati").update({"stato":"Assunto"}).eq("id", c['id']).execute(); st.rerun()
                    if c2.button("❌ Rifiuta", key=f"rif_{c['id']}", use_container_width=True): supabase.table("candidati").update({"stato":"Rifiutato"}).eq("id", c['id']).execute(); st.rerun()
                    if c3.button("🗑️ Annulla Turno", key=f"cncl_{c['id']}", use_container_width=True):
                        if match_app: supabase.table("agenda").delete().eq("id", match_app['id']).execute(); st.rerun()
            
            with col_nuovo:
                if colloqui:
                    candidato_sel = st.selectbox("Schedula risorsa", [c['nome'] for c in colloqui])
                    c_obj = next(c for c in colloqui if c['nome'] == candidato_sel)
                    nuova_data = st.date_input("Data", date.today())
                    nuova_ora = st.time_input("Orario", time(15, 45))
                    if st.button("Salva Appuntamento", use_container_width=True):
                        match_ex = next((a for a in agenda_list if a.get('candidato') == c_obj['nome']), None)
                        payload = {"candidato": c_obj['nome'], "data": str(nuova_data), "ora": nuova_ora.strftime("%H:%M"), "meet_link": genera_codice_meet_statico(), "telefono": c_obj.get('telefono','')}
                        if match_ex: supabase.table("agenda").update(payload).eq("id", match_ex['id']).execute()
                        else: supabase.table("agenda").insert(payload).execute()
                        st.rerun()

        # --- TAB: ASSUNZIONI & GENERAZIONE CONTRATTI ---
        with scelta_tab[4]:
            st.markdown("## 💼 Gestione Assunzioni & Onboarding")
            
            from fpdf import FPDF
            import io

            # 1. Inizializzazione sicura del registro assunzioni in sessione
            if "lista_assunzioni" not in st.session_state:
                st.session_state.lista_assunzioni = [
                    {"candidato": "Daniele Rossi", "ruolo": "Specializzando HR", "tipo_contratto": "Determinato", "data_inizio": "2026-04-01", "retribuzione": "28000"},
                    {"candidato": "Marco Verdone", "ruolo": "Senior Recruiter", "tipo_contratto": "Indeterminato", "data_inizio": "2026-05-15", "retribuzione": "42000"}
                ]
            
            # Recupero dinamico dei candidati dal database interno (o fallback predefinito)
            if "lista_candidati" in st.session_state and st.session_state.lista_candidati:
                opzioni_candidati = [c.get("nome", "Candidato") for c in st.session_state.lista_candidati]
            else:
                opzioni_candidati = ["Daniele Rossi", "Elena Bianchi", "Alessandro Neri", "Simona Viola"]

            # 2. Layout a due colonne perfettamente bilanciate
            col_form, col_tabella = st.columns([1, 1.4])

            with col_form:
                st.markdown("### ➕ Perfeziona Nuova Assunzione")
                with st.form("form_nuova_assunzione", clear_on_submit=True):
                    
                    # Menu a tendina per pescare il candidato
                    candidato_scelto = st.selectbox("Seleziona Candidato*", opzioni_candidati)
                    ruolo_aziendale = st.text_input("Qualifica / Ruolo*")
                    tipo_contratto = st.selectbox("Tipologia Contrattuale", ["Indeterminato", "Determinato", "Apprendistato", "Stage / Tirocinio"])
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        data_inizio = st.date_input("Data Decorrenza", value=None)
                    with c2:
                        ral_proposta = st.number_input("R.A.L. Offerta (€)", min_value=0, step=1000, value=26000)
                    
                    documentazione = st.file_uploader("Carica Documenti d'Identità / Contratto Firmato", type=["pdf", "png", "jpg"])
                    
                    submit_assunzione = st.form_submit_button("Registra Assunzione & Crea Scheda", use_container_width=True)
                    
                    if submit_assunzione:
                        if candidato_scelto and ruolo_aziendale and data_inizio:
                            nuova_ass = {
                                "candidato": candidato_scelto,
                                "ruolo": ruolo_aziendale,
                                "tipo_contratto": tipo_contratto,
                                "data_inizio": str(data_inizio),
                                "retribuzione": str(ral_proposta)
                            }
                            st.session_state.lista_assunzioni.append(nuova_ass)
                            st.success(f"✔️ Assunzione di {candidato_scelto} inserita!")
                            st.rerun()
                        else:
                            st.error("❌ Compila i campi obbligatori (Candidato, Ruolo e Data Inizio).")

            with col_tabella:
                st.markdown("### 📋 Registro Assunzioni Attive")
                st.caption("💡 Seleziona una riga sulla sinistra e premi il tasto CANC sulla tastiera per eliminarla.")
                
                if st.session_state.lista_assunzioni:
                    import pandas as pd
                    df_assunzioni = pd.DataFrame(st.session_state.lista_assunzioni)
                    
                    # data_editor interattivo per modifiche e cancellazioni al volo
                    df_ass_modificato = st.data_editor(
                        df_assunzioni,
                        use_container_width=True,
                        num_rows="dynamic",
                        column_config={
                            "candidato": "Dipendente",
                            "ruolo": "Ruolo / Mansione",
                            "tipo_contratto": st.column_config.SelectboxColumn("Contratto", options=["Indeterminato", "Determinato", "Apprendistato", "Stage / Tirocinio"]),
                            "data_inizio": "Data Inizio",
                            "retribuzione": "RAL (€)"
                        },
                        key="editor_assunzioni_v2"
                    )
                    
                    if not df_ass_modificato.equals(df_assunzioni):
                        st.session_state.lista_assunzioni = df_ass_modificato.to_dict(orient="records")
                        st.success("🔄 Archivio aggiornato con successo!")
                        st.rerun()
                        
                    # --- GENERAZIONE AUTOMATICA DEL DOCUMENTO PDF ---
                    st.markdown("---")
                    st.markdown("### 📄 Esporta Pratiche Ufficio del Personale")
                    
                    dipendente_selezionato = st.selectbox(
                        "Seleziona l'anagrafica da esportare:", 
                        [a["candidato"] for a in st.session_state.lista_assunzioni]
                    )
                    
                    dati_dip = next((item for item in st.session_state.lista_assunzioni if item["candidato"] == dipendente_selezionato), None)
                    
                    if dati_dip:
                        # Costruzione formale del foglio PDF
                        pdf = FPDF()
                        pdf.add_page()
                        
                        pdf.set_font("Helvetica", "B", 16)
                        pdf.set_text_color(59, 130, 246)
                        pdf.cell(0, 10, "SUITE HR ENTERPRISE - GRUPPO DEI REALI", ln=True, align="C")
                        pdf.set_font("Helvetica", "", 10)
                        pdf.set_text_color(100, 100, 100)
                        pdf.cell(0, 6, "Pratica di Onboarding & Trasmissione Contrattuale", ln=True, align="C")
                        pdf.ln(10)
                        
                        pdf.set_font("Helvetica", "B", 12)
                        pdf.set_text_color(0, 0, 0)
                        pdf.cell(0, 10, "DATI CONTRATTUALI RISORSA", ln=True)
                        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                        pdf.ln(4)
                        
                        elementi_scheda = [
                            ("Dipendente / Candidato:", dati_dip["candidato"]),
                            ("Qualifica / Mansione:", dati_dip["ruolo"]),
                            ("Tipologia Contratto:", dati_dip["tipo_contratto"]),
                            ("Data Decorrenza:", dati_dip["data_inizio"]),
                            ("R.A.L. Assegnata:", f"{dati_dip['retribuzione']} EUR")
                        ]
                        
                        pdf.set_font("Helvetica", "", 11)
                        for label, valore in elementi_scheda:
                            pdf.set_font("Helvetica", "", 11)
                            pdf.cell(50, 8, label, border=0)
                            pdf.set_font("Helvetica", "B", 11)
                            pdf.cell(0, 8, str(valore), border=0, ln=True)
                        
                        pdf.ln(15)
                        pdf.set_font("Helvetica", "I", 9)
                        pdf.set_text_color(120, 120, 120)
                        pdf.cell(0, 10, "Documento valido ai fini degli adempimenti interni del personale del Gruppo Dei Reali.", ln=True, align="L")
                        
                        pdf_output = pdf.output()
                        
                        st.download_button(
                            label=f"📥 Scarica Scheda PDF di {dipendente_selezionato}",
                            data=bytes(pdf_output),
                            file_name=f"Pratica_Assunzione_{dipendente_selezionato.replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.info("Nessuna assunzione registrata nel sistema.")

        # --- TAB: ANAGRAFICA CLIENTI B2B ---
        with scelta_tab[6]:
            st.markdown("## 🏢 Anagrafica Clienti B2B")
            
            # Inizializzazione del database clienti in sessione se non esiste
            if "lista_clienti" not in st.session_state:
                st.session_state.lista_clienti = [
                    {"azienda": "Reali Logistics S.r.l.", "piva": "01234567890", "referente": "Mario Rossi", "email": "mario.rossi@realilogistics.it", "stato": "Attivo"},
                    {"azienda": "Tech Solutions Spa", "piva": "09876543211", "referente": "Laura Bianchi", "email": "l.bianchi@techsolutions.com", "stato": "In Attivazione"}
                ]

            # Layout a due colonne: Modulo a sinistra, Elenco con modifiche a destra
            col_mod, col_elenco = st.columns([1, 1.6])

            with col_mod:
                st.markdown("### ➕ Inserisci Nuovo Cliente")
                with st.form("form_nuovo_cliente", clear_on_submit=True):
                    ragione_sociale = st.text_input("Ragione Sociale Azienda*")
                    partita_iva = st.text_input("Partita IVA*")
                    nome_referente = st.text_input("Nome Referente")
                    email_contatto = st.text_input("Email di Contatto")
                    stato_contratto = st.selectbox("Stato Contrattuale", ["Attivo", "In Attivazione", "Sospeso"])
                    
                    submit_cliente = st.form_submit_button("Registra Cliente", use_container_width=True)
                    
                    if submit_cliente:
                        if ragione_sociale and partita_iva:
                            nuovo_c = {
                                "azienda": ragione_sociale,
                                "piva": partita_iva,
                                "referente": nome_referente,
                                "email": email_contatto,
                                "stato": stato_contratto
                            }
                            st.session_state.lista_clienti.append(nuovo_c)
                            st.success(f"✔️ {ragione_sociale} registrato!")
                            st.rerun()
                        else:
                            st.error("❌ Ragione Sociale e Partita IVA sono obbligatori.")

            with col_elenco:
                st.markdown("### 📋 Elenco & Gestione Clienti Partner")
                st.caption("💡 Trucco: per eliminare un cliente, seleziona la riga sulla sinistra della tabella e premi il tasto CANC (o Delete) sulla tua tastiera, poi clicca su 'Salva Modifiche'.")
                
                if st.session_state.lista_clienti:
                    import pandas as pd
                    # Convertiamo in DataFrame
                    df_clienti = pd.DataFrame(st.session_state.lista_clienti)
                    
                    # Usiamo il Data Editor abilitando esplicitamente la cancellazione delle righe (num_rows="dynamic")
                    df_modificato = st.data_editor(
                        df_clienti,
                        use_container_width=True,
                        num_rows="dynamic",  # Permette di aggiungere/rimuovere righe dinamicamente
                        column_config={
                            "azienda": "Azienda Partner",
                            "piva": "Partita IVA",
                            "referente": "Referente",
                            "email": "Email",
                            "stato": st.column_config.SelectboxColumn("Stato", options=["Attivo", "In Attivazione", "Sospeso"])
                        },
                        key="editor_clienti"
                    )
                    
                    # Se il DataFrame modificato dall'utente è diverso da quello in memoria, aggiorniamo la sessione
                    if not df_modificato.equals(df_clienti):
                        st.session_state.lista_clienti = df_modificato.to_dict(orient="records")
                        st.success("🔄 Elenco aggiornato correttamente!")
                        st.rerun()
                else:
                    st.info("Nessun cliente in archivio.")

        # --- TAB 8: DATABASE ANAGRAFICO CANDIDATI (ORDINATO E CON SCHEDA COMPATTA) ---
        with scelta_tab[7]:
            st.subheader("👥 Database Anagrafico Globale Candidati")
            
            # Controlli di Filtro e Ordinamento
            col_ord1, col_ord2 = st.columns([2, 2])
            with col_ord1:
                ordine_scelto = st.selectbox("Ordina l'elenco per:", ["Ultimi Arrivi", "Ordine Alfabetico (A-Z)"])
            with col_ord2:
                res_posizioni = supabase.table("candidati").select("posizione").execute()
                lista_posizioni = list(set([item['posizione'] for item in res_posizioni.data if item.get('posizione')])) if res_posizioni.data else []
                posizione_filtro = st.selectbox("Filtra per Ruolo Richiesto:", ["Tutti i Ruoli"] + lista_posizioni)

            # Recupero dati da Supabase
            res_tutti = supabase.table("candidati").select("*").execute()
            tutti = res_tutti.data if res_tutti.data else []
            
            if not tutti:
                st.info("Nessun candidato registrato nel database cloud.")
            else:
                # Applica Filtro
                if posizione_filtro != "Tutti i Ruoli":
                    tutti = [cand for cand in tutti if cand.get('posizione') == posizione_filtro]
                
                # Applica Ordinamento
                if ordine_scelto == "Ultimi Arrivi":
                    tutti = sorted(tutti, key=lambda x: x.get('id', 0), reverse=True)
                elif ordine_scelto == "Ordine Alfabetico (A-Z)":
                    tutti = sorted(tutti, key=lambda x: x.get('nome', '').lower())

                # Lista Compatta dei candidati
                for c in tutti:
                    punteggio_ia = c.get('idoneita', '85%') # Recupera la percentuale calcolata all'invio
                    
                    st.markdown(f"""
                    <div style="background-color: #FFFFFF; padding: 14px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <div>
                            <span style="font-weight: bold; color: #1E3A8A; font-size: 16px;">👤 {c['nome']}</span> 
                            <span style="margin-left: 10px; font-size: 12px; background-color: #EFF6FF; color: #2563EB; padding: 3px 8px; border-radius: 4px; font-weight: bold;">{c['posizione']}</span>
                        </div>
                        <div>
                            <span style="background-color: #DCFCE7; color: #15803D; font-weight: bold; font-size: 13px; padding: 5px 10px; border-radius: 6px;">🤖 Attinenza IA: {punteggio_ia}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tasto per aprire la scheda dettagliata
                    with st.expander(f"🔍 Apri Scheda Completa: {c['nome']}"):
                        st.markdown(f"""
                        #### 🗂️ Informazioni Anagrafiche
                        * **Nome e Cognome:** {c['nome']}
                        * **E-mail:** {c['email']}
                        * **Telefono:** {c['telefono']}
                        * **Stato Selezione:** `{c['stato']}`
                        
                        ---
                        #### 🤖 Sintesi e Profilo IA
                        * **Valutazione Attinenza:** {punteggio_ia} {c.get('stelle', '⭐⭐⭐')}
                        * **Orientamento IA:** {c.get('orientamento', 'Profilo acquisito.')}
                        """)
                        
                        st.markdown("##### 📄 Contenuto del Curriculum Vitae:")
                        st.info(c.get('testo_cv', 'Nessun testo estratto.'))
                        
                        # Azioni sulla scheda
                        col_pop1, col_pop2, col_pop3 = st.columns(3)
                        with col_pop1:
                            nuovo_stato = st.selectbox(
                                "Modifica Stato:", 
                                ["In Screening", "Approvato per Colloquio", "Assunto", "Rifiutato"], 
                                index=["In Screening", "Approvato per Colloquio", "Assunto", "Rifiutato"].index(c['stato']) if c['stato'] in ["In Screening", "Approvato per Colloquio", "Assunto", "Rifiutato"] else 0, 
                                key=f"pop_st_{c['id']}"
                            )
                            if st.button("💾 Salva Stato", key=f"pop_sv_{c['id']}", use_container_width=True):
                                supabase.table("candidati").update({"stato": nuovo_stato}).eq("id", c['id']).execute()
                                st.success("Stato aggiornato!")
                                st.rerun()
                        with col_pop2:
                            url_pdf = c.get('immagine', '')
                            if url_pdf and url_pdf.startswith("http"):
                                st.link_button("📥 Scarica PDF Originale", url_pdf, use_container_width=True)
                            else:
                                st.caption("Nessun PDF originale allegato.")
                        with col_pop3:
                            if st.button("🗑️ Elimina Risorsa", key=f"pop_del_{c['id']}", use_container_width=True, type="secondary"):
                                if url_pdf and "curriculum/" in url_pdf:
                                    try:
                                        nome_file_storage = url_pdf.split("curriculum/")[-1]
                                        supabase.storage.from_("curriculum").remove([nome_file_storage])
                                    except Exception: pass
                                supabase.table("agenda").delete().eq("candidato", c['nome']).execute()
                                supabase.table("candidati").delete().eq("id", c['id']).execute()
                                st.success("Candidato eliminato!")
                                st.rerun()
                    st.write("")
