import json
from pathlib import Path
import streamlit as st

APP_DIR = Path(__file__).parent
PDF_DIR = APP_DIR / "pdfs"
CATALOG_FILE = APP_DIR / "catalogo.json"

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
    if len(relativa.parts) > 1:
        return relativa.parts[0]
    return "Sin categoría"

catalogo = cargar_catalogo()

st.title("Biblioteca digital")
st.write("Explora las categorías y consulta cada publicación directamente en esta página.")

PDF_DIR.mkdir(exist_ok=True)
archivos = sorted(PDF_DIR.rglob("*.pdf"), key=lambda p: str(p).lower())

if not archivos:
    st.info("Todavía no hay publicaciones. Coloca archivos PDF en una carpeta temática dentro de pdfs.")
else:
    categorias = sorted({nombre_categoria(a) for a in archivos}, key=str.lower)
    categoria = st.selectbox("Categoría", ["Todas"] + categorias)
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
        st.warning("No se encontraron publicaciones con esos criterios.")
    else:
        for archivo, datos, titulo in visibles:
            descripcion = datos.get("descripcion", "Publicación en formato PDF.")
            with st.expander(titulo):
                st.caption(f"Categoría: {nombre_categoria(archivo)}")
                st.write(descripcion)
                try:
                    st.pdf(str(archivo), height=700)
                except Exception as error:
                    st.error("No se pudo mostrar el PDF dentro de la página.")
                    st.caption(str(error))
                with archivo.open("rb") as pdf:
                    st.download_button(
                        label="Descargar PDF",
                        data=pdf.read(),
                        file_name=archivo.name,
                        mime="application/pdf",
                        key=f"descarga_{archivo.relative_to(PDF_DIR)}",
                    )

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
