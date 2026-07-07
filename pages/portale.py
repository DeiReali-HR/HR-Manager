import streamlit as st
from supabase import create_client

# Configurazione
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
st.set_page_config(layout="wide", page_title="Lavora con Noi - Dei Reali")

# CSS Editoriale
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400&display=swap');
    
    .titolo-sezione { font-family: 'Playfair Display', serif; font-size: 2rem; color: #1e293b; margin-top: 40px; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
    .box-vetrina { background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 30px; border-radius: 8px; margin-bottom: 40px; display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; }
    .card-vetrina { aspect-ratio: 395/704; background-size: cover; background-position: center; border-radius: 4px; border: 1px solid #cbd5e1; transition: transform 0.2s; }
    .card-vetrina:hover { transform: scale(1.02); }

    /* Card a due colonne */
    .card-orizzontale { display: flex; border: 1px solid #e2e8f0; border-radius: 8px; height: 350px; overflow: hidden; background: white; margin-bottom: 20px; }
    .img-lato { width: 40%; background-size: cover; background-position: center; border-right: 1px solid #e2e8f0; background-color: #f1f5f9; }
    .testo-lato { width: 60%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
    .btn-black { background: #0f172a; color: white !important; padding: 12px; border-radius: 4px; text-align: center; text-decoration: none; font-weight: bold; font-family: 'Inter', sans-serif; }
</style>
""", unsafe_allow_html=True)

def mostra_portale():
    st.markdown('<h1 style="font-family: \'Playfair Display\', serif; font-size: 3rem;">Opportunità di Carriera</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: \'Inter\', sans-serif; color: #64748b; font-size: 1.2rem;">Selezioniamo i migliori talenti per una crescita professionale d\'eccellenza.</p>', unsafe_allow_html=True)
    
    annunci = supabase.table("annunci").select("*").execute().data or []
    annunci_vivi = [a for a in annunci if a.get("stato") != "Sospeso"]

    # VETRINA
    evidenza = [a for a in annunci_vivi if a.get("in_evidenza") in [True, 1, "true", "True"]][:7]
    if evidenza:
        st.markdown('<h2 class="titolo-sezione">In Primo Piano</h2>', unsafe_allow_html=True)
        html_vetrina = '<div class="box-vetrina">'
        for a in evidenza:
            img_url = a.get("foto_vetrina") or a.get("immagine") or "https://via.placeholder.com/395x704?text=No+Img"
            html_vetrina += f'<a href="?job={a["id"]}"><div class="card-vetrina" style="background-image: url(\'{img_url}\');"></div></a>'
        html_vetrina += '</div>'
        st.markdown(html_vetrina, unsafe_allow_html=True)

    # LISTA A DUE COLONNE
    st.markdown('<h2 class="titolo-sezione">Tutte le Posizioni</h2>', unsafe_allow_html=True)
    for i in range(0, len(annunci_vivi), 2):
        row = st.columns(2)
        for j in range(2):
            if i + j < len(annunci_vivi):
                a = annunci_vivi[i + j]
                img_url = a.get("foto_annuncio") or a.get("immagine") or "https://via.placeholder.com/200x280?text=No+Img"
                with row[j]:
                    st.markdown(f"""
                    <div class="card-orizzontale">
                        <div class="img-lato" style="background-image: url('{img_url}');"></div>
                        <div class="testo-lato">
                            <div style="overflow-y:auto;">
                                <h3 style="font-family: 'Playfair Display', serif; margin-top:0;">{a.get('posizione', 'Posizione')}</h3>
                                <p style="font-size:0.9rem; color: #64748B;">📍 {a.get('sede', 'Roma')} | 💸 {a.get('importo', '0')}€</p>
                                <p style="font-size:0.9rem;">{str(a.get('note', ''))[:150] + '...'}</p>
                            </div>
                            <a href="?job={a['id']}" class="btn-black">CANDIDATI ORA ↗</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if "job" in st.query_params:
    st.write("Redirect al form...")
else:
    mostra_portale()
