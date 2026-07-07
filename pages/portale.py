import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS "Editoriale"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400&display=swap');
    
    .epigrafe { font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #475569; font-style: italic; max-width: 800px; margin-bottom: 20px; line-height: 1.6; }
    .titolo-editoriale { font-family: 'Playfair Display', serif; font-size: 3.5rem; color: #0F172A; margin-bottom: 40px; }
    
    /* Striscia azzurra a tutto schermo */
    .fascia-azzurra-container { background-color: #EFF6FF; padding: 40px 0; margin: 40px -50px; }
    .contenuto-centrato { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
    
    .vetrina-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; }
    .card-vetrina { aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: transform 0.2s; }
    
    .card-orizzontale { display: flex; border-bottom: 1px solid #E2E8F0; padding: 30px 0; background: white; }
    .img-lato { width: 250px; height: 350px; background-size: cover; background-position: center; border-radius: 4px; }
    .testo-lato { padding-left: 30px; display: flex; flex-direction: column; justify-content: center; }
</style>
""", unsafe_allow_html=True)

def mostra_portale():
    # Intestazione Editoriale
    st.markdown('<p class="epigrafe">Abbiamo dato spazio al valore e messo le persone al centro: ora tocca a te. Esplora le nostre opportunità d\'impiego sempre aggiornate e trova la posizione ideale per le tue competenze.</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="titolo-editoriale">🌍 Portale Carriera & Opportunità</h1>', unsafe_allow_html=True)
    
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # 1. STRISCIA AZZURRA CON 7 ANNUNCI
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        st.markdown('<div class="fascia-azzurra-container"><div class="contenuto-centrato">', unsafe_allow_html=True)
        st.markdown('### 🌟 In Vetrina', unsafe_allow_html=True)
        cols = st.columns(7)
        for i, a in enumerate(evidenza):
            img_url = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
            cols[i].markdown(f'<a href="?job={a["id"]}"><div class="card-vetrina" style="background-image: url(\'{img_url}\');"></div></a>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # 2. LISTA EDITORIALE
    st.subheader("Tutte le posizioni")
    for a in annunci_vivi:
        img_url = a.get("foto_annuncio") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
        st.markdown(f"""
        <div class="card-orizzontale">
            <div class="img-lato" style="background-image: url('{img_url}');"></div>
            <div class="testo-lato">
                <h2 style="font-family: 'Playfair Display', serif;">{a.get('posizione', 'Posizione')}</h2>
                <p style="color: #64748B;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                <div style="margin: 20px 0;">{a.get('note', '')[:300] + '...'}</div>
                <a href="?job={a['id']}" style="color: #0F172A; font-weight: bold; text-decoration: underline;">Leggi l'offerta completa ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_portale()
