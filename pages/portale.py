import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS aggiornato
st.markdown("""
<style>
    /* Stile per la frase introduttiva e titolo */
    .intro-text { font-size: 1.1rem; color: #475569; margin-bottom: 5px; font-weight: 300; }
    .main-title { font-size: 2.5rem; font-weight: 800; color: #0F172A; margin-bottom: 30px; }
    
    /* Stile per la striscia azzurra */
    .fascia-azzurra { background-color: #EFF6FF; padding: 30px 20px; border-radius: 12px; margin-bottom: 40px; border: 1px solid #DBEAFE; }
    
    /* Stile per le card in vetrina e lista */
    .vetrina-top { display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; }
    .card-vetrina { aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 8px; border: 1px solid #BFDBFE; transition: transform 0.2s; }
    .card-vetrina:hover { transform: scale(1.03); }

    .card-orizzontale { display: flex; border: 1px solid #E2E8F0; border-radius: 12px; height: 380px; margin-bottom: 25px; overflow: hidden; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .img-lato { width: 40%; background-size: cover; background-position: center; border-right: 1px solid #E2E8F0; background-color: #f0f0f0; }
    .testo-lato { width: 60%; padding: 20px; display: flex; flex-direction: column; }
    .contenuto-scroll { flex-grow: 1; overflow-y: auto; margin-bottom: 15px; }
    .btn-black { background: #0F172A; color: white !important; padding: 12px; border-radius: 6px; text-align: center; text-decoration: none; font-weight: bold; width: 100%; display: block; }
</style>
""", unsafe_allow_html=True)

def mostra_portale():
    # Intestazione
    st.markdown('<p class="intro-text">Abbiamo dato spazio al valore e messo le persone al centro: ora tocca a te. Esplora le nostre opportunità d\'impiego sempre aggiornate e trova la posizione ideale per le tue competenze.</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">🌍 Portale Carriera & Opportunità</h1>', unsafe_allow_html=True)
    
    # Recupero dati
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # 1. STRISCIA 7 ANNUNCI IN EVIDENZA (FASCIA AZZURRA)
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        st.markdown('<div class="fascia-azzurra">', unsafe_allow_html=True)
        st.subheader("🌟 In Vetrina")
        cols = st.columns(7)
        for i, a in enumerate(evidenza):
            img_url = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
            cols[i].markdown(f'<a href="?job={a["id"]}"><div class="card-vetrina" style="background-image: url(\'{img_url}\');"></div></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. LISTA COMPLETA
    st.subheader("Tutte le posizioni")
    for i in range(0, len(annunci_vivi), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(annunci_vivi):
                a = annunci_vivi[i + j]
                img_url = a.get("foto_annuncio") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
                with row[j]:
                    st.markdown(f"""
                    <div class="card-orizzontale">
                        <div class="img-lato" style="background-image: url('{img_url}');"></div>
                        <div class="testo-lato">
                            <div class="contenuto-scroll">
                                <h3>{a.get('posizione', 'Posizione Aperta')}</h3>
                                <p style="font-size:12px; color: #64748B;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                                <div style="font-size:13px;">{a.get('note', '')}</div>
                            </div>
                            <a href="?job={a['id']}" class="btn-black">CANDIDATI ORA ↗️</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form di candidatura...")
else:
    mostra_portale()
