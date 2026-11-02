import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app  = Flask(__name__)

@app.route("/api", methods=["GET"])
def index():
    return "ENTRASTE A LA API", 200


if __name__ == "__main__":
    puerto=int(os.getenv("PORT_API_BACKEND", 5001))
    app.run(port=puerto, debug=False)
