import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS Editoriale "Blindato"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400&display=swap');
    
    .epigrafe { font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #475569; font-style: italic; margin-bottom: 20px; }
    .titolo-editoriale { font-family: 'Playfair Display', serif; font-size: 3.5rem; color: #0F172A; margin-bottom: 40px; }
    
    /* Fascia azzurra protetta */
    .fascia-azzurra { 
        background-color: #EFF6FF !important; 
        padding: 30px !important; 
        border-radius: 12px !important; 
        margin-bottom: 40px !important; 
        border: 1px solid #DBEAFE !important; 
        display: block !important;
    }
    
    .grid-vetrina { display: flex; flex-wrap: wrap; gap: 15px; }
    .card-vetrina { width: 130px; aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    
    /* Stile lista */
    .card-editoriale { display: flex; border-bottom: 1px solid #E2E8F0; padding: 40px 0; align-items: flex-start; }
    .img-box { width: 200px; min-width: 200px; height: 280px; background-size: cover; background-position: center; border-radius: 4px; margin-right: 30px; }
    .testo-box { flex: 1; }
</style>
""", unsafe_allow_html=True)

def mostra_portale():
    # Intestazione
    st.markdown('<p class="epigrafe">Abbiamo dato spazio al valore e messo le persone al centro: ora tocca a te. Esplora le nostre opportunità d\'impiego sempre aggiornate e trova la posizione ideale per le tue competenze.</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="titolo-editoriale">🌍 Portale Carriera & Opportunità</h1>', unsafe_allow_html=True)
    
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # 1. STRISCIA AZZURRA
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        st.markdown('<div class="fascia-azzurra">', unsafe_allow_html=True)
        st.markdown('### 🌟 In Vetrina', unsafe_allow_html=True)
        # Usiamo un contenitore HTML flex per le immagini invece delle colonne Streamlit
        html_cards = '<div class="grid-vetrina">'
        for a in evidenza:
            img = a.get("foto_vetrina") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
            html_cards += f'<a href="?job={a["id"]}"><div class="card-vetrina" style="background-image: url(\'{img}\');"></div></a>'
        html_cards += '</div></div>'
        st.markdown(html_cards, unsafe_allow_html=True)

    # 2. LISTA EDITORIALE
    st.markdown("---")
    st.header("Tutte le posizioni")
    for a in annunci_vivi:
        img_url = a.get("foto_annuncio") or a.get("immagine") or "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=395"
        st.markdown(f"""
        <div class="card-editoriale">
            <div class="img-box" style="background-image: url('{img_url}');"></div>
            <div class="testo-box">
                <h2 style="font-family: 'Playfair Display', serif; margin-top:0;">{a.get('posizione', 'Posizione')}</h2>
                <p style="color: #64748B; font-weight: 600;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                <div style="margin: 15px 0; font-family: 'Inter', sans-serif; line-height:1.6;">{a.get('note', '')[:300] + '...'}</div>
                <a href="?job={a['id']}" style="color: #0F172A; font-weight: bold; text-decoration: underline;">Leggi l'offerta completa ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_portale()
