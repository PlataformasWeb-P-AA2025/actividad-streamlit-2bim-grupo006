# streamlit_explorar2.py

import streamlit as st
from db2 import get_session
from clases2 import Usuario, Publicacion, Reaccion      

# Configura la página de la app Streamlit 
st.set_page_config(page_title="Explorador Red Social", layout="wide")


# Función para listar todos los usuarios
def listar_usuarios():
    st.header("Usuarios") 
    session = get_session() # Se crea una sesion
    usuarios = session.query(Usuario).all() # Obtiene todos los usuarios

    if not usuarios:
        st.info("No hay registros en 'usuario'.")
        return
    # recorrer cada usuario
    for usuario in usuarios:
        with st.expander(f"ID {usuario.id} → {usuario.nombre}"):
            st.write(f"**ID:** {usuario.id}")
            st.write(f"**Nombre:** {usuario.nombre}")

            if usuario.publicaciones:
                st.write("**Publicaciones:**")
                filas_pub = []
                for pub in usuario.publicaciones:
                    # obtiene toda la informacion de lobjeto
                    filas_pub.append({
                        "ID": pub.id,
                        "Contenido": pub.contenido[:50],
                        "Fecha": pub.fecha.strftime("%Y-%m-%d %H:%M"),
                        "Reacciones": len(pub.reacciones)
                    })
                st.table(filas_pub) # tabla con las publicaciones
            else:
                st.write("_Este usuario no ha publicado nada._")

            if usuario.reacciones:
                st.write("**Reacciones hechas:**")
                filas_reac = []
                for r in usuario.reacciones:
                        filas_reac.append({
                        "Publicación ID": r.publicacion.id,
                        "Contenido": r.publicacion.contenido[:50],
                        "Tipo emoción": r.tipo_emocion,
                    })
                st.table(filas_reac) # tambien se muestra las reacciones
            else:
                st.write("_Este usuario no ha reaccionado a nada._")

    session.close()

# Funcion para listar todas las publicaciones

def listar_publicaciones():
    st.header("Publicaciones")
    session = get_session()
    publicaciones = session.query(Publicacion).all()

    if not publicaciones:
        st.info("No hay registros en 'publicacion'.")
        return

    for pub in publicaciones:
        with st.expander(f"ID {pub.id} → {pub.contenido[:40]}..."):
            st.write(f"**ID:** {pub.id}")
            st.write(f"**Contenido:** {pub.contenido}")
            st.write(f"**Fecha:** {pub.fecha.strftime('%Y-%m-%d %H:%M')}")
            st.write(f"**Autor:** {pub.usuario.nombre}")

            if pub.reacciones:
                st.write("**Reacciones recibidas:**")
                filas_reac = []
                for r in pub.reacciones:
                    filas_reac.append({
                        "Usuario": r.usuario.nombre,
                        "Tipo emoción": r.tipo_emocion
                    }) 
                st.table(filas_reac) # tabla con reacciones recibidas
            else:
                st.write("_No hay reacciones para esta publicación._")

    session.close()

# Funcion para listar todas las reacciones
def listar_reacciones():
    st.header("Reacciones")
    session = get_session()
    reacciones = session.query(Reaccion).all()

    if not reacciones:
        st.info("No hay registros en 'reaccion'.")
        return

    filas = []
    for r in reacciones:
        filas.append({
            "Usuario": r.usuario.nombre,
            "Publicación": r.publicacion.contenido[:50],
            "Emoción": r.tipo_emocion
        })

    st.table(filas)
    session.close()

# Funcion para controlar la navegacion en Streamlit
def main():
    st.title("Explorador de la base Premier_League con SQLAlchemy y Streamlit")

    entidad = st.sidebar.selectbox(
        "Selecciona una entidad para explorar:",
        ("Usuario", "Publicacion", "Reaccion")
    )

    if entidad == "Usuario":
        listar_usuarios()
    elif entidad == "Publicacion":
        listar_publicaciones()
    elif entidad == "Reaccion":
        listar_reacciones()


if __name__ == "__main__":
    main()
