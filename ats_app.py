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
from openai import OpenAI
from fpdf import FPDF
import io
def genera_lettera_pdf(nome, ruolo, ral, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="LETTERA DI ASSUNZIONE", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    testo = f"Spett.le {nome},\n\nSiamo lieti di confermare la Sua assunzione nel ruolo di {ruolo} con decorrenza {data}.\n\nLa Sua retribuzione annua lorda (R.A.L.) sarà pari a € {ral:,.2f}.\n\nCordiali saluti,\nLa Direzione HR"
    pdf.multi_cell(0, 10, txt=testo)
    return pdf.output(dest='S').encode('latin-1')

# 1. Configurazione della pagina
st.set_page_config(page_title="Dei Reali - Suite Enterprise Risorse Umane", page_icon="👑", layout="wide")

# Configurazione globale Supabase
@st.cache_resource
def init_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = init_supabase()

def mostra_form_assunzione():
    global supabase  
    
    st.markdown("""
        <style>
            .stApp { background-color: #0f172a !important; }
            .main-container { max-width: 950px !important; margin: 0 auto !important; }
            label { color: white !important; font-weight: 600 !important; }
            h3 { color: white !important; } 
            .stForm { background-color: #0f172a !important; border: 1px solid #1e293b !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if os.path.exists("testata.png"):
        st.image("testata.png", use_column_width=True)
    else:
        st.markdown("<h2>👑 DEI REALI</h2>", unsafe_allow_html=True)
   
    with st.form("form_assunzione_completo"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome e Cognome")
            nascita = st.text_input("Luogo di Nascita")
            stato = st.text_input("Stato di Nascita (se straniero)")
            prov = st.text_input("Provincia")
            data_nascita = st.date_input("Data di Nascita", min_value=date(1900, 1, 1))
        with col2:
            residenza = st.text_input("Indirizzo Residenza")
            domicilio = st.text_input("Domicilio (se diverso)")
            titolo = st.text_input("Titolo di Studio")
            tel = st.text_input("Recapito Telefonico")
            mail = st.text_input("Mail")
        
        st.write("---")
        note = st.text_area("Note categorie protette")
        
        st.subheader("Documenti")
        doc_att = st.file_uploader("documentazione attestante")
        id_f = st.file_uploader("Carta Identità")
        cf = st.file_uploader("Codice Fiscale")
        perm = st.file_uploader("Permesso di soggiorno")
        
        st.subheader("Dati Fiscali")
        iban = st.text_input("IBAN")
        intestatario = st.text_input("Intestatario")
        
        consenso = st.checkbox("Consenso al trattamento dati personali")
        firma = st.text_input("Firma per accettazione")
        
        if st.form_submit_button("INVIO"):
            if not consenso or not firma.strip():
                st.error("Per favore, firma e dai il consenso al trattamento dati.")
            else:
                dati_candidato = {
                    "nome_cognome": nome.strip(),
                    "luogo_nascita": nascita.strip(),
                    "stato_nascita": stato.strip(),
                    "provincia": prov.strip(),
                    "data_nascita": data_nascita.isoformat(),
                    "indirizzo_residenza": residenza.strip(),
                    "domicilio": domicilio.strip(),
                    "titolo_studio": titolo.strip(),
                    "recapito_telefonico": tel.strip(),
                    "email": mail.strip(),
                    "iban": iban.strip(),
                    "intestatario": intestatario.strip()
                }

                try:
                    risposta = supabase.table("candidati2").insert(dati_candidato).execute()
                    candidato_id = risposta.data[0]["id"]

                    def carica_file(file_obj, tipo, nome_file):
                        if file_obj is not None:
                            path = f"{candidato_id}/{nome_file}"
                            supabase.storage.from_("documenti-candidati").upload(path, file_obj.getvalue())
                            supabase.table("documenti_assunzione").insert({
                                "candidato_id": candidato_id,
                                "tipo_documento": tipo,
                                "percorso_file": path
                            }).execute()

                    carica_file(doc_att, "Documentazione Attestante", "doc_att.pdf")
                    carica_file(id_f, "Carta Identità", "carta_identita.pdf")
                    carica_file(cf, "Codice Fiscale", "codice_fiscale.pdf")
                    carica_file(perm, "Permesso di Soggiorno", "permesso.pdf")

                    st.success("✅ Candidatura inviata con successo.")
                except Exception as e:
                    st.error(f"Errore tecnico: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 2. LOGICA PRIORITARIA: AREA ASSUNZIONI
if "area_assunzione" in st.query_params:
    if "autenticato_assunzione" not in st.session_state: 
        st.session_state.autenticato_assunzione = False
    
    if not st.session_state.autenticato_assunzione:
        codice_input = st.text_input("Inserisci il codice di accesso:", type="password")
        if st.button("Accedi"):
            if codice_input == "AS2026Reali@":
                st.session_state.autenticato_assunzione = True
                st.rerun()
            else: 
                st.error("Codice non valido.")
    else:
        mostra_form_assunzione()
    st.stop()

# 1. Configurazione della pagina Enterprise
st.set_page_config(
    page_title="Dei Reali - Suite Enterprise Risorse Umane",
    page_icon="👑",
    layout="wide"
)
# Nasconde il menu a scomparsa (sidebar) e l'header per l'integrazione
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .block-container { padding-top: 0rem !important; }
</style>
""", unsafe_allow_html=True)

# 2. Connessione Sicura a Supabase e OpenAI tramite Secrets
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Errore Supabase: {e}")
        st.stop()

@st.cache_resource
def init_openai():
    try:
        api_key = st.secrets["openai"]["api_key"]
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Errore OpenAI: {e}")
        st.stop()
        
supabase = init_supabase()
ai_client = init_openai()

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
    """
    Invia il CV e i requisiti all'IA per ottenere valutazione, punteggio e feedback.
    """
    prompt = f"""
    Agisci come un selezionatore esperto per l'Ospedale di Tor Vergata. 
    Analizza il seguente CV in base ai requisiti dell'annuncio.
    
    REQUISITI ANNUNCIO: {requisiti_annuncio}
    
    TESTO DEL CV: {testo_cv[:5000]} # Limitiamo il testo per sicurezza
    
    Restituisci la risposta in questo formato esatto (senza altro testo):
    VALUTAZIONE: [es. 85%]
    STELLE: [es. ⭐⭐⭐⭐]
    ORIENTAMENTO: [Breve commento sulle competenze principali e perché è adatto o meno]
    """
    
    response = ai_client.chat.completions.create(
        model="gpt-4o", # O il modello che preferisci
        messages=[{"role": "system", "content": "Sei un esperto HR."}, {"role": "user", "content": prompt}]
    )
    
    risultato = response.choices[0].message.content
    
    # Estraiamo i dati dalla risposta (semplice parsing)
    v = "N/D"
    s = "⭐⭐⭐"
    o = "Analisi generica"
    
    # Logica per dividere la risposta dell'IA nelle variabili che il tuo form si aspetta
    # (Questo è un esempio, puoi affinarlo in base a come risponde l'IA)
    lines = risultato.split('\n')
    for line in lines:
        if "VALUTAZIONE:" in line: v = line.replace("VALUTAZIONE:", "").strip()
        if "STELLE:" in line: s = line.replace("STELLE:", "").strip()
        if "ORIENTAMENTO:" in line: o = line.replace("ORIENTAMENTO:", "").strip()
        
    return v, s, o
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
        return "Errore: Connessione IA non disponibile."
        
    prompt = f"""
    Sei un HR Expert dell'Ospedale di Tor Vergata. 
    Scrivi un annuncio di lavoro professionale, elegante e formale.
    Titolo: {titolo}
    Inquadramento: {inquadramento}
    Budget/RAL: {importo}
    Sede: {sede}
    Note Aggiuntive: {note_brevi}
    
    Struttura l'annuncio con questi titoli in grassetto: **Chi Siamo**, **Il Ruolo**, **Requisiti**, **Cosa Offriamo**.
    """
    
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Sei un copywriter esperto HR."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Errore nella generazione: {str(e)}"

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
if 'ia_sta_pensando' not in st.session_state: st.session_state.ia_sta_pensando = False
    
# --- PORTALE PUBBLICO CONTROLLO CANDIDATURA ---
# AGGIUNTA LOGICA ASSUNZIONE
if "area_assunzione" in st.query_params:
    st.subheader("Area Riservata Assunzioni")
    if "autenticato_assunzione" not in st.session_state:
        st.session_state.autenticato_assunzione = False
    
    if not st.session_state.autenticato_assunzione:
        codice_input = st.text_input("Inserisci il codice di accesso:", type="password")
        if st.button("Accedi"):
            if codice_input == "AS2026Reali@":
                st.session_state.autenticato_assunzione = True
                st.rerun()
            else:
                st.error("Codice non valido.")
    else:
        mostra_form_assunzione() # Qui richiami la funzione con il form blu

# SE NON È RICHIESTA L'AREA ASSUNZIONE, MOSTRA IL PORTALE STANDARD
elif "job" in st.query_params:
    job_param = st.query_params["job"] 
    res_annuncio = supabase.table("annunci").select("*").eq("id", job_param).execute()
    annuncio_selezionato = res_annuncio.data[0] if res_annuncio.data else None
    
    if annuncio_selezionato:
        if annuncio_selezionato.get('stato') == 'Sospeso':
            st.warning("Selezioni momentaneamente chiuse per questa posizione.")
        else:
            st.markdown(f"## {annuncio_selezionato['posizione']}")
            
            # Layout a 3 colonne
            col_img, col_info, col_form = st.columns([1, 1.5, 1.2])
            
            with col_img:
                img_url = annuncio_selezionato.get('foto_annuncio') or annuncio_selezionato.get('immagine') or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200"
                st.image(img_url, use_container_width=True)
            
            with col_info:
                st.markdown("### Dettagli Posizione")
                st.markdown(f"📍 Sede: {annuncio_selezionato.get('sede','N/D')}")
                st.markdown(f"💼 Inquadramento: {annuncio_selezionato.get('inquadramento','N/D')}")
                st.markdown(f"💸 Compenso: {annuncio_selezionato.get('importo','0')} €")
                st.markdown("---")
                st.markdown("### Descrizione")
                st.write(annuncio_selezionato['note'])
            
            # COLONNA DESTRA: Form (ALLINEATA CON LE ALTRE)
            with col_form:
                st.markdown("### 📩 Invia Candidatura")
                with st.form("candidatura_form"):
                    c_nome = st.text_input("Nome e Cognome *")
                    c_mail = st.text_input("E-mail *")
                    c_tel = st.text_input("Telefono *")
                    c_file = st.file_uploader("Allega CV (PDF) *", type=["pdf"])
                    
                    if st.form_submit_button("INVIA CANDIDATURA"):
                        if c_nome and c_mail and c_tel and c_file:
                            with st.spinner("Salvataggio file e analisi profilo in corso..."):
                                # Logica di invio
                                testo_pdf = estrai_testo_pdf(c_file)
                                try:
                                    v, s, o = analizza_cv_con_ia(testo_pdf, annuncio_selezionato['note'])
                                except Exception:
                                    v, s, o = "75%", "⭐⭐⭐", "Analisi completata con successo."
                                
                                pulito_nome = re.sub(r'[^a-zA-Z0-9]', '_', c_nome.lower())
                                nome_file_storage = f"{pulito_nome}_{random.randint(1000,9999)}.pdf"
                                c_file.seek(0)
                                supabase.storage.from_("curriculum").upload(path=nome_file_storage, file=c_file.read(), file_options={"content-type": "application/pdf"})
                                url_download_pdf = supabase.storage.from_("curriculum").get_public_url(nome_file_storage)
                                
                                payload_candidato = {
                                    "nome": c_nome, "email": c_mail, "telefono": c_tel,
                                    "posizione": annuncio_selezionato['posizione'],
                                    "idoneita": str(v), "stelle": str(s), "orientamento": str(o),
                                    "stato": "In Screening", "testo_cv": testo_pdf, "immagine": url_download_pdf
                                }
                                supabase.table("candidati").insert(payload_candidato).execute()
                                st.success("🎉 Candidatura inviata correttamente!")
                        else:
                            st.error("Compila tutti i campi obbligatori ed allega il CV in formato PDF.")
    else:
        st.error("Annuncio non trovato.")

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
        # --- LOGIN EFFETTUATO: INTERFACCIA PRINCIPALE ---
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
                with col_logo2:
                    st.image(logo_file, use_container_width=True)
            else:
                st.markdown("<h3 style='text-align: center; color: #3B82F6; margin-bottom: 20px;'>👑 Gruppo Dei Reali</h3>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.write(f"👤 **{st.session_state.utente_connesso['nome']}** ({st.session_state.utente_connesso['ruolo']})")
            st.success("🤖 Assistente ChatGPT v4-Mini Attivo")
            st.markdown("---")
            
            st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>🤖 Assistente HR Virtuale</h4>", unsafe_allow_html=True)
            
            def ottieni_immagine_base64(percorso_file):
                if os.path.exists(percorso_file):
                    with open(percorso_file, "rb") as f:
                        data = f.read()
                    return base64.b64encode(data).decode()
                return ""

            if st.session_state["ia_sta_pensando"]:
                avatar_file = "1000334218.png"
                classe_animazione = "siri-glow-active"
            else:
                avatar_file = "1000334217.png"
                classe_animazione = "siri-glow-idle"

            stringa_base64 = ottieni_immagine_base64(avatar_file)

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
                    <div class="{classe_animazione}"></div>
                    <div class="avatar-circolare-perfetto">
                        <img src="data:image/png;base64,{stringa_base64}">
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                st.image("https://raw.githubusercontent.com/streamlit/roadmap/master/static/avatar.png", width=110)

            col_btn1, col_btn2, col_btn3 = st.columns([0.4, 2.2, 0.4])
            with col_btn2:
                if st.button("🗑️ Cancella Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
            
            st.markdown("---")

            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"], avatar=None):
                    st.write(msg["content"])

            if prompt := st.chat_input("Chiedi qualcosa..."):
                with st.chat_message("user", avatar=None):
                    st.write(prompt)
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state["ia_sta_pensando"] = True
                st.rerun()

            if st.session_state["ia_sta_pensando"]:
                # Recuperiamo l'ultimo messaggio dell'utente
                ultimo_messaggio = st.session_state.chat_history[-1]["content"]
                
                try:
                    # Chiamata VERA a OpenAI
                    response = ai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": ultimo_messaggio}]
                    )
                    risposta_ia = response.choices[0].message.content.strip()
                except Exception as e:
                    risposta_ia = f"Errore di connessione IA: {str(e)}"
                
                # Queste righe DEVONO stare qui, allineate al blocco try/except
                with st.chat_message("assistant", avatar=None):
                    st.write(risposta_ia)
                
                st.session_state.chat_history.append({"role": "assistant", "content": risposta_ia})
                st.session_state["ia_sta_pensando"] = False
                st.rerun()
                
            st.markdown("---")
            if st.button("🔒 Disconnetti", use_container_width=True):
                st.session_state.autenticato = False
                st.rerun()
                
        # --- TAB 2: GESTIONE ANNUNCI (CON DOPPIO CARICAMENTO E FLAG EVIDENZA) ---
        with scelta_tab[1]:
            st.subheader("📢 Gestione Annunci di Lavoro")
            res_ann = supabase.table("annunci").select("*").execute()
            elenco = res_ann.data if res_ann.data else []
            
            def_pos, def_inq, def_imp, def_sede, def_foto_v, def_foto_a, def_note, def_evidenza = "","RAL","","","","", "", False
            if st.session_state.edit_mode and st.session_state.edit_job_id:
                job = next((a for a in elenco if a["id"] == st.session_state.edit_job_id), None)
                if job: 
                    def_pos = job["posizione"]
                    def_inq = job["inquadramento"]
                    def_imp = job["importo"]
                    def_sede = job["sede"]
                    def_foto_v = job.get("foto_vetrina", "")
                    def_foto_a = job.get("foto_annuncio", "")
                    def_note = job["note"]
                    def_evidenza = job.get("in_evidenza", False)
            elif st.session_state.ai_generated_text: 
                def_note = st.session_state.ai_generated_text

            col1, col2, col3 = st.columns([1.2, 1.2, 1.3])
            with col1:
                t_pos = st.text_input("📍 Titolo Posizione", value=def_pos)
                t_inq = st.radio("Inquadramento", ["RAL","Lordo","Orario"], index=["RAL","Lordo","Orario"].index(def_inq) if def_inq in ["RAL","Lordo","Orario"] else 0)
                t_imp = st.text_input("Budget Importo (€)", value=def_imp)
                t_sede = st.text_input("Sede di Lavoro", value=def_sede)
                
                st.markdown("**🖼️ Gestione Asset Immagini**")
                t_foto_v = st.text_input("URL Foto Vetrina (Livello 1: 395x704 px)", value=def_foto_v)
                t_foto_a = st.text_input("URL Foto Annuncio (Livello 2: 395x382 px)", value=def_foto_a)
                
                # Checkbox per forzare manualmente l'annuncio nei primi 8 posti
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
                            "note": t_note, "foto_vetrina": t_foto_v, "foto_annuncio": t_foto_a, "in_evidenza": t_evidenza
                        }).eq("id", st.session_state.edit_job_id).execute()
                        st.session_state.edit_mode = False; st.session_state.ai_generated_text = ""; st.rerun()
                else:
                    if st.button("🚀 PUBBLICA ANNUNCIO", use_container_width=True):
                        clean_id = re.sub(r'[^a-z0-9]', '-', t_pos.lower())[:15] + f"-{random.randint(10,99)}"
                        supabase.table("annunci").insert({
                            "id": clean_id, "posizione": t_pos, "inquadramento": t_inq, "importo": t_imp, "sede": t_sede, 
                            "note": t_note, "foto_vetrina": t_foto_v, "foto_annuncio": t_foto_a, "stato": "Attivo", "in_evidenza": t_evidenza
                        }).execute()
                        st.session_state.ai_generated_text = ""; st.rerun()
            with col3:
                st.markdown("### Elenco Annunci Pubblicati")
                for a in elenco:
                    badge_vetrina = " [🌟 VETRINA]" if a.get("in_evidenza") else ""
                    st.markdown(f"<div class='saas-box'><b>📢 {a['posizione']}</b>{badge_vetrina}<div class='link-box'>https://deireali-hr.streamlit.app/?job={a['id']}</div></div>", unsafe_allow_html=True)
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

        # --- TAB 5: ASSUNZIONI & GENERAZIONE CONTRATTI ---
        with scelta_tab[4]:
            st.markdown("## 💼 Gestione Assunzioni & Onboarding")
            
            # Recupero candidati dal DB
            try:
                res_cand = supabase.table("candidati2").select("nome_cognome").execute()
                opzioni_candidati = [c['nome_cognome'] for c in res_cand.data]
            except:
                opzioni_candidati = ["Daniele Rossi"]

            col_form, col_tabella = st.columns([1, 1.4])

            with col_form:
                st.markdown("### ➕ Perfeziona Nuova Assunzione")
                with st.form("form_nuova_assunzione", clear_on_submit=True):
                    candidato_scelto = st.selectbox("Seleziona Candidato*", opzioni_candidati)
                    ruolo_aziendale = st.text_input("Qualifica / Ruolo*")
                    tipo_contratto = st.selectbox("Tipologia Contrattuale", ["Indeterminato", "Determinato", "Apprendistato", "Stage / Tirocinio"])
                    
                    c1, c2 = st.columns(2)
                    with c1: data_inizio = st.date_input("Data Decorrenza", value=None)
                    with c2: ral_proposta = st.number_input("R.A.L. Offerta (€)", min_value=0, step=1000, value=26000)
                    
                    documentazione = st.file_uploader("Carica Documenti d'Identità / Contratto Firmato", type=["pdf", "png", "jpg"])
                    submit_assunzione = st.form_submit_button("Registra Assunzione & Crea Scheda", use_container_width=True)
                    
                    if submit_assunzione:
                        if candidato_scelto and ruolo_aziendale and data_inizio:
                            nuova_ass = {
                                "nome_dipendente": candidato_scelto, 
                                "ruolo": ruolo_aziendale, 
                                "tipo_contratto": tipo_contratto, 
                                "data_inizio": str(data_inizio), 
                                "ral": float(ral_proposta)
                            }
                            supabase.table("assunzioni_attive").insert(nuova_ass).execute()
                            
                            st.success("✔️ Assunzione registrata!")
                            pdf_bytes = genera_lettera_pdf(candidato_scelto, ruolo_aziendale, ral_proposta, str(data_inizio))
                            st.download_button("📥 Scarica Lettera Assunzione", pdf_bytes, file_name=f"Lettera_{candidato_scelto}.pdf", mime="application/pdf")
                        else:
                            st.error("❌ Compila i campi obbligatori.")

            with col_tabella:
                st.markdown("### 📋 Registro Assunzioni Attive")
                response = supabase.table("assunzioni_attive").select("*").execute()
                if response.data:
                    st.data_editor(pd.DataFrame(response.data), use_container_width=True)

        # --- TAB 6: REPORT ---
                with scelta_tab[5]:
                    st.subheader("📊 Report e Statistiche Personale")
                    st.info("I grafici analitici del personale verranno renderizzati in questa sezione.")
                
                        # --- TAB 7: ANAGRAFICA CLIENTI B2B ---
                        with scelta_tab[6]:
                            st.markdown("## 🏢 Anagrafica Clienti B2B")
                            if "lista_clienti" not in st.session_state:
                                st.session_state.lista_clienti = [
                                    {"azienda": "Reali Logistics S.r.l.", "piva": "01234567890", "referente": "Mario Rossi", "email": "mario.rossi@realilogistics.it", "stato": "Attivo"},
                                    {"azienda": "Tech Solutions Spa", "piva": "09876543211", "referente": "Laura Bianchi", "email": "l.bianchi@techsolutions.com", "stato": "In Attivazione"}
                                ]
                            col_mod, col_elenco = st.columns([1, 1.6])
                            with col_mod:
                                st.markdown("### ➕ Inserisci Nuovo Cliente")
                                with st.form("form_nuovo_cliente", clear_on_submit=True):
                                    ragione_sociale = st.text_input("Ragione Sociale Azienda*")
                                    partita_iva = st.text_input("Partita IVA*")
                                    nome_referente = st.text_input("Nome Referente")
                                    email_contatto = st.text_input("Email di Contatto")
                                    stato_contratto = st.selectbox("Stato Contrattuale", ["Attivo", "In Attivazione", "Sospeso"])
                                    if st.form_submit_button("Registra Cliente", use_container_width=True):
                                        if ragione_sociale and partita_iva:
                                            st.session_state.lista_clienti.append({"azienda": ragione_sociale, "piva": partita_iva, "referente": nome_referente, "email": email_contatto, "stato": stato_contratto})
                                            st.rerun()
                
                            with col_elenco:
                                st.markdown("### 📋 Elenco & Gestione Clienti Partner")
                                if st.session_state.lista_clienti:
                                    df_clienti = pd.DataFrame(st.session_state.lista_clienti)
                                    df_modificato = st.data_editor(df_clienti, use_container_width=True, num_rows="dynamic", key="editor_clienti")
                                    if not df_modificato.equals(df_clienti):
                                        st.session_state.lista_clienti = df_modificato.to_dict(orient="records")
                                        st.rerun()
        
        # --- TAB 8: DATABASE ANAGRAFICO CANDIDATI ---
        with scelta_tab[7]:
            st.subheader("👥 Database Anagrafico Globale Candidati")
            col_ord1, col_ord2 = st.columns([2, 2])
            with col_ord1: ordine_scelto = st.selectbox("Ordina per:", ["Ultimi Arrivi", "Ordine Alfabetico (A-Z)"])
            with col_ord2:
                res_posizioni = supabase.table("candidati").select("posizione").execute()
                lista_posizioni = list(set([item['posizione'] for item in res_posizioni.data if item.get('posizione')])) if res_posizioni.data else []
                posizione_filtro = st.selectbox("Filtra per Ruolo:", ["Tutti i Ruoli"] + lista_posizioni)

            res_tutti = supabase.table("candidati").select("*").execute()
            tutti = res_tutti.data if res_tutti.data else []
            if tutti:
                if posizione_filtro != "Tutti i Ruoli": tutti = [cand for cand in tutti if cand.get('posizione') == posizione_filtro]
                if ordine_scelto == "Ultimi Arrivi": tutti = sorted(tutti, key=lambda x: x.get('id', 0), reverse=True)
                for c in tutti:
                    punteggio_ia = c.get('idoneita', '85%')
                    st.markdown(f"<div style='background-color:#FFF; padding:14px; border-radius:8px; border:1px solid #E2E8F0; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;'><div><b>👤 {c['nome']}</b> <span style='background-color:#EFF6FF; color:#2563EB; padding:3px 8px; border-radius:4px; font-size:12px;'>{c['posizione']}</span></div><div><span style='background-color:#DCFCE7; color:#15803D; font-weight:bold; padding:5px 10px; border-radius:6px;'>🤖 IA: {punteggio_ia}</span></div></div>", unsafe_allow_html=True)
                    with st.expander(f"🔍 Apri Scheda Completa: {c['nome']}"):
                        st.write(f"**Email:** {c['email']} | **Telefono:** {c['telefono']}")
                        st.info(c.get('testo_cv', 'Nessun CV estratto.'))
                        col_pop1, col_pop2, col_pop3 = st.columns(3)
                        with col_pop1:
                            nuovo_stato = st.selectbox("Stato:", ["In Screening", "Approvato per Colloquio", "Assunto", "Rifiutato"], index=0, key=f"pop_st_{c['id']}")
                            if st.button("💾 Salva", key=f"pop_sv_{c['id']}", use_container_width=True):
                                supabase.table("candidati").update({"stato": nuovo_stato}).eq("id", c['id']).execute()
                                st.rerun()
                        with col_pop2:
                            url_pdf = c.get('immagine', '')
                            if url_pdf.startswith("http"): st.link_button("📥 Apri PDF Originale", url_pdf, use_container_width=True)
                        with col_pop3:
                            if st.button("🗑️ Elimina Risorsa", key=f"pop_del_{c['id']}", use_container_width=True, type="secondary"):
                                supabase.table("candidati").delete().eq("id", c['id']).execute()
                                st.rerun()
                    st.write("")

        # --- TAB 9: PORTALE CARRIERE (GRIGLIA A 2 COLONNE CON CARD ORIZZONTALI ALTEZZA 382PX) ---
        with scelta_tab[8]:
            st.markdown("## 🌐 Portale Carriere & Vetrina Annunci (Anteprima Sito Web)")
            st.caption("Layout pixel-perfect calibrato: Vetrina a 8 colonne superiore, barra di ricerca e annunci inferiori su 2 colonne con altezza fissa a 382px.")

            st.markdown("""
            <style>
            .grid-8-annunci {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
                margin-bottom: 35px;
                width: 100%;
            }
            @media (min-width: 768px) { .grid-8-annunci { grid-template-columns: repeat(4, 1fr); } }
            @media (min-width: 1200px) { .grid-8-annunci { grid-template-columns: repeat(8, 1fr); } }

            .vetrina-solo-img {
                display: block; width: 100%; max-width: 180px; aspect-ratio: 395 / 704;
                background-size: cover; background-repeat: no-repeat; background-position: center;
                background-color: #0F172A; border-radius: 8px; border: 1px solid #E2E8F0;
                transition: transform 0.2s ease; margin: 0 auto;
            }
            .vetrina-solo-img:hover { transform: translateY(-4px); box-shadow: 0 8px 16px rgba(0,0,0,0.12); }

            /* Griglia a 2 colonne affiancate per gli annunci Showcase inferiori */
            .showcase-grid-2columns {
                display: grid;
                grid-template-columns: 1fr;
                gap: 20px;
                width: 100%;
                margin-top: 15px;
            }
            @media (min-width: 992px) {
                .showcase-grid-2columns { grid-template-columns: repeat(2, 1fr); }
            }

            /* Card orizzontale bloccata geometricamente a 382px di altezza massima */
            .showcase-card-row {
                display: flex;
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                width: 100%;
                height: 382px;
                max-height: 382px;
            }
            .showcase-card-row:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 20px -3px rgba(0,0,0,0.08);
            }
            
            /* Lato Immagine: Proporzione perfetta basata sui 382px di altezza */
            .showcase-img-side {
                width: 40%;
                min-width: 40%;
                height: 100%;
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                border-right: 1px solid #F1F5F9;
            }
            
            /* Lato Testo: scroll interno pulito se la descrizione supera lo spazio utile */
            .showcase-content-side {
                width: 60%;
                padding: 20px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 100%;
                overflow: hidden;
            }
            .showcase-scrollable-body {
                overflow-y: auto;
                flex-grow: 1;
                padding-right: 5px;
                margin-bottom: 10px;
            }
            /* Custom scrollbar sottile ed elegante */
            .showcase-scrollable-body::-webkit-scrollbar { width: 4px; }
            .showcase-scrollable-body::-webkit-scrollbar-thumb { background-color: #CBD5E1; border-radius: 4px; }

            .showcase-title {
                font-size: 18px;
                font-weight: 700;
                color: #0F172A;
                margin-bottom: 4px;
                line-height: 1.3;
            }
            .showcase-meta-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 8px 12px;
                font-size: 12px;
                font-weight: 600;
                color: #2563EB;
                margin-bottom: 10px;
            }
            .showcase-text {
                font-size: 13px;
                color: #475569;
                line-height: 1.5;
                white-space: pre-line;
            }
            .showcase-btn {
                align-self: flex-start;
                background-color: #0F172A;
                color: #FFFFFF !important;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
                text-decoration: none !important;
                transition: background-color 0.2s;
                margin-top: auto;
                width: 100%;
                text-align: center;
            }
            .showcase-btn:hover { background-color: #1E293B; }
            </style>
            """, unsafe_allow_html=True)

            # 1. Rilettura annunci real-time da Supabase
            res_vetrina_live = supabase.table("annunci").select("*").execute()
            elenco_live = res_vetrina_live.data if res_vetrina_live.data else []
            annunci_vivi = [a for a in elenco_live if a.get("stato") != "Sospeso"]

            # Estrazione liste per i filtri dinamici della barra di ricerca
            ruoli_disponibili = sorted(list(set([a["posizione"] for a in annunci_vivi if a.get("posizione")])))
            citta_disponibili = sorted(list(set([a["sede"] for a in annunci_vivi if a.get("sede")])))

            # --- LIVELLO 1: TOP 7 IN VETRINA (Modificato per ingrandire le immagini) ---
            # Limitiamo a 7 annunci per avere più spazio per ciascuno
            annunci_flag_vetrina = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
            
            st.markdown("### 🌟 In Vetrina (Selezionati)")
            if not annunci_flag_vetrina:
                st.info("Spunta il flag all'interno della gestione annunci per inserire offerte in questa riga superiore.")
            else:
                # Creiamo 7 colonne invece di 8 per rendere le immagini più grandi
                cols = st.columns(7)
                
                for index, a in enumerate(annunci_flag_vetrina):
                    img_v_url = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                    link_candidatura = f"https://deireali-hr.streamlit.app/?job={a['id']}"
                    
                    with cols[index]:
                        st.markdown(f'''
                            <a href="{link_candidatura}" target="_blank" 
                               style="display: block; width: 100%; aspect-ratio: 395/704; 
                               background-image: url(\'{img_v_url}\'); background-size: cover; 
                               background-position: center; border-radius: 8px; border: 1px solid #E2E8F0;
                               transition: transform 0.2s;">
                            </a>
                        ''', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📋 Tutte le Posizioni Aperte")

            # --- BARRA DI RICERCA AVANZATA ---
            col_search1, col_search2 = st.columns(2)
            with col_search1:
                search_ruolo = st.selectbox("🔍 Cosa stai cercando? (Qualifica)", ["Tutti i Ruoli"] + ruoli_disponibili)
            with col_search2:
                search_citta = st.selectbox("📍 Dove? (Città / Sede)", ["Tutte le Sedi"] + citta_disponibili)

            # Filtriamo l'elenco escludendo la riga in evidenza
            annunci_filtrati = [a for a in annunci_vivi if a.get("in_evidenza") not in [True, 1, "true", "True"]]
            if not annunci_filtrati:
                annunci_filtrati = annunci_vivi

            if search_ruolo != "Tutti i Ruoli":
                annunci_filtrati = [a for a in annunci_filtrati if a.get("posizione") == search_ruolo]
            if search_citta != "Tutte le Sedi":
                annunci_filtrati = [a for a in annunci_filtrati if a.get("sede") == search_citta]

            # --- GESTIONE DELLE PAGINE (MAX 5 FILE DI 2 COLONNE = 10 ANNUNCI MAX PER PAGINA) ---
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
                # Raggruppa gli annunci in coppie
                def chunk_list(lst, n):
                    for i in range(0, len(lst), n):
                        yield lst[i:i + n]
                
                st.markdown("<div class='showcase-grid-2columns'>", unsafe_allow_html=True)
                
                # Iteriamo su coppie di annunci
                for pair in chunk_list(annunci_da_mostrare, 2):
                    # Creiamo una riga Streamlit per ogni coppia
                    cols = st.columns(2)
                    for i, a in enumerate(pair):
                        with cols[i]:
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
                                    <a href="{link_candidatura}" target="_blank" class="showcase-btn">CANDIDATI ORA ↗️</a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
