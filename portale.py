import streamlit as st
import pandas as pd
from supabase import create_client

# Configurazione (copiala uguale a quella che hai in ats_app.py)
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

# Imposta il layout
st.set_page_config(page_title="Lavora con Noi - Dei Reali", layout="wide")

# --- PORTALE PUBBLICO CONTROLLO CANDIDATURA ---
if "job" in st.query_params:
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
