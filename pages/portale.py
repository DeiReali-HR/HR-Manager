import streamlit as st
import random  # <--- AGGIUNTO
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")
st.markdown("""
<style>
    /* Nasconde elementi di sistema Streamlit */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Rimozione spazio in alto */
    .block-container { padding-top: 0rem !important; }
    
    /* Ottimizzazione Mobile */
    @media (max-width: 600px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        /* Nasconde il tasto di gestione flottante su mobile */
        div[data-testid="stDecoration"] { display: none; }
    }
</style>
""", unsafe_allow_html=True)

# CSS Compattato e allineato
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400&display=swap');
    
    .main .block-container { padding-top: 1rem !important; }
    
    /* Riga blu di separazione */
    .riga-blu { border-top: 2px solid #0f172a; margin: 20px 0; width: 100%; }
    
    .titolo-area { font-family: 'Playfair Display', serif; font-size: 0.9rem; color: #64748b; margin-top: 25px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Vetrina sfondo infinito */
    .vetrina-full-width { background-color: #f1f5f9; margin-left: -500px; margin-right: -500px; padding: 30px 500px; margin-bottom: 30px; }
    .grid-vetrina { display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; max-width: 1400px; margin: auto; }
    .card-vetrina { aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 4px; border: 1px solid #cbd5e1; }
    
    /* Annunci con scrolling interno */
    .card-orizzontale { display: flex; border: 1px solid #e2e8f0; border-radius: 8px; background: white; margin-bottom: 10px; height: 350px; overflow: hidden; }
    .img-lato {width: 35%;height: 100%; background-size: contain; /* Cambiato da cover a contain */background-repeat: no-repeat; /* Evita che l'immagine si ripeta se piccola */background-position: center; border-right: 1px solid #e2e8f0; background-color: #f1f5f9; }
    .testo-lato { width: 65%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; height: 100%; }
    .contenuto-scrollabile { flex-grow: 1; overflow-y: auto; margin-bottom: 15px; padding-right: 10px; }
    .btn-black { background: #0f172a; color: white !important; padding: 12px; border-radius: 4px; text-align: center; text-decoration: none; font-weight: bold; display: block; font-size: 0.9rem; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

def render_card(a):
    img_url = a.get("foto_annuncio") or a.get("immagine") or "https://via.placeholder.com/200x350"
    note_testo = str(a.get('note', ''))
    
    # Link diretto e pulito (bypass del login)
    link_candidatura = f"/?job={a['id']}"
    
    return f"""
    <div class="card-orizzontale">
        <div class="img-lato" style="background-image: url('{img_url}');"></div>
        <div class="testo-lato">
            <div class="contenuto-scrollabile">
                <h3 style="font-family: 'Playfair Display', serif; margin-top:0; font-size:1.2rem;">{a.get('posizione', 'Posizione')}</h3>
                <p style="font-size:0.85rem; color: #64748B;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                <p style="font-size:0.85rem;">{note_testo}</p>
            </div>
            <a href="{link_candidatura}" class="btn-black">CANDIDATI ORA ↗</a>
        </div>
    </div>
    <div class="riga-blu"></div>
    """

def mostra_portale():
    # Intestazione compatta
    st.markdown('<h1 style="font-family: \'Playfair Display\', serif; font-size: 2.2rem; margin-top: 0; margin-bottom: 5px;">Opportunità di Carriera</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: \'Inter\', sans-serif; color: #64748b; font-size: 0.9rem; margin-bottom: 5px;">Selezioniamo i migliori talenti per una crescita professionale d\'eccellenza.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="riga-blu"></div>', unsafe_allow_html=True)
    
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # VETRINA
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]]
    
    # Mescola la lista casualmente
    random.shuffle(evidenza)
    
    # Prendi solo i primi 7 dopo averli mescolati
    evidenza = evidenza[:7]
    
    if evidenza:
        st.markdown('<p class="titolo-area">In primo piano</p>', unsafe_allow_html=True)
        html_vetrina = '<div class="vetrina-full-width"><div class="grid-vetrina">'
        for a in evidenza:
            img_url = a.get("foto_vetrina") or a.get("immagine") or "https://via.placeholder.com/395x704"
            html_vetrina += f'<a href="?job={a["id"]}"><div class="card-vetrina" style="background-image: url(\'{img_url}\');"></div></a>'
        html_vetrina += '</div></div>'
        st.markdown(html_vetrina, unsafe_allow_html=True)

    # LISTA
    st.markdown('<p class="titolo-area">Selezioni Aperte</p>', unsafe_allow_html=True)
    for i in range(0, len(annunci_vivi), 2):
        cols = st.columns(2)
        cols[0].markdown(render_card(annunci_vivi[i]), unsafe_allow_html=True)
        if i + 1 < len(annunci_vivi):
            cols[1].markdown(render_card(annunci_vivi[i+1]), unsafe_allow_html=True)

# LOGICA DI VISUALIZZAZIONE
if "job" in st.query_params:
    st.write("Redirect al form...")
    # Qui andrà il tuo codice che carica il modulo di candidatura
else:
    mostra_portale()
