from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Text, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


# se importa información del archivo configuracion
from config2 import cadena_base_datos2


engine = create_engine(cadena_base_datos2)

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)

    publicaciones = relationship("Publicacion", back_populates="usuario")
    reacciones = relationship("Reaccion", back_populates="usuario")

    def __repr__(self):
        return "Usuario: nombre=%s" % (self.nombre)


class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key=True)
    contenido = Column(Text, unique=True, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

    usuario = relationship("Usuario", back_populates="publicaciones")
    reacciones = relationship("Reaccion", back_populates="publicacion")

    def __repr__(self):
        return "Publicacion: contenido=%s..." % (self.contenido[:30])



class Reaccion(Base):
    __tablename__ = 'reaccion'
    usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    publicacion_id = Column(Integer, ForeignKey('publicacion.id'), primary_key=True)
    tipo_emocion = Column(String(50), nullable=False)

    usuario = relationship("Usuario", back_populates="reacciones")
    publicacion = relationship("Publicacion", back_populates="reacciones")
# cambios


    def __repr__(self):
        return "Reaccion: usuario=%s, publicacion=%s, tipo_emocion=%s" % (
            self.usuario.nombre,
            self.publicacion.contenido[:30] + "...",
            self.tipo_emocion
        )

Base.metadata.create_all(engine)