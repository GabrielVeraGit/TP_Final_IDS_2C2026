import os
from dotenv import load_dotenv
from flask import Flask, render_template
from source import users, utils, extend_jwt
load_dotenv()

app  = Flask(__name__)
#Configuracion Tokens
extend_jwt.config(app)

app.register_blueprint(users.user_bp,  url_prefix="/cine_paradiso")

@app.route("/cine_paradiso", methods=["GET"])
@extend_jwt.seguro(optional=True)
def index():
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    return render_template('index.html', logueado=identificador)


@app.context_processor
def inyectar_variables_index():
    return dict(vars_footer=utils.cargar_vars_footer())



if __name__ == "__main__":
    puerto = int(os.getenv("PORT_APLICATIVO_FRONTEND", 5002))
    app.run(port=puerto, debug=True)