import csv
from sqlalchemy.orm import sessionmaker
from clases2 import Usuario, Publicacion, Reaccion, engine

Session = sessionmaker(bind=engine)
session = Session()

# Poblar usuarios
with open('DATA/usuarios_red_x.csv', encoding='utf-8') as archivo:
    reader = csv.reader(archivo)
    next(reader)  # Saltar encabezado
    for fila in reader:
        nombre_usuario = fila[0].strip()
        if not session.query(Usuario).filter_by(nombre=nombre_usuario).first():
            usuario = Usuario(nombre=nombre_usuario)
            session.add(usuario)

session.commit()
print("Usuarios cargados")


# Poblar publicaciones
with open('DATA/usuarios_publicaciones.csv', encoding='utf-8') as archivo:
    reader = csv.reader(archivo, delimiter='|')
    next(reader)  # Saltar encabezado
    for fila in reader:
        nombre_usuario = fila[0].strip()
        contenido = fila[1].strip()
        usuario = session.query(Usuario).filter_by(nombre=nombre_usuario).first()
        if usuario and not session.query(Publicacion).filter_by(contenido=contenido).first():
            publicacion = Publicacion(contenido=contenido, usuario=usuario)
            session.add(publicacion)

session.commit()
print("Publicaciones cargadas.")

# Poblar reacciones
with open('DATA/usuario_publicacion_emocion.csv', encoding='utf-8') as archivo:
    reader = csv.reader(archivo, delimiter='|')
    next(reader)  # Saltar encabezado
    
    for fila in reader:
        nombre_usuario = fila[0].strip()
        contenido = fila[1].strip()
        emocion = fila[2].strip()

        usuario = session.query(Usuario).filter_by(nombre=nombre_usuario).first()
        publicacion = session.query(Publicacion).filter_by(contenido=contenido).first()

        if usuario and publicacion:
            if not session.query(Reaccion).filter_by(usuario_id=usuario.id, publicacion_id=publicacion.id).first():
                reaccion = Reaccion(usuario=usuario, publicacion=publicacion, tipo_emocion=emocion)
                session.add(reaccion)

session.commit()
print("Reacciones cargadas.")
