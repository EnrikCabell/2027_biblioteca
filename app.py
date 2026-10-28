import json
from pathlib import Path
import streamlit as st

APP_DIR = Path(__file__).parent
PDF_DIR = APP_DIR / "pdfs"
CATALOG_FILE = APP_DIR / "catalogo.json"
CATEGORIAS_BASE = ["Ciencias", "Ciencias Sociales", "Maico", "Audiología", "Administración", "Mercadotecnia", "Sustentabilidad"]

st.set_page_config(page_title="Biblioteca digital", page_icon="📚", layout="wide")

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

catalogo = cargar_catalogo()
st.title("Biblioteca digital")
st.write("Selecciona una categoría para consultar las publicaciones disponibles.")

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
            try:
                st.pdf(str(archivo), height=700)
            except Exception:
                st.warning("No se pudo abrir la vista previa. Puedes descargar el PDF.")
            with archivo.open("rb") as pdf:
                st.download_button("Descargar PDF", data=pdf.read(), file_name=archivo.name, mime="application/pdf", key=f"descarga_{archivo.relative_to(PDF_DIR)}")

st.markdown("""
<div style="text-align: center; font-size: 12px; line-height: 1.8;">
    Initial code and all additional changes are property and registered by<br>
    Juan Enrique Cabello Vargas, PhD &amp; MSc.<br>
    Conceptualized and created by<br>
    Juan Enrique Cabello Vargas, PhD &amp; MSc.<br>
    All rights reserved.<br>
    Pax et Bonum.
</div>
""", unsafe_allow_html=True)
