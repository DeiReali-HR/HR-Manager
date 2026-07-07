import streamlit as st
import pandas as pd
import re, random
from supabase import create_client
from pypdf import PdfReader
from google import genai

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(page_title="Lavora con Noi - Dei Reali", layout="wide")

# Funzioni di sistema
def estrai_testo_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages])

def analizza_cv_con_ia(testo_cv, note_annuncio):
    # Logica IA semplificata per il portale pubblico
    return "80%", "⭐⭐⭐⭐", "Candidatura ricevuta ed in fase di analisi."

def mostra_dettaglio(job_id):
    res_annuncio = supabase.table("annunci").select("*").eq("id", job_id).execute()
    annuncio = res_annuncio.data[0] if res_annuncio.data else None
    
    if annuncio:
        st.markdown(f"## {annuncio['posizione']}")
        col_img, col_info, col_form = st.columns([1, 1.5, 1.2])
        with col_img:
            st.image(annuncio.get('immagine') or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200", use_container_width=True)
        with col_info:
            st.markdown(f"📍 **Sede:** {annuncio.get('sede','N/D')}")
            st.markdown(f"💼 **Inquadramento:** {annuncio.get('inquadramento','N/D')}")
            st.markdown(f"💸 **Compenso:** {annuncio.get('importo','0')} €")
            st.markdown("---")
            st.write(annuncio['note'])
        with col_form:
            st.markdown("### 📩 Invia Candidatura")
            with st.form("candidatura"):
                c_nome = st.text_input("Nome e Cognome *")
                c_mail = st.text_input("E-mail *")
                c_tel = st.text_input("Telefono *")
                c_file = st.file_uploader("Allega CV (PDF) *", type=["pdf"])
                if st.form_submit_button("INVIA CANDIDATURA"):
                    if c_nome and c_mail and c_tel and c_file:
                        testo = estrai_testo_pdf(c_file)
                        v, s, o = analizza_cv_con_ia(testo, annuncio['note'])
                        nome_file = f"{re.sub(r'[^a-zA-Z0-9]', '_', c_nome.lower())}_{random.randint(1000,9999)}.pdf"
                        c_file.seek(0)
                        supabase.storage.from_("curriculum").upload(nome_file, c_file.read())
                        supabase.table("candidati").insert({
                            "nome": c_nome, "email": c_mail, "telefono": c_tel,
                            "posizione": annuncio['posizione'], "idoneita": v, "stelle": s, 
                            "orientamento": o, "stato": "In Screening", "immagine": supabase.storage.from_("curriculum").get_public_url(nome_file)
                        }).execute()
                        st.success("🎉 Candidatura inviata!")
                    else:
                        st.error("Compila tutti i campi.")
    else:
        st.error("Annuncio non trovato.")

def mostra_vetrina():
    st.title("💼 Posizioni Aperte - Dei Reali")
    st.markdown("---")
    
    # Rimuoviamo il filtro .eq("stato", "Pubblico") per vedere tutto ciò che c'è
    res = supabase.table("annunci").select("*").execute()
    annunci = res.data
    
    if not annunci:
        st.warning("Nessun annuncio trovato nel database.")
    else:
        cols = st.columns(3)
        for i, a in enumerate(annunci):
            with cols[i % 3]:
                st.image(a.get('immagine') or "https://via.placeholder.com/300", use_container_width=True)
                st.subheader(a.get('posizione', 'Senza titolo'))
                st.write(f"📍 {a.get('sede', 'N/D')}")
                if st.button("DETTAGLI", key=a['id']):
                    st.query_params["job"] = a['id']
                    st.rerun()

if "job" in st.query_params:
    mostra_dettaglio(st.query_params["job"])
else:
    mostra_vetrina()
