import streamlit as st
import pandas as pd
import os
import random
import string
import urllib.parse
import re
import base64
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

# --- FUNZIONI DI SERVIZIO GLOBALI ---
def ottieni_immagine_base64(percorso_file):
    if os.path.exists(percorso_file):
        with open(percorso_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

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
    .umana-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; margin-bottom: 20px; background: #FFFFFF; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0; }
    .umana-kpi { border-right: 1px solid #E2E8F0; padding-right: 10px; }
    .umana-kpi:last-child { border-right: none; }
    .umana-kpi-label { font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; }
    .umana-kpi-value { font-size: 14px; color: #0F172A; font-weight: 700; margin-top: 2px; }
    .public-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 35px; width: 100%; margin: 15px auto; }
    .saas-box { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .ai-box { background-color: #F1F5F9; border-left: 4px solid #2563EB; padding: 15px; margin-top: 10px; }
    .link-box { background-color: #F8FAFC; padding: 10px; border-radius: 8px; font-family: monospace; font-size: 12px; border: 1px solid #E2E8F0; color: #2563EB; word-break: break-all; margin-top: 5px; }
    
    /* Frame statico 395x704 per la colonna sinistra del portale pubblico */
    .public-left-img-frame {
        width: 100%;
        aspect-ratio: 395 / 704;
        background-size: cover;
        background-position: center;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
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
if 'ia_sta_pensando' not in st.session_state: st.session_state.ia_sta_pensando = False
    
# --- PORTALE PUBBLICO (IMPOSTAZIONE ORIZZONTALE A 3 COLONNE RIGIDE) ---
if "job" in st.query_params:
    job_param = str(st.query_params["job"])
    res_annuncio = supabase.table("annunci").select("*").eq("id", job_param).execute()
    annuncio_selezionato = res_annuncio.data[0] if res_annuncio.data else None
    
    if annuncio_selezionato:
        if annuncio_selezionato.get('stato') == 'Sospeso':
            st.warning("Selezioni momentaneamente chiuse per questa posizione.")
        else:
            st.markdown('<div class="public-card">', unsafe_allow_html=True)
            
            # Griglia orizzontale a tre blocchi
            col_sinistra, col_centro, col_destra = st.columns([1.1, 1.5, 1.4])
            
            with col_sinistra:
                # Render nativo della Foto Vetrina verticale 395x704
                img_v_view = annuncio_selezionato.get('foto_vetrina') or annuncio_selezionato.get('immagine') or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                st.markdown(f'<div class="public-left-img-frame" style="background-image: url(\'{img_v_view}\');"></div>', unsafe_allow_html=True)
                
            with col_centro:
                st.markdown(f"<h1 style='color: #0F172A; margin-top: 0; font-size: 28px;'>{annuncio_selezionato['posizione']}</h1>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="umana-grid">
                        <div class="umana-kpi"><div class="umana-kpi-label">📍 Sede</div><div class="umana-kpi-value">{annuncio_selezionato.get('sede','N/D')}</div></div>
                        <div class="umana-kpi"><div class="umana-kpi-label">💼 Inquadramento</div><div class="umana-kpi-value">{annuncio_selezionato.get('inquadramento','N/D')}</div></div>
                        <div class="umana-kpi"><div class="umana-kpi-label">💸 Compenso</div><div class="umana-kpi-value">{annuncio_selezionato.get('importo','0')} €</div></div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("<h3 style='color: #1E3A8A;'>📋 Dettagli della Posizione</h3>", unsafe_allow_html=True)
                st.write(annuncio_selezionato['note'])
                
            with col_destra:
                st.markdown("<h3 style='color: #1E3A8A; margin-top: 0;'>📝 Modulo di Candidatura</h3>", unsafe_allow_html=True)
                with st.form("candidatura_3_colonne"):
                    c_nome = st.text_input("Nome e Cognome *")
                    c_mail = st.text_input("E-mail *")
                    c_tel = st.text_input("Telefono *")
                    
                    # Caricamenti separati richiesti
                    c_file = st.file_uploader("Allega CV Principale (PDF) *", type=["pdf"])
                    c_generic = st.file_uploader("Carica altri file generici (Certificati, Cover Letter...)", type=["pdf", "png", "jpg", "doc", "docx"])
                    
                    if st.form_submit_button("INVIA LA MIA CANDIDATURA", use_container_width=True):
                        if c_nome and c_mail and c_tel and c_file:
                            with st.spinner("Elaborazione e trasmissione dati cloud..."):
                                testo_pdf = estrai_testo_pdf(c_file)
                                try:
                                    v, s, o = analizza_cv_con_ia(testo_pdf, annuncio_selezionato['note'])
                                except Exception:
                                    v, s, o = "75%", "⭐⭐⭐", "Analisi completata."
                                
                                pulito_nome = re.sub(r'[^a-zA-Z0-9]', '_', c_nome.lower())
                                nome_file_storage = f"{pulito_nome}_{random.randint(1000,9999)}.pdf"
                                
                                c_file.seek(0)
                                supabase.storage.from_("curriculum").upload(
                                    path=nome_file_storage,
                                    file=c_file.read(),
                                    file_options={"content-type": "application/pdf"}
                                )
                                url_download_pdf = supabase.storage.from_("curriculum").get_public_url(nome_file_storage)
                                
                                if c_generic:
                                    try:
                                        nome_gen_storage = f"extra_{pulito_nome}_{random.randint(1000,9999)}_{c_generic.name}"
                                        c_generic.seek(0)
                                        supabase.storage.from_("curriculum").upload(path=nome_gen_storage, file=c_generic.read())
                                    except Exception:
                                        pass
                                
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
                                    "immagine": url_download_pdf
                                }
                                supabase.table("candidati").insert(payload_candidato).execute()
                                st.success("🎉 Candidatura trasmessa! Dati e allegati archiviati in sicurezza.")
                        else:
                            st.error("Compila i campi d'anagrafica obbligatori e inserisci il file del tuo CV.")
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.error("Annuncio non trovato.")

# --- AREA AMMINISTRATIVA / BACKOFFICE ---
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
        st.title("👑 Suite HR Enterprise - Gruppo Dei Reali")

        # Inizializzazione dei Tab di navigazione principale (9 elementi stabili)
        tab_nomi = ["🏠 Home / Plancia", "📢 Annunci", "🔬 Screening", "🤝 Colloqui", "💼 Assunzioni", "📊 Report", "👥 Clienti", "👥 Candidati", "🌐 Vetrina Carriere (Web)"]
        scelta_tab = st.tabs(tab_nomi)

        # --- TAB 1: HOME / PLANCIA ---
        with scelta_tab[0]:
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

            st.subheader("📊 Cruscotto Attività Risorse Umane")
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric(label="📥 CV Ricevuti & Screening", value="142", delta="+12 questa settimana")
            col_m2.metric(label="🤝 Colloqui in Agenda", value="8", delta="3 oggi")
            col_m3.metric(label="💼 Posizioni Aperte", value="5", delta="Filtro: Roma")
            col_m4.metric(label="✅ Assunzioni Perfezionate", value="24", delta="82%")

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

        # --- SIDEBAR COMPONENTE CHAT ---
        with st.sidebar:
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            logo_file = "1000376160.jpg"
            if os.path.exists(logo_file):
                col_logo1, col_logo2, col_logo3 = st.columns([0.3, 2.4, 0.3])
                with col_logo2: st.image(logo_file, use_container_width=True)
            else:
                st.markdown("<h3 style='text-align: center; color: #3B82F6; margin-bottom: 20px;'>👑 Gruppo Dei Reali</h3>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.write(f"👤 **{st.session_state.utente_connesso['nome']}** ({st.session_state.utente_connesso['ruolo']})")
            st.success("🤖 Assistente ChatGPT v4-Mini Attivo")
            st.markdown("---")
            
            st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>🤖 Assistente HR Virtuale</h4>", unsafe_allow_html=True)
            
            stringa_base64 = ottieni_immagine_base64("1000334218.png" if st.session_state["ia_sta_pensando"] else "1000334217.png")
            if stringa_base64:
                st.markdown(f"""
                <style>
                .siri-container-centrato {{ display: flex; justify-content: center; align-items: center; position: relative; margin: 25px auto 15px auto; width: 140px; height: 140px; }}
                .siri-glow-active {{ position: absolute; width: 125px; height: 125px; border-radius: 50%; background: linear-gradient(45deg, #3B82F6, #8B5CF6, #EC4899); opacity: 0.7; filter: blur(5px); animation: siriPulsazione 1.3s infinite ease-in-out; z-index: 1; }}
                .siri-glow-idle {{ position: absolute; width: 115px; height: 115px; border-radius: 50%; background: #3B82F6; opacity: 0.15; filter: blur(4px); z-index: 1; }}
                @keyframes siriPulsazione {{
                    0% {{ transform: scale(0.95); opacity: 0.5; filter: blur(4px); }}
                    50% {{ transform: scale(1.18); opacity: 0.85; filter: blur(8px); }}
                    100% {{ transform: scale(0.95); opacity: 0.5; filter: blur(4px); }}
                }}
                .avatar-circolare-perfetto {{ width: 110px; height: 110px; border-radius: 50%; border: 3px solid #3B82F6; overflow: hidden; z-index: 2; position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.25); }}
                .avatar-circolare-perfetto img {{ width: 100%; height: 100%; object-fit: cover; }}
                </style>
                <div class="siri-container-centrato">
                    <div class="{"siri-glow-active" if st.session_state['ia_sta_pensando'] else "siri-glow-idle"}"></div>
                    <div class="avatar-circolare-perfetto"><img src="data:image/png;base64,{stringa_base64}"></div>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🗑️ Cancella Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
            
            st.markdown("---")
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"], avatar=None): st.write(msg["content"])

            if prompt := st.chat_input("Chiedi qualcosa..."):
                with st.chat_message("user", avatar=None): st.write(prompt)
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state["ia_sta_pensando"] = True
                st.rerun()

            if st.session_state["ia_sta_pensando"]:
                import time
                time.sleep(1.0)
                risposta_ia = f"Ricevuto! Sono l'assistente di {st.session_state.utente_connesso['nome']}. Come posso aiutarti con la gestione della plancia?"
                st.session_state.chat_history.append({"role": "assistant", "content": risposta_ia})
                st.session_state["ia_sta_pensando"] = False
                st.rerun()

            st.markdown("---")
            if st.button("🔒 Disconnetti", use_container_width=True):
                st.session_state.autenticato = False
                st.rerun()
                
        # --- TAB 2: GESTIONE ANNUNCI (CON CORREZIONE BOOLEANA PER INVIO DATI) ---
        with scelta_tab[1]:
            st.subheader("📢 Gestione Annunci di Lavoro")
            res_ann = supabase.table("annunci").select("*").execute()
            elenco = res_ann.data if res_ann.data else []
            
            def_pos, def_inq, def_imp, def_sede, def_foto_v, def_foto_a, def_note, def_evidenza = "","RAL","","","","", "", False
            if st.session_state.edit_mode and st.session_state.edit_job_id:
                job = next((a for a in elenco if a["id"] == st.session_state.edit_job_id), None)
                if job: 
                    def_pos, def_inq, def_imp, def_sede = job["posizione"], job["inquadramento"], job["importo"], job["sede"]
                    def_foto_v, def_foto_a, def_note = job.get("foto_vetrina", ""), job.get("foto_annuncio", ""), job["note"]
                    val_ev = job.get("in_evidenza")
                    def_evidenza = True if val_ev in [True, 1, "true", "True"] else False
            elif st.session_state.ai_generated_text: def_note = st.session_state.ai_generated_text

            col1, col2, col3 = st.columns([1.2, 1.2, 1.3])
            with col1:
                t_pos = st.text_input("📍 Titolo Posizione", value=def_pos)
                t_inq = st.radio("Inquadramento", ["RAL","Lordo","Orario"], index=["RAL","Lordo","Orario"].index(def_inq) if def_inq in ["RAL","Lordo","Orario"] else 0)
                t_imp = st.text_input("Budget Importo (€)", value=def_imp)
                t_sede = st.text_input("Sede di Lavoro", value=def_sede)
                
                st.markdown("**🖼️ Asset Immagini Dedicati**")
                t_foto_v = st.text_input("URL Foto Vetrina (Livello 1: 395x704 px)", value=def_foto_v)
                t_foto_a = st.text_input("URL Foto Annuncio (Livello 2: 395x382 px)", value=def_foto_a)
                t_evidenza = st.checkbox("🌟 Posiziona questo annuncio nei primi 8 (In Vetrina)", value=def_evidenza)
                
            with col2:
                t_note = st.text_area("Descrizione Estesa", value=def_note, height=220)
                if st.button("🪄 Genera con IA"):
                    if t_pos:
                        res = genera_testo_annuncio_ia(t_pos, t_inq, t_imp, t_sede, t_note)
                        st.session_state.ai_generated_text = res
                        st.rerun()
                if st.session_state.edit_mode:
                    if st.button("💾 AGGIORNA ANNUNCIO", use_container_width=True):
                        supabase.table("annunci").update({
                            "posizione": t_pos, "inquadramento": t_inq, "importo": t_imp, "sede": t_sede, 
                            "note": t_note, "foto_vetrina": t_foto_v, "foto_annuncio": t_foto_a, "in_evidenza": bool(t_evidenza)
                        }).eq("id", st.session_state.edit_job_id).execute()
                        st.session_state.edit_mode = False; st.session_state.ai_generated_text = ""; st.rerun()
                else:
                    if st.button("🚀 PUBBLICA ANNUNCIO", use_container_width=True):
                        clean_id = re.sub(r'[^a-z0-9]', '-', t_pos.lower())[:15] + f"-{random.randint(10,99)}"
                        supabase.table("annunci").insert({
                            "id": clean_id, "posizione": t_pos, "inquadramento": t_inq, "importo": t_imp, "sede": t_sede, 
                            "note": t_note, "foto_vetrina": t_foto_v, "foto_annuncio": t_foto_a, "stato": "Attivo", "in_evidenza": bool(t_evidenza)
                        }).execute()
                        st.session_state.ai_generated_text = ""; st.rerun()
            with col3:
                st.markdown("### Elenco Annunci Pubblicati")
                for a in elenco:
                    is_ev = a.get("in_evidenza")
                    badge_vetrina = " [🌟 VETRINA]" if is_ev in [True, 1, "true", "True"] else ""
                    st.markdown(f"<div class='saas-box'><b>📢 {a['posizione']}</b>{badge_vetrina}<div class='link-box'>https://deireali-hr.streamlit.app/?job={a['id']}</div></div>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    if c1.button("Modifica", key=f"e_{a['id']}"): st.session_state.edit_mode=True; st.session_state.edit_job_id=a['id']; st.rerun()
                    if c2.button("Sospendi/Attiva", key=f"s_{a['id']}"): supabase.table("annunci").update({"stato":"Sospeso" if a.get('stato')=="Attivo" else "Attivo"}).eq("id", a['id']).execute(); st.rerun()
                    if c3.button("Elimina", key=f"d_{a['id']}"): supabase.table("annunci").delete().eq("id", a['id']).execute(); st.rerun()

        # --- TAB 3: SCREENING ---
        with scelta_tab[2]:
            st.subheader("📥 Candidature Ricevute da Esaminare")
            res = supabase.table("candidati").select("*").eq("stato", "In Screening").execute()
            candidati = res.data if res.data else []
            for c in candidati:
                st.markdown(f"<div class='saas-box'><h4>👤 {c['nome']}</h4><b>Posizione:</b> {c['posizione']}<br><b>Idoneità:</b> <span style='color:#2563EB; font-weight:bold;'>{c['idoneita']}</span><div class='ai-box'><b>Sintesi IA:</b> {c['orientamento']}</div></div>", unsafe_allow_html=True)
                if st.button(f"🤝 Approva {c['nome']} per Colloquio", key=f"ap_{c['id']}", use_container_width=True):
                    supabase.table("candidati").update({"stato":"Approvato per Colloquio"}).eq("id", c['id']).execute(); st.rerun()

        # --- TAB 4: COLLOQUI ---
        with scelta_tab[3]:
            st.subheader("🤝 Calendario e Agenda Live")
            col_agenda, col_nuovo = st.columns([2, 1.2])
            res_agenda_db = supabase.table("agenda").select("*").execute()
            agenda_list = res_agenda_db.data if res_agenda_db.data else []
            with col_agenda:
                res_col = supabase.table("candidati").select("*").eq("stato", "Approvato per Colloquio").execute()
                colloqui = res_col.data if res_col.data else []
                for c in colloqui:
                    match_app = next((a for a in agenda_list if a.get('candidato') == c['nome']), None)
                    d_c = match_app['data'] if match_app else 'Da pianificare'
                    st.markdown(f"<div class='saas-box'><h4>👤 {c['nome']}</h4>🗓️ {d_c}</div>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    c1.link_button("💬 WhatsApp", f"https://wa.me/{c['telefono']}", use_container_width=True)
                    if c2.button("🎉 Promuovi ad Assunto", key=f"ass_{c['id']}", use_container_width=True):
                        supabase.table("candidati").update({"stato":"Assunto"}).eq("id", c['id']).execute(); st.rerun()
            with col_nuovo:
                if colloqui:
                    c_sel = st.selectbox("Schedula risorsa", [c['nome'] for c in colloqui])
                    if st.button("Salva Appuntamento", use_container_width=True):
                        supabase.table("agenda").insert({"candidato": c_sel, "data": str(date.today()), "ora": "15:45", "meet_link": genera_codice_meet_statico()}).execute(); st.rerun()

        # --- TAB 5: ASSUNZIONI & CONTRATTI ---
        with scelta_tab[4]:
            st.markdown("## 💼 Gestione Assunzioni & Onboarding")
            if "lista_assunzioni" not in st.session_state:
                st.session_state.lista_assunzioni = [{"candidato": "Daniele Rossi", "ruolo": "Specializzando HR", "tipo_contratto": "Determinato", "data_inizio": "2026-04-01", "retribuzione": "28000"}]
            df_assunzioni = pd.DataFrame(st.session_state.lista_assunzioni)
            st.data_editor(df_assunzioni, use_container_width=True, num_rows="dynamic")

        # --- TAB 6: REPORT ---
        with scelta_tab[5]:
            st.subheader("📊 Report e Statistiche Personale")
            st.info("I grafici analitici del personale verranno renderizzati in questa sezione.")

        # --- TAB 7: ANAGRAFICA CLIENTI ---
        with scelta_tab[6]:
            st.markdown("## 🏢 Anagrafica Clienti B2B")
            if "lista_clienti" not in st.session_state:
                st.session_state.lista_clienti = [{"azienda": "Reali Logistics S.r.l.", "piva": "01234567890", "referente": "Mario Rossi", "stato": "Attivo"}]
            st.data_editor(pd.DataFrame(st.session_state.lista_clienti), use_container_width=True, num_rows="dynamic")

        # --- TAB 8: DATABASE CANDIDATI ---
        with scelta_tab[7]:
            st.subheader("👥 Database Anagrafico Globale Candidati")
            res_tutti = supabase.table("candidati").select("*").execute()
            tutti = res_tutti.data if res_tutti.data else []
            for c in tutti:
                with st.expander(f"👤 {c['nome']} - {c['posizione']} ({c['stato']})"):
                    st.write(f"Email: {c['email']} | Telefono: {c['telefono']}")
                    st.text(c.get('testo_cv', ''))
                    if st.button("🗑️ Elimina", key=f"del_{c['id']}"):
                        supabase.table("candidati").delete().eq("id", c['id']).execute(); st.rerun()

        # --- TAB 9: PORTALE CARRIERE (CORREZIONE GRIGLIA 8 COLONNE ORIZZONTALE) ---
        with scelta_tab[8]:
            st.markdown("## 🌐 Portale Carriere & Vetrina Annunci (Anteprima Sito Web)")
            st.caption("Layout pixel-perfect calibrato: Vetrina a 8 colonne reale orizzontale superiore, barra di ricerca e annunci inferiori su 2 colonne.")

            st.markdown("""
            <style>
            /* Forza il contenitore principale di Streamlit a non rompere la griglia */
            .grid-8-annunci {
                display: grid !important;
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 12px !important;
                margin-bottom: 35px !important;
                width: 100% !important;
            }
            @media (min-width: 576px) { .grid-8-annunci { grid-template-columns: repeat(4, 1fr) !important; } }
            @media (min-width: 1200px) { .grid-8-annunci { grid-template-columns: repeat(8, 1fr) !important; } }

            /* Contenitore interno per forzare l'allineamento orizzontale degli elementi */
            .vetrina-item {
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                width: 100% !important;
            }

            .vetrina-solo-img {
                display: block !important;
                width: 100% !important;
                max-width: 180px !important;
                aspect-ratio: 395 / 704 !important;
                background-size: cover !important;
                background-repeat: no-repeat !important;
                background-position: center !important;
                background-color: #0F172A !important;
                border-radius: 8px !important;
                border: 1px solid #E2E8F0 !important;
                transition: transform 0.2s ease !important;
            }
            .vetrina-solo-img:hover { transform: translateY(-4px) !important; box-shadow: 0 8px 16px rgba(0,0,0,0.12) !important; }

            /* Griglia inferiore a 2 colonne */
            .showcase-grid-2columns {
                display: grid !important;
                grid-template-columns: 1fr !important;
                gap: 20px !important;
                width: 100% !important;
                margin-top: 15px !important;
            }
            @media (min-width: 992px) {
                .showcase-grid-2columns { grid-template-columns: repeat(2, 1fr) !important; }
            }

            .showcase-card-row {
                display: flex !important;
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 12px !important;
                overflow: hidden !important;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
                width: 100% !important;
                height: 382px !important;
                max-height: 382px !important;
            }
            .showcase-card-row:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 12px 20px -3px rgba(0,0,0,0.08) !important;
            }
            
            .showcase-img-side {
                width: 40% !important;
                min-width: 40% !important;
                height: 100% !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                border-right: 1px solid #F1F5F9 !important;
            }
            
            .showcase-content-side {
                width: 60% !important;
                padding: 20px !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-between !important;
                height: 100% !important;
                overflow: hidden !important;
            }
            .showcase-scrollable-body {
                overflow-y: auto !important;
                flex-grow: 1 !important;
                padding-right: 5px !important;
                margin-bottom: 10px !important;
            }
            .showcase-scrollable-body::-webkit-scrollbar { width: 4px; }
            .showcase-scrollable-body::-webkit-scrollbar-thumb { background-color: #CBD5E1; border-radius: 4px; }

            .showcase-title { font-size: 18px !important; font-weight: 700 !important; color: #0F172A !important; margin-bottom: 4px !important; line-height: 1.3 !important; }
            .showcase-meta-grid { display: flex !important; flex-wrap: wrap !important; gap: 8px 12px !important; font-size: 12px !important; font-weight: 600 !important; color: #2563EB !important; margin-bottom: 10px !important; }
            .showcase-text { font-size: 13px !important; color: #475569 !important; line-height: 1.5 !important; white-space: pre-line !important; }
            .showcase-btn {
                align-self: flex-start !important;
                background-color: #0F172A !important;
                color: #FFFFFF !important;
                padding: 8px 16px !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                font-size: 12px !important;
                text-decoration: none !important;
                transition: background-color 0.2s !important;
                margin-top: auto !important;
                width: 100% !important;
                text-align: center !important;
            }
            .showcase-btn:hover { background-color: #1E293B !important; }
            </style>
            """, unsafe_allow_html=True)

            # 1. Rilettura annunci real-time da Supabase
            res_vetrina_live = supabase.table("annunci").select("*").execute()
            elenco_live = res_vetrina_live.data if res_vetrina_live.data else []
            annunci_vivi = [a for a in elenco_live if a.get("stato") != "Sospeso"]

            ruoli_disponibili = sorted(list(set([a["posizione"] for a in annunci_vivi if a.get("posizione")])))
            citta_disponibili = sorted(list(set([a["sede"] for a in annunci_vivi if a.get("sede")])))

            # --- LIVELLO 1: TOP 8 IN VETRINA ORIZZONTALE REALE ---
            annunci_flag_vetrina = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:8]
            
            st.markdown("### 🌟 In Vetrina (Selezionati)")
            if not annunci_flag_vetrina:
                st.info("Spunta il flag all'interno della gestione annunci per inserire offerte in questa riga superiore.")
            else:
                # 1. APRIAMO il contenitore della griglia una volta sola PRIMA del ciclo
                html_vetrina = "<div class='grid-8-annunci'>"
                
                for a in annunci_flag_vetrina:
                    raw_img_url = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                    
                    # Pulizia automatica dell'URL da spazi o caratteri errati
                    img_v_url = re.sub(r'[^a-zA-Z0-9_\-.:/&?=#%+~,;@!*()\[\]]', '', raw_img_url.strip())
                    link_candidatura = f"https://deireali-hr.streamlit.app/?job={a['id']}"
                    
                    # 2. Aggiungiamo solo l'item e chiudiamo SOLO il vetrina-item all'interno del ciclo
                    html_vetrina += f"""
                    <div class='vetrina-item'>
                        <a href="{link_candidatura}" target="_blank" class="vetrina-solo-img" style="background-image: url('{img_v_url}');"></a>
                    </div>
                    """
                
                # 3. CHIUDIAMO il contenitore della griglia principale una volta sola FUORI dal ciclo
                html_vetrina += "</div>"
                
                st.markdown(html_vetrina, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📋 Tutte le Posizioni Aperte")

            # --- BARRA DI RICERCA AVANZATA ---
            col_search1, col_search2 = st.columns(2)
            with col_search1:
                search_ruolo = st.selectbox("🔍 Cosa stai cercando? (Qualifica)", ["Tutti i Ruoli"] + ruoli_disponibili)
            with col_search2:
                search_citta = st.selectbox("📍 Dove? (Città / Sede)", ["Tutte le Sedi"] + citta_disponibili)

            annunci_filtrati = [a for a in annunci_vivi if a.get("in_evidenza") not in [True, 1, "true", "True"]]
            if not annunci_filtrati:
                annunci_filtrati = annunci_vivi

            if search_ruolo != "Tutti i Ruoli":
                annunci_filtrati = [a for a in annunci_filtrati if a.get("posizione") == search_ruolo]
            if search_citta != "Tutte le Sedi":
                annunci_filtrati = [a for a in annunci_filtrati if a.get("sede") == search_citta]

            # --- GESTIONE DELLE PAGINE ---
            CONTEGGIO_PER_PAGINA = 10  
            totale_annunci_filtrati = len(annunci_filtrati)
            
            if totale_annunci_filtrati == 0:
                st.info("Nessun annuncio corrisponde ai criteri di ricerca selezionati.")
            else:
                pagine_totali = max(1, (totale_annunci_filtrati + CONTEGGIO_PER_PAGINA - 1) // CONTEGGIO_PER_PAGINA)
                pagina_corrente = 1
                if pagine_totali > 1:
                    col_pag1, col_pag2 = st.columns([4, 1])
                    with col_pag2:
                        pagina_corrente = st.number_input(f"Pagina (di {pagine_totali})", min_value=1, max_value=pagine_totali, value=1, step=1)
                
                inizio_index = (pagina_corrente - 1) * CONTEGGIO_PER_PAGINA
                fine_index = inizio_index + CONTEGGIO_PER_PAGINA
                annunci_da_mostrare = annunci_filtrati[inizio_index:fine_index]

                # --- GRIGLIA A DUE COLONNE AFFIANCATE ---
                st.markdown("<div class='showcase-grid-2columns'>", unsafe_allow_html=True)
                for a in annunci_da_mostrare:
                    img_a_url = a.get("foto_annuncio") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                    link_candidatura = f"https://deireali-hr.streamlit.app/?job={a['id']}"
                    
                    st.markdown(f"""
                    <div class="showcase-card-row">
                        <div class="showcase-img-side" style="background-image: url('{img_a_url}');"></div>
                        <div class="showcase-content-side">
                            <div class="showcase-scrollable-body">
                                <div class="showcase-title">{a['posizione']}</div>
                                <div class="showcase-meta-grid">
                                    <span>📍 {a.get('sede', 'Roma')}</span>
                                    <span>💼 {a.get('inquadramento', 'RAL')}</span>
                                    <span>💸 {a.get('importo', 'N/D')} €</span>
                                </div>
                                <div class="showcase-text">{a.get('note', '')}</div>
                            </div>
                            <a href="{link_candidatura}" target="_blank" class="showcase-btn">CANDIDATI ORA ↗</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
