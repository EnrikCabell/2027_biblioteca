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

catalogo = cargar_catalogo()

st.title("Biblioteca digital")
st.write("Consulta las publicaciones disponibles y descarga los archivos PDF.")

PDF_DIR.mkdir(exist_ok=True)
archivos = sorted(PDF_DIR.glob("*.pdf"), key=lambda p: p.name.lower())

if not archivos:
    st.info("Todavía no hay publicaciones. Cuando tengas archivos PDF, colócalos en la carpeta `pdfs`.")
else:
    buscar = st.text_input("Buscar publicación", placeholder="Escribe parte del título")
    visibles = [
        archivo for archivo in archivos
        if buscar.lower() in archivo.stem.lower()
        or buscar.lower() in str(catalogo.get(archivo.name, {}).get("titulo", "")).lower()
    ]

    if not visibles:
        st.warning("No se encontraron publicaciones con esa búsqueda.")
    else:
        for archivo in visibles:
            datos = catalogo.get(archivo.name, {})
            titulo = datos.get("titulo", archivo.stem.replace("_", " "))
            descripcion = datos.get("descripcion", "Publicación en formato PDF.")
            st.subheader(titulo)
            st.write(descripcion)
            with archivo.open("rb") as pdf:
                st.download_button(
                    label="Descargar PDF",
                    data=pdf.read(),
                    file_name=archivo.name,
                    mime="application/pdf",
                    key=f"descarga_{archivo.name}",
                )
            st.divider()

st.caption("Versión inicial. El registro de usuarios y el panel privado para subir archivos se añadirán en la siguiente etapa.")
