import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS Editoriale "Senza confini"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400&display=swap');
    
    /* Rimozione spazi di default Streamlit */
    .main .block-container { padding-top: 2rem; }
    
    .titolo-area { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #64748b; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Background che sborda lateralmente */
    .vetrina-full-width { 
        background-color: #f1f5f9; 
        margin-left: -500px; 
        margin-right: -500px; 
        padding: 40px 500px; 
        margin-bottom: 40px;
    }
    
    .grid-vetrina { display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; max-width: 1400px; margin: auto; }
    .card-vetrina { aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 4px; border: 1px solid #cbd5e1; }
    
    .card-orizzontale { display: flex; border: 1px solid #e2e8f0; border-radius: 8px; height: 320px; margin-bottom: 20px; background: white; }
    .img-lato { width: 35%; background-size: cover; background-position: center; border-right: 1px solid #e2e8f0; }
    .testo-lato { width: 65%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
    .btn-black { background: #0f172a; color: white !important; padding: 10px; border-radius: 4px; text-align: center; text-decoration: none; font-weight: bold; font-family: 'Inter', sans-serif; }
</style>
""", unsafe_allow_html=True)

def mostra_portale():
    # Intestazione compattata
    st.markdown('<h1 style="font-family: \'Playfair Display\', serif; font-size: 2.5rem; margin-bottom: 0;">Opportunità di Carriera</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: \'Inter\', sans-serif; color: #64748b; font-size: 1rem; margin-bottom: 30px;">Selezioniamo i migliori talenti per una crescita professionale d\'eccellenza.</p>', unsafe_allow_html=True)
    
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # 1. VETRINA (Sfondo infinito)
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        st.markdown('<p class="titolo-area">In primo piano</p>', unsafe_allow_html=True)
        html_vetrina = '<div class="vetrina-full-width"><div class="grid-vetrina">'
        for a in evidenza:
            img_url = a.get("foto_vetrina") or a.get("immagine") or "https://via.placeholder.com/395x704"
            html_vetrina += f'<a href="?job={a["id"]}"><div class="card-vetrina" style="background-image: url(\'{img_url}\');"></div></a>'
        html_vetrina += '</div></div>'
        st.markdown(html_vetrina, unsafe_allow_html=True)

    # 2. SELEZIONI APERTE
    st.markdown('<p class="titolo-area">Selezioni Aperte</p>', unsafe_allow_html=True)
    for i in range(0, len(annunci_vivi), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(annunci_vivi):
                a = annunci_vivi[i + j]
                img_url = a.get("foto_annuncio") or a.get("immagine") or "https://via.placeholder.com/200x280"
                with row[j]:
                    st.markdown(f"""
                    <div class="card-orizzontale">
                        <div class="img-lato" style="background-image: url('{img_url}');"></div>
                        <div class="testo-lato">
                            <div>
                                <h3 style="font-family: 'Playfair Display', serif; margin-top:0;">{a.get('posizione', 'Posizione')}</h3>
                                <p style="font-size:0.85rem; color: #64748B;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                                <p style="font-size:0.85rem;">{str(a.get('note', ''))[:120] + '...'}</p>
                            </div>
                            <a href="?job={a['id']}" class="btn-black">CANDIDATI ORA ↗</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_portale()
