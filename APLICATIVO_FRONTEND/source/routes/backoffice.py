from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from source import API
from source import utils

backoffice_bp = Blueprint("backoffice_bp", __name__)


@backoffice_bp.route("/backoffice", methods=["GET"])
def backoffice():
    return render_template('backoffice.html')


@backoffice_bp.route("/backoffice/agregar_pelicula", methods=["GET", "POST"])
def agregar_pelicula():
    acceso = utils.verificar_sesion("admin")
    if acceso:
        return acceso
    
    peli_a_agregar={}
    if request.method == "POST":
        peli_a_agregar["titulo"]=request.form.get("titulo")
        peli_a_agregar["anio"]=request.form.get("anio")
        peli_a_agregar["disponible_desde"]=request.form.get("disponible_desde")
        peli_a_agregar["disponible_hasta"]=f"{request.form.get("disponible_hasta")} 23:59:59"

        error, respuesta, codigo = utils.llamar("POST", f"/peliculas",datos=peli_a_agregar)
        if error:
            return utils.manejar_error(respuesta, codigo, url_for('backoffice_bp.agregar_pelicula'))
        flash(f"Pelicula {peli_a_agregar["titulo"]} ({peli_a_agregar["anio"]}) fue agregada, EXITO!")
        return render_template('agregar_pelicula.html')

    
    descripcion_pelicula=request.args.get("descripcion_pelicula", None)#form tipo get
    if descripcion_pelicula:
        error, respuesta, codigo = utils.llamar("GET", "/buscar_pelicula",datos={"descripcion":descripcion_pelicula})
        if error:
            return utils.manejar_error(respuesta, codigo, url_for('backoffice_bp.agregar_pelicula'))
        return render_template('agregar_pelicula.html', pelicula=respuesta )
    else:
        return render_template('agregar_pelicula.html')