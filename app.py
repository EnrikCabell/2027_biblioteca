import base64
import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

APP_DIR = Path(__file__).parent
PDF_DIR = APP_DIR / "pdfs"
CATALOG_FILE = APP_DIR / "catalogo.json"
BANNER_FILE = APP_DIR / "2027_PUMABIEN.jpg"
CATEGORIAS_BASE = ["Ciencias", "Ciencias Sociales", "Maico", "Audiología", "Administración", "Mercadotecnia", "Sustentabilidad"]

ICON_FILE = APP_DIR / "logo_kitACA.png"
st.set_page_config(page_title="kitACA", page_icon=str(ICON_FILE) if ICON_FILE.exists() else "📚", layout="wide")

st.markdown("""
<style>
:root { --primary-color: #1769aa; }
[data-testid="stAppViewContainer"] h1, [data-testid="stAppViewContainer"] h2, [data-testid="stAppViewContainer"] h3 { color: #1769aa; }
h1 a, h2 a, h3 a, [data-testid="stHeaderActionElements"] { display: none !important; }
[data-testid="stToolbar"], [data-testid="stStatusWidget"], [data-testid="stDecoration"], [data-testid="stDeployButton"], a[href*="github.com/streamlit"], button[aria-label*="Fork"], [data-testid="stAppDeployButton"] { display: none !important; }
[data-testid="stButton"] button, [data-testid="stDownloadButton"] button { background-color: #1769aa; color: white; border-color: #1769aa; }
[data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover { background-color: #0d4f85; color: white; border-color: #0d4f85; }
[data-baseweb="select"] > div:focus-within, [data-baseweb="input"] > div:focus-within { border-color: #1769aa; }
@media (max-width: 640px) {
  [data-testid="stAppViewContainer"] .block-container { padding-top: 0.35rem !important; padding-left: 0.65rem; padding-right: 0.65rem; }
  [data-testid="stAppViewContainer"] .main { padding-top: 0 !important; }
}
</style>
""", unsafe_allow_html=True)

# Encabezado propio para conservar nombre e identidad al ocultar la barra de Streamlit.
if ICON_FILE.exists():
    logo_b64 = base64.b64encode(ICON_FILE.read_bytes()).decode("ascii")
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;background:#1769aa;color:white;padding:8px 12px;border-radius:6px;margin:0 0 10px 0;">
      <img src="data:image/png;base64,{logo_b64}" alt="kitACA" style="width:34px;height:34px;object-fit:contain;background:white;border-radius:4px;padding:2px;">
      <span style="font-size:18px;font-weight:600;">kitACA</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div style="background:#1769aa;color:white;padding:12px 14px;border-radius:6px;font-size:18px;font-weight:600;margin-bottom:16px;">kitACA</div>', unsafe_allow_html=True)

if BANNER_FILE.exists():
    st.image(str(BANNER_FILE), use_container_width=True)

st.markdown("""
<div style="text-align:center; color:#1769aa; font-style:italic; font-size:18px; margin-bottom:18px;">
Conceptualized and created by<br>Juan Enrique Cabello Vargas, PhD &amp; MSc.
</div>
""", unsafe_allow_html=True)

def cargar_catalogo():
    if CATALOG_FILE.exists():
        try:
            return json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def nombre_categoria(archivo):
    relativa = archivo.relative_to(PDF_DIR)
    return relativa.parts[0] if len(relativa.parts) > 1 else ""

def mostrar_pdf_responsivo(contenido_pdf):
    pdf_base64 = base64.b64encode(contenido_pdf).decode("ascii")
    html = f"""
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <div style="width:100%;max-width:100%;overflow:hidden;">
      <iframe title="Vista previa del PDF" src="data:application/pdf;base64,{pdf_base64}#view=FitH"
        style="display:block;width:100%;max-width:100%;height:70vh;min-height:360px;border:0;" loading="lazy"></iframe>
    </div>
    """
    components.html(html, height=520, scrolling=False)

catalogo = cargar_catalogo()
st.title("Biblioteca académica")
st.write("Elige la categoría para consultar las publicaciones existentes.")

PDF_DIR.mkdir(exist_ok=True)
for categoria_base in CATEGORIAS_BASE:
    (PDF_DIR / categoria_base).mkdir(exist_ok=True)

archivos = sorted(PDF_DIR.rglob("*.pdf"), key=lambda p: str(p).lower())
categorias = ["Todas"] + CATEGORIAS_BASE
categoria = st.selectbox("Categoría", categorias)
buscar = st.text_input("Buscar publicación", placeholder="Escribe parte del título")

visibles = []
for archivo in archivos:
    datos = catalogo.get(archivo.name, {})
    titulo = datos.get("titulo", archivo.stem.replace("_", " "))
    coincide_categoria = categoria == "Todas" or nombre_categoria(archivo) == categoria
    coincide_busqueda = buscar.lower() in archivo.stem.lower() or buscar.lower() in titulo.lower()
    if coincide_categoria and coincide_busqueda:
        visibles.append((archivo, datos, titulo))

if not visibles:
    st.info("No hay publicaciones en esta categoría todavía.")
else:
    for archivo, datos, titulo in visibles:
        with st.expander(titulo):
            if nombre_categoria(archivo):
                st.caption(f"Categoría: {nombre_categoria(archivo)}")
            st.write(datos.get("descripcion", "Publicación en formato PDF."))
            contenido_pdf = archivo.read_bytes()
            mostrar_pdf_responsivo(contenido_pdf)
            st.download_button("Descargar PDF", data=contenido_pdf, file_name=archivo.name, mime="application/pdf", key=f"descarga_{archivo.relative_to(PDF_DIR)}")

st.markdown("""
<div style="text-align:center;font-size:12px;line-height:1.8;">
Initial code and all additional changes are property and registered by<br>
Juan Enrique Cabello Vargas, PhD &amp; MSc.<br>
Conceptualized and created by<br>
Juan Enrique Cabello Vargas, PhD &amp; MSc.<br>
All rights reserved.<br>
Pax et Bonum.
</div>
""", unsafe_allow_html=True)
