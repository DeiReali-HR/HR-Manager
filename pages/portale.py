import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS Compattato e allineato
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400&display=swap');
    
    /* Elimina spazio bianco superiore */
    .main .block-container { padding-top: 1rem !important; }
    
    .titolo-area { font-family: 'Playfair Display', serif; font-size: 0.9rem; color: #64748b; margin-top: 25px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Vetrina sfondo infinito */
    .vetrina-full-width { background-color: #f1f5f9; margin-left: -500px; margin-right: -500px; padding: 30px 500px; margin-bottom: 30px; }
    .grid-vetrina { display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; max-width: 1400px; margin: auto; }
    .card-vetrina { aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 4px; border: 1px solid #cbd5e1; }
    
    /* Annunci compatti e allineati */
    .card-orizzontale { display: flex; border: 1px solid #e2e8f0; border-radius: 8px; background: white; margin-bottom: 20px; height: 350px; overflow: hidden; }
    .img-lato { width: 35%; height: 100%; background-size: cover; background-position: center; border-right: 1px solid #e2e8f0; background-color: #f1f5f9; }
    .testo-lato { width: 65%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
    .btn-black { background: #0f172a; color: white !important; padding: 12px; border-radius: 4px; text-align: center; text-decoration: none; font-weight: bold; display: block; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

def render_card(a):
    img_url = a.get("foto_annuncio") or a.get("immagine") or "https://via.placeholder.com/200x350"
    return f"""
    <div class="card-orizzontale">
        <div class="img-lato" style="background-image: url('{img_url}');"></div>
        <div class="testo-lato">
            <div style="flex-grow: 1;">
                <h3 style="font-family: 'Playfair Display', serif; margin-top:0; font-size:1.2rem;">{a.get('posizione', 'Posizione')}</h3>
                <p style="font-size:0.85rem; color: #64748B;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                <p style="font-size:0.85rem;">{str(a.get('note', ''))[:110] + '...'}</p>
            </div>
            <a href="?job={a['id']}" class="btn-black">CANDIDATI ORA ↗</a>
        </div>
    </div>
    """

def mostra_portale():
    # Intestazione compatta
    st.markdown('<h1 style="font-family: \'Playfair Display\', serif; font-size: 2.2rem; margin-top: 0; margin-bottom: 5px;">Opportunità di Carriera</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: \'Inter\', sans-serif; color: #64748b; font-size: 0.9rem; margin-bottom: 25px;">Selezioniamo i migliori talenti per una crescita professionale d\'eccellenza.</p>', unsafe_allow_html=True)
    
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # VETRINA
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
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

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_portale()
