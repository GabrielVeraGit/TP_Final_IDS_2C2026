import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app  = Flask(__name__)

@app.route("/aplicativo", methods=["GET"])
def index():
    return "ENTRASTE AL APLICATIVO", 200


if __name__ == "__main__":
    puerto = int(os.getenv("PORT_APLICATIVO_FRONTEND", 5002))
    app.run(port=puerto, debug=False)