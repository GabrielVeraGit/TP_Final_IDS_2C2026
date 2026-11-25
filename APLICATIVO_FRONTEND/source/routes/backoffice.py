from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from source import API
from source import utils

backoffice_bp = Blueprint("backoffice_bp", __name__)


@backoffice_bp.route("/backoffice", methods=["GET"])
def backoffice():
    return render_template('backoffice.html')