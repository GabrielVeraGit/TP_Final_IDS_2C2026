from flask import Blueprint, render_template, request, url_for, flash
from source.utils import verificar_sesion, llamar, manejar_error, tomar_campos
from source.formato import leer_fecha
from source.llamadas_api import llamar_api
from source.config import DIAS_SEMANA, MESES, HORAS_LIMITE_CANCELACION, MAX_ENTRADAS

cartelera_bp = Blueprint("cartelera_bp", __name__)

def obtener_generos(peliculas:list):
    generos = []
    for p in peliculas:
        for genero in (p.get("genero") or "").split(","):
            genero = genero.strip()
            if genero != "" and genero not in generos:
                generos.append(genero)
    generos.sort()
    return generos

#portada publica: 
@cartelera_bp.route("/", methods=["GET"])
def inicio():
    error, peliculas, codigo = llamar_api("GET", "/peliculas/disponibles")
    mensaje = None
    if error:
        mensaje = peliculas
        peliculas = []
    return render_template("inicio.html", peliculas=peliculas, mensaje=mensaje, horas_limite=HORAS_LIMITE_CANCELACION, max_entradas=MAX_ENTRADAS)

@cartelera_bp.route("/cartelera", methods=["GET"])
def index():
    redireccion = verificar_sesion()
    if redireccion:
        return redireccion
    params = tomar_campos(request.args, ("titulo", "genero"))
    error, peliculas, codigo = llamar("GET", "/peliculas/cartelera", params=params)
    if error:
        return manejar_error(peliculas, codigo, url_for("usuarios_bp.login"))
    #los botones de genero se arman con toda la cartelera, no solo con lo filtrado
    todas = peliculas
    if params:
        error, todas, codigo = llamar("GET", "/peliculas/cartelera")
        if error:
            todas = peliculas
    return render_template("cartelera.html", peliculas=peliculas, filtros=params, generos=obtener_generos(todas))

@cartelera_bp.route("/pelicula/<int:id_pelicula>", methods=["GET"])
def pelicula(id_pelicula:int):
    redireccion = verificar_sesion()
    if redireccion:
        return redireccion
    error, datos_pelicula, codigo = llamar("GET", f"/peliculas/{id_pelicula}")
    if error:
        return manejar_error(datos_pelicula, codigo, url_for("cartelera_bp.index"))
    error, todas, codigo = llamar("GET", "/funciones", params={"id_pelicula": id_pelicula})
    if error:
        flash(todas, "error")
        todas = []

    #sedes y dias disponibles para los filtros
    sedes = []
    ids_sedes = []
    dias = []
    fechas = []
    for f in todas:
        if f["id_sede"] not in ids_sedes:
            ids_sedes.append(f["id_sede"])
            sedes.append({"id_sede": f["id_sede"], "nombre": f["sede"]})
        fecha = f["fecha_hora"][:10]
        if fecha not in fechas:
            fechas.append(fecha)
            inicio = leer_fecha(f["fecha_hora"])
            dias.append({"fecha": fecha, "nombre": DIAS_SEMANA[inicio.weekday()].upper(), "numero": f"{inicio.day} {MESES[inicio.month - 1]}"})

    sede = None
    if request.args.get("sede", "").isdigit():
        sede = int(request.args.get("sede"))
    dia = request.args.get("dia", "")

    funciones = []
    for f in todas:
        if sede is not None and f["id_sede"] != sede:
            continue
        if dia != "" and f["fecha_hora"][:10] != dia:
            continue
        funciones.append(f)

    actores = []
    for actor in (datos_pelicula.get("actores") or "").split(","):
        if actor.strip() != "":
            actores.append(actor.strip())
    return render_template("pelicula.html", pelicula=datos_pelicula, funciones=funciones, sedes=sedes, dias=dias, sede=sede, dia=dia, actores=actores)