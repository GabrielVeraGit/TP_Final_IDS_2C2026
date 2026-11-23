from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from source import API
from source import utils

pelicula_bp = Blueprint("pelicula_bp", __name__)


@pelicula_bp.route("/pelicula/<int:id_pelicula>", methods=["GET"])
def pelicula_id(id_pelicula:int):
    redireccion = utils.verificar_sesion()
    if redireccion:
        return redireccion
    
    error, datos_pelicula, codigo = utils.llamar("GET", f"/peliculas/{id_pelicula}")
    if error:
        return utils.manejar_error(datos_pelicula, codigo, url_for("index"))
    error, funciones, codigo = utils.llamar("GET", "/funciones", params={"id_pelicula": id_pelicula})
    if error:
        flash(funciones, "error")
        funciones = []
    return render_template("pelicula.html", pelicula=datos_pelicula, funciones=funciones)