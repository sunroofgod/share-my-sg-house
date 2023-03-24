from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('listings', __name__)

@bp.route('/')
def index():
    db = get_db()
    listings = db.execute(
        '''SELECT h.location, h.price, h.num_room, hr.rating, hr.date, u.username
        FROM houses h, house_ratings hr, users u
        WHERE u.email = h.owner_email AND
        hr.houseid = h.id
        ORDER BY h.id DESC'''
    ).fetchall()
    return render_template('listings/index.html', listing=listings)

