"""Servicios del módulo de carta digital."""
from typing import Optional

from app.extensions import db
from app.models.categoria import Categoria
from app.models.platillo import Platillo
from app.utils.exceptions import ServiceError


def listar_categorias_publicas() -> list[dict]:
    """Lista categorías activas con platillos activos (RF-09)."""
    categorias = Categoria.query.filter_by(activo=True).order_by(Categoria.id).all()
    return [c.to_dict(include_platillos=True, solo_activos=True) for c in categorias]


def listar_categorias_admin() -> list[dict]:
    """Lista todas las categorías para el panel admin."""
    return [c.to_dict() for c in Categoria.query.order_by(Categoria.id).all()]


def crear_categoria(datos: dict) -> dict:
    """Crea una nueva categoría (RF-11)."""
    if Categoria.query.filter_by(nombre=datos["nombre"]).first():
        raise ServiceError("Ya existe una categoría con ese nombre.", 409, campo="nombre")

    categoria = Categoria(
        nombre=datos["nombre"],
        descripcion=datos.get("descripcion"),
        activo=True,
    )
    db.session.add(categoria)
    db.session.commit()
    return categoria.to_dict()


def actualizar_categoria(categoria_id: int, datos: dict) -> dict:
    """Edita una categoría existente."""
    categoria = db.session.get(Categoria, categoria_id)
    if not categoria:
        raise ServiceError("Categoría no encontrada.", 404)

    if "nombre" in datos and datos["nombre"] != categoria.nombre:
        if Categoria.query.filter_by(nombre=datos["nombre"]).first():
            raise ServiceError("Ya existe una categoría con ese nombre.", 409, campo="nombre")
        categoria.nombre = datos["nombre"]

    if "descripcion" in datos:
        categoria.descripcion = datos["descripcion"]

    db.session.commit()
    return categoria.to_dict()


def eliminar_categoria(categoria_id: int) -> None:
    """
    Elimina una categoría si no tiene platillos activos (RN-09, RF-11).
    """
    categoria = db.session.get(Categoria, categoria_id)
    if not categoria:
        raise ServiceError("Categoría no encontrada.", 404)

    platillos_activos = categoria.platillos.filter_by(activo=True).count()
    if platillos_activos > 0:
        raise ServiceError("No se puede eliminar una categoría con platillos activos.", 409)

    db.session.delete(categoria)
    db.session.commit()


def listar_platillos(
    categoria_id: Optional[int] = None,
    activo: Optional[bool] = None,
) -> list[dict]:
    """Lista platillos con filtros opcionales (RF-10)."""
    query = Platillo.query

    if categoria_id is not None:
        query = query.filter_by(categoria_id=categoria_id)
    if activo is not None:
        query = query.filter_by(activo=activo)
    elif activo is None and categoria_id is None:
        # Carta pública: solo activos por defecto cuando no hay filtro admin
        pass

    return [p.to_dict() for p in query.order_by(Platillo.nombre).all()]


def listar_platillos_publicos(categoria_id: Optional[int] = None) -> list[dict]:
    """Lista solo platillos activos para la carta pública."""
    return listar_platillos(categoria_id=categoria_id, activo=True)


def crear_platillo(datos: dict) -> dict:
    """Crea un nuevo platillo (RF-12)."""
    categoria = db.session.get(Categoria, datos["categoria_id"])
    if not categoria:
        raise ServiceError("Categoría no encontrada.", 404, campo="categoria_id")

    platillo = Platillo(
        nombre=datos["nombre"],
        descripcion=datos.get("descripcion"),
        precio=datos["precio"],
        imagen_url=datos.get("imagen_url"),
        categoria_id=datos["categoria_id"],
        activo=True,
    )
    db.session.add(platillo)
    db.session.commit()
    return {
        "id": platillo.id,
        "nombre": platillo.nombre,
        "precio": float(platillo.precio),
        "categoria": categoria.nombre,
    }


def actualizar_platillo(platillo_id: int, datos: dict) -> dict:
    """Edita un platillo existente (RF-12)."""
    platillo = db.session.get(Platillo, platillo_id)
    if not platillo:
        raise ServiceError("Platillo no encontrado.", 404)

    if "categoria_id" in datos:
        categoria = db.session.get(Categoria, datos["categoria_id"])
        if not categoria:
            raise ServiceError("Categoría no encontrada.", 404, campo="categoria_id")
        platillo.categoria_id = datos["categoria_id"]

    if "nombre" in datos:
        platillo.nombre = datos["nombre"]
    if "descripcion" in datos:
        platillo.descripcion = datos["descripcion"]
    if "precio" in datos:
        platillo.precio = datos["precio"]
    if "imagen_url" in datos:
        platillo.imagen_url = datos["imagen_url"]

    db.session.commit()
    return {
        "id": platillo.id,
        "nombre": platillo.nombre,
        "precio": float(platillo.precio),
        "categoria": platillo.categoria.nombre if platillo.categoria else None,
    }


def cambiar_visibilidad_platillo(platillo_id: int, activo: bool) -> None:
    """Activa o desactiva un platillo en la carta (RF-13, RN-08)."""
    platillo = db.session.get(Platillo, platillo_id)
    if not platillo:
        raise ServiceError("Platillo no encontrado.", 404)

    platillo.activo = activo
    db.session.commit()
