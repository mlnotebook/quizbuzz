from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """Renders the custom 404 error webpage."""
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """Renders the custom 500 error webpage."""
    db.session.rollback()
    return render_template('errors/500.html'), 500